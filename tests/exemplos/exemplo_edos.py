"""Exemplo: resolver EDOs com Runge-Kutta (scalar e sistemas).

Executar: python tests/exemplos/exemplo_edos.py
"""
from codigos import EDOs
import numpy as np

if __name__ == '__main__':
    # Exemplo escalar: dy/dx = y, y(0)=1
    x_vals, y_vals = EDOs.runge_kutta('y', 0.0, 1.0, 0.1, 1.0, 4)
    print('RK4 escalar: y(1) ≈', y_vals[-1], 'exato e ≈', np.exp(1.0))

    # Exemplo de sistema
    funcs = ['y[1]', '2*y[2]']
    t_vals, u_vals = EDOs.runge_kutta_sistema(funcs, np.array([1.0, 1.0]), 0.0, 1.0, 0.1, 4)
    print('RK4 sistema: u(1) ≈', u_vals[-1], 'exato [e, e^2] ≈', np.exp(1.0), np.exp(2.0))
