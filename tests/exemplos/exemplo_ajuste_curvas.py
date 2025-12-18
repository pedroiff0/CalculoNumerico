"""Exemplo: ajuste de curva linear simples (ajustecurvas)"""
import numpy as np
from codigos import ajustecurvas as ac

if __name__ == '__main__':
    x = np.array([0.0,1.0,2.0])
    y = 1.0 + 2.0 * x
    ac.grafico = False
    ac.tabela = False
    ac.minquadrados(x, y)
    stats = ac.calcula_chi_e_r2(x, y, b0=1.0, b1=2.0, n_params=2)
    print('R2 ->', stats['R2'])