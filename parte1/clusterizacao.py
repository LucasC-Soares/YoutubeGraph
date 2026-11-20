"""Itens 11-12 da Parte I: coeficiente de clusterização médio e número de triângulos.

Usa a implementação própria (amostrável) e, se o igraph estiver instalado, valores exatos.
"""
import time

import numpy as np

from comum.estatistica import ic95
from comum.grafo import arestas
from comum.triangulos import clustering_local, triangulos_nos


def medir(ip, ind, amostra, rng, usar_igraph, status):
    n = len(ip) - 1
    deg = np.diff(ip)
    alvo = np.arange(n) if amostra in (0, n) or amostra >= n \
        else rng.choice(n, size=amostra, replace=False)
    t0 = time.perf_counter()
    tri, dg = triangulos_nos(ip, ind, alvo)
    c_loc = clustering_local(tri, dg)
    c_med, _, c_ic, _ = ic95(c_loc)
    exato = len(alvo) == n
    status["Coeficiente de clusterização médio"] = (
        c_med, "exato" if exato else f"estimado ({len(alvo)} vértices, IC95% ±{c_ic:.4f})")
    tri_est = float(tri.mean() * n / 3.0)
    print(f"[clustering] {time.perf_counter() - t0:.1f}s")

    tri_exato = None
    if usar_igraph:
        try:
            import igraph as ig
            u, v = arestas(ip, ind)
            g = ig.Graph(n=n, edges=np.stack([u, v], 1).tolist())
            cl = np.array(g.transitivity_local_undirected(mode="zero"))
            tri_exato = float((cl * deg * (deg - 1) / 2.0).sum() / 3.0)
            status["Coeficiente de clusterização médio"] = (float(cl.mean()), "exato (igraph)")
        except Exception as e:  # igraph ausente ou falhou
            print(f"[triângulos] igraph indisponível ({e}); usando estimativa por amostragem")
    if tri_exato is not None:
        status["Número de triângulos"] = (int(round(tri_exato)), "exato (igraph)")
    else:
        status["Número de triângulos"] = (int(round(tri_est)), f"estimado por amostragem ({len(alvo)} vértices)")
