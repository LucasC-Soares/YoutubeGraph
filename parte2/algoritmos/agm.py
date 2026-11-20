"""Árvore geradora mínima: Kruskal (com união-busca) e Prim."""
import heapq


class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.r = [0] * n

    def find(self, x):
        p = self.p
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.r[a] < self.r[b]:
            a, b = b, a
        self.p[b] = a
        if self.r[a] == self.r[b]:
            self.r[a] += 1
        return True


def kruskal(n, arestas_w):
    """O(E log E). Retorna (peso total, nº de arestas da floresta geradora)."""
    dsu = DSU(n)
    total, usadas = 0, 0
    for u, v, w in sorted(arestas_w, key=lambda e: e[2]):
        if dsu.union(u, v):
            total += w
            usadas += 1
            if usadas == n - 1:
                break
    return total, usadas


def prim(adjw, s=0):
    """Heap binário. O(E log V). Gera a árvore da componente de s. Retorna (peso, nº arestas)."""
    n = len(adjw)
    em = [False] * n
    h = [(0, s)]
    total, usadas = 0, -1
    while h:
        w, u = heapq.heappop(h)
        if em[u]:
            continue
        em[u] = True
        total += w
        usadas += 1
        for v, wv in adjw[u]:
            if not em[v]:
                heapq.heappush(h, (wv, v))
    return total, usadas
