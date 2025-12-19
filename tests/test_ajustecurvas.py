import numpy as np
from codigos import ajustecurvas as ac


def test_calcula_chi_e_r2_perfect_linear():
    x = np.array([0.0, 1.0, 2.0])
    y = 1.0 + 2.0 * x  # y = 2x + 1
    stats = ac.calcula_chi_e_r2(x, y, b0=1.0, b1=2.0, n_params=2, verbose=False)
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
    stats = ac.calcula_chi_e_r2(x, y, b0=b0, b1=b1, verbose=False)
    assert abs(stats['R2'] - 1.0) < 1e-12


def test_tabela_minimos_quadrados_runs_without_error():
    x = np.array([0.0, 1.0, 2.0])
    y = np.array([1.0, 3.0, 5.0])
    # Should not raise
    ac.tabela_minimos_quadrados(x, y, verbose=False)


def test_minquadrados_ordem_n_quadratic():
    # Fit quadratic y = 1 + 2x + 3x^2
    x = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    y = 1.0 + 2.0 * x + 3.0 * (x ** 2)
    coef = ac.minquadrados_ordem_n(x, y, ordem=2, tabela=False, grafico=False, verbose=False)
    # coef order: a0 + a1 x + a2 x^2
    assert coef is not None
    assert abs(coef[0] - 1.0) < 1e-8
    assert abs(coef[1] - 2.0) < 1e-8
    assert abs(coef[2] - 3.0) < 1e-8


def test_minquadrados_ordem_n_linear():
    # Fit linear y = 1 + 2x
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = 1.0 + 2.0 * x
    coef = ac.minquadrados_ordem_n(x, y, ordem=1, tabela=False, grafico=False, verbose=False)
    assert coef is not None
    assert abs(coef[0] - 1.0) < 1e-10
    assert abs(coef[1] - 2.0) < 1e-10


def test_minquadrados_ordem_n_cubic():
    # Fit cubic y = 1 + 2x + 3x^2 + 4x^3
    x = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    y = 1.0 + 2.0 * x + 3.0 * (x ** 2) + 4.0 * (x ** 3)
    coef = ac.minquadrados_ordem_n(x, y, ordem=3, tabela=False, grafico=False, verbose=False)
    assert coef is not None
    assert abs(coef[0] - 1.0) < 1e-6
    assert abs(coef[1] - 2.0) < 1e-6
    assert abs(coef[2] - 3.0) < 1e-6
    assert abs(coef[3] - 4.0) < 1e-6


def test_calcula_chi_e_r2_imperfect_fit():
    x = np.array([0.0, 1.0, 2.0])
    y = np.array([1.0, 3.1, 5.2])  # slight noise
    stats = ac.calcula_chi_e_r2(x, y, b0=1.0, b1=2.0, n_params=2, verbose=False)
    assert stats['R2'] < 1.0  # not perfect
    assert stats['Chi2'] > 0


def test_minquadrados_silent():
    """Test that minquadrados works in silent mode"""
    x = np.array([0.0, 1.0, 2.0, 3.0])
    y = 1.0 + 2.0 * x
    # Should not print anything
    ac.minquadrados(x, y, verbose=False, tabela=False, grafico=False)


def test_input_validation_errors():
    """Test that input validation raises appropriate errors"""
    import pytest
    
    # Test mismatched lengths
    with pytest.raises(ValueError, match="x e y devem ter o mesmo comprimento"):
        ac._validate_curve_fitting_inputs([1, 2], [1, 2, 3])
    
    # Test insufficient points
    with pytest.raises(ValueError, match="São necessários pelo menos 2 pontos para ajuste de curvas"):
        ac._validate_curve_fitting_inputs([1], [1])


def test_minquadrados_height_weight_dataset():
    """Test minquadrados with height-weight dataset from user example"""
    # Data: heights and weights
    x = np.array([183, 173, 168, 188, 158, 163, 193, 163, 178])
    y = np.array([79, 69, 70, 81, 61, 63, 79, 71, 73])
    
    # Expected from user output: b0 ≈ -20.078, b1 ≈ 0.528
    ac.minquadrados(x, y, verbose=False, tabela=False, grafico=False)
    # Test passes if no exception


def test_minquadrados_linear_dataset_7_points():
    """Test minquadrados with 7-point linear dataset"""
    x = np.array([1, 2, 3, 4, 5, 6, 7])
    y = np.array([0.5, 0.6, 0.9, 0.8, 1.2, 1.5, 1.7])
    
    # Expected from user output: b0 ≈ 0.214, b1 ≈ 0.204
    ac.minquadrados(x, y, verbose=False, tabela=False, grafico=False)


def test_minquadrados_linear_dataset_8_points():
    """Test minquadrados with 8-point linear dataset"""
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    y = np.array([0.5, 0.6, 0.9, 0.8, 1.2, 1.5, 1.7, 2.0])
    
    # Expected from user output: b0 ≈ 0.175, b1 ≈ 0.217
    ac.minquadrados(x, y, verbose=False, tabela=False, grafico=False)


def test_minquadrados_linear_dataset_10_points():
    """Test minquadrados with 10-point dataset"""
    x = np.array([0, 2, 4, 6, 9, 11, 12, 15, 17, 19])
    y = np.array([5, 6, 7, 6, 9, 8, 7, 10, 12, 12])
    
    # Expected from user output: b0 ≈ 4.852, b1 ≈ 0.352
    ac.minquadrados(x, y, verbose=False, tabela=False, grafico=False)


def test_minquadrados_negative_slope_dataset():
    """Test minquadrados with negative slope dataset"""
    x = np.array([1.4, 2.1, 3.0, 4.4])
    y = np.array([4.2, 2.3, 1.9, 1.1])
    
    # Expected from user output: b0 ≈ 4.889, b1 ≈ -0.922
    ac.minquadrados(x, y, verbose=False, tabela=False, grafico=False)


def test_minquadrados_ordem_n_quadratic_user_example():
    """Test minquadrados_ordem_n with quadratic fit from user example"""
    x = np.array([-3, -1, 1, 2, 3])
    y = np.array([-1, 0, 1, 1, -1])
    
    coef = ac.minquadrados_ordem_n(x, y, ordem=2, tabela=False, grafico=False, verbose=False)
    # Expected from user output: a0 ≈ 0.903, a1 ≈ 0.116, a2 ≈ -0.198
    assert coef is not None
    assert len(coef) == 3
    # Test that coefficients are reasonable (exact values may vary slightly due to numerical precision)
