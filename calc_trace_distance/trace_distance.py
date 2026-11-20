"""Estimate accepted CCZ trace distance under the referee's logical-Z model."""
import argparse
import json
import os
import tempfile
from importlib.metadata import version
from pathlib import Path

# Small state vectors run faster on a single thread; explicit user settings win.
for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ.setdefault(variable, '1')

import numpy as np
from downstream import sample_variant
from preparation import encoded_target, logical_frames, prepare


def distance(rho, target):
    delta = rho - np.outer(target, target.conj())
    return float(np.abs(np.linalg.eigvalsh((delta + delta.conj().T) / 2)).sum() / 2)


def apply_z_channel(rho, probabilities, frames):
    return rho * (frames.T @ (probabilities[:, None] * frames))


def pack_density(rho):
    indices = np.flatnonzero(np.any(rho != 0, axis=0))
    block = rho[np.ix_(indices, indices)]
    return dict(basis_indices=indices.tolist(), real=block.real.tolist(), imag=block.imag.tolist())


def binomial_record(errors, accepted):
    # Wilson 95% interval conditional on acceptance, including zero observed events.
    z = 1.959963984540054
    f = errors / accepted
    denom = 1 + z*z / accepted
    mid = (f + z*z / (2*accepted)) / denom
    half = z * np.sqrt(f*(1-f)/accepted + z*z/(4*accepted**2)) / denom
    lower = 0. if errors == 0 else max(0., float(mid - half))
    upper = 1. if errors == accepted else min(1., float(mid + half))
    return dict(errors=int(errors), lep=float(f), wilson95=[lower, upper])


def prep_record(ensemble, rho, target, shots):
    return dict(shots=shots, accepted=ensemble.accepted, fifth_syndrome_ones=ensemble.fifth,
                trace_distance=distance(rho, target), **binomial_record(int(ensemble.errors[0]), ensemble.accepted),
                errors_if_frame_applied=ensemble.errors.tolist(), density=pack_density(rho))


def stim_record(counts, shots):
    accepted = int(counts.sum())
    return dict(shots=shots, accepted=accepted, residual_counts=counts.tolist(),
                **binomial_record(int(counts[1:].sum()), accepted))


def run(args):
    # Fixed stream indices keep d3 and pre9 results unchanged when run together.
    streams = np.random.SeedSequence(args.seed).spawn(5)
    prep_rng = np.random.default_rng(streams[0])
    standalone, split = prepare(args.p, args.prep_shots, prep_rng)
    rho_fig, rho_split = standalone.density(), split.density()
    target, frames = encoded_target(), logical_frames()
    result = dict(model='independent postselected preparation and stochastic logical Z',
                  scope={
                      'preparation': 'Figure 14 four-bit acceptance; fifth syndrome measured and recorded',
                      'composition': 'Independent accepted ensembles; 12 stand-alone idles replaced by AIT couplings',
                      'unmeasured': 'Logical X/Y components, including wrong repeated ZZ outcomes, and joint stage postselection',
                      'frame_order': 'k = obs0 + 2*obs1 + 4*obs2; physical Z masks [3,5,17]',
                  },
                  p=args.p, seed=args.seed, stim_batch=args.batch_size,
                  versions={lib: version(lib) for lib in ('numpy', 'qulacs', 'stim', 'pymatching')},
                  figure14=prep_record(standalone, rho_fig, target, args.prep_shots),
                  preparation_for_composition=prep_record(split, rho_split, target, args.prep_shots),
                  variants={})
    for v in (('d3', 'pre9') if args.variant == 'both' else (args.variant,)):
        offset = 1 if v == 'd3' else 3
        seeds = [int(s.generate_state(1, dtype=np.uint64)[0]) for s in streams[offset:offset+2]]
        downstream, reference, meta = sample_variant(v, args.p, args.stim_shots, args.batch_size, seeds)
        weights = downstream / downstream.sum()
        rho_output = apply_z_channel(rho_split, weights, frames)
        figure14_output = apply_z_channel(rho_fig, weights, frames)
        result['variants'][v] = dict(
            stim_source=meta['source'], stim_sha256=meta['sha256'],
            downstream=dict(**stim_record(downstream, args.stim_shots),
                            trace_distance_on_ideal_input=float(weights[1:].sum())),
            full_clifford_reference=stim_record(reference, args.stim_shots),
            figure14_plus_downstream_z=dict(
                trace_distance=distance(figure14_output, target),
                lep=float(weights @ (standalone.errors / standalone.accepted))),
            trace_distance_z_model=distance(rho_output, target),
            lep_z_model=float(weights @ (split.errors / split.accepted)))
    return result


def positive(value):
    n = int(value)
    if n < 1:
        raise argparse.ArgumentTypeError('must be a positive integer')
    return n


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--p', required=True, type=float)
    parser.add_argument('--variant', choices=['d3', 'pre9', 'both'], default='both')
    parser.add_argument('--prep-shots', type=positive, required=True)
    parser.add_argument('--stim-shots', type=positive, required=True)
    parser.add_argument('--batch-size', type=positive, default=4096)
    parser.add_argument('--seed', type=int, default=1)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if not 0 <= args.p <= 1 or args.seed < 0:
        parser.error('p must be between 0 and 1 and seed must be nonnegative')
    if not args.output.parent.is_dir():
        parser.error('the output directory must exist')
    result = run(args)
    with tempfile.NamedTemporaryFile('w', dir=args.output.parent, delete=False) as f:
        tmp = Path(f.name)
        try:
            json.dump(result, f, indent=2, allow_nan=False)
            f.write('\n')
            f.close()
            os.replace(tmp, args.output)
        finally:
            tmp.unlink(missing_ok=True)
    print('Fig. 14  D = {:.8g}  LEP = {:.8g}  ({}/{} accepted)'.format(
        result['figure14']['trace_distance'], result['figure14']['lep'],
        result['figure14']['accepted'], args.prep_shots))
    for v, r in result['variants'].items():
        post = r['downstream']
        print(f"{v}: D(Z model) = {r['trace_distance_z_model']:.8g}, "
              f"LEP(Z model) = {r['lep_z_model']:.8g}, "
              f"downstream Z errors = {post['errors']}/{post['accepted']}")
    print(args.output)


if __name__ == '__main__':
    main()
