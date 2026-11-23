"""Decomposição em k-cores (implementação própria, Batagelj & Zaversnik, 2003), O(n + m).
coreness[v] = maior k tal que v pertence ao subgrafo em que todo vértice tem grau >= k."""
import numpy as np


def coreness(indptr, indices):
    n = len(indptr) - 1
    deg = np.diff(indptr).tolist()
    md = max(deg)
    cont = [0] * (md + 1)
    for d in deg:
        cont[d] += 1
    bin_ = [0] * (md + 1)  # início de cada faixa de grau em `vert`
    s = 0
    for d in range(md + 1):
        bin_[d], s = s, s + cont[d]
    pos, vert = [0] * n, [0] * n
    for v in range(n):
        pos[v] = bin_[deg[v]]
        vert[pos[v]] = v
        bin_[deg[v]] += 1
    for d in range(md, 0, -1):
        bin_[d] = bin_[d - 1]
    bin_[0] = 0
    for i in range(n):
        v = vert[i]
        dv = deg[v]
        for u in indices[indptr[v]:indptr[v + 1]].tolist():
            du = deg[u]
            if du > dv:
                pu, pw = pos[u], bin_[du]
                w = vert[pw]
                if u != w:
                    pos[u], pos[w] = pw, pu
                    vert[pu], vert[pw] = w, u
                bin_[du] += 1
                deg[u] = du - 1
    return np.array(deg, dtype=np.int64)
