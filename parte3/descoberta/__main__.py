"""Parte III.4 — Descoberta com análise própria: k-cores, assortatividade e modelo nulo com os mesmos graus.

Perguntas: (1) a clusterização alta é explicada só pela distribuição de graus? Compara-se o grafo real com um
configuration model (laços e arestas múltiplas apagados) de MESMA sequência de graus; (2) como os hubs se
posicionam na estrutura de núcleos (k-core)? Os hubs estão no núcleo mais interno?

Uso (na raiz do repositório):  python -m parte3.descoberta [--fontes 300] [--amostra-clust 20000]
Validação (NetworkX):          python -m parte3.descoberta.validacao
Saídas em parte3/resultados/: parte3_descoberta.json, tab_nulo.tex, tab_nucleo.tex, fig/nucleo.pdf
"""
import argparse

import numpy as np

from comum.config import pasta_saida, rng_padrao
from comum.dados import carregar_grafo
from comum.saida import salvar_json
from parte3.descoberta.grafico import grafico
from parte3.descoberta.kcore import coreness
from parte3.descoberta.nulo import assortatividade, configuracao_apagada
from parte3.descoberta.tabela import tabela_nucleo, tabela_nulo
from parte3.smallworld.medidas import medir


def perfil_nucleo(core, deg):
    kmax = int(core.max())
    nucleo = core == kmax
    top = np.argsort(-deg, kind="stable")[:100]
    return {"kmax": kmax, "n_nucleo": int(nucleo.sum()), "frac_nucleo": float(nucleo.mean()),
            "grau_medio": float(deg.mean()), "grau_medio_nucleo": float(deg[nucleo].mean()),
            "frac_core1": float((core == 1).mean()),
            "top100_no_nucleo": int(nucleo[top].sum()), "top100_coreness_mediano": float(np.median(core[top]))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fontes", type=int, default=300)
    ap.add_argument("--amostra-clust", type=int, default=20000)
    args = ap.parse_args()

    pasta = pasta_saida("parte3")
    rng = rng_padrao(5)
    ip, ind, _, _ = carregar_grafo()
    deg = np.diff(ip)

    print("[descoberta] k-cores ...", flush=True)
    core = coreness(ip, ind)
    nuc = perfil_nucleo(core, deg)
    print("[descoberta]", nuc, flush=True)

    print("[descoberta] grafo real: C, L, assortatividade ...", flush=True)
    real = medir(ip, ind, args.fontes, args.amostra_clust, rng)
    real["r"] = assortatividade(ip, ind)

    print("[descoberta] nulo (configuration model) ...", flush=True)
    nip, nind, perda = configuracao_apagada(deg, rng)
    nulo = medir(nip, nind, args.fontes, args.amostra_clust, rng)
    nulo["r"], nulo["perda"] = assortatividade(nip, nind), perda

    salvar_json(pasta, "parte3_descoberta.json", {"nucleo": nuc, "real": real, "nulo": nulo})
    tabela_nulo(real, nulo, pasta)
    tabela_nucleo(nuc, pasta)
    grafico(core, deg, pasta)
    print("[descoberta] real:", real, "\n[descoberta] nulo:", nulo, flush=True)


if __name__ == "__main__":
    main()
