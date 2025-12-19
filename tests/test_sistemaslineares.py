import numpy as np
import pytest
from codigos import sistemaslineares as sl


def test_eliminacao_sem_pivotamento_basic():
    """Verifica solução de um sistema 2x2 pelo método de Gauss sem pivotamento.

    - Matriz A e vetor b simples; compara a solução retornada com
      `numpy.linalg.solve` para garantir correção numérica.
    """
    A = np.array([[2.0, 1.0], [4.0, -6.0]])
    b = np.array([3.0, -2.0])
    x, Atri, bmod, flag = sl.eliminacao_gauss_sem_pivotamento(A, b)
    assert x is not None
    assert np.allclose(x, np.linalg.solve(A, b), atol=1e-12)


def test_eliminacao_sem_pivotamento_pivo_zero():
    """Garante que o método sem pivotamento detecta pivô zero e retorna falha.

    - Matriz com zero na diagonal principal (pivô) deve provocar retorno
      com solução ``None`` e erro sinalizado.
    """
    A = np.array([[0.0, 1.0], [0.0, 2.0]])
    b = np.array([1.0, 2.0])
    x, *_ = sl.eliminacao_gauss_sem_pivotamento(A, b)
    assert x is None


def test_eliminacao_com_pivotamento_basic():
    """Verifica que a eliminação com pivotamento resolve sistemas que
    necessitam troca de linhas para evitar pivôs nulos.
    """
    A = np.array([[0.0, 2.0], [1.0, 3.0]])
    b = np.array([1.0, 4.0])
    x, A_mod, b_mod, flag = sl.eliminacao_gauss_com_pivotamento(A, b)
    assert x is not None
    assert flag is False
    assert np.allclose(x, np.linalg.solve(A, b), atol=1e-12)


def test_lu_sem_pivot_reconstructs_A():
    """Verifica que a decomposição LU sem pivotamento reconstrói A (L@U == A)."""
    A = np.array([[4.0, 3.0], [6.0, 3.0]])
    L, U = sl.lu_sem_pivot(A, np.zeros(2))
    assert np.allclose(L @ U, A, atol=1e-12)


def test_lu_com_pivot_reconstructs_PA():
    """Verifica que para LU com pivotamento vale P @ A == L @ U."""
    A = np.array([[0.0, 2.0], [1.0, 3.0]])
    P, L, U = sl.lu_com_pivot(A, np.zeros(2))
    assert np.allclose(P @ A, L @ U, atol=1e-12)


def test_calcular_residuo_zero_for_exact_solution():
    """Garante que o resíduo r = b - A x é zero quando x é solução exata."""
    A = np.array([[2.0, 0.0], [0.0, 5.0]])
    x = np.array([1.0, -1.0])
    b = A @ x
    r = sl.calcular_residuo(A, x, b)
    assert np.allclose(r, np.zeros_like(r), atol=1e-12)


def test_eliminacao_sem_pivotamento_flag_error():
    """Verifica que a função sinaliza erro (flag True) quando detecta pivô zero."""
    A = np.array([[0.0, 1.0], [0.0, 2.0]])
    b = np.array([1.0, 2.0])
    x, Atri, bmod, flag = sl.eliminacao_gauss_sem_pivotamento(A, b)
    assert x is None
    assert flag is True


def test_eliminacao_com_pivotamento_impossible():
    """Caso degenerado: matriz nula deve ser marcada como impossível pelo método."""
    A = np.array([[0.0, 0.0], [0.0, 0.0]])
    b = np.array([1.0, 2.0])
    x, A_mod, b_mod, flag = sl.eliminacao_gauss_com_pivotamento(A, b)
    assert x is None
    assert flag is True


def test_forward_solve_basic():
    """Testa substituição progressiva (forward solve) para uma L triangular inferior."""
    L = np.array([[1.0, 0.0], [0.5, 1.0]])
    b = np.array([2.0, 3.0])
    y = sl.forward_solve(L, b)
    expected = np.array([2.0, 2.0])  # 2, 3 - 0.5*2
    assert np.allclose(y, expected)


def test_backward_solve_basic():
    """Testa substituição regressiva (backward solve) para uma U triangular superior."""
    U = np.array([[2.0, 1.0], [0.0, 3.0]])
    y = np.array([5.0, 3.0])
    x = sl.backward_solve(U, y)
    expected = np.array([2.0, 1.0])  # From U x = y: x1=3/3=1, x0=(5-1*1)/2=2
    assert np.allclose(x, expected)


def test_lu_sem_pivot_zero_pivot_raises():
    """Verifica que LU sem pivotamento lança ZeroDivisionError quando pivô é zero."""
    A = np.array([[0.0, 1.0], [1.0, 2.0]])
    with pytest.raises(ZeroDivisionError):
        sl.lu_sem_pivot(A, None)


def test_gauss_com_pivotamento_example_1():
    """Exemplo realista (3x3) testando eliminação com pivotamento.

    - Checa consistência A @ x == b e flag == False para sucesso
    """
    A = np.array([[8.0, 2.0, -2.0], [10.0, 2.0, 4.0], [12.0, 2.0, 2.0]])
    b = np.array([-2.0, 4.0, 6.0])
    x, A_mod, b_mod, flag = sl.eliminacao_gauss_com_pivotamento(A, b)
    assert x is not None
    assert flag is False
    assert np.allclose(A @ x, b, atol=1e-12)


def test_gauss_sem_pivotamento_example_2():
    """Exemplo 3x3 testando eliminação sem pivotamento retorna solução correta."""
    A = np.array([[8.0, 4.0, -1.0], [-2.0, 5.0, 1.0], [2.0, -1.0, 6.0]])
    b = np.array([11.0, 4.0, 7.0])
    x, Atri, bmod, flag = sl.eliminacao_gauss_sem_pivotamento(A, b)
    assert x is not None
    assert np.allclose(A @ x, b, atol=1e-12)
    assert flag is False  # success


def test_lu_sem_pivot_example_3():
    """Outro exemplo 3x3 verificando LU sem pivotamento e solução resultante."""
    A = np.array([[2.0, -6.0, -1.0], [-3.0, -1.0, 7.0], [-8.0, 1.0, -2.0]])
    b = np.array([-38.0, -34.0, -20.0])
    L, U = sl.lu_sem_pivot(A, b)
    assert np.allclose(L @ U, A, atol=1e-12)
    # Solve and check
    y = sl.forward_solve(L, b)
    x = sl.backward_solve(U, y)
    assert np.allclose(A @ x, b, atol=1e-12)


def test_gauss_sem_pivotamento_example_4():
    """Exemplo 3x3 com resultados conhecidos para validação do método sem pivotamento."""
    A = np.array([[10.0, 2.0, -1.0], [-3.0, -6.0, 2.0], [1.0, 1.0, 5.0]])
    b = np.array([27.0, -61.5, -21.5])
    x, Atri, bmod, flag = sl.eliminacao_gauss_sem_pivotamento(A, b)
    assert x is not None
    assert np.allclose(A @ x, b, atol=1e-12)


def test_gauss_com_pivotamento_5x5():
    """Caso 5x5 retirado do conjunto de exemplos interativos, valida convergência."""
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
    """Validação: matriz não quadrada deve levantar ValueError."""
    A = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])  # 2x3
    b = np.array([1.0, 2.0])
    with pytest.raises(ValueError, match="A deve ser uma matriz quadrada 2D"):
        sl.eliminacao_gauss_sem_pivotamento(A, b)


def test_input_validation_b_wrong_shape():
    """Validação: vetor b com tamanho incompatível deve levantar ValueError."""
    A = np.array([[1.0, 2.0], [3.0, 4.0]])
    b = np.array([1.0, 2.0, 3.0])  # wrong length
    with pytest.raises(ValueError, match="b deve ser um vetor 1D com comprimento igual ao número de linhas de A"):
        sl.eliminacao_gauss_sem_pivotamento(A, b)


def test_input_validation_b_not_1d():
    """Validação: vetor b com dimensões incorretas (2D) deve levantar ValueError."""
    A = np.array([[1.0, 2.0], [3.0, 4.0]])
    b = np.array([[1.0], [2.0]])  # 2x1 instead of 1d
    with pytest.raises(ValueError, match="b deve ser um vetor 1D"):
        sl.eliminacao_gauss_sem_pivotamento(A, b)


def test_montar_sistema_valores_eof(monkeypatch):
    """Se ocorrer EOF durante a leitura interativa, a função retorna None.

    - Simula `input` que levanta EOFError e verifica comportamento seguro.
    """
    def raise_eof(prompt=''):
        raise EOFError
    monkeypatch.setattr('builtins.input', raise_eof)
    assert sl.montar_sistema_valores() is None
