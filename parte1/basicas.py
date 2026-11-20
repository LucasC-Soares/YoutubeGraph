"""Itens 1-5 da Parte I: vértices, arestas, graus, distribuição de graus e densidade."""
import numpy as np


def medir(ip, ind, status, pasta):
    """Preenche `status` e grava distribuicao_graus.csv.
    Devolve (valores de grau presentes, contagem por grau)."""
    n = len(ip) - 1
    m = ind.size // 2
    deg = np.diff(ip)
    status["Número de vértices"] = (n, "exato")
    status["Número de arestas"] = (m, "exato")
    status["Grau mínimo"] = (int(deg.min()), "exato")
    status["Grau máximo"] = (int(deg.max()), "exato")
    status["Grau médio"] = (float(deg.mean()), "exato")
    cont = np.bincount(deg)
    ks = np.flatnonzero(cont)
    np.savetxt(pasta / "distribuicao_graus.csv",
               np.stack([ks, cont[ks], cont[ks] / n], 1),
               delimiter=",", header="grau,contagem,P(k)", comments="", fmt=["%d", "%d", "%.10g"])
    status["Mediana do grau"] = (float(np.median(deg)), "exato")
    status["Distribuição de graus"] = (f"{len(ks)} valores distintos de grau", "exato (CSV + figura)")
    status["Densidade"] = (2.0 * m / (n * (n - 1)), "exato")
    return ks, cont
