# Análise do grafo com-Youtube (SNAP)

Trabalho de análise de grafos (Partes I, II e III) sobre o grafo **com-Youtube**
(1.134.890 vértices, 2.987.624 arestas), com relatório no template WebMedia.
Repositório: <https://github.com/LucasC-Soares/YoutubeGraph>

## Grafo atribuído (cálculo pela matrícula)

O grafo de cada aluno é `g = (S(M) · (U(M) + 1)) mod 129`, em que `S(M)` é a soma dos dígitos da
matrícula `M` e `U(M)` é o número formado pelos dois últimos dígitos.

Para `M = 224215940`: `S = 2+2+4+2+1+5+9+4+0 = 29`, `U = 40`, então
`g = (29 · 41) mod 129 = 1189 mod 129 = 28`. O índice 28 é o
[com-Youtube](https://snap.stanford.edu/data/com-Youtube.html) (rede de amizades do YouTube,
não direcionada e não ponderada; o SNAP distribui apenas a maior componente conexa).

## Resultados principais

| Item | Resultado |
|------|-----------|
| Vértices / arestas | 1.134.890 / 2.987.624 (uma única componente) |
| Grau médio / mediana / máximo | 5,27 / 1 / 28.754 |
| Densidade | 4,64·10⁻⁶ |
| Diâmetro / raio | 24 / 12 (exatos, ver relatório) |
| Caminho médio | 5,36 ± 0,12 (200 fontes, IC95%) |
| Clusterização média / triângulos | 0,0808 / 3.056.386 (exatos, igraph) |
| Small-world | L = 5,34 (aleatório 8,55); C = 0,0796 (aleatório ≈ 4·10⁻⁶); σ ≈ 3,6·10⁴ |
| Lei de potência | γ_MLE = 2,14 (k_min = 8); γ_regressão = 2,43 |
| Robustez (5% dos vértices) | maior componente: 91% (aleatório), 30% (ataque por grau), 25% (PageRank) |
| Grafo completo (Parte II) | não euleriano; 667.090 pontes; 223.409 pontos de articulação |

Detalhes, tabelas e discussão: `relatorio/relatorio.tex`. Dados brutos em `parteN/resultados/`.

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
dados/        bruto e cache baixados/gerados automaticamente (ignorados pelo git);
              arestas_tratadas.csv.gz é a lista tratada, versionada
```

Cada `parteN/` grava em `parteN/resultados/` (JSON, tabelas `.tex`, `fig/*.pdf`);
o `relatorio.tex` inclui esses arquivos por `../parteN/resultados/...`.

## Dado tratado

`dados/arestas_tratadas.csv.gz` é a lista de arestas após a limpeza (sem laços, sem duplicatas,
uma linha por aresta com `u < v`), em CSV com cabeçalho `u,v` e os **IDs originais do SNAP**.
O vértice de índice `i` usado no código (0..n-1) é o `i`-ésimo menor ID original. Para ler:

```python
import numpy as np
arestas = np.loadtxt("dados/arestas_tratadas.csv.gz", delimiter=",", skiprows=1, dtype=np.int64)
```

O bruto (`com-youtube.ungraph.txt.gz`) e o cache binário (`grafo_csr.npz`, ~42 MB) são
regenerados automaticamente e **não** são versionados (ver `.gitignore`).

## Requisitos e instalação

- Python 3.13 (versão usada no desenvolvimento e na validação).
- Dependências com versões fixadas em `requirements.txt` (NumPy, Matplotlib, NetworkX; igraph é opcional).

```bash
pip install -r requirements.txt
```

As medidas de grafo (BFS, componentes, triângulos, Parte II e Parte III) são implementadas do zero
com NumPy; o NetworkX é usado só na visualização e na validação cruzada, e o igraph só para a
contagem exata de triângulos/clusterização da Parte I.

## Execução (sempre a partir da raiz do repositório)

```bash
python -m parte2.validacao                      # prova de corretude contra o NetworkX (rápido)
python -m parte1                                # Parte I
python -m parte2 --rep 30 --completo            # Parte II (demorado; --completo roda no grafo inteiro)
python -m parte3.smallworld                     # Parte III.1
python -m parte3.potencia                       # Parte III.2
python -m parte3.robustez --reps 30             # Parte III.3 (demorado)
python -m comum.exportar                        # exporta dados/arestas_tratadas.csv.gz
```

Compilação do relatório (precisa de `ACM-Reference-Format.bst`):

```bash
cd relatorio && pdflatex relatorio && bibtex relatorio && pdflatex relatorio && pdflatex relatorio
```

### Variáveis de ambiente (opcionais)
`GRAPH_DATA_DIR`, `GRAPH_OUT_ROOT` (raiz de `parteN/resultados`), `GRAPH_SEED` (padrão 42),
`GRAPH_RAW` (caminho do `.txt.gz`, se já baixou), `GRAPH_CACHE`.

## Checklist: requisito → arquivo

| Requisito | Onde está |
|-----------|-----------|
| Determinação do grafo (matrícula) | este README; `relatorio.tex`, seção "Descrição do Grafo Original" |
| Tratamento dos dados | `comum/dados.py`, `comum/exportar.py` (dado tratado); relatório, subseção "Responsabilidade pelo Tratamento dos Dados" |
| **Parte I** — vértices, arestas, graus, densidade | `parte1/basicas.py` |
| Distribuição de graus (CSV + figura) | `parte1/grafico_graus.py` → `parte1/resultados/distribuicao_graus.csv`, `fig/graus.pdf` |
| Componentes conexas e tamanhos | `parte1/componentes.py`, `comum/caminhos.py` |
| Diâmetro, raio, caminho médio | `parte1/distancias.py`, `comum/caminhos.py` |
| Clusterização média e triângulos | `parte1/clusterizacao.py`, `comum/triangulos.py` |
| Visualização do grafo | `parte1/visualizacao.py` → `fig/visualizacao.pdf` |
| **Parte II** — BFS, DFS | `parte2/algoritmos/busca.py` |
| Eulerianidade | `parte2/algoritmos/euleriano.py` |
| Dijkstra, Bellman-Ford, Floyd-Warshall | `parte2/algoritmos/caminhos_minimos.py` |
| Tarjan (pontes e articulações) | `parte2/algoritmos/tarjan.py` |
| AGM (Kruskal, Prim) | `parte2/algoritmos/agm.py` |
| Complexidade teórica × observada, média/desvio/IC | `parte2/complexidade.py`, `medicao.py`, `resumo.py`, `comum/estatistica.py` |
| Execução no grafo completo | `parte2/grafo_completo.py` |
| Prova de corretude dos algoritmos | `parte2/validacao.py` |
| **Parte III.A** — small-world (sem biblioteca pronta) | `parte3/smallworld/` |
| **Parte III.B** — lei de potência | `parte3/potencia/` |
| **Parte III.C** — robustez (aleatória × direcionada) | `parte3/robustez/` |
| Descoberta mais interessante; modelos clássicos | `relatorio.tex`, Parte III |
| Metodologia e discussão crítica | `relatorio.tex`, seções "Metodologia" e "Discussão Crítica" |

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

## Se o seu grafo não for o com-Youtube inteiro
Gere um arquivo de arestas no mesmo formato (duas colunas, `#` para comentários), aponte `GRAPH_RAW`
para ele e apague `dados/grafo_csr.npz`.

## Observações
- Diâmetro/raio/caminho médio: BFS amostradas; o diâmetro é um limite inferior e o raio um limite
  superior (no com-Youtube ambos coincidem com o valor exato, ver relatório). A robustez usa só 20 BFS
  por medição (`--bfs`).
- Clusterização: a Parte I usa o igraph (exato) se instalado; o small-world usa a implementação própria
  em amostra de 20.000 vértices (`--amostra-clust 0` = todos, mais lento).
- Lei de potência: MLE + KS (Clauset et al.), sem teste de bondade de ajuste por bootstrap.
- Algoritmos ponderados usam pesos aleatórios em [1,10] apenas para o estudo de complexidade.
- Reprodutibilidade: sementes fixas (`GRAPH_SEED`, padrão 42).
