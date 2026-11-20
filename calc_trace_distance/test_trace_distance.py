"""Deterministic controls for the state, subsystem split, and Clifford observables."""
import unittest

from trace_distance import apply_z_channel, distance
from downstream import circuits
from preparation import (Ensemble, Schedule, encoded_target, logical_frames,
                         summarize_trajectory)
import numpy as np
import stim


class PrepControls(unittest.TestCase):
    def setUp(self):
        self.v = encoded_target()
        self.frames = logical_frames()
        self.targets = self.frames * self.v
        self.projector = np.outer(self.v, self.v)

    def test_all_logical_z_are_orthogonal(self):
        np.testing.assert_allclose(self.targets @ self.targets.T, np.eye(8))
        for i, xmask in enumerate((0x55, 0x33, 0x0f)):
            for j in range(3):
                self.assertEqual(self.frames[1 << j, xmask], -1 if j == i else 1)
        w = np.arange(1, 9) / 36
        mixed = apply_z_channel(self.projector, w, self.frames)
        self.assertAlmostEqual(distance(mixed, self.v), 1 - w[0])

    def test_every_noiseless_feedforward_record(self):
        s = Schedule()
        self.assertEqual(len(s.locations), 242)
        self.assertEqual(len(s.interface), 12)
        for k in range(32):
            draws = np.full(s.measurements, 0.5)
            # Three feedforward measurements in round 19 and two in round 22.
            for i in range(5):
                draws[12+i] = 0.75 if k & (1 << i) else 0.25
            state, fifth = s.trajectory({}, draws)
            self.assertEqual(fifth, 0)
            self.assertAlmostEqual(abs(state[0] @ self.v), 1)

    def test_average_density_and_trace_out_ancillas(self):
        # Two coherent branches in distinct ancilla states. After tracing out the
        # ancillas their off-diagonal terms cancel, including for complex amplitudes.
        a = np.zeros((256, 256), complex)
        for i, sign in enumerate((1, -1)):
            a[i] = (self.v + sign * 1j * self.targets[1]) / 2
        ensemble = Ensemble()
        ensemble.add(summarize_trajectory((a, 0), self.targets))
        self.assertAlmostEqual(distance(ensemble.density(), self.v), 0.5)
        self.assertAlmostEqual(distance(np.outer(a[0], a[0].conj()) * 2, self.v), np.sqrt(0.5))
        # A complex-phase pure branch also checks the orientation of the partial trace.
        ensemble = Ensemble()
        a[0] *= np.sqrt(2)
        a[1] = 0
        ensemble.add(summarize_trajectory((a, 0), self.targets))
        np.testing.assert_allclose(ensemble.density(), np.outer(a[0], a[0].conj()))

    def test_original_acceptance_and_known_faults(self):
        class Inject(Schedule):
            def __init__(self, ops):
                self.ops = ops
                super().__init__()

            def reject(self, count):
                super().reject(count)
                if count == 6:  # After swaps but before the ideal stabilizer checks.
                    for axis, q in self.ops:
                        getattr(self.circuit, f'add_{axis}_gate')(q)

        rng = np.random.default_rng(725)
        ensemble = Ensemble()
        for ops, fifth, n in [((), 0, 3), ((('Z', 0), ('Z', 4)), 0, 1)]:
            s = Inject(ops)
            result = s.trajectory({}, rng.random(s.measurements))
            self.assertEqual(result[1], fifth)
            ensemble.add(summarize_trajectory(result, self.targets), n)
        self.assertAlmostEqual(distance(ensemble.density(), self.v), 0.25)
        s = Inject((('X', 0), ('X', 1)))
        result = s.trajectory({}, rng.random(s.measurements))
        self.assertEqual(result[1], 1)
        self.assertAlmostEqual(abs(result[0][0] @ self.v), 0)
        s = Inject((('X', 0),))
        self.assertIsNone(s.trajectory({}, rng.random(s.measurements)))


class CliffordControls(unittest.TestCase):
    def test_matching_zz_readout_flips_are_invisible(self):
        for v in ('d3', 'pre9'):
            full, downstream, postselect, meta = circuits(v, 0)
            self.assertEqual(full.without_noise(), downstream.without_noise())
            for ids in meta['zz_measurement_records']:
                for flips in (ids[:1], ids):
                    faulty = stim.Circuit()
                    record = injected = 0
                    for op in downstream.without_noise():
                        if op.name == 'MR':
                            for t in op.targets_copy():
                                if record in flips:
                                    faulty.append('X_ERROR', [t], 1)
                                    injected += 1
                                faulty.append('MR', [t])
                                record += 1
                        else:
                            faulty.append(op)
                            record += op.num_measurements
                    self.assertEqual(injected, len(flips))
                    det, obs = faulty.compile_detector_sampler(seed=917).sample(
                        4, separate_observables=True)
                    if len(flips) == 1:
                        self.assertTrue(det[:, postselect].any(axis=1).all())
                    else:
                        self.assertFalse(det.any())
                        self.assertFalse(obs.any())


if __name__ == '__main__':
    unittest.main()
