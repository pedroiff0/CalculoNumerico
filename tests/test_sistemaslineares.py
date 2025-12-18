import numpy as np
from codigos import sistemaslineares as sl


def test_eliminacao_sem_pivotamento_basic():
    A = np.array([[2.0, 1.0], [4.0, -6.0]])
    b = np.array([3.0, -2.0])
    x, Atri, bmod, flag = sl.eliminacao_gauss_sem_pivotamento(A, b)
    assert x is not None
    assert np.allclose(x, np.linalg.solve(A, b), atol=1e-12)


def test_eliminacao_sem_pivotamento_pivo_zero():
    A = np.array([[0.0, 1.0], [0.0, 2.0]])
    b = np.array([1.0, 2.0])
    x, *_ = sl.eliminacao_gauss_sem_pivotamento(A, b)
    assert x is None


def test_eliminacao_com_pivotamento_basic():
    A = np.array([[0.0, 2.0], [1.0, 3.0]])
    b = np.array([1.0, 4.0])
    x, A_mod, b_mod = sl.eliminacao_gauss_com_pivotamento(A, b)
    assert x is not None
    assert np.allclose(x, np.linalg.solve(A, b), atol=1e-12)


def test_lu_sem_pivot_reconstructs_A():
    A = np.array([[4.0, 3.0], [6.0, 3.0]])
    L, U = sl.lu_sem_pivot(A, np.zeros(2))
    assert np.allclose(L @ U, A, atol=1e-12)


def test_lu_com_pivot_reconstructs_PA():
    A = np.array([[0.0, 2.0], [1.0, 3.0]])
    P, L, U = sl.lu_com_pivot(A, np.zeros(2))
    assert np.allclose(P @ A, L @ U, atol=1e-12)


def test_calcular_residuo_zero_for_exact_solution():
    A = np.array([[2.0, 0.0], [0.0, 5.0]])
    x = np.array([1.0, -1.0])
    b = A @ x
    r = sl.calcular_residuo(A, x, b)
    assert np.allclose(r, np.zeros_like(r), atol=1e-12)
