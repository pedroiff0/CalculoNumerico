"""Testes para o módulo `codigos.ajustecurvas`.

Cobre mínimos quadrados (linear e ordem n), cálculo de Chi²/R², validações
básicas e execução silenciosa (verbose=False).
"""

import numpy as np
from codigos import ajustecurvas as ac


def test_calcula_chi_e_r2_perfect_linear():
    """Verifica que métricas (Desvio, Chi², R²) indicam ajuste perfeito para reta exata."""
    x = np.array([0.0, 1.0, 2.0])
    y = 1.0 + 2.0 * x  # y = 2x + 1
    stats = ac.calcula_chi_e_r2(x, y, b0=1.0, b1=2.0, n_params=2, verbose=False)
    assert abs(stats['Desvio']) < 1e-12
    assert abs(stats['Chi2']) < 1e-12
    assert abs(stats['R2'] - 1.0) < 1e-12


def test_minquadrados_coefficients():
    """Verifica que o cálculo de coeficientes por fórmula produz R² ≈ 1 em dados perfeitos."""
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = 1.0 + 2.0 * x
    n = len(x)
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_xy = np.sum(x * y)
    sum_x2 = np.sum(x ** 2)
    b1 = (sum_x * sum_y - n * sum_xy) / ((sum_x) ** 2 - n * sum_x2)
    b0 = (sum_y - b1 * sum_x) / n

    stats = ac.calcula_chi_e_r2(x, y, b0=b0, b1=b1, verbose=False)
    assert abs(stats['R2'] - 1.0) < 1e-12


def test_tabela_minimos_quadrados_runs_without_error():
    """Garante que a função de impressão de tabela não lança exceções (modo silencioso)."""
    x = np.array([0.0, 1.0, 2.0])
    y = np.array([1.0, 3.0, 5.0])
    ac.tabela_minimos_quadrados(x, y, verbose=False)


def test_minquadrados_ordem_n_quadratic():
    """Ajuste polinomial de ordem 2 recupera coeficientes exatos em dados sintéticos."""
    x = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    y = 1.0 + 2.0 * x + 3.0 * (x ** 2)
    coef = ac.minquadrados_ordem_n(x, y, ordem=2, tabela=False, grafico=False, verbose=False)
    assert coef is not None
    assert abs(coef[0] - 1.0) < 1e-8
    assert abs(coef[1] - 2.0) < 1e-8
    assert abs(coef[2] - 3.0) < 1e-8


def test_minquadrados_ordem_n_linear():
    """Ajuste linear recupera coeficientes exatos em dados sintéticos."""
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = 1.0 + 2.0 * x
    coef = ac.minquadrados_ordem_n(x, y, ordem=1, tabela=False, grafico=False, verbose=False)
    assert coef is not None
    assert abs(coef[0] - 1.0) < 1e-10
    assert abs(coef[1] - 2.0) < 1e-10


def test_minquadrados_ordem_n_cubic():
    """Ajuste cúbico recupera coeficientes exatos em dados sintéticos."""
    x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    y = 1.0 + 2.0 * x + 3.0 * (x ** 2) + 4.0 * (x ** 3)
    coef = ac.minquadrados_ordem_n(x, y, ordem=3, tabela=False, grafico=False, verbose=False)
    assert coef is not None
    assert abs(coef[0] - 1.0) < 1e-6
    assert abs(coef[1] - 2.0) < 1e-6
    assert abs(coef[2] - 3.0) < 1e-6
    assert abs(coef[3] - 4.0) < 1e-6


def test_calcula_chi_e_r2_imperfect_fit():
    """Dados não perfeitos devem resultar em R² < 1 e Chi² > 0."""
    x = np.array([0.0, 1.0, 2.0])
    y = np.array([1.0, 3.1, 5.2])
    stats = ac.calcula_chi_e_r2(x, y, b0=1.0, b1=2.0, n_params=2, verbose=False)
    assert stats['R2'] < 1.0 
    assert stats['Chi2'] > 0


def test_minquadrados_silent():
    """Verifica que minquadrados executa sem imprimir em modo silencioso."""
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = 1.0 + 2.0 * x
    ac.minquadrados(x, y, verbose=False, tabela=False, grafico=False)


def test_input_validation_errors():
    """Valida que validações de entrada levantam erros apropriados."""
    import pytest
    
    with pytest.raises(ValueError, match="x e y devem ter o mesmo comprimento"):
        ac._validate_curve_fitting_inputs([1, 2], [1, 2, 3])
    
    with pytest.raises(ValueError, match="São necessários pelo menos 2 pontos para ajuste de curvas"):
        ac._validate_curve_fitting_inputs([1], [1])


def test_minquadrados_height_weight_dataset():
    """Exemplo prático: ajuste de altura x peso (aceita execução sem exceção)."""
    x = np.array([183, 173, 168, 188, 158, 163, 193, 163, 178])
    y = np.array([79, 69, 70, 81, 61, 63, 79, 71, 73])
    
    ac.minquadrados(x, y, verbose=False, tabela=False, grafico=False)


def test_minquadrados_linear_dataset_7_points():
    """Valida execução em conjunto de 7 pontos (no-throw)."""
    x = np.array([1, 2, 3, 4, 5, 6, 7])
    y = np.array([0.5, 0.6, 0.9, 0.8, 1.2, 1.5, 1.7])

    ac.minquadrados(x, y, verbose=False, tabela=False, grafico=False)


def test_minquadrados_linear_dataset_8_points():
    """Valida execução em conjunto de 8 pontos (no-throw)."""
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    y = np.array([0.5, 0.6, 0.9, 0.8, 1.2, 1.5, 1.7, 2.0])
    
    ac.minquadrados(x, y, verbose=False, tabela=False, grafico=False)


def test_minquadrados_linear_dataset_10_points():
    """Valida execução em conjunto de 10 pontos (no-throw)."""
    x = np.array([0, 2, 4, 6, 9, 11, 12, 15, 17, 19])
    y = np.array([5, 6, 7, 6, 9, 8, 7, 10, 12, 12])
    
    ac.minquadrados(x, y, verbose=False, tabela=False, grafico=False)


def test_minquadrados_negative_slope_dataset():
    """Valida execução para conjunto com declive negativo (no-throw)."""
    x = np.array([1.4, 2.1, 3.0, 4.4])
    y = np.array([4.2, 2.3, 1.9, 1.1])
    
    ac.minquadrados(x, y, verbose=False, tabela=False, grafico=False)


def test_minquadrados_ordem_n_quadratic_user_example():
    """Ajuste polinomial de ordem n em exemplo fornecido pelo usuário."""
    x = np.array([-3, -1, 1, 2, 3])
    y = np.array([-1, 0, 1, 1, -1])
    
    coef = ac.minquadrados_ordem_n(x, y, ordem=2, tabela=False, grafico=False, verbose=False)
    assert coef is not None
    assert len(coef) == 3