"""Triângulos e clusterização local (implementação própria, amostrável)."""
import numpy as np


def triangulos_nos(indptr, indices, nos):
    """Número de triângulos e grau de cada vértice em `nos`.
    Para cada vizinho u de v, conta |N(u) ∩ N(v)| com busca binária
    (listas de adjacência já ordenadas). Cada triângulo de v é contado 2x."""
    tri = np.zeros(len(nos), dtype=np.float64)
    deg = np.zeros(len(nos), dtype=np.int64)
    for i, v in enumerate(nos):
        a, b = indptr[v], indptr[v + 1]
        d = b - a
        deg[i] = d
        if d < 2:
            continue
        nv = indices[a:b]
        c = 0
        for u in nv:
            nu = indices[indptr[u]:indptr[u + 1]]
            pos = np.minimum(np.searchsorted(nv, nu), d - 1)
            c += int(np.count_nonzero(nv[pos] == nu))
        tri[i] = c / 2.0
    return tri, deg


def clustering_local(tri, deg):
    par = deg * (deg - 1) / 2.0
    out = np.zeros(len(tri))
    ok = par > 0
    out[ok] = tri[ok] / par[ok]  # grau < 2 -> 0 (convenção "zero")
    return out
