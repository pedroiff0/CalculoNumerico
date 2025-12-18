import math
from codigos import raizes
import pytest

def test_bissecao_basic():
    raiz, iters = raizes.bissecao('x**2 - 4', 0.0, 3.0, 1e-8, 100)
    assert raiz is not None
    assert abs(raiz - 2.0) < 1e-8
    assert iters > 0

def test_bissecao_invalid_interval():
    raiz, iters = raizes.bissecao('x**2 + 1', -1.0, 1.0, 1e-8, 10)
    assert raiz is None
    assert iters == 0

def test_newton_basic():
    raiz, iters = raizes.newton('x**2 - 2', 1.5, 1e-12, 50)
    assert raiz is not None
    assert abs(raiz - math.sqrt(2.0)) < 1e-10

def test_newton_derivative_zero():
    # f(x) = x^3 at x=0 has derivative = 0; finite-difference may yield tiny derivative,
    # but the method should produce a root (x=0) or None; accept 0.0 as valid root here.
    raiz, iters = raizes.newton('x**3', 0.0, 1e-12, 10)
    assert raiz is not None
    assert abs(raiz - 0.0) < 1e-12

def test_secante_basic():
    raiz, iters = raizes.secante('x**3 - 0.5', 0.0, 1.0, 1e-10, 100)
    assert raiz is not None
    # verify residual is small
    fval = (raiz**3 - 0.5)
    assert abs(fval) < 1e-8

def test_pedir_dados_raizes_for_menu(monkeypatch):
    # Simulate inputs for bissecao: func, tol, max_iter, a, b
    inputs = iter(['x**2 - 4', '1e-8', '100', '0', '3'])
    monkeypatch.setattr('builtins.input', lambda prompt='': next(inputs))
    func_str, tol, max_iter, params = raizes.pedir_dados_raizes('bissecao')
    assert func_str == 'x**2 - 4'
    assert abs(float(tol) - 1e-8) < 1e-20
    assert int(max_iter) == 100
    assert params == (0.0, 3.0)