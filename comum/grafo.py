"""Representação do grafo: CSR simétrico (indptr int64, indices int32 ordenados por linha)."""
import numpy as np


def csr_from_edges(n: int, u: np.ndarray, v: np.ndarray):
    """Cada aresta não direcionada informada UMA vez (u,v) -> CSR simétrico."""
    src = np.concatenate([u, v]).astype(np.int64)
    dst = np.concatenate([v, u]).astype(np.int64)
    ordem = np.lexsort((dst, src))  # ordena por src e depois por dst
    src, dst = src[ordem], dst[ordem]
    indptr = np.zeros(n + 1, dtype=np.int64)
    np.cumsum(np.bincount(src, minlength=n), out=indptr[1:])
    return indptr, dst.astype(np.int32)


def arestas(indptr: np.ndarray, indices: np.ndarray):
    """Retorna (u, v) com u < v, cada aresta uma única vez."""
    n = len(indptr) - 1
    src = np.repeat(np.arange(n, dtype=np.int64), np.diff(indptr))
    m = src < indices
    return src[m], indices[m].astype(np.int64)


def subgrafo(indptr, indices, nodes):
    """Subgrafo induzido pelos vértices `nodes` (reindexados 0..k-1)."""
    n = len(indptr) - 1
    nodes = np.asarray(nodes, dtype=np.int64)
    novo = np.full(n, -1, dtype=np.int64)
    novo[nodes] = np.arange(len(nodes))
    u, v = arestas(indptr, indices)
    a, b = novo[u], novo[v]
    keep = (a >= 0) & (b >= 0)
    return csr_from_edges(len(nodes), a[keep], b[keep])
