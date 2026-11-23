"""Tabelas LaTeX: nulo que preserva os graus e perfil dos k-cores."""
from comum.saida import fmt, salvar_tex


def tabela_nulo(real, nulo, pasta):
    f = fmt
    sinal = lambda x: f(x).replace('-', '$-$')  # menos tipográfico
    linhas = [
        f"    $C$ (clusterização média) & {f(real['C'])} & {f(nulo['C'])} \\\\",
        f"    $L$ (caminho médio) & {f(real['L'], 2)} & {f(nulo['L'], 2)} \\\\",
        f"    Diâmetro ($\\geq$) & {real['diam_lb']} & {nulo['diam_lb']} \\\\",
        f"    Assortatividade de grau $r$ & {sinal(real['r'])} & {sinal(nulo['r'])} \\\\",
        f"    Arestas perdidas na construção & --- & {f(100 * nulo['perda'], 2)}\\% \\\\",
    ]
    salvar_tex(pasta, "tab_nulo.tex",
               "\\begin{tabular}{lrr}\n    \\toprule\n    Medida & com-Youtube & Nulo (mesmos graus) \\\\\n    \\midrule\n"
               + "\n".join(linhas) + "\n    \\bottomrule\n\\end{tabular}\n")


def tabela_nucleo(k, salvar_pasta):
    f = fmt
    linhas = [
        f"    Degenerescência (maior coreness) $k_{{max}}$ & {k['kmax']} \\\\",
        f"    Vértices no núcleo máximo & {f(k['n_nucleo'])} ({f(100 * k['frac_nucleo'], 2)}\\%) \\\\",
        f"    Grau médio no núcleo máximo (global: {f(k['grau_medio'], 2)}) & {f(k['grau_medio_nucleo'], 1)} \\\\",
        f"    Vértices com coreness 1 & {f(100 * k['frac_core1'], 1)}\\% \\\\",
        f"    Dos 100 maiores graus, no núcleo máximo & {k['top100_no_nucleo']}\\% \\\\",
        f"    Coreness mediano dos 100 maiores graus & {f(k['top100_coreness_mediano'], 0)} \\\\",
    ]
    salvar_tex(salvar_pasta, "tab_nucleo.tex",
               "\\begin{tabular}{lr}\n    \\toprule\n    Medida & Valor \\\\\n    \\midrule\n" + "\n".join(linhas)
               + "\n    \\bottomrule\n\\end{tabular}\n")
