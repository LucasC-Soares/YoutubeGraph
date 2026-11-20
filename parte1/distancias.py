"""Itens 8-10 da Parte I: diâmetro, raio e comprimento médio dos caminhos (BFS amostradas)."""
import numpy as np

from comum.caminhos import amostra_caminhos, bfs_dist
from comum.estatistica import ic95
from comum.grafo import subgrafo


def medir(ip, ind, lcc, fontes, rng, status):
    """Trabalha na maior componente. Devolve (diâmetro_lb, raio_ub, dict do caminho médio)."""
    ip2, ind2 = subgrafo(ip, ind, lcc)
    n2 = len(ip2) - 1
    deg2 = np.diff(ip2)
    k = min(fontes, n2)
    aleat = rng.choice(n2, size=k, replace=False)
    hubs = np.argsort(-deg2)[:50]
    print(f"[caminhos] {k} BFS aleatórias + {len(hubs)} em hubs ...")
    medias, ecc = amostra_caminhos(ip2, ind2, aleat)
    _, ecc_hub = amostra_caminhos(ip2, ind2, hubs)
    # double sweep: BFS a partir do vértice mais distante de cada fonte
    ecc_ds = []
    for s in aleat[: min(k, 50)]:
        d = bfs_dist(ip2, ind2, int(s))
        far = int(np.argmax(d))
        ecc_ds.append(int(bfs_dist(ip2, ind2, far).max()))
    diam_lb = int(max(ecc.max(), ecc_hub.max(), max(ecc_ds)))
    raio_ub = int(min(ecc.min(), ecc_hub.min()))
    mL, sL, hL, _ = ic95(medias)
    status["Diâmetro"] = (diam_lb, f"estimado (limite inferior; {k + len(hubs) + len(ecc_ds)} BFS) na maior componente")
    status["Raio"] = (raio_ub, f"estimado (limite superior; {k + len(hubs)} BFS) na maior componente")
    status["Comprimento médio dos caminhos"] = (
        mL, f"estimado ({k} fontes, IC95% ±{hL:.4f}) na maior componente")
    return diam_lb, raio_ub, {"media": mL, "desvio": sL, "ic95": hL}
