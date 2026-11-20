"""Stratified samples of the existing Fig. 14 state-vector preparation circuit."""
import argparse
import os
import sys
from importlib.metadata import version
from pathlib import Path

for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ.setdefault(variable, '1')
import numpy as np
from scipy.stats import binom

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from preparation import Schedule, encoded_target


def reduced_state(result, basis):
    if result is None:
        return None
    vectors, _ = result
    vectors = vectors[:, basis]
    vectors = vectors[np.any(vectors != 0, axis=1)]
    rho = vectors.T @ vectors.conj()
    if not np.isclose(rho.trace(), 1, atol=1e-10, rtol=0):
        raise ArithmeticError('Unexpected probability outside the accepted data basis.')
    return rho


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--groups', type=int, default=20)
    parser.add_argument('--seed', type=int, default=736511)
    parser.add_argument('--stratum-sizes', type=int, nargs=5, default=(512, 3200, 640, 160, 40),
                        metavar=('N1', 'N2', 'N3', 'N4', 'N5PLUS'))
    parser.add_argument('--tail-p', type=float, default=0.016)
    parser.add_argument('--data-dir', type=Path, default=Path(__file__).resolve().parent / 'data')
    args = parser.parse_args()
    if args.groups < 2 or args.seed < 0 or min(args.stratum_sizes) < 1 or not 0 < args.tail_p < 1:
        parser.error('need positive stratum sizes, at least two groups and 0 < tail-p < 1')
    args.data_dir.mkdir(parents=True, exist_ok=True)
    schedule = Schedule()
    n = len(schedule.locations)
    # The accepted Z checks for registers 1,2,3 give three independent parity
    # constraints; leave both outcomes of the fifth syndrome (register 4) intact.
    basis = np.array([x for x in range(256) if all(
        (x & m).bit_count() % 2 == 0 for m in (0x0f, 0xf0, 0x33))])
    target = encoded_target()[basis]
    ideal = np.outer(target, target)
    k_tail = np.arange(5, n+1)
    tail_probs = binom.pmf(k_tail, n, args.tail_p) / binom.sf(4, n, args.tail_p)
    children = np.random.SeedSequence(args.seed).spawn(args.groups)
    group_sums = []
    group_counts = []
    for g, child in enumerate(children, 1):
        rng = np.random.default_rng(child)
        counts = np.zeros(n+1, np.int64)
        sums = {}
        for stratum, size in enumerate(args.stratum_sizes, 1):
            ks = (np.full(size, stratum) if stratum < 5
                  else rng.choice(k_tail, p=tail_probs, size=size))
            for k in ks:
                if k not in sums:
                    sums[k] = np.zeros((2, len(basis), len(basis)), complex)
                counts[k] += 1
                faults = schedule.sample_faults(rng, k)
                draws = rng.random(schedule.measurements)
                standalone = reduced_state(schedule.trajectory(faults, draws), basis)
                if standalone is not None:
                    sums[k][0] += standalone
                if schedule.interface.isdisjoint(faults):
                    split = standalone
                else:
                    other = {i: code for i, code in faults.items() if i not in schedule.interface}
                    split = reduced_state(schedule.trajectory(other, draws), basis) if other else ideal
                if split is not None:
                    sums[k][1] += split
        group_sums.append(sums)
        group_counts.append(counts)
        print(f'Preparation group {g}/{args.groups}', flush=True)
    max_k = max(max(s) for s in group_sums)
    data = np.zeros((args.groups, max_k+1, 2, len(basis), len(basis)), complex)
    for g, sums in enumerate(group_sums):
        for k, value in sums.items():
            data[g, k] = value
    np.savez_compressed(args.data_dir / 'preparation.npz', rho_sums=data,
                        drawn=np.stack(group_counts)[:, :max_k+1], basis=basis,
                        n_locations=n, seed=args.seed, stratum_sizes=args.stratum_sizes,
                        tail_p=args.tail_p, groups=args.groups, qulacs_version=version('qulacs'),
                        numpy_version=version('numpy'), scipy_version=version('scipy'))


if __name__ == '__main__':
    main()
