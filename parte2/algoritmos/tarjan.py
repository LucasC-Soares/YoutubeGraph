"""Algoritmo de Tarjan: pontes e pontos de articulação (grafo não direcionado)."""


def tarjan_pontes_articulacoes(adj):
    """Low-link de Tarjan, iterativo. Retorna (pontes, articulações). O(V+E).
    Obs.: em grafo NÃO direcionado as componentes fortemente conexas coincidem com as
    componentes conexas; por isso o uso relevante de Tarjan aqui é pontes/articulações."""
    n = len(adj)
    disc = [-1] * n
    low = [0] * n
    pai = [-1] * n
    pontes = []
    art = [False] * n
    t = 0
    for r in range(n):
        if disc[r] != -1:
            continue
        filhos_raiz = 0
        disc[r] = low[r] = t
        t += 1
        pilha = [(r, 0)]
        while pilha:
            u, i = pilha[-1]
            if i < len(adj[u]):
                pilha[-1] = (u, i + 1)
                v = adj[u][i]
                if disc[v] == -1:
                    pai[v] = u
                    disc[v] = low[v] = t
                    t += 1
                    if u == r:
                        filhos_raiz += 1
                    pilha.append((v, 0))
                elif v != pai[u] and disc[v] < low[u]:
                    low[u] = disc[v]
            else:
                pilha.pop()
                p = pai[u]
                if p != -1:
                    if low[u] < low[p]:
                        low[p] = low[u]
                    if low[u] > disc[p]:
                        pontes.append((p, u))
                    if p != r and low[u] >= disc[p]:
                        art[p] = True
        if filhos_raiz > 1:
            art[r] = True
    return pontes, [v for v in range(n) if art[v]]
