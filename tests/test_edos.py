import numpy as np
import pytest
import math
from codigos import EDOs


def test_runge_kutta_scalar_exp():
    # dy/dx = y, y(0)=1 -> y(1)=e
    x_vals, y_vals = EDOs.runge_kutta('y', 0.0, 1.0, 0.01, 1.0, 4)
    approx = y_vals[-1]
    assert abs(approx - np.exp(1.0)) < 5e-4


def test_runge_kutta_system_exp():
    # system: u0' = u0, u1' = 2*u1 with u0(0)=u1(0)=1
    funcs = ['y[1]', '2*y[2]']
    # usar passo menor para alcançar precisão suficiente em testes automatizados
    t_vals, u_vals = EDOs.runge_kutta_sistema(funcs, np.array([1.0, 1.0]), 0.0, 1.0, 0.001, 4)
    u_end = u_vals[-1]
    assert abs(u_end[0] - np.exp(1.0)) < 1e-4
    assert abs(u_end[1] - np.exp(2.0)) < 1e-3


def test_passos_edo_with_m():
    h, xn = EDOs.passos_edo(0.0, 1.0, 0.0, m=10)
    assert pytest.approx(h) == 0.1
    assert xn == 1.0


def test_runge_kutta_orders_accuracy():
    # dy/dx = y, y(0)=1 -> y(1) = e
    exact = math.e
    h = 0.001
    tol_order = {1:5e-3, 2:1e-4, 3:5e-5, 4:1e-6}
    for order, tol in tol_order.items():
        x_vals, y_vals = EDOs.runge_kutta('y', 0.0, 1.0, h, 1.0, order)
        approx = y_vals[-1]
        assert abs(approx - exact) < tol


def test_runge_kutta_h_nonpositive_raises():
    with pytest.raises(ValueError):
        EDOs.runge_kutta('y', 0.0, 1.0, 0.0, 1.0, 4)


def test_runge_kutta_sistema_last_step():
    # system: u0' = u0, u1' = u1, with initial [1,1], exact at t=1 => [e, e]
    funcs = ['y[1]', 'y[2]']
    t_vals, u_vals = EDOs.runge_kutta_sistema(funcs, np.array([1.0,1.0]), 0.0, 1.0, 0.3, 4)
    # ensure final time equals tf exactly (last step smaller than h)
    assert pytest.approx(t_vals[-1], rel=1e-12) == 1.0
    # check values reasonable
    assert abs(u_vals[-1][0] - math.e) < 1e-3
    assert abs(u_vals[-1][1] - math.e) < 1e-3
