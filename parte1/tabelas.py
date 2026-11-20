"""Tabelas LaTeX da Parte I."""
import numpy as np

from comum.saida import fmt, salvar_tex


def tabela_estrutural(status, pasta):
    linhas = []
    for nome, (val, _) in status.items():
        if isinstance(val, (int, np.integer)):
            s = fmt(val)
        elif isinstance(val, float):
            s = fmt(val, 6 if abs(val) < 0.01 else 4)
        else:
            s = str(val).replace("%", "\\%")
        linhas.append(f"    {nome} & {s} \\\\")
    salvar_tex(pasta, "tab_estrutural.tex",
               "\\begin{tabular}{lr}\n    \\toprule\n    Medida & Valor \\\\\n    \\midrule\n"
               + "\n".join(linhas) + "\n    \\bottomrule\n\\end{tabular}\n")


def tabela_componentes(tam_ord, n, pasta):
    top = tam_ord[:10]
    linhas = [f"    {i + 1} & {fmt(int(t))} & {t / n:.4%} \\\\".replace("%", "\\%").replace(".", ",", 1)
              for i, t in enumerate(top)]
    extra = ""
    if len(tam_ord) > 10:
        extra = (f"    \\multicolumn{{3}}{{l}}{{(+{len(tam_ord) - 10} componentes; menor = {int(tam_ord[-1])}, "
                 f"mediana = {int(np.median(tam_ord))})}} \\\\\n")
    salvar_tex(pasta, "tab_componentes.tex",
               "\\begin{tabular}{rrr}\n    \\toprule\n    Componente & Tamanho & \\% dos vértices \\\\\n"
               "    \\midrule\n" + "\n".join(linhas) + "\n" + extra + "    \\bottomrule\n\\end{tabular}\n")


def tabela_computado(status, pasta):
    linhas = []
    for nome, (_, como) in status.items():
        sim = "Sim" if "não computado" not in como else "Não"
        como_tex = como.replace("%", "\\%")
        linhas.append(f"    {nome} & {sim} & {como_tex} \\\\")
    salvar_tex(pasta, "tab_computado.tex",
               "\\begin{tabular}{llp{0.45\\linewidth}}\n    \\toprule\n    Medida & Computada? & Observação \\\\\n"
               "    \\midrule\n" + "\n".join(linhas) + "\n    \\bottomrule\n\\end{tabular}\n")
