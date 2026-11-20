"""Medidas L (caminho médio) e C (clusterização média) na maior componente."""
import numpy as np

from comum.caminhos import amostra_caminhos, maior_componente
from comum.estatistica import ic95
from comum.grafo import subgrafo
from comum.triangulos import clustering_local, triangulos_nos


def medir(ip, ind, fontes, n_clust, rng):
    """Dict com n, m, L, L_ic95, C, C_ic95, diam_lb e k_medio da maior componente de (ip, ind)."""
    lcc, _ = maior_componente(ip, ind)
    ip2, ind2 = subgrafo(ip, ind, lcc)
    n2 = len(ip2) - 1
    src = rng.choice(n2, size=min(fontes, n2), replace=False)
    medias, ecc = amostra_caminhos(ip2, ind2, src)
    L, _, hL, _ = ic95(medias)
    alvo = np.arange(n2) if n_clust <= 0 or n_clust >= n2 else rng.choice(n2, n_clust, replace=False)
    tri, dg = triangulos_nos(ip2, ind2, alvo)
    C, _, hC, _ = ic95(clustering_local(tri, dg))
    return {"n": n2, "m": ind2.size // 2, "L": L, "L_ic95": hL, "C": C, "C_ic95": hC,
            "diam_lb": int(ecc.max()), "k_medio": 2.0 * (ind2.size // 2) / n2}
