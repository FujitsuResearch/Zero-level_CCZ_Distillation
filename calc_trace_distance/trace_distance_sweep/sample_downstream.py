"""Sample both AIT/surface-code channels in independent batches at each physical p."""
import argparse
import json
import math
import struct
import sys
from pathlib import Path

import numpy as np
import pymatching
import stim

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from downstream import circuits

RATES = (0.0001, 0.0002, 0.0004, 0.0006, 0.0008, 0.001)
BATCHES = 20
SEED = 812735


def data_path(directory, variant, p):
    return directory / f'{variant}_p{repr(float(p))}.json'


def sample(p, variant, total_shots, groups, seed):
    full, downstream, postselect, meta = circuits(variant, p)
    decoder = pymatching.Matching.from_detector_error_model(
        full.detector_error_model(decompose_errors=True))
    decoder.ensure_num_fault_ids(3)
    mask = np.zeros(full.num_detectors, np.uint8)
    mask[postselect] = 1
    mask = np.packbits(mask, bitorder='little')
    zero_prediction = decoder.decode(np.zeros(full.num_detectors, np.uint8))
    mask0 = int(zero_prediction @ np.array([1, 2, 4], np.uint8))
    words = struct.unpack('<II', struct.pack('<d', p))
    children = np.random.SeedSequence([seed, int(variant == 'pre9'), *words]).spawn(groups)
    counts = np.zeros((groups, 8), np.int64)
    group_size = math.ceil(total_shots / groups)
    for i, child in enumerate(children):
        sampler = downstream.compile_detector_sampler(seed=int(child.generate_state(1, np.uint64)[0]))
        for start in range(0, group_size, 8192):
            det, obs = sampler.sample(min(8192, group_size - start), bit_packed=True,
                                      separate_observables=True)
            keep = ~(det & mask).any(axis=1)
            det = det[keep]
            residual = obs[keep, 0].copy()
            nonzero = det.any(axis=1)
            if nonzero.any():
                pred = decoder.decode_batch(det[nonzero], bit_packed_shots=True,
                                            bit_packed_predictions=True)
                residual[nonzero] ^= pred[:, 0]
            residual[~nonzero] ^= mask0
            counts[i] += np.bincount(residual, minlength=8)
    return dict(p=p, variant=variant, seed=seed, shots_per_group=group_size,
                groups=groups, residual_counts=counts.tolist(), stim_sha256=meta['sha256'],
                stim_version=stim.__version__, pymatching_version=pymatching.__version__)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--p', nargs='+', type=float, default=RATES)
    parser.add_argument('--variant', choices=('d3', 'pre9', 'both'), default='both')
    parser.add_argument('--groups', type=int, default=BATCHES)
    parser.add_argument('--seed', type=int, default=SEED)
    parser.add_argument('--shots', type=int, help='total shots per rate and variant')
    parser.add_argument('--data-dir', type=Path, default=Path(__file__).resolve().parent / 'data')
    args = parser.parse_args()
    if args.groups < 2 or args.seed < 0 or (args.shots is not None and args.shots < args.groups):
        parser.error('need at least two groups, one shot per group, and a nonnegative seed')
    if any(not 0 < p < 1 for p in args.p):
        parser.error('each p must be between 0 and 1')
    args.data_dir.mkdir(parents=True, exist_ok=True)
    for p in args.p:
        budget = args.shots or round(max(2e6, min(48e6, 48e6 * (1e-4 / p)**2)))
        for v in (('d3', 'pre9') if args.variant == 'both' else (args.variant,)):
            result = sample(p, v, budget, args.groups, args.seed)
            path = data_path(args.data_dir, v, p)
            path.write_text(json.dumps(result, indent=2) + '\n')
            counts = np.sum(result['residual_counts'], axis=0)
            print(f'{v} p={p:g}: {counts[1:].sum()}/{counts.sum()} residuals', flush=True)


if __name__ == '__main__':
    main()
