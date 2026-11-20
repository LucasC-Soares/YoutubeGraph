"""Métricas A-D do Apêndice C, calculadas após remover vértices.

  A  S = |maior componente| / n          (fração do grafo original que continua conectada)
  B  número de componentes (entre os vértices restantes; inclui isolados)
  C  distâncias: caminho médio e limite inferior do diâmetro na maior componente (BFS amostradas)
  D  fração de nós isolados (grau 0 entre os vértices restantes)
"""
import numpy as np

from comum.caminhos import amostra_caminhos, componentes

CHAVES = ["A_S", "B_componentes", "C_caminho_medio", "C_diametro_lb", "D_isolados"]


def medir(ip, ind, n0, u, v, src_all, alive, rng, k_bfs):
    n = len(ip) - 1
    ok = alive[u] & alive[v]
    lab = componentes(n, u[ok], v[ok])
    vivos = np.flatnonzero(alive)
    rot, cnt = np.unique(lab[vivos], return_counts=True)
    S = cnt.max() / n0
    B = len(cnt)
    ok2 = alive[src_all] & alive[ind]
    degv = np.bincount(src_all[ok2], minlength=n)[vivos]
    D = float((degv == 0).mean())
    grande = vivos[lab[vivos] == rot[cnt.argmax()]]
    fontes = rng.choice(grande, size=min(k_bfs, len(grande)), replace=False)
    medias, ecc = amostra_caminhos(ip, ind, fontes, alive)
    return {"A_S": float(S), "B_componentes": int(B), "C_caminho_medio": float(medias.mean()),
            "C_diametro_lb": int(ecc.max()), "D_isolados": D}
