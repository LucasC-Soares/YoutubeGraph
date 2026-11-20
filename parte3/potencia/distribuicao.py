"""Distribuição de graus P(k) e CCDF P(K >= k)."""
import numpy as np


def distribuicao(deg):
    """Devolve (graus >= 1, valores distintos de grau, P(k), CCDF)."""
    graus = deg[deg >= 1]
    cont = np.bincount(graus)
    ks = np.flatnonzero(cont)
    pk = cont[ks] / len(graus)
    ccdf = 1.0 - (np.cumsum(cont)[ks] - cont[ks]) / len(graus)  # P(K >= k)
    return graus, ks, pk, ccdf
