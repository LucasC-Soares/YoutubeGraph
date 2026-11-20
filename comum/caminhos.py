"""BFS vetorizada por níveis, componentes conexas e amostragem de distâncias.

Não é o BFS "didático" da Parte II (esse, com fila, está em parte2/algoritmos/busca.py);
aqui o objetivo é escala.
"""
from __future__ import annotations

import numpy as np

from comum.grafo import arestas


def bfs_dist(indptr, indices, src: int, alive: np.ndarray | None = None) -> np.ndarray:
    """Distâncias (em arestas) a partir de src; -1 = inalcançável.
    `alive` (bool) restringe o grafo aos vértices vivos."""
    n = len(indptr) - 1
    if alive is None:
        dist = np.full(n, -1, dtype=np.int32)
    else:
        dist = np.where(alive, -1, -2).astype(np.int32)  # -2: removido
    dist[src] = 0
    fronteira = np.array([src], dtype=np.int64)
    d = 0
    while fronteira.size:
        ini = indptr[fronteira]
        cnt = indptr[fronteira + 1] - ini
        total = int(cnt.sum())
        if total == 0:
            break
        offs = np.repeat(ini - (np.cumsum(cnt) - cnt), cnt) + np.arange(total)
        viz = indices[offs]
        viz = viz[dist[viz] == -1]
        viz = np.unique(viz)
        d += 1
        dist[viz] = d
        fronteira = viz.astype(np.int64)
    dist[dist == -2] = -1
    return dist


def componentes(n: int, u: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Rótulo de componente conexa (menor id do componente) por vértice.
    Hooking + pointer jumping vetorizado; recebe cada aresta uma vez."""
    lab = np.arange(n, dtype=np.int64)
    while True:
        lu, lv = lab[u], lab[v]
        dif = lu != lv
        if not dif.any():
            return lab
        hi = np.maximum(lu[dif], lv[dif])
        lo = np.minimum(lu[dif], lv[dif])
        np.minimum.at(lab, hi, lo)
        while True:
            nl = lab[lab]
            if np.array_equal(nl, lab):
                break
            lab = nl


def maior_componente(indptr, indices):
    """Vértices da maior componente conexa e vetor de rótulos."""
    n = len(indptr) - 1
    u, v = arestas(indptr, indices)
    lab = componentes(n, u, v)
    rot, cnt = np.unique(lab, return_counts=True)
    grande = rot[cnt.argmax()]
    return np.flatnonzero(lab == grande), lab


def amostra_caminhos(indptr, indices, fontes, alive=None):
    """Para cada fonte: (média das distâncias aos alcançáveis, excentricidade)."""
    medias, ecc = [], []
    for s in fontes:
        d = bfs_dist(indptr, indices, int(s), alive)
        pos = d > 0
        if pos.any():
            medias.append(d[pos].mean())
            ecc.append(int(d.max()))
        else:
            medias.append(0.0)
            ecc.append(0)
    return np.array(medias), np.array(ecc)
