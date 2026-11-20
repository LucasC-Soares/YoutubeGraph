"""Figura: P(k) e CCDF em escala log-log, com o ajuste por máxima verossimilhança."""
import numpy as np

from comum.saida import plt


def grafico(ks, pk, ccdf, melhor, pasta):
    _plt = plt()
    fig, axs = _plt.subplots(1, 2, figsize=(7.0, 3.0))
    axs[0].loglog(ks, pk, ".", ms=3)
    axs[0].set_xlabel("grau $k$")
    axs[0].set_ylabel("$P(k)$")
    axs[1].loglog(ks, ccdf, ".", ms=3, label="CCDF empírica")
    if melhor:
        kk = np.logspace(np.log10(melhor["kmin"]), np.log10(ks.max()), 100)
        ref = ccdf[ks >= melhor["kmin"]][0]
        axs[1].loglog(kk, ref * ((kk - 0.5) / (melhor["kmin"] - 0.5)) ** (1 - melhor["gamma"]), "r-", lw=1,
                      label=f"MLE: $\\gamma={melhor['gamma']:.2f}$, $k_{{min}}={melhor['kmin']}$")
    axs[1].set_xlabel("grau $k$")
    axs[1].set_ylabel("$P(K \\geq k)$")
    axs[1].legend(fontsize=7)
    for ax in axs:
        ax.grid(alpha=.3, which="both")
    fig.tight_layout()
    fig.savefig(pasta / "fig" / "potencia.pdf")
    _plt.close(fig)
