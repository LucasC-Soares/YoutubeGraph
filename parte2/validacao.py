"""Validação cruzada: compara as implementações próprias com o NetworkX em um subgrafo
pequeno (use para provar corretude no relatório).

Uso (na raiz do repositório):  python -m parte2.validacao [--n 1500]
"""
import argparse

import networkx as nx
import numpy as np

from comum.caminhos import bfs_dist, componentes
from comum.config import rng_padrao
from comum.dados import carregar_grafo
from comum.grafo import arestas, subgrafo
from comum.triangulos import clustering_local, triangulos_nos
from parte2 import algoritmos as al
from parte2.subgrafos import bola, montar


def ok(nome, cond):
    print(f"[{'OK ' if cond else 'ERRO'}] {nome}")
    return cond


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1500)
    args = ap.parse_args()
    rng = rng_padrao(9)
    ip, ind, _, _ = carregar_grafo()
    deg = np.diff(ip)
    nos = bola(ip, ind, deg, args.n, rng)
    n, E, adj, adjw, ar_w, arcos = montar(ip, ind, nos, rng)
    sp, si = subgrafo(ip, ind, nos)

    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_weighted_edges_from(ar_w)
    todos = []
    s = int(rng.integers(n))

    # componentes e arestas
    todos.append(ok("nº de arestas", G.number_of_edges() == E))
    todos.append(ok("componentes (vetorizado) == NetworkX",
                    len(np.unique(componentes(n, *arestas(sp, si)))) == nx.number_connected_components(G)))

    # BFS / DFS
    ref = nx.single_source_shortest_path_length(G, s)
    d1 = al.bfs(adj, s)
    d2 = bfs_dist(sp, si, s)
    todos.append(ok("BFS (fila)", all(d1[v] == ref.get(v, -1) for v in range(n))))
    todos.append(ok("BFS (vetorizado)", all(int(d2[v]) == ref.get(v, -1) for v in range(n))))
    ordem, _ = al.dfs(adj, s)
    todos.append(ok("DFS visita a componente de s", set(ordem) == set(ref)))

    # Eulerianidade
    tipo, _ = al.eulerianidade(adj)
    esperado = "circuito euleriano" if nx.is_eulerian(G) else (
        "caminho euleriano" if nx.has_eulerian_path(G) else "nao euleriano")
    todos.append(ok(f"Eulerianidade ({tipo})", tipo == esperado))
    for caso, H in [("ciclo C5", nx.cycle_graph(5)), ("caminho P4", nx.path_graph(4)), ("K4", nx.complete_graph(4))]:
        a = [list(H.neighbors(i)) for i in range(H.number_of_nodes())]
        e2 = "circuito euleriano" if nx.is_eulerian(H) else (
            "caminho euleriano" if nx.has_eulerian_path(H) else "nao euleriano")
        todos.append(ok(f"Eulerianidade {caso}", al.eulerianidade(a)[0] == e2))

    # Dijkstra / Bellman-Ford
    rd = nx.single_source_dijkstra_path_length(G, s)
    dj = al.dijkstra(adjw, s)
    todos.append(ok("Dijkstra", all(abs(dj[v] - rd.get(v, np.inf)) < 1e-9 for v in range(n))))
    bf, neg = al.bellman_ford(n, arcos, s)
    todos.append(ok("Bellman-Ford", (not neg) and all(abs(bf[v] - rd.get(v, np.inf)) < 1e-9 for v in range(n))))

    # Floyd-Warshall (subgrafo de 60 vértices)
    sub = bola(ip, ind, deg, 60, rng)
    n60, _, a60, aw60, arw60, _ = montar(ip, ind, sub, rng)
    H = nx.Graph()
    H.add_nodes_from(range(n60))
    H.add_weighted_edges_from(arw60)
    D = al.floyd_warshall(n60, arw60)
    R = nx.floyd_warshall_numpy(H, nodelist=range(n60))
    todos.append(ok("Floyd-Warshall", np.allclose(D, np.asarray(R))))

    # Tarjan
    pontes, art = al.tarjan_pontes_articulacoes(adj)
    todos.append(ok(f"Tarjan: pontes ({len(pontes)})",
                    {frozenset(p) for p in pontes} == {frozenset(p) for p in nx.bridges(G)}))
    todos.append(ok(f"Tarjan: articulações ({len(art)})", set(art) == set(nx.articulation_points(G))))

    # MST
    ref_w = nx.minimum_spanning_tree(G).size(weight="weight")
    pk, _ = al.kruskal(n, ar_w)
    pp, _ = al.prim(adjw, 0)
    todos.append(ok("Kruskal", pk == ref_w))
    todos.append(ok("Prim", pp == ref_w))

    # Triângulos e clusterização
    tri, dg = triangulos_nos(sp, si, np.arange(n))
    ref_t = nx.triangles(G)
    todos.append(ok("triângulos por vértice", all(int(tri[v]) == ref_t[v] for v in range(n))))
    todos.append(ok("clusterização média",
                    abs(clustering_local(tri, dg).mean() - nx.average_clustering(G)) < 1e-12))

    print("\nTODOS OS TESTES PASSARAM" if all(todos) else "\nHÁ FALHAS")
    raise SystemExit(0 if all(todos) else 1)


if __name__ == "__main__":
    main()
