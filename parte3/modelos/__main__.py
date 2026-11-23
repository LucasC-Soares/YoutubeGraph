"""Parte III.5 (extra) — Aproximação a modelos clássicos, por simulação (implementação própria).

Gera, com o MESMO nº de vértices, grafos Erdős–Rényi G(n, m) (mesmo m do real), Barabási–Albert
(grau médio casado com o real, ver geradores.py) e Watts–Strogatz (k e p dados) e compara com o grafo
real: grau médio, grau máximo, clusterização C, caminho médio L, diâmetro (limite inferior), γ (MLE) e CCDF.
A ordem de sorteios (real, ER, depois BA e WS) repete a de parte3.smallworld com a mesma semente, então
as linhas do real e do ER coincidem com a tabela de small-world.

Uso (na raiz do repositório):  python -m parte3.modelos [--fontes 300] [--amostra-clust 20000] [--ws-k 6] [--ws-p 0.1]
Saídas em parte3/resultados/: parte3_modelos.json, tab_modelos.tex, fig/modelos.pdf
"""
import argparse

import numpy as np

from comum.config import pasta_saida, rng_padrao
from comum.dados import carregar_grafo
from comum.saida import salvar_json
from parte3.modelos.geradores import barabasi_albert, watts_strogatz
from parte3.modelos.grafico import grafico
from parte3.modelos.tabela import tabela
from parte3.potencia.ajuste import melhor_kmin
from parte3.potencia.distribuicao import distribuicao
from parte3.smallworld.grafo_aleatorio import gnm
from parte3.smallworld.medidas import medir


def avaliar(nome, ip, ind, args, rng, ccdfs):
    r = medir(ip, ind, args.fontes, args.amostra_clust, rng)
    graus, ks, _, ccdf = distribuicao(np.diff(ip))
    r["grau_max"] = int(graus.max())
    r["mle"] = melhor_kmin(graus, 200)
    ccdfs[nome] = (ks, ccdf)
    print(f"[modelos] {nome}: C={r['C']:.3g} L={r['L']:.3f} k_max={r['grau_max']}", flush=True)
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fontes", type=int, default=300)
    ap.add_argument("--amostra-clust", type=int, default=20000)
    ap.add_argument("--ws-k", type=int, default=6)
    ap.add_argument("--ws-p", type=float, default=0.1)
    args = ap.parse_args()

    pasta = pasta_saida("parte3")
    rng = rng_padrao(3)  # mesma semente/ordem de parte3.smallworld
    ip, ind, _, _ = carregar_grafo()
    ccdfs, res = {}, {}

    res["com-Youtube"] = avaliar("com-Youtube", ip, ind, args, rng, ccdfs)
    n, m = res["com-Youtube"]["n"], res["com-Youtube"]["m"]
    res["Erdős–Rényi"] = avaliar("Erdős–Rényi", *gnm(n, m, rng), args, rng, ccdfs)
    res["Barabási–Albert"] = avaliar("Barabási–Albert", *barabasi_albert(n, m / n - 2, rng), args, rng, ccdfs)
    res["Watts–Strogatz"] = avaliar("Watts–Strogatz", *watts_strogatz(n, args.ws_k, args.ws_p, rng), args, rng, ccdfs)

    salvar_json(pasta, "parte3_modelos.json", {"parametros": {"ws_k": args.ws_k, "ws_p": args.ws_p}, "modelos": res})
    tabela(res, pasta)
    grafico(ccdfs, pasta)


if __name__ == "__main__":
    main()
