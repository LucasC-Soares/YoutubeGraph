"""Item 13 da Parte I: visualização reduzida do grafo."""
import numpy as np

from comum.caminhos import bfs_dist
from comum.config import SEED
from comum.grafo import arestas, subgrafo
from comum.saida import plt


def visualizar(ip, ind, k, pasta):
    """Subgrafo reduzido: k vértices mais próximos do hub de maior grau."""
    import networkx as nx
    deg = np.diff(ip)
    hub = int(np.argmax(deg))
    d = bfs_dist(ip, ind, hub)
    cand = np.flatnonzero(d >= 0)
    ordem = np.lexsort((-deg[cand], d[cand]))
    escolhidos = cand[ordem[:k]]
    sp, si = subgrafo(ip, ind, escolhidos)
    u, v = arestas(sp, si)
    g = nx.Graph()
    g.add_nodes_from(range(len(sp) - 1))
    g.add_edges_from(zip(u.tolist(), v.tolist()))
    _plt = plt()
    fig, ax = _plt.subplots(figsize=(4.2, 4.2))
    pos = nx.spring_layout(g, seed=SEED)
    gr = np.diff(sp)
    nx.draw_networkx_edges(g, pos, ax=ax, alpha=.25, width=.5)
    nx.draw_networkx_nodes(g, pos, ax=ax, node_size=8 + 6 * np.sqrt(gr), node_color=gr,
                           cmap="viridis", linewidths=0)
    ax.set_axis_off()
    fig.tight_layout()
    fig.savefig(pasta / "fig" / "visualizacao.pdf")
    _plt.close(fig)
