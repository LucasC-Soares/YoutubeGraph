"""Caminhos, semente e URL do conjunto de dados, compartilhados por todas as partes.

Variáveis de ambiente (todas opcionais):
  GRAPH_DATA_DIR   pasta dos dados baixados            (padrão: <raiz>/dados)
  GRAPH_OUT_ROOT   raiz onde ficam parteN/resultados   (padrão: raiz do repositório)
  GRAPH_SEED       semente aleatória                   (padrão: 42)
  GRAPH_RAW        caminho do .txt.gz, se já baixado
  GRAPH_CACHE      caminho do cache .npz do grafo
"""
import os
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get("GRAPH_DATA_DIR", str(RAIZ / "dados")))
SAIDA_RAIZ = Path(os.environ.get("GRAPH_OUT_ROOT", str(RAIZ)))
SEED = int(os.environ.get("GRAPH_SEED", "42"))
URL = "https://snap.stanford.edu/data/bigdata/communities/com-youtube.ungraph.txt.gz"
RAW = Path(os.environ.get("GRAPH_RAW", str(DATA_DIR / "com-youtube.ungraph.txt.gz")))
CACHE = Path(os.environ.get("GRAPH_CACHE", str(DATA_DIR / "grafo_csr.npz")))


def pasta_saida(parte: str) -> Path:
    """<raiz>/<parte>/resultados (com a subpasta fig/), criada se não existir."""
    d = SAIDA_RAIZ / parte / "resultados"
    (d / "fig").mkdir(parents=True, exist_ok=True)
    return d


def rng_padrao(offset: int = 0) -> np.random.Generator:
    return np.random.default_rng(SEED + offset)
