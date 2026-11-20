"""Figura da distribuição de graus P(k) em escala log-log."""
from comum.saida import plt


def grafico_graus(ks, cont, n, pasta):
    _plt = plt()
    fig, ax = _plt.subplots(figsize=(4.2, 3.2))
    ax.loglog(ks[ks > 0], cont[ks[ks > 0]] / n, ".", ms=3)
    ax.set_xlabel("grau $k$")
    ax.set_ylabel("$P(k)$")
    ax.grid(alpha=.3)
    fig.tight_layout()
    fig.savefig(pasta / "fig" / "graus.pdf")
    _plt.close(fig)
