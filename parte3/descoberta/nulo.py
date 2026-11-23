"""Modelo nulo que preserva a sequência de graus e assortatividade de grau."""
import numpy as np

from comum.grafo import arestas, csr_from_edges


def configuracao_apagada(deg, rng):
    """Configuration model: emparelha ao acaso as 'pontas' de aresta (grau[v] cópias de v) e APAGA laços e
    arestas múltiplas, o que reduz levemente alguns graus (sobretudo dos maiores hubs).
    Devolve (indptr, indices, fração de arestas perdidas)."""
    n = len(deg)
    pontas = rng.permutation(np.repeat(np.arange(n, dtype=np.int64), deg))
    a, b = pontas[0::2], pontas[1::2]
    ok = a != b
    chave = np.unique(np.minimum(a[ok], b[ok]) * n + np.maximum(a[ok], b[ok]))
    perda = 1.0 - len(chave) / len(a)
    ip, ind = csr_from_edges(n, chave // n, chave % n)
    return ip, ind, float(perda)


def assortatividade(indptr, indices):
    """Coeficiente de assortatividade de grau de Newman (2002): correlação de Pearson entre os graus
    das duas pontas de cada aresta."""
    u, v = arestas(indptr, indices)
    d = np.diff(indptr).astype(np.float64)
    j, k = d[u], d[v]
    m = len(u)
    a = np.sum(j * k) / m
    b = np.sum(j + k) / (2 * m)
    c = np.sum(j * j + k * k) / (2 * m)
    return float((a - b * b) / (c - b * b))
