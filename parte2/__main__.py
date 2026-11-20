"""Parte II — Algoritmos da disciplina: complexidade teórica x tempo real.

Uso (na raiz do repositório):
  python -m parte2 [--rep 30] [--tamanhos 1000 2000 4000 8000 16000 32000]
                   [--completo] [--rep-completo 5]
Validação das implementações contra o NetworkX:  python -m parte2.validacao

Metodologia (documentar no relatório):
 * Cada algoritmo é executado em R repetições, cada uma sobre um subgrafo induzido
   diferente ("bola" BFS ao redor de uma fonte aleatória) de tamanho V alvo, e com
   fonte aleatória quando o algoritmo exige uma.
 * Para cada (algoritmo, V): média, desvio padrão e IC95%.
     R >= 30 -> distribuição Normal (z = 1,96); R < 30 -> t-Student (gl = R-1).
 * O grafo é não ponderado; Dijkstra, Bellman-Ford, Floyd-Warshall, Kruskal e Prim
   só têm sentido com pesos, então usamos pesos inteiros aleatórios em [1,10]
   (semente fixa). Com peso 1 em todas as arestas, Dijkstra = BFS.
 * Complexidade observada: ajuste log-log tempo ~ c * f(V,E)^b, onde f é a função
   teórica; b próximo de 1 indica aderência ao modelo teórico.

Saídas em parte2/resultados/: parte2.json, tab_tempos.tex, tab_complexidade.tex, fig/tempos.pdf
"""
import argparse

import numpy as np

from comum.config import pasta_saida, rng_padrao
from comum.dados import carregar_grafo
from comum.saida import salvar_json
from parte2.complexidade import LIMITE, TEORICA
from parte2.grafico import grafico
from parte2.grafo_completo import rodar_completo
from parte2.medicao import executar
from parte2.resumo import resumir
from parte2.subgrafos import bola, montar
from parte2.tabelas import tabela_complexidade, tabela_tempos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rep", type=int, default=30)
    ap.add_argument("--tamanhos", type=int, nargs="+", default=[1000, 2000, 4000, 8000, 16000, 32000])
    ap.add_argument("--completo", action="store_true",
                    help="também roda os algoritmos lineares no grafo inteiro")
    ap.add_argument("--rep-completo", type=int, default=5)
    args = ap.parse_args()

    pasta = pasta_saida("parte2")
    rng = rng_padrao(2)
    ip, ind, _, _ = carregar_grafo()
    deg = np.diff(ip)
    tempos = {}  # (algoritmo, V alvo) -> {"t": [...], "V": [...], "E": [...]}

    for V in args.tamanhos:
        algs = [a for a in TEORICA if V <= LIMITE.get(a, 10 ** 9)]
        for a in algs:
            tempos[(a, V)] = {"t": [], "V": [], "E": []}
        print(f"[V={V}] {args.rep} repetições: {', '.join(algs)}", flush=True)
        for r in range(args.rep):
            nos = bola(ip, ind, deg, V, rng)
            n, E, adj, adjw, ar_w, arcos = montar(ip, ind, nos, rng)
            s = int(rng.integers(n))
            for a in algs:
                tempos[(a, V)]["t"].append(executar(a, n, adj, adjw, ar_w, arcos, s))
                tempos[(a, V)]["V"].append(n)
                tempos[(a, V)]["E"].append(E)

    # Floyd-Warshall em subgrafos pequenos (O(V^3))
    for V in [50, 100, 200, 400]:
        tempos[("Floyd-Warshall", V)] = {"t": [], "V": [], "E": []}
        for r in range(args.rep):
            nos = bola(ip, ind, deg, V, rng)
            n, E, adj, adjw, ar_w, arcos = montar(ip, ind, nos, rng)
            tempos[("Floyd-Warshall", V)]["t"].append(executar("Floyd-Warshall", n, adj, adjw, ar_w, arcos, 0))
            tempos[("Floyd-Warshall", V)]["V"].append(n)
            tempos[("Floyd-Warshall", V)]["E"].append(E)
        print(f"[Floyd-Warshall V={V}] ok", flush=True)

    resultados = resumir(tempos)

    if args.completo:
        resultados["grafo_completo"] = rodar_completo(ip, ind, args.rep_completo, rng)

    salvar_json(pasta, "parte2.json", resultados)
    tabela_tempos(resultados, pasta)
    tabela_complexidade(resultados, pasta)
    grafico(resultados, pasta)


if __name__ == "__main__":
    main()
