"""Cronometragem de cada algoritmo sobre um subgrafo já montado."""
import time

from parte2 import algoritmos as al


def cronometrar(f, *a):
    t0 = time.perf_counter()
    r = f(*a)
    return time.perf_counter() - t0, r


def executar(nome, n, adj, adjw, ar_w, arcos, s):
    if nome == "BFS":
        return cronometrar(al.bfs, adj, s)[0]
    if nome == "DFS":
        return cronometrar(al.dfs, adj, s)[0]
    if nome == "Eulerianidade":
        return cronometrar(al.eulerianidade, adj)[0]
    if nome == "Dijkstra":
        return cronometrar(al.dijkstra, adjw, s)[0]
    if nome == "Bellman-Ford":
        return cronometrar(al.bellman_ford, n, arcos, s)[0]
    if nome == "Floyd-Warshall":
        return cronometrar(al.floyd_warshall, n, ar_w)[0]
    if nome == "Tarjan (pontes/art.)":
        return cronometrar(al.tarjan_pontes_articulacoes, adj)[0]
    if nome == "Kruskal":
        return cronometrar(al.kruskal, n, ar_w)[0]
    if nome == "Prim":
        return cronometrar(al.prim, adjw, s)[0]
    raise ValueError(nome)
