"""Seeded state-vector trajectories for the two preparation ensembles."""
from dataclasses import dataclass
from heapq import merge

import numpy as np
from qulacs import QuantumCircuit, QuantumState, gate

from figure14 import build_figure14


def logical_frames():
    """Row k is the physical diagonal of Z for little-endian Stim residual k."""
    # Data MX masks in OBSERVABLE_INCLUDE(0,1,2): 0x55, 0x33, 0x0f.
    # Each Z representative anticommutes with just its corresponding X.
    masks = (0x03, 0x05, 0x11)
    return np.array([
        [(-1) ** sum((x & mask).bit_count() for i, mask in enumerate(masks)
                     if k & (1 << i)) for x in range(256)]
        for k in range(8)
    ])


def encoded_target():
    v = np.zeros(256)
    for x in range(256):
        if all((x & m).bit_count() % 2 == 0 for m in (0x0f, 0xf0, 0x33, 0x55)):
            is_111 = all((x & m).bit_count() % 2 for m in (0x11, 0x05, 0x03))
            v[x] = -0.25 if is_111 else 0.25
    return v


@dataclass
class Event:
    order: int
    gate_offset: int
    kind: str
    args: tuple


class Schedule:
    """Keep ideal gates in Qulacs. Insert sampled Pauli faults and projectors in order."""
    def __init__(self):
        self.circuit = QuantumCircuit(16)
        self.actions = []
        self.locations = []
        self.interface = set()
        self.measurements = 0
        self.paulis = [[None, gate.X(i), gate.Y(i), gate.Z(i)] for i in range(16)]
        self.projectors = [(gate.P0(i), gate.P1(i)) for i in range(16)]
        build_figure14(self)

    def event(self, kind, *args):
        index = len(self.locations) + len(self.actions)
        return Event(index, self.circuit.get_gate_count(), kind, args)

    def noise(self, kind, *qubits):
        self.locations.append(self.event(kind, *qubits))

    def measure(self, q, reg):
        self.actions.append(self.event('measure', q, reg, self.measurements))
        self.measurements += 1

    def reject(self, count):
        self.actions.append(self.event('reject', count))

    def correct(self, reg, *ops):
        gates = tuple(getattr(gate, name)(q) for name, q in ops)
        self.actions.append(self.event('correct', reg, gates))

    def h(self, q):
        self.circuit.add_H_gate(q)

    def ideal_cx(self, a, b):
        self.circuit.add_CNOT_gate(a, b)

    def cx(self, a, b):
        self.ideal_cx(a, b)
        self.noise('depol2', a, b)

    def swap(self, a, b):
        self.circuit.add_SWAP_gate(a, b)

    def t(self, q):
        self.circuit.add_T_gate(q)
        self.noise('depol1', q)

    def tdag(self, q):
        self.circuit.add_Tdag_gate(q)
        self.noise('depol1', q)

    def idle(self, *qubits, interface=False):
        for q in qubits:
            if interface:
                self.interface.add(len(self.locations))
            self.noise('depol1', q)

    def reset_z(self, q):
        # Fig. 14 reuses measured qubits with its explicit feedforward.
        self.noise('x', q)

    def reset_x(self, q):
        self.h(q)
        self.noise('z', q)

    def mes_z(self, q, reg):
        self.noise('x', q)
        self.measure(q, reg)

    def mes_x(self, q, reg):
        self.h(q)
        self.mes_z(q, reg)

    def mes_reset_x(self, q, reg):
        self.mes_x(q, reg)
        self.reset_x(q)

    def sample_faults(self, rng, count):
        # Conditional on the number of Bernoulli(p) faults, their subset is uniform.
        result = {}
        for i in sorted(rng.choice(len(self.locations), count, replace=False)):
            kind = self.locations[i].kind
            if kind in ('x', 'z'):
                result[i] = 1 if kind == 'x' else 3
            else:
                result[i] = int(rng.integers(1, 16 if kind == 'depol2' else 4))
        return result

    def trajectory(self, faults, uniforms):
        state = QuantumState(16)
        registers = [0] * 12
        fault_events = (
            Event(self.locations[i].order, self.locations[i].gate_offset, 'pauli',
                  (self.locations[i].args, faults[i])) for i in sorted(faults)
        )
        previous = 0
        for e in merge(self.actions, fault_events, key=lambda e: e.order):
            if previous != e.gate_offset:
                self.circuit.update_quantum_state(state, previous, e.gate_offset)
                previous = e.gate_offset
            if e.kind == 'measure':
                q, reg, measurement = e.args
                prob0 = min(1.0, max(0.0, state.get_zero_probability(q)))
                bit = int(uniforms[measurement] >= prob0)
                self.projectors[q][bit].update_quantum_state(state)
                state.normalize(state.get_squared_norm())
                registers[reg] = bit
            elif e.kind == 'correct':
                reg, gates = e.args
                if registers[reg]:
                    for correction in gates:
                        correction.update_quantum_state(state)
            elif e.kind == 'reject':
                if any(registers[:e.args[0]]):
                    return None
            elif e.kind == 'pauli':
                qubits, code = e.args
                for q in qubits:
                    pauli = self.paulis[q][code & 3]
                    if pauli is not None:
                        pauli.update_quantum_state(state)
                    code >>= 2
        if previous != self.circuit.get_gate_count():
            self.circuit.update_quantum_state(state, previous, self.circuit.get_gate_count())
        return state.get_vector().reshape(256, 256), registers[4]


def summarize_trajectory(result, frame_targets):
    if result is None:
        return None
    a, fifth = result  # a[ancilla basis, data basis]; Qulacs bit 0 is least significant.
    # Fig. 14 uses the absolute overlap with the full 16-qubit reference, ancilla = 0.
    errors = np.abs(frame_targets @ a[0]) < 0.999
    rows = a[np.any(a != 0, axis=1)]
    cols = np.flatnonzero(np.any(rows != 0, axis=0))
    reduced = rows[:, cols]
    return cols, reduced.T @ reduced.conj(), errors, fifth


class Ensemble:
    def __init__(self):
        self.total = np.zeros((256, 256), dtype=complex)
        self.errors = np.zeros(8, dtype=np.int64)
        self.accepted = 0
        self.fifth = 0

    def add(self, summary, n=1):
        if summary is not None:
            cols, rho, errors, fifth = summary
            self.total[np.ix_(cols, cols)] += n * rho
            self.errors += n * errors
            self.accepted += n
            self.fifth += n * fifth

    def density(self):
        if not self.accepted:
            raise ValueError("No preparation shot was accepted. Increase --prep-shots.")
        rho = self.total / self.accepted
        if not np.isclose(rho.trace(), 1, rtol=0, atol=1e-9):
            raise ArithmeticError("Preparation density matrix lost normalization.")
        return rho


def prepare(p, shots, rng):
    schedule = Schedule()
    target = encoded_target()
    frame_targets = logical_frames() * target
    standalone, split = Ensemble(), Ensemble()
    # The noiseless preparation deterministically returns the target after feedforward.
    check = schedule.trajectory({}, rng.random(schedule.measurements))
    if check is None or check[1] or not np.isclose(abs(check[0][0] @ target), 1, rtol=0, atol=1e-10):
        raise ArithmeticError("Noiseless preparation failed its encoded CCZ reference check.")
    ideal = np.zeros((256, 256), complex)
    ideal[0] = target
    clean_summary = summarize_trajectory((ideal, 0), frame_targets)
    # Aggregate the many fault-free trajectories exactly. Sample all fault counts with
    # their binomial probabilities, including patterns containing three or more faults.
    left = shots
    while left:
        size = min(left, 65536)
        counts = rng.binomial(len(schedule.locations), p, size)
        clean = int(np.count_nonzero(counts == 0))
        standalone.add(clean_summary, clean)
        split.add(clean_summary, clean)
        for count in counts[counts != 0]:
            faults = schedule.sample_faults(rng, count)
            uniforms = rng.random(schedule.measurements)
            summary = summarize_trajectory(schedule.trajectory(faults, uniforms), frame_targets)
            standalone.add(summary)
            if not schedule.interface.isdisjoint(faults):
                remaining = {i: code for i, code in faults.items() if i not in schedule.interface}
                summary = (summarize_trajectory(schedule.trajectory(remaining, uniforms), frame_targets)
                           if remaining else clean_summary)
            split.add(summary)
        left -= size
    return standalone, split
