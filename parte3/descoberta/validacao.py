"""Valida k-core e assortatividade contra o NetworkX em grafos pequenos.  python -m parte3.descoberta.validacao"""
import networkx as nx
import numpy as np

from comum.grafo import arestas, csr_from_edges
from parte3.descoberta.kcore import coreness
from parte3.descoberta.nulo import assortatividade, configuracao_apagada


def main():
    rng = np.random.default_rng(0)
    for n, m in [(50, 120), (300, 900), (2000, 9000)]:
        u, v = rng.integers(0, n, m), rng.integers(0, n, m)
        ok = u != v
        chave = np.unique(np.minimum(u[ok], v[ok]) * n + np.maximum(u[ok], v[ok]))
        ip, ind = csr_from_edges(n, chave // n, chave % n)
        g = nx.Graph()
        g.add_nodes_from(range(n))
        g.add_edges_from(zip(*arestas(ip, ind)))
        ref = nx.core_number(g)
        assert all(coreness(ip, ind)[i] == ref[i] for i in range(n)), "k-core difere"
        assert abs(assortatividade(ip, ind) - nx.degree_assortativity_coefficient(g)) < 1e-9, "assortatividade difere"
    ip, ind, perda = configuracao_apagada(np.diff(ip), rng)
    assert 0 <= perda < 0.2
    print("ok: k-core, assortatividade e nulo concordam/são consistentes")


if __name__ == "__main__":
    main()
