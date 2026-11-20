"""Parte III.3 / Apêndice C — Robustez à remoção de 5% dos vértices.

Política para grafo desconexo (documentar): trabalhamos na MAIOR COMPONENTE CONEXA.
 n = |V|, r = ceil(0.05 n). Métricas A-D em parte3/robustez/metricas.py.
Cenários:
  * aleatório: T repetições (média ± desvio, boxplot);
  * direcionado ("ataque"): ranking FIXO por centralidade de grau e por PageRank.
    Betweenness exata é inviável neste porte; o apêndice recomenda betweenness OU grau.

Uso (na raiz do repositório):  python -m parte3.robustez [--reps 30] [--bfs 20]
Saídas em parte3/resultados/: parte3_robustez.json, tab_robustez.tex, fig/robustez.pdf
"""
import argparse

import numpy as np

from comum.caminhos import maior_componente
from comum.config import pasta_saida, rng_padrao
from comum.dados import carregar_grafo
from comum.grafo import arestas, subgrafo
from comum.saida import salvar_json
from parte3.robustez.grafico import grafico
from parte3.robustez.metricas import CHAVES, medir
from parte3.robustez.pagerank import pagerank
from parte3.robustez.tabela import tabela


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=30)
    ap.add_argument("--bfs", type=int, default=20, help="BFS amostradas por medição de distância")
    args = ap.parse_args()

    pasta = pasta_saida("parte3")
    rng = rng_padrao(4)
    ip0, ind0, _, _ = carregar_grafo()
    lcc, _ = maior_componente(ip0, ind0)
    ip, ind = subgrafo(ip0, ind0, lcc)
    n = len(ip) - 1
    r = int(np.ceil(0.05 * n))
    u, v = arestas(ip, ind)
    src_all = np.repeat(np.arange(n, dtype=np.int64), np.diff(ip))
    print(f"[robustez] n={n}, r={r} vértices removidos por cenário", flush=True)

    base = medir(ip, ind, n, u, v, src_all, np.ones(n, bool), rng, args.bfs)
    print("[robustez] base:", base, flush=True)

    # --- aleatório -----------------------------------------------------------
    aleat = []
    for t in range(args.reps):
        alive = np.ones(n, bool)
        alive[rng.choice(n, size=r, replace=False)] = False
        aleat.append(medir(ip, ind, n, u, v, src_all, alive, rng, args.bfs))
        print(f"[robustez] aleatório {t + 1}/{args.reps}", flush=True)

    # --- direcionado (ranking fixo) ------------------------------------------
    cenarios = {}
    grau = np.diff(ip)
    ordem_grau = np.argsort(-grau, kind="stable")
    pr = pagerank(n, src_all, ind.astype(np.int64))
    ordem_pr = np.argsort(-pr, kind="stable")
    for nome, ordem in [("grau", ordem_grau), ("PageRank", ordem_pr)]:
        alive = np.ones(n, bool)
        alive[ordem[:r]] = False
        cenarios[nome] = medir(ip, ind, n, u, v, src_all, alive, rng, args.bfs)
        print(f"[robustez] ataque por {nome}:", cenarios[nome], flush=True)

    resumo = {c: {"media": float(np.mean([a[c] for a in aleat])), "desvio": float(np.std([a[c] for a in aleat], ddof=1))
                  if len(aleat) > 1 else 0.0} for c in CHAVES}
    salvar_json(pasta, "parte3_robustez.json", {"n": n, "r": r, "base": base, "aleatorio_resumo": resumo,
                                                "aleatorio_reps": aleat, "direcionado": cenarios})
    grafico(base, aleat, cenarios, pasta)
    tabela(base, resumo, cenarios, args.reps, pasta)


if __name__ == "__main__":
    main()
