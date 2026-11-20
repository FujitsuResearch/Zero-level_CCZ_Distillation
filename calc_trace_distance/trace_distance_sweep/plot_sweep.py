"""Reweight the preparation trajectories and plot the three trace-distance estimates."""
import argparse
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from scipy.stats import binom

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from preparation import encoded_target, logical_frames
from trace_distance import apply_z_channel, distance
from sample_downstream import RATES, data_path

SERIES = ('preparation', 'd3', 'pre9')


def weighted_groups(prep, p):
    n = int(prep['n_locations'])
    q = float(prep['tail_p'])
    rho = prep['rho_sums']
    k = np.arange(rho.shape[1])
    sizes = prep['stratum_sizes']
    w = np.zeros(k.size)
    w[1:5] = binom.pmf(k[1:5], n, p) / sizes[:4]
    # k >= 5 was sampled from Binom(n,q) conditional on k>=5. Each draw
    # contributes its unconditional probability at p divided by its proposal.
    w[5:] = np.exp(binom.logpmf(k[5:], n, p) - binom.logpmf(k[5:], n, q)
                   + binom.logsf(4, n, q)) / sizes[4]
    target = encoded_target()[prep['basis']]
    clean = binom.pmf(0, n, p) * np.outer(target, target)
    return clean + np.einsum('k,gkvij->gvij', w, rho, optimize=True)


def metrics(unnormalized, counts, target, frames, *, include_alternative=False):
    accept = np.trace(unnormalized, axis1=1, axis2=2).real
    if np.any(accept <= 0) or np.any(counts.sum(axis=1) == 0):
        raise ValueError('At least one stage has no accepted shots.')
    rho = unnormalized / accept[:, None, None]
    values = [distance(rho[0], target)]
    for hist in counts:
        values.append(distance(apply_z_channel(rho[1], hist / hist.sum(), frames), target))
    if include_alternative:
        for hist in counts:
            values.append(distance(apply_z_channel(rho[0], hist / hist.sum(), frames), target))
    return np.array(values)


def estimate(p, prep, directory):
    basis = prep['basis']
    target, frames = encoded_target()[basis], logical_frames()[:, basis]
    groups = weighted_groups(prep, p)
    hist, run_info = [], {}
    for v in SERIES[1:]:
        raw = json.loads(data_path(directory, v, p).read_text())
        if raw['p'] != p or raw['variant'] != v or raw['groups'] != len(groups):
            raise ValueError('Inconsistent probability, variant or number of groups in raw data.')
        c = np.asarray(raw['residual_counts'], dtype=np.int64)
        if c.shape != (len(groups), 8):
            raise ValueError('Invalid logical frame counts.')
        hist.append(c)
        run_info[v] = dict(shots=raw['groups'] * raw['shots_per_group'],
                           accepted=int(c.sum()), z_errors=int(c[:, 1:].sum()))
    hist = np.stack(hist, axis=1)
    a, c = groups.sum(axis=0), hist.sum(axis=0)
    point = metrics(a, c, target, frames, include_alternative=True)
    jackknife = np.array([metrics(a-ag, c-cg, target, frames, include_alternative=True)
                          for ag, cg in zip(groups, hist)])
    centered = jackknife - jackknife.mean(axis=0)
    covariance = (len(groups)-1) / len(groups) * (centered.T @ centered)
    se = np.sqrt(np.diag(covariance))
    if not np.isfinite(point).all() or not np.isfinite(se).all():
        raise ArithmeticError('Non-finite point estimate or sampling uncertainty.')
    return dict(p=p, estimates={s: dict(D=float(d), se=float(e)) for s,d,e in zip(SERIES, point, se)},
                figure14_plus_downstream_z={s: dict(D=float(d), se=float(e))
                                            for s,d,e in zip(SERIES[1:], point[3:], se[3:])},
                covariance=covariance[:3,:3].tolist(), downstream=run_info,
                preparation_acceptance=(np.trace(a, axis1=1, axis2=2).real / len(groups)).tolist())


def p_label(x, pos=None):
    if x <= 0:
        return ''
    exponent = int(np.floor(np.log10(x) + 1e-12))
    m = x / 10**exponent
    return (rf'$10^{{{exponent}}}$' if np.isclose(m, 1) else
            rf'${m:.3g}\!\times\!10^{{{exponent}}}$')


def plot(points, output, figure14_idles=False):
    p = np.array([a['p'] for a in points])
    styles = [
        ('#474b50', 's', '--', 'Preparation only (Fig. 14)', 'white'),
        ('#b64129', 'o', '-', r'Logical $Z$ model, $d=3$', 'white'),
        ('#1c6099', '^', '-.', r'Logical $Z$ model, $d=3\,\to\,9$', '#1c6099')]
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'axes.labelsize': 12, 'pdf.fonttype': 42, 'mathtext.fontset': 'dejavusans'})
    fig, axes = plt.subplots(2, figsize=(6.65, 5.55), sharex=True,
                             gridspec_kw={'height_ratios': [1.65, 1]})
    fig.subplots_adjust(left=.142, right=.976, top=.973, bottom=.15, hspace=.12)
    for s, (color, marker, ls, label, face) in zip(SERIES, styles):
        field = 'figure14_plus_downstream_z' if figure14_idles and s != 'preparation' else 'estimates'
        d = np.array([a[field][s]['D'] for a in points])
        se = np.array([a[field][s]['se'] for a in points])
        for ax, y, err in ((axes[0], d, se), (axes[1], d / p**2, se / p**2)):
            ax.errorbar(p, y, yerr=err, color=color, marker=marker, ls=ls, label=label,
                        markersize=5.3, markerfacecolor=face, markeredgewidth=1.15,
                        linewidth=1.25, elinewidth=.95, capsize=2.6)
    for ax in axes:
        ax.set_xscale('log')
        ax.spines[['top', 'right']].set_visible(False)
        ax.tick_params(which='both', direction='out')
        ax.set_axisbelow(True)
        ax.grid(axis='y', which='major', color='#d8dbdf', lw=.65)
    axes[0].set_yscale('log')
    axes[0].set_ylabel(r'Trace distance $D$')
    axes[0].margins(y=.16)
    axes[0].legend(loc='upper left', frameon=False, handlelength=2.5, fontsize=9.3)
    axes[1].set_ylabel(r'$D\,/\,p^2$')
    axes[1].set_xlabel(r'Physical error rate $p$', labelpad=6)
    if len(p) <= 7:
        axes[1].xaxis.set_major_locator(ticker.FixedLocator(p))
        axes[1].xaxis.set_major_formatter(ticker.FuncFormatter(p_label))
        axes[1].xaxis.set_minor_locator(ticker.NullLocator())
    axes[1].yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
    left, right = (p.min()/1.09, p.max()*1.09)
    axes[1].set_xlim(left, right)
    caption = 'Error bars show one Monte Carlo standard error.'
    stem = 'trace_distance_vs_p'
    if figure14_idles:
        caption += ' Preparation retains the Fig. 14 idle noise.'
        stem += '_figure14_idles'
    fig.text(.142, .027, caption, fontsize=8.5, color='#43484f')
    fig.savefig(output / f'{stem}.pdf')
    fig.savefig(output / f'{stem}.png', dpi=250)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--p', nargs='+', type=float, default=RATES)
    parser.add_argument('--figure14-idles', action='store_true',
                        help='plot composition retaining stand-alone Fig. 14 idle noise')
    parser.add_argument('--data-dir', type=Path, default=Path(__file__).resolve().parent / 'data')
    parser.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    if any(not 0 < x < 1 for x in args.p):
        parser.error('Log axes and binomial weights require 0 < p < 1.')
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with np.load(args.data_dir / 'preparation.npz') as prep:
        points = [estimate(p, prep, args.data_dir) for p in sorted(set(args.p))]
        summary = dict(model='independently accepted preparation and logical Z channel; interface idles excluded for d3/pre9',
                       uncertainty='one delete-one-group jackknife standard error; shared preparation across probabilities and variants',
                       groups=int(prep['groups']), preparation_shots=int(prep['drawn'].sum()),
                       series_order=SERIES, points=points)
    (args.output_dir / 'trace_distance_vs_p.json').write_text(json.dumps(summary, indent=2) + '\n')
    plot(points, args.output_dir, args.figure14_idles)


if __name__ == '__main__':
    main()
