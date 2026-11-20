"""Itens 6-7 da Parte I: número e tamanho das componentes conexas."""
import time

import numpy as np

from comum.caminhos import maior_componente


def medir(ip, ind, status):
    """Devolve (vértices da maior componente, tamanhos das componentes em ordem decrescente)."""
    n = len(ip) - 1
    t0 = time.perf_counter()
    lcc, lab = maior_componente(ip, ind)
    rot, tam = np.unique(lab, return_counts=True)
    ordem = np.argsort(-tam)
    tam_ord = tam[ordem]
    status["Número de componentes conexas"] = (int(len(rot)), "exato")
    status["Tamanho de cada componente"] = (
        f"maior = {int(tam_ord[0])} ({tam_ord[0] / n:.4%} dos vértices)", "exato (tab. componentes)")
    print(f"[componentes] {len(rot)} componente(s) em {time.perf_counter() - t0:.1f}s")
    return lcc, tam_ord
