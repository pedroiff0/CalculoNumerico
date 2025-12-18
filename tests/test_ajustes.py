from codigos import ajustecurvasv2 as ajustecurvas
import numpy as np


def test_calcula_chi_e_r2_perfect_linear():
    x = np.array([0.0, 1.0, 2.0])
    y = 1.0 + 2.0 * x  # y = 2x + 1
    stats = ajustecurvas.calcula_chi_e_r2(x, y, b0=1.0, b1=2.0, n_params=2)
    assert abs(stats['Desvio']) < 1e-12
    assert abs(stats['Chi2']) < 1e-12
    assert abs(stats['R2'] - 1.0) < 1e-12
