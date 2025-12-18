import numpy as np
from codigos import ajustecurvas as ac


def test_calcula_chi_e_r2_perfect_linear():
    x = np.array([0.0, 1.0, 2.0])
    y = 1.0 + 2.0 * x  # y = 2x + 1
    stats = ac.calcula_chi_e_r2(x, y, b0=1.0, b1=2.0, n_params=2)
    assert abs(stats['Desvio']) < 1e-12
    assert abs(stats['Chi2']) < 1e-12
    assert abs(stats['R2'] - 1.0) < 1e-12


def test_minquadrados_coefficients():
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = 1.0 + 2.0 * x
    # compute expected coefficients
    n = len(x)
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_xy = np.sum(x * y)
    sum_x2 = np.sum(x ** 2)
    b1 = (sum_x * sum_y - n * sum_xy) / ((sum_x) ** 2 - n * sum_x2)
    b0 = (sum_y - b1 * sum_x) / n

    # call module computation (replicate the formula)
    stats = ac.calcula_chi_e_r2(x, y, b0=b0, b1=b1)
    assert abs(stats['R2'] - 1.0) < 1e-12


def test_tabela_minimos_quadrados_runs_without_error():
    x = np.array([0.0, 1.0, 2.0])
    y = np.array([1.0, 3.0, 5.0])
    # Should not raise
    ac.tabela_minimos_quadrados(x, y)


def test_minquadrados_ordem_n_quadratic():
    # Fit quadratic y = 1 + 2x + 3x^2
    x = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    y = 1.0 + 2.0 * x + 3.0 * (x ** 2)
    coef = ac.minquadrados_ordem_n_manual(x, y, ordem=2, tabela=False, grafico=False)
    # coef order: a0 + a1 x + a2 x^2
    assert coef is not None
    assert abs(coef[0] - 1.0) < 1e-8
    assert abs(coef[1] - 2.0) < 1e-8
    assert abs(coef[2] - 3.0) < 1e-8
