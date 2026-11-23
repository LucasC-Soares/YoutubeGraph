"""Figura: (a) fração de vértices em cada k-core e (b) grau médio por coreness."""
import numpy as np

from comum.saida import plt


def grafico(core, deg, pasta):
    _plt = plt()
    fig, axs = _plt.subplots(1, 2, figsize=(7.0, 2.8))
    ks = np.arange(1, core.max() + 1)
    cont = np.bincount(core, minlength=core.max() + 2)
    frac_ge = 1.0 - (np.cumsum(cont)[ks] - cont[ks]) / len(core)  # fração com coreness >= k
    axs[0].semilogy(ks, frac_ge, "k-", lw=1.2)
    axs[0].set_xlabel("$k$")
    axs[0].set_ylabel("fração de vértices no $k$-core")
    cs = np.flatnonzero(cont)
    cs = cs[cs >= 1]
    media = np.array([deg[core == c].mean() for c in cs])
    axs[1].loglog(cs, media, "b.", ms=4)
    axs[1].set_xlabel("coreness")
    axs[1].set_ylabel("grau médio")
    for ax in axs:
        ax.grid(alpha=.3, which="both")
    fig.tight_layout()
    fig.savefig(pasta / "fig" / "nucleo.pdf")
    _plt.close(fig)
