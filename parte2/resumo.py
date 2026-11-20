"""Estatística dos tempos (média, desvio, IC95%) e ajuste do expoente observado."""
import numpy as np

from comum.estatistica import ic95
from parte2.complexidade import TEORICA


def resumir(tempos):
    """tempos: (algoritmo, V alvo) -> {"t": [...], "V": [...], "E": [...]}."""
    out = {"linhas": [], "ajuste": {}}
    por_alg = {}
    for (a, Valvo), d in sorted(tempos.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        media, desv, ic, dist = ic95(d["t"])
        V, E = float(np.mean(d["V"])), float(np.mean(d["E"]))
        f = TEORICA[a][1](V, E)
        linha = {"algoritmo": a, "V": V, "E": E, "R": len(d["t"]), "media_s": media, "desvio_s": desv,
                 "ic95_s": ic, "dist": dist, "f_teorica": float(f), "razao": media / float(f)}
        out["linhas"].append(linha)
        por_alg.setdefault(a, []).append(linha)
    for a, ls in por_alg.items():
        if len(ls) >= 2:
            x = np.log([l["f_teorica"] for l in ls])
            y = np.log([l["media_s"] for l in ls])
            b, c = np.polyfit(x, y, 1)
            r2 = float(np.corrcoef(x, y)[0, 1] ** 2)
            out["ajuste"][a] = {"expoente": float(b), "r2": r2}
    return out
