"""PageRank por iteração de potência (implementação própria)."""
import numpy as np


def pagerank(n, src, dst, iters=60, d=0.85):
    """PageRank (grafo não direcionado -> cada aresta nos dois sentidos)."""
    deg = np.bincount(src, minlength=n).astype(float)
    x = np.full(n, 1.0 / n)
    for _ in range(iters):
        novo = np.bincount(dst, weights=x[src] / deg[src], minlength=n)
        novo = (1 - d) / n + d * novo
        if np.abs(novo - x).sum() < 1e-10:
            x = novo
            break
        x = novo
    return x
