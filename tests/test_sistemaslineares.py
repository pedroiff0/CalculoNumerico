import numpy as np
import pytest
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
    x, A_mod, b_mod, flag = sl.eliminacao_gauss_com_pivotamento(A, b)
    assert x is not None
    assert flag is False
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


def test_eliminacao_sem_pivotamento_flag_error():
    A = np.array([[0.0, 1.0], [0.0, 2.0]])
    b = np.array([1.0, 2.0])
    x, Atri, bmod, flag = sl.eliminacao_gauss_sem_pivotamento(A, b)
    assert x is None
    assert flag is True  # Should be True for error, but currently False - bug!


def test_eliminacao_com_pivotamento_impossible():
    A = np.array([[0.0, 0.0], [0.0, 0.0]])
    b = np.array([1.0, 2.0])
    x, A_mod, b_mod, flag = sl.eliminacao_gauss_com_pivotamento(A, b)
    assert x is None
    assert flag is True


def test_forward_solve_basic():
    L = np.array([[1.0, 0.0], [0.5, 1.0]])
    b = np.array([2.0, 3.0])
    y = sl.forward_solve(L, b)
    expected = np.array([2.0, 2.0])  # 2, 3 - 0.5*2
    assert np.allclose(y, expected)


def test_backward_solve_basic():
    U = np.array([[2.0, 1.0], [0.0, 3.0]])
    y = np.array([5.0, 3.0])
    x = sl.backward_solve(U, y)
    expected = np.array([2.0, 1.0])  # From U x = y: x1=3/3=1, x0=(5-1*1)/2=2
    assert np.allclose(x, expected)


def test_lu_sem_pivot_zero_pivot_raises():
    A = np.array([[0.0, 1.0], [1.0, 2.0]])
    with pytest.raises(ZeroDivisionError):
        sl.lu_sem_pivot(A, None)


def test_gauss_com_pivotamento_example_1():
    # From interactive: A = [[8,2,-2],[10,2,4],[12,2,2]], b = [-2,4,6]
    A = np.array([[8.0, 2.0, -2.0], [10.0, 2.0, 4.0], [12.0, 2.0, 2.0]])
    b = np.array([-2.0, 4.0, 6.0])
    x, A_mod, b_mod, flag = sl.eliminacao_gauss_com_pivotamento(A, b)
    assert x is not None
    assert flag is False
    assert np.allclose(A @ x, b, atol=1e-12)


def test_gauss_sem_pivotamento_example_2():
    # From interactive: A = [[8,4,-1],[-2,5,1],[2,-1,6]], b = [11,4,7]
    A = np.array([[8.0, 4.0, -1.0], [-2.0, 5.0, 1.0], [2.0, -1.0, 6.0]])
    b = np.array([11.0, 4.0, 7.0])
    x, Atri, bmod, flag = sl.eliminacao_gauss_sem_pivotamento(A, b)
    assert x is not None
    assert np.allclose(A @ x, b, atol=1e-12)
    assert flag is False  # success


def test_lu_sem_pivot_example_3():
    # From interactive: A = [[2,-6,-1],[-3,-1,7],[-8,1,-2]], b = [-38,-34,-20]
    A = np.array([[2.0, -6.0, -1.0], [-3.0, -1.0, 7.0], [-8.0, 1.0, -2.0]])
    b = np.array([-38.0, -34.0, -20.0])
    L, U = sl.lu_sem_pivot(A, b)
    assert np.allclose(L @ U, A, atol=1e-12)
    # Solve and check
    y = sl.forward_solve(L, b)
    x = sl.backward_solve(U, y)
    assert np.allclose(A @ x, b, atol=1e-12)


def test_gauss_sem_pivotamento_example_4():
    # From interactive: A = [[10,2,-1],[-3,-6,2],[1,1,5]], b = [27,-61.5,-21.5]
    A = np.array([[10.0, 2.0, -1.0], [-3.0, -6.0, 2.0], [1.0, 1.0, 5.0]])
    b = np.array([27.0, -61.5, -21.5])
    x, Atri, bmod, flag = sl.eliminacao_gauss_sem_pivotamento(A, b)
    assert x is not None
    assert np.allclose(A @ x, b, atol=1e-12)


def test_gauss_com_pivotamento_5x5():
    # From interactive 5x5 system
    A = np.array([
        [0.0, 1.0, 3.0, 2.0, 4.0],
        [8.0, -2.0, 9.0, -1.0, 2.0],
        [5.0, 1.0, 1.0, 7.0, 2.0],
        [-2.0, 4.0, 5.0, 1.0, 0.0],
        [7.0, -3.0, 2.0, -4.0, 1.0]
    ])
    b = np.array([3.0, -5.0, 6.0, -1.0, 8.0])
    x, A_mod, b_mod, flag = sl.eliminacao_gauss_com_pivotamento(A, b)
    assert x is not None
    assert flag is False
    assert np.allclose(A @ x, b, atol=1e-12)


def test_input_validation_non_square_A():
    A = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])  # 2x3
    b = np.array([1.0, 2.0])
    with pytest.raises(ValueError, match="A deve ser uma matriz quadrada 2D"):
        sl.eliminacao_gauss_sem_pivotamento(A, b)


def test_input_validation_b_wrong_shape():
    A = np.array([[1.0, 2.0], [3.0, 4.0]])
    b = np.array([1.0, 2.0, 3.0])  # wrong length
    with pytest.raises(ValueError, match="b deve ser um vetor 1D com comprimento igual ao número de linhas de A"):
        sl.eliminacao_gauss_sem_pivotamento(A, b)


def test_input_validation_b_not_1d():
    A = np.array([[1.0, 2.0], [3.0, 4.0]])
    b = np.array([[1.0], [2.0]])  # 2x1 instead of 1d
    with pytest.raises(ValueError, match="b deve ser um vetor 1D"):
        sl.eliminacao_gauss_sem_pivotamento(A, b)
