from codigos import interpolacoes


def test_tabela_diferencas_divididas_and_newton():
    x = [0.0, 1.0, 2.0]
    y = [0.0, 1.0, 4.0]  # f(x) = x^2
    tabela = interpolacoes.tabela_diferencas_divididas(x, y)
    assert tabela[0] == y
    assert len(tabela) == 3
    # avaliar polinômio de Newton em xp = 1.5 -> 2.25
    val = interpolacoes.newton_dif_divididas(x, tabela, 1.5)
    assert abs(val - 2.25) < 1e-12


def test_lagrange_interpol():
    x = [0.0, 1.0, 2.0]
    y = [0.0, 1.0, 4.0]
    val = interpolacoes.lagrange_interpol(x, y, 1.5)
    assert abs(val - 2.25) < 1e-12


def test_tabela_diferencas_finitas_and_gregory():
    x = [0.0, 1.0, 2.0]
    y = [0.0, 1.0, 4.0]  # y = x^2
    tabela = interpolacoes.tabela_diferencas_finitas(y)
    # tabela[0] == y, tabela[1] == [1,3], tabela[2] == [2]
    assert tabela[0] == y
    assert tabela[1] == [1.0, 3.0]
    assert tabela[2] == [2.0]
    # Gregory-Newton on equally spaced nodes should give same result at 1.5
    val = interpolacoes.gregory_newton_progressivo(x, y, 1.5)
    assert abs(val - 2.25) < 1e-12


def test_dispositivo_pratico_lagrange():
    x = [0.0, 1.0, 2.0]
    y = [0.0, 1.0, 4.0]
    val = interpolacoes.dispositivo_pratico_lagrange(x, y, 1.5)
    assert abs(val - 2.25) < 1e-12


def test_verifica_espaçamento_uniforme_and_calcular_erro():
    x = [0.0, 1.0, 2.0]
    ok, h = interpolacoes.verifica_espaçamento_uniforme(x)
    assert ok and abs(h - 1.0) < 1e-12
    # calcular_erro with x^2 and degree 2 -> derivative of order 3 is zero -> error 0
    erro_trunc, _ = interpolacoes.calcular_erro('x**2', x, 1.5, 2, 2.25)
    assert erro_trunc == 0 or abs(erro_trunc) < 1e-14
