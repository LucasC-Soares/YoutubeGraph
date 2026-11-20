"""Parte III.1 / Apêndice A — Propriedade small-world (implementação própria, sem bibliotecas prontas).

Critério (definição formal do apêndice), medido na maior componente conexa:
    L(G) ≈ L_aleatório        e        C(G) >> C_aleatório
O grafo aleatório de referência é um G(n, m) (Erdős–Rényi) com o MESMO nº de vértices
e de arestas (logo, o mesmo grau médio), gerado e medido pelos mesmos códigos.
Também reportamos os valores teóricos  L_rand ≈ ln n / ln<k>  e  C_rand ≈ <k>/n
e o índice sigma = (C/C_rand) / (L/L_rand)  (Humphries & Gurney, 2008; sigma > 1 sugere small-world).

Uso (na raiz do repositório):  python -m parte3.smallworld [--fontes 300] [--amostra-clust 20000]
Saídas em parte3/resultados/: parte3_smallworld.json, tab_smallworld.tex
"""
import argparse
import json

import numpy as np

from comum.config import pasta_saida, rng_padrao
from comum.dados import carregar_grafo
from comum.saida import salvar_json
from parte3.smallworld.grafo_aleatorio import gnm
from parte3.smallworld.medidas import medir
from parte3.smallworld.tabela import tabela


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fontes", type=int, default=300)
    ap.add_argument("--amostra-clust", type=int, default=20000)
    args = ap.parse_args()

    pasta = pasta_saida("parte3")
    rng = rng_padrao(3)
    ip, ind, _, _ = carregar_grafo()

    print("[small-world] medindo o grafo real ...", flush=True)
    real = medir(ip, ind, args.fontes, args.amostra_clust, rng)

    print("[small-world] gerando e medindo G(n,m) equivalente ...", flush=True)
    rip, rind = gnm(real["n"], real["m"], rng)
    rnd = medir(rip, rind, args.fontes, args.amostra_clust, rng)

    k = real["k_medio"]
    teo = {"L_rand_teorico": float(np.log(real["n"]) / np.log(k)), "C_rand_teorico": float(k / real["n"])}
    razao_L = real["L"] / rnd["L"]
    razao_C = real["C"] / rnd["C"]
    sigma = razao_C / razao_L
    saida = {"real": real, "aleatorio": rnd, "teorico": teo, "razao_L": razao_L, "razao_C": razao_C,
             "sigma": sigma}
    salvar_json(pasta, "parte3_smallworld.json", saida)
    tabela(saida, pasta)
    print(json.dumps(saida, indent=2, default=float))


if __name__ == "__main__":
    main()
