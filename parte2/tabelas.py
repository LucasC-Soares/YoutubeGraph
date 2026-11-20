"""Tabelas LaTeX da Parte II."""
from comum.saida import fmt, salvar_tex
from parte2.complexidade import TEORICA


def tabela_tempos(res, pasta):
    linhas = []
    for l in res["linhas"]:
        linhas.append(f"    {l['algoritmo']} & {fmt(int(round(l['V'])))} & {fmt(int(round(l['E'])))} & "
                      f"{l['R']} & {fmt(l['media_s'] * 1e3, 2)} & {fmt(l['desvio_s'] * 1e3, 2)} & "
                      f"[{fmt((l['media_s'] - l['ic95_s']) * 1e3, 2)}; {fmt((l['media_s'] + l['ic95_s']) * 1e3, 2)}] & "
                      f"{l['dist']} \\\\")
    salvar_tex(pasta, "tab_tempos.tex",
               "\\begin{tabular}{lrrrrrcc}\n    \\toprule\n"
               "    Algoritmo & $V$ & $E$ & $R$ & Média (ms) & Desvio (ms) & IC95\\% (ms) & Dist. \\\\\n    \\midrule\n"
               + "\n".join(linhas) + "\n    \\bottomrule\n\\end{tabular}\n")


def tabela_complexidade(res, pasta):
    linhas = []
    for a, (lab, _) in TEORICA.items():
        aj = res["ajuste"].get(a)
        obs = f"{fmt(aj['expoente'], 2)} & {fmt(aj['r2'], 3)}" if aj else "-- & --"
        linhas.append(f"    {a} & {lab} & {obs} \\\\")
    salvar_tex(pasta, "tab_complexidade.tex",
               "\\begin{tabular}{llrr}\n    \\toprule\n    Algoritmo & Teórica & Expoente $b$ & $R^2$ \\\\\n    \\midrule\n"
               + "\n".join(linhas) + "\n    \\bottomrule\n\\end{tabular}\n")
