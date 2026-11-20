"""Amostragem de subgrafos ("bolas" BFS) e montagem das estruturas usadas pelos algoritmos."""
import numpy as np

from comum.caminhos import bfs_dist
from comum.grafo import arestas, subgrafo


def bola(ip, ind, deg, n_alvo, rng):
    """n_alvo vértices mais próximos (em saltos) de uma fonte aleatória -> subgrafo conexo."""
    while True:
        s = int(rng.integers(len(ip) - 1))
        d = bfs_dist(ip, ind, s)
        cand = np.flatnonzero(d >= 0)
        if len(cand) >= n_alvo:
            break
    ordem = np.lexsort((rng.random(len(cand)), d[cand]))
    return cand[ordem[:n_alvo]]


def montar(ip, ind, nos, rng):
    """Subgrafo induzido por `nos` com pesos inteiros aleatórios em [1,10].
    Devolve (n, E, adj, adjw, ar_w, arcos)."""
    sp, si = subgrafo(ip, ind, nos)
    n = len(sp) - 1
    u, v = arestas(sp, si)
    w = rng.integers(1, 11, size=len(u))
    adj = [si[sp[i]:sp[i + 1]].tolist() for i in range(n)]
    adjw = [[] for _ in range(n)]
    for a, b, c in zip(u.tolist(), v.tolist(), w.tolist()):
        adjw[a].append((b, c))
        adjw[b].append((a, c))
    ar_w = list(zip(u.tolist(), v.tolist(), w.tolist()))
    arcos = ar_w + [(b, a, c) for a, b, c in ar_w]
    return n, len(u), adj, adjw, ar_w, arcos
