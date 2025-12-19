"""Testes para o módulo `codigos.edos`.

Cobre solver Runge-Kutta (ordens 1-4) para EDOs escalares e sistemas, bem
como validações de entradas e tratamento de passos/resíduos."""

import numpy as np
import pytest
import math
from codigos import edos

def test_runge_kutta_scalar_exp():
    """Verifica RK (4ª ordem) para dy/dx = y com y(0)=1; y(1) ≈ e."""
    x_vals, y_vals = edos.runge_kutta('y', 0.0, 1.0, 0.01, 1.0, 4)
    approx = y_vals[-1]
    assert abs(approx - np.exp(1.0)) < 5e-4


def test_runge_kutta_system_exp():
    """Sistema simples: u0' = u0, u1' = 2*u1; verifica solução analítica em t=1."""
    funcs = ['y[1]', '2*y[2]']
    t_vals, u_vals = edos.runge_kutta_sistema(funcs, np.array([1.0, 1.0]), 0.0, 1.0, 0.001, 4)
    u_end = u_vals[-1]
    assert abs(u_end[0] - np.exp(1.0)) < 1e-4
    assert abs(u_end[1] - np.exp(2.0)) < 1e-3


def test_passos_edo_with_m():
    """Verifica cálculo de h e xn dado número de subintervalos m."""
    h, xn = edos.passos_edo(0.0, 1.0, 0.0, m=10)
    assert pytest.approx(h) == 0.1
    assert xn == 1.0


def test_runge_kutta_orders_accuracy():
    """Valida precisão aproximada por ordem do método Runge-Kutta."""
    exact = math.e
    h = 0.001
    tol_order = {1:5e-3, 2:1e-4, 3:5e-5, 4:1e-6}
    for order, tol in tol_order.items():
        x_vals, y_vals = edos.runge_kutta('y', 0.0, 1.0, h, 1.0, order)
        approx = y_vals[-1]
        assert abs(approx - exact) < tol


def test_runge_kutta_h_nonpositive_raises():
    """h <= 0 deve levantar ValueError."""
    with pytest.raises(ValueError):
        edos.runge_kutta('y', 0.0, 1.0, 0.0, 1.0, 4)


def test_runge_kutta_sistema_last_step():
    """Garante que o tempo final coincide exatamente com tf quando o último passo é menor que h."""
    funcs = ['y[1]', 'y[2]']
    t_vals, u_vals = edos.runge_kutta_sistema(funcs, np.array([1.0,1.0]), 0.0, 1.0, 0.3, 4)
    assert pytest.approx(t_vals[-1], rel=1e-12) == 1.0


def test_runge_kutta_sistema_predator_prey():
    """Teste qualitativo da simulação de Lotka-Volterra (predador-presa)."""
    funcs = ['y[1] - y[1]*y[2]', '-y[2] + y[1]*y[2]']
    t_vals, u_vals = edos.runge_kutta_sistema(funcs, np.array([2.0, 1.0]), 0.0, 0.5, 0.01, 4)
    # Check that values are positive and reasonable
    assert all(u > 0 for u in u_vals.flatten())
    assert u_vals[0][0] == 2.0  # initial
    assert u_vals[0][1] == 1.0


def test_runge_kutta_negative_h_raises():
    with pytest.raises(ValueError):
        edos.runge_kutta('y', 0.0, 1.0, -0.1, 1.0, 4)


def test_runge_kutta_invalid_order_raises():
    with pytest.raises(ValueError):
        edos.runge_kutta('y', 0.0, 1.0, 0.1, 1.0, 0)
