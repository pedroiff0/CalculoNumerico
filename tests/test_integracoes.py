from codigos import integracoes as ig
import pytest


def test_erro_truncamento_composta():
    a, b = 0.0, 1.0
    # derivada_max = 1 for testing
    assert abs(ig.erro_truncamento_composta(a, b, 1, 1.0, 'trapezio') - (-1/12)) < 1e-12
    assert abs(ig.erro_truncamento_composta(a, b, 1, 1.0, 'simpson13') - (-(1**5)/180)) < 1e-12
    assert abs(ig.erro_truncamento_composta(a, b, 1, 1.0, 'simpson38') - (-(1**5)/80)) < 1e-12


def test_trapezio_composta_simple(monkeypatch):
    # Integral of f(x)=x from 0 to 1 is 0.5
    monkeypatch.setattr(ig, 'pedir_m_ou_h', lambda a, b, regra: (10, (b-a)/10))
    # avoid interactive plotting and error estimation: patch input to always 'n'
    monkeypatch.setattr('builtins.input', lambda *args, **kwargs: 'n')
    res = ig.trapezio_composta('x', 0.0, 1.0)
    assert abs(res - 0.5) < 1e-3


def test_erro_truncamento_composta_values():
    # For trapezio with derivada_max = 1 on [0,1], m=10 -> formula: -((b-a)^3)/(12*m^2)*derivada_max
    a, b, m, derivada_max = 0.0, 1.0, 10, 1.0
    expected = -((b-a)**3) / (12 * m**2) * derivada_max
    assert pytest.approx(ig.erro_truncamento_composta(a, b, m, derivada_max, 'trapezio')) == expected
    # Simpson 1/3
    expected_s13 = -((b-a)**5) / (180 * m**4) * derivada_max
    assert pytest.approx(ig.erro_truncamento_composta(a, b, m, derivada_max, 'simpson13')) == expected_s13
    # Simpson 3/8
    expected_s38 = -((b-a)**5) / (80 * m**4) * derivada_max
    assert pytest.approx(ig.erro_truncamento_composta(a, b, m, derivada_max, 'simpson38')) == expected_s38


def test_newton_cotes_trapezio_linear(monkeypatch):
    # Prevent interactive plotting prompt
    monkeypatch.setattr('builtins.input', lambda prompt='': 'n')
    # integral of x from 0 to 1 = 0.5
    res = ig.newton_cotes('x', 0.0, 1.0, 1)
    assert pytest.approx(res, rel=1e-12) == 0.5


def test_newton_cotes_simpson_on_quadratic(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda prompt='': 'n')
    # integral of x**2 from 0 to 1 = 1/3
    res = ig.newton_cotes('x**2', 0.0, 1.0, 2)
    assert pytest.approx(res, rel=1e-12) == 1.0/3.0


def test_trapezio_composta_monkeypatch(monkeypatch):
    # Make pedir_m_ou_h return m=4, h=0.25 for interval 0..1
    monkeypatch.setattr(ig, 'pedir_m_ou_h', lambda a, b, regra: (4, 0.25))
    # Prevent interactive plotting/error prompts (always 'n')
    monkeypatch.setattr('builtins.input', lambda prompt='': 'n')
    res = ig.trapezio_composta('x', 0.0, 1.0)
    assert pytest.approx(res, rel=1e-12) == 0.5


def test_simpson_1_3_composta_monkeypatch(monkeypatch):
    # m must be even; choose m=4
    monkeypatch.setattr(ig, 'pedir_m_ou_h', lambda a, b, regra: (4, 0.25))
    monkeypatch.setattr('builtins.input', lambda prompt='': 'n')
    res = ig.simpson_1_3_composta('x**2', 0.0, 1.0)
    assert pytest.approx(res, rel=1e-12) == 1.0/3.0


def test_simpson_3_8_composta_monkeypatch(monkeypatch):
    # m must be multiple of 3; choose m=3
    monkeypatch.setattr(ig, 'pedir_m_ou_h', lambda a, b, regra: (3, (1.0/3.0)))
    monkeypatch.setattr('builtins.input', lambda prompt='': 'n')
    res = ig.simpson_3_8_composta('x**3', 0.0, 1.0)
    # integral of x^3 from 0 to1 = 1/4
    assert pytest.approx(res, rel=1e-12) == 0.25
