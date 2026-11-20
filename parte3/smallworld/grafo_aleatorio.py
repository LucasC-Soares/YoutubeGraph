"""Grafo aleatório de referência G(n, m) (Erdős–Rényi)."""
import numpy as np

from comum.grafo import csr_from_edges


def gnm(n, m, rng):
    """G(n, m) aproximado: sorteia pares, remove laços/duplicatas e fica com m arestas."""
    extra = int(m * 1.1) + 1000
    u = rng.integers(0, n, extra)
    v = rng.integers(0, n, extra)
    ok = u != v
    a, b = np.minimum(u[ok], v[ok]), np.maximum(u[ok], v[ok])
    chave = np.unique(a.astype(np.int64) * n + b)
    chave = rng.permutation(chave)[:m]
    return csr_from_edges(n, chave // n, chave % n)
