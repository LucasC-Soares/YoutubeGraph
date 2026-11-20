"""Verificação de eulerianidade."""
from .busca import bfs


def eulerianidade(adj):
    """Classifica o grafo: 'circuito euleriano', 'caminho euleriano' ou 'nao euleriano'.
    Critério: arestas em uma só componente + nº de vértices de grau ímpar (0 ou 2). O(V+E)."""
    n = len(adj)
    impares = sum(1 for a in adj if len(a) % 2 == 1)
    com_aresta = [i for i in range(n) if adj[i]]
    if not com_aresta:
        return "circuito euleriano", 0
    d = bfs(adj, com_aresta[0])
    conexo = all(d[i] >= 0 for i in com_aresta)
    if not conexo:
        return "nao euleriano", impares
    if impares == 0:
        return "circuito euleriano", 0
    if impares == 2:
        return "caminho euleriano", 2
    return "nao euleriano", impares
