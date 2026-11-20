"""Busca em largura e em profundidade."""
from collections import deque


def bfs(adj, s):
    """BFS com fila. Retorna lista de distâncias (-1 = inalcançável). O(V+E)."""
    dist = [-1] * len(adj)
    dist[s] = 0
    fila = deque([s])
    while fila:
        u = fila.popleft()
        du = dist[u] + 1
        for v in adj[u]:
            if dist[v] < 0:
                dist[v] = du
                fila.append(v)
    return dist


def dfs(adj, s):
    """DFS iterativa. Retorna (ordem de descoberta, pai). O(V+E)."""
    pai = [-1] * len(adj)
    vis = [False] * len(adj)
    ordem = []
    pilha = [(s, 0)]
    vis[s] = True
    ordem.append(s)
    while pilha:
        u, i = pilha[-1]
        if i < len(adj[u]):
            pilha[-1] = (u, i + 1)
            v = adj[u][i]
            if not vis[v]:
                vis[v] = True
                pai[v] = u
                ordem.append(v)
                pilha.append((v, 0))
        else:
            pilha.pop()
    return ordem, pai
