"""Original full Clifford decoder and the AIT/surface-code noise sample."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np
import pymatching
import stim


def circuits(variant, p):
    root = Path(__file__).resolve().parent / 'circuits'
    meta = json.loads((root / f'{variant}.json').read_text())
    raw = gzip.decompress((root / f'{variant}.stim.gz').read_bytes())
    if hashlib.sha256(raw).hexdigest() != meta['sha256']:
        raise ValueError('The Stim circuit and the postselection metadata do not match.')
    template = stim.Circuit(raw.decode())
    if template.num_detectors != meta['num_detectors'] or template.num_observables != 3:
        raise ValueError('Unexpected Stim detector/observable layout.')
    full, downstream = stim.Circuit(), stim.Circuit()
    round_no = 1
    initial = set(meta['initial_block'])
    data = set(meta['data_readout'])
    block = initial.copy()
    crossings = Counter()
    readouts = []
    instructions = list(template)
    for i, op in enumerate(instructions):
        if op.name == 'TICK':
            round_no += 1
            if round_no == 20:
                # One register is reset on a fresh physical site in the Stim layout.
                block |= data
        if op.name not in ('DEPOLARIZE1', 'DEPOLARIZE2', 'X_ERROR', 'Z_ERROR'):
            if stim.gate_data(op.name).is_noisy_gate and op.gate_args_copy():
                raise ValueError(f'Unexpected parametrized noise instruction {op}')
            full.append(op)
            downstream.append(op)
            continue
        if op.gate_args_copy() != [0.001]:
            raise ValueError('Unexpected reference noise parameter in Stim template.')
        targets = op.targets_copy()
        full.append(op.name, targets, p)
        if round_no > 24:
            downstream.append(op.name, targets, p)
            continue
        kept = []
        if op.name == 'DEPOLARIZE2':
            for first, second in zip(targets[::2], targets[1::2]):
                n_base = int(first.value in block) + int(second.value in block)
                if n_base == 1:
                    crossings[round_no] += 1
                if n_base < 2:
                    kept.extend((first, second))
        else:
            mx_targets = set()
            if round_no == 24 and op.name == 'Z_ERROR' and instructions[i + 1].name == 'MX':
                mx_targets = data.intersection(t.value for t in instructions[i + 1].targets_copy())
            for t in targets:
                if t.value in mx_targets:
                    readouts.append(t.value)
                if t.value not in block or t.value in mx_targets:
                    kept.append(t)
        if kept:
            downstream.append(op.name, kept, p)
    if crossings != {14: 6, 18: 6} or readouts != meta['data_readout']:
        raise ValueError('The AIT boundaries do not match the preparation layout.')
    if full.without_noise() != downstream.without_noise():
        raise ValueError('The noise split changed the ideal circuit.')
    return full, downstream, np.array(meta['postselect']), meta


def residual_counts(circuit, matcher, postselect, shots, batch, seed):
    sampler = circuit.compile_detector_sampler(seed=seed)
    counts = np.zeros(8, dtype=np.int64)
    left = shots
    while left:
        n = min(batch, left)
        detectors, observed = sampler.sample(n, separate_observables=True)
        keep = ~np.any(detectors[:, postselect], axis=1)
        if np.any(keep):
            predicted = matcher.decode_batch(detectors[keep])
            residual = observed[keep] ^ predicted
            counts += np.bincount(residual.astype(np.uint8) @ np.array([1, 2, 4], np.uint8),
                                  minlength=8)
        left -= n
    if not counts.sum():
        raise ValueError('No Clifford shot was accepted. Increase --stim-shots.')
    return counts


def sample_variant(variant, p, shots, batch, seeds):
    full, downstream, postselect, meta = circuits(variant, p)
    matcher = pymatching.Matching.from_detector_error_model(
        full.detector_error_model(decompose_errors=True))
    matcher.ensure_num_fault_ids(3)
    residual = residual_counts(downstream, matcher, postselect, shots, batch, seeds[0])
    reference = residual_counts(full, matcher, postselect, shots, batch, seeds[1])
    return residual, reference, meta
