# Análise do grafo com-Youtube (SNAP)

## Estrutura

```
comum/        código compartilhado (dados, grafo CSR, BFS/componentes, triângulos, estatística, saída)
parte1/       Parte I  — análise estrutural                 (python -m parte1)
parte2/       Parte II — algoritmos da disciplina           (python -m parte2)
  algoritmos/   busca, euleriano, caminhos_minimos, tarjan, agm
parte3/       Parte III
  smallworld/   Apêndice A  (python -m parte3.smallworld)
  potencia/     Apêndice B  (python -m parte3.potencia)
  robustez/     Apêndice C  (python -m parte3.robustez)
relatorio/    relatorio.tex, refs.bib, webmedia.cls
dados/        baixado automaticamente do SNAP (ignorado pelo git)
```

Cada `parteN/` grava em `parteN/resultados/` (JSON, tabelas `.tex`, `fig/*.pdf`);
o `relatorio.tex` inclui esses arquivos por `../parteN/resultados/...`.

## Instalação
```bash
pip install -r requirements.txt   # igraph é opcional (triângulos exatos)
```

## Execução (sempre a partir da raiz do repositório)
```bash
python -m parte2.validacao                      # prova de corretude contra o NetworkX (rápido)
python -m parte1                                # Parte I
python -m parte2 --rep 30 --completo            # Parte II (demorado; --completo roda no grafo inteiro)
python -m parte3.smallworld                     # Parte III.1
python -m parte3.potencia                       # Parte III.2
python -m parte3.robustez --reps 30             # Parte III.3 (demorado)
```
Compilação do relatório (precisa de `ACM-Reference-Format.bst`):
```bash
cd relatorio && pdflatex relatorio && bibtex relatorio && pdflatex relatorio && pdflatex relatorio
```

## Onde mexer
| Quero alterar...                         | Arquivo |
|------------------------------------------|---------|
| leitura/limpeza do dataset               | `comum/dados.py` |
| BFS vetorizada, componentes, amostragem  | `comum/caminhos.py` |
| triângulos / clusterização               | `comum/triangulos.py` |
| IC95% (Z / t-Student)                    | `comum/estatistica.py` |
| um algoritmo da Parte II                 | `parte2/algoritmos/<família>.py` |
| tamanhos/limites do experimento          | `parte2/complexidade.py`, argumentos de `python -m parte2` |
| ajuste da lei de potência                | `parte3/potencia/ajuste.py` |
| métricas de robustez                     | `parte3/robustez/metricas.py` |
| formato de uma tabela                    | `tabela.py` / `tabelas.py` da respectiva parte |

## Variáveis de ambiente (opcionais)
`GRAPH_DATA_DIR`, `GRAPH_OUT_ROOT` (raiz de `parteN/resultados`), `GRAPH_SEED` (padrão 42),
`GRAPH_RAW` (caminho do `.txt.gz`, se já baixou), `GRAPH_CACHE`.

## Se o seu grafo não for o com-Youtube inteiro
Gere um arquivo de arestas no mesmo formato (duas colunas, `#` para comentários), aponte `GRAPH_RAW`
para ele e apague `dados/grafo_csr.npz`.

## Observações
- Diâmetro/raio/caminho médio: estimados por BFS amostradas (limite inferior / superior).
- Clusterização: a Parte I usa o igraph (exato) se instalado; o small-world usa a implementação própria
  em amostra de 20 000 vértices (`--amostra-clust 0` = todos, mais lento).
- Lei de potência: MLE + KS (Clauset et al.), sem teste de bondade de ajuste por bootstrap.
- Algoritmos ponderados usam pesos aleatórios em [1,10] apenas para o estudo de complexidade.
