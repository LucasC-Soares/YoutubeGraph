"""Figura dos tempos médios com IC95% (log-log)."""
from comum.saida import plt


def grafico(res, pasta):
    _plt = plt()
    fig, ax = _plt.subplots(figsize=(4.4, 3.4))
    por = {}
    for l in res["linhas"]:
        por.setdefault(l["algoritmo"], []).append(l)
    for a, ls in por.items():
        ax.errorbar([l["V"] for l in ls], [l["media_s"] for l in ls],
                    yerr=[l["ic95_s"] for l in ls], marker="o", ms=3, lw=1, capsize=2, label=a)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("vértices $V$ do subgrafo")
    ax.set_ylabel("tempo médio (s)")
    ax.grid(alpha=.3, which="both")
    ax.legend(fontsize=6)
    fig.tight_layout()
    fig.savefig(pasta / "fig" / "tempos.pdf")
    _plt.close(fig)
