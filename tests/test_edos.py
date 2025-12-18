import numpy as np
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
