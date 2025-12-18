from codigos import integracoes


def test_erro_truncamento_composta():
    a, b = 0.0, 1.0
    # derivada_max = 1 for testing
    assert abs(integracoes.erro_truncamento_composta(a, b, 1, 1.0, 'trapezio') - (-1/12)) < 1e-12
    assert abs(integracoes.erro_truncamento_composta(a, b, 1, 1.0, 'simpson13') - (-(1**5)/180)) < 1e-12
    assert abs(integracoes.erro_truncamento_composta(a, b, 1, 1.0, 'simpson38') - (-(1**5)/80)) < 1e-12


def test_trapezio_composta_simple(monkeypatch):
    # Integral of f(x)=x from 0 to 1 is 0.5
    monkeypatch.setattr(integracoes, 'pedir_m_ou_h', lambda a, b, regra: (10, (b-a)/10))
    # avoid interactive plotting and error estimation: patch input to always 'n'
    monkeypatch.setattr('builtins.input', lambda *args, **kwargs: 'n')
    res = integracoes.trapezio_composta('x', 0.0, 1.0)
    assert abs(res - 0.5) < 1e-3
