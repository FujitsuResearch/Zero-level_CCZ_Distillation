"""Plot the six trace-distance estimates in the style of the manuscript LEP figure."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
import scienceplots  # Registers the manuscript's science and ieee styles.

root = Path(__file__).resolve().parent
points = sorted(json.loads((root / "trace_distance_vs_p.json").read_text())["points"],
                key=lambda row: row["p"])
p = [row["p"] for row in points]
plt.style.use(["science", "ieee"])
fig, ax = plt.subplots()
for series, label, color, marker, line in [
    ("preparation", "Preparation only", "0.35", "s", "--"),
    ("d3", r"Ungrown ($d=3$)", "r", ".", "-"),
    ("pre9", r"Grown ($d=3\!\to\!9$)", "b", "x", "-."),
]:
    values = [row["estimates"][series] for row in points]
    artists = ax.errorbar(p, [v["D"] for v in values], yerr=[v["se"] for v in values],
                color=color, marker=marker, linestyle=line, linewidth=0.65,
                markerfacecolor="none" if series == "preparation" else color,
                markersize=4, capsize=2, elinewidth=0.6, label=label)
    # Keep complete endpoint markers and error-bar caps on the axis boundaries.
    line_artist, caps, _ = artists.lines
    line_artist.set_clip_on(False)
    for cap in caps:
        cap.set_clip_on(False)
ax.set(xscale="log", yscale="log", xlabel="Physical Error Rate", ylabel="Trace Distance")
ax.margins(y=0.13)
ax.set_xlim(min(p), max(p))
ax.xaxis.set_minor_formatter(NullFormatter())
ax.grid()
ax.legend(loc="lower right", fontsize="x-small")
for ext in ("pdf", "png"):
    fig.savefig(root / f"trace_distance_single.{ext}", dpi=350)
