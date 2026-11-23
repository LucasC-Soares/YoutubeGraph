"""Exporta a lista de arestas TRATADA (sem laços nem duplicatas, u < v) em CSV comprimido.

Uso (na raiz do repositório):  python -m comum.exportar
Saída: dados/arestas_tratadas.csv.gz  (colunas u,v com os IDs ORIGINAIS do SNAP)

O vértice de índice i no código (0..n-1) é o i-ésimo menor ID original, então o mapeamento
índice -> ID original é a ordenação crescente dos IDs presentes no arquivo.
"""
import gzip

import numpy as np

from comum.config import DATA_DIR
from comum.dados import carregar_grafo

SAIDA = DATA_DIR / "arestas_tratadas.csv.gz"


def main():
    ip, ind, ids, rel = carregar_grafo()
    u = np.repeat(np.arange(len(ip) - 1, dtype=np.int64), np.diff(ip))
    v = ind.astype(np.int64)
    m = u < v  # cada aresta não direcionada aparece duas vezes no CSR; guarda uma
    pares = np.stack([ids[u[m]], ids[v[m]]], axis=1)
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(SAIDA, "wt", encoding="utf-8") as f:
        np.savetxt(f, pares, fmt="%d", delimiter=",", header="u,v", comments="")
    assert len(pares) == rel["n_arestas"], (len(pares), rel["n_arestas"])
    print(f"[exportar] {len(pares)} arestas, {len(ids)} vértices -> {SAIDA}")


if __name__ == "__main__":
    main()
