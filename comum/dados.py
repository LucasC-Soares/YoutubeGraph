"""Carga e limpeza dos dados (seção "responsabilidade pelo tratamento dos dados" do relatório)."""
import json
import urllib.request

import numpy as np

from comum.config import CACHE, DATA_DIR, RAW, URL
from comum.grafo import csr_from_edges


def baixar_se_preciso() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    RAW.parent.mkdir(parents=True, exist_ok=True)
    if not RAW.exists():
        print(f"[dados] baixando {URL} ...")
        urllib.request.urlretrieve(URL, RAW)


def limpar(edges: np.ndarray):
    """Remove laços e arestas duplicadas, trata o grafo como não direcionado e
    reindexa os IDs originais (não contíguos) para 0..n-1. Devolve relatório."""
    rel = {"linhas_arquivo": int(len(edges))}
    sem_laco = edges[edges[:, 0] != edges[:, 1]]
    rel["lacos_removidos"] = int(len(edges) - len(sem_laco))
    lo = np.minimum(sem_laco[:, 0], sem_laco[:, 1])
    hi = np.maximum(sem_laco[:, 0], sem_laco[:, 1])
    par = np.unique(np.stack([lo, hi], axis=1), axis=0)
    rel["duplicatas_removidas"] = int(len(sem_laco) - len(par))
    ids, inv = np.unique(par.ravel(), return_inverse=True)
    uv = inv.reshape(-1, 2)
    rel["n_vertices"] = int(len(ids))
    rel["n_arestas"] = int(len(uv))
    return uv[:, 0], uv[:, 1], ids, rel


def carregar_grafo():
    """Retorna (indptr, indices, ids_originais, relatorio_limpeza)."""
    if CACHE.exists():
        z = np.load(CACHE, allow_pickle=False)
        return z["indptr"], z["indices"], z["ids"], json.loads(str(z["rel"]))
    baixar_se_preciso()
    print("[dados] lendo lista de arestas (pode levar ~1 min) ...")
    edges = np.loadtxt(RAW, dtype=np.int64, comments="#")  # aceita .gz
    u, v, ids, rel = limpar(edges)
    indptr, indices = csr_from_edges(len(ids), u, v)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    np.savez(CACHE, indptr=indptr, indices=indices, ids=ids, rel=np.array(json.dumps(rel)))
    return indptr, indices, ids, rel
