"""Figura: boxplots (remoção aleatória) + marcadores (ataques) + linha do grafo original."""
from comum.saida import plt

NOMES = {"A_S": "A: $S$ (maior comp./n)", "B_componentes": "B: nº de componentes",
         "C_caminho_medio": "C: caminho médio", "D_isolados": "D: fração de isolados"}


def grafico(base, aleat, cenarios, pasta):
    _plt = plt()
    fig, axs = _plt.subplots(1, 4, figsize=(7.2, 3.0))
    for ax, c in zip(axs, NOMES):
        ax.boxplot([a[c] for a in aleat], widths=.5, positions=[1])
        ax.axhline(base[c], color="k", ls="--", lw=.8, label="original")
        ax.plot([1], [cenarios["grau"][c]], "rx", label="ataque: grau")
        ax.plot([1], [cenarios["PageRank"][c]], "b+", label="ataque: PageRank")
        ax.set_title(NOMES[c], fontsize=7)
        ax.set_xticks([])
        ax.tick_params(labelsize=6)
    axs[0].legend(fontsize=5)
    fig.tight_layout()
    fig.savefig(pasta / "fig" / "robustez.pdf")
    _plt.close(fig)
