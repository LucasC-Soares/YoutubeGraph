"""Caminhos mínimos: Dijkstra, Bellman-Ford e Floyd-Warshall."""
import heapq

import numpy as np

INF = float("inf")


def dijkstra(adjw, s):
    """Heap binário (lazy deletion). Pesos >= 0. O((V+E) log V)."""
    dist = [INF] * len(adjw)
    dist[s] = 0
    h = [(0, s)]
    while h:
        d, u = heapq.heappop(h)
        if d > dist[u]:
            continue
        for v, w in adjw[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(h, (nd, v))
    return dist


def bellman_ford(n, arcos, s):
    """arcos = lista de (u, v, w) DIRECIONADOS (grafo não direcionado: incluir os dois sentidos).
    Para quando uma passada não relaxa nada (pior caso O(V·E)). Retorna (dist, ciclo_negativo)."""
    dist = [INF] * n
    dist[s] = 0
    for _ in range(n - 1):
        mudou = False
        for u, v, w in arcos:
            du = dist[u]
            if du != INF and du + w < dist[v]:
                dist[v] = du + w
                mudou = True
        if not mudou:
            return dist, False
    for u, v, w in arcos:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return dist, True
    return dist, False


def floyd_warshall(n, arestas_w):
    """arestas_w = (u, v, w) não direcionadas. O(V^3), linha-a-linha vetorizado."""
    D = np.full((n, n), np.inf)
    np.fill_diagonal(D, 0.0)
    for u, v, w in arestas_w:
        if w < D[u, v]:
            D[u, v] = D[v, u] = w
    for k in range(n):
        np.minimum(D, D[:, k:k + 1] + D[k:k + 1, :], out=D)
    return D
