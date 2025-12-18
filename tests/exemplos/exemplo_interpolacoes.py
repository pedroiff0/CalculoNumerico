"""Exemplo: uso de interpolação (Newton e Lagrange)"""
from codigos import interpolacoes

if __name__ == '__main__':
    x = [0.0, 1.0, 2.0]
    y = [0.0, 1.0, 4.0]
    tabela = interpolacoes.tabela_diferencas_divididas(x, y)
    print('Newton @1.5 ->', interpolacoes.newton_dif_divididas(x, tabela, 1.5))
    print('Lagrange @1.5 ->', interpolacoes.lagrange_interpol(x, y, 1.5))
