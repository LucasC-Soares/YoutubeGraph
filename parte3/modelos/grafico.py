"""Figura: CCDF do grau do grafo real e dos modelos clássicos (log-log)."""
from comum.saida import plt

ESTILOS = ["k.", "b-", "r--", "g:"]


def grafico(ccdfs, pasta):
    _plt = plt()
    fig, ax = _plt.subplots(figsize=(3.4, 2.8))
    for (nome, (ks, ccdf)), est in zip(ccdfs.items(), ESTILOS):
        ax.loglog(ks, ccdf, est, ms=3, lw=1, label=nome)
    ax.set_xlabel("grau $k$")
    ax.set_ylabel("$P(K \\geq k)$")
    ax.set_ylim(bottom=1e-7)
    ax.legend(fontsize=7)
    ax.grid(alpha=.3, which="both")
    fig.tight_layout()
    fig.savefig(pasta / "fig" / "modelos.pdf")
    _plt.close(fig)
