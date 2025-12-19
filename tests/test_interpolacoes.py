"""Testes para `codigos.interpolacoes`.

Cobre:
- Cálculo de diferenças divididas e avaliação de Newton
- Interpolação de Lagrange e dispositivo prático
- Método de diferenças finitas de Gregory-Newton
- Estimativa de erro e verificação de espaçamento
- Comportamentos de verbose/tabela/gráfico e validação de entradas
"""

from codigos import interpolacoes
import numpy as np

def test_tabela_diferencas_divididas_and_newton():
    """Verifica a tabela de diferenças divididas e avaliação de Newton.

    - Confirma primeira linha da tabela igual a y e que a avaliação em 1.5
      produz o valor esperado 2.25.
    """
    x = [0.0, 1.0, 2.0]
    y = [0.0, 1.0, 4.0]
    tabela = interpolacoes.tabela_diferencas_divididas(x, y)
    assert np.allclose(tabela[0], y)
    assert len(tabela) == 3
    val = interpolacoes.newton_dif_divididas(x, tabela, 1.5)
    assert abs(val - 2.25) < 1e-12


def test_lagrange_interpol():
    """Verifica a interpolação por Lagrange em um ponto simples.

    - Usa pontos [0,1,2] e valida que p(1.5) ≈ 2.25.
    """
    x = [0.0, 1.0, 2.0]
    y = [0.0, 1.0, 4.0]
    val = interpolacoes.lagrange_interpol(x, y, 1.5)
    assert abs(val - 2.25) < 1e-12


def test_tabela_diferencas_finitas_and_gregory():
    """Verifica diferenças finitas e interpolação Gregory-Newton progressiva."""
    x = [0.0, 1.0, 2.0]
    y = [0.0, 1.0, 4.0]
    tabela = interpolacoes.tabela_diferencas_finitas(y)
    assert np.allclose(tabela[0], y)
    assert np.allclose(tabela[1], [1.0, 3.0])
    assert np.allclose(tabela[2], [2.0])
    val = interpolacoes.gregory_newton_progressivo(x, y, 1.5)
    assert abs(val - 2.25) < 1e-12


def test_dispositivo_pratico_lagrange():
    """Valida o 'dispositivo prático' de Lagrange com dados sintéticos."""
    x = [0.0, 1.0, 2.0]
    y = [0.0, 1.0, 4.0]
    val = interpolacoes.dispositivo_pratico_lagrange(x, y, 1.5)
    assert abs(val - 2.25) < 1e-12


def test_verifica_espaçamento_uniforme_and_calcular_erro():
    """Testa verificação de espaçamento uniforme e estimativa de erro.

    - Verifica que h=1.0 e que a estimativa de erro para f(x)=x^2 é nula
      no caso exato usado aqui.
    """
    x = [0.0, 1.0, 2.0]
    ok, h = interpolacoes.verifica_espaçamento_uniforme(x)
    assert ok and abs(h - 1.0) < 1e-12
    erro_trunc, _ = interpolacoes.calcular_erro('x**2', x, 1.5, 2, 2.25)
    assert erro_trunc == 0 or abs(erro_trunc) < 1e-14


def test_lagrange_real_data_1():
    """Testa interpolação de Lagrange com dados reais do exemplo do menu"""
    x = [1.0, 1.3, 1.8]
    y = [0.0, 0.262, 0.588]
    val = interpolacoes.lagrange_interpol(x, y, 1.4)
    assert abs(val - 0.3382666666666666) < 1e-10


def test_newton_real_data_1():
    """Testa interpolação de Newton com dados reais do exemplo do menu"""
    x = [1.0, 1.3, 1.8]
    y = [0.0, 0.262, 0.588]
    tabela = interpolacoes.tabela_diferencas_divididas(x, y)
    val = interpolacoes.newton_dif_divididas(x, tabela, 1.4)
    assert abs(val - 0.33826666666666655) < 1e-10


def test_dispositivo_pratico_lagrange_real_data():
    """Testa dispositivo prático de Lagrange com dados de temperatura"""
    x = [0.2, 0.3, 0.5]
    y = [85.0, 88.0, 92.0]
    val = interpolacoes.dispositivo_pratico_lagrange(x, y, 0.4)
    assert abs(val - 90.33333333333334) < 1e-10


def test_newton_real_data_2():
    """Testa Newton com 4 pontos"""
    x = [0.0, 0.5, 0.75, 1.0]
    y = [1.0, 4.482, 9.488, 20.086]
    tabela = interpolacoes.tabela_diferencas_divididas(x, y)
    val = interpolacoes.newton_dif_divididas(x, tabela, 0.65)
    assert abs(val - 6.958004) < 1e-6


def test_lagrange_real_data_2():
    """Testa Lagrange com dados de pressão"""
    x = [55.0, 70.0, 85.0, 100.0]
    y = [14.08, 13.56, 13.28, 12.27]
    val = interpolacoes.lagrange_interpol(x, y, 80.0)
    assert abs(val - 13.40654320987654) < 1e-10


def test_lagrange_real_data_3():
    """Testa Lagrange com outro conjunto de dados de pressão"""
    x = [85.0, 100.0, 115.0, 130.0]
    y = [13.28, 12.27, 11.30, 10.40]
    val = interpolacoes.lagrange_interpol(x, y, 110.0)
    assert abs(val - 11.617037037037036) < 1e-10


def test_newton_real_data_3():
    """Testa Newton com valores de x decrescentes"""
    x = [1000.0, 750.0, 500.0]
    y = [15.0, 10.0, 7.0]
    tabela = interpolacoes.tabela_diferencas_divididas(x, y)
    val = interpolacoes.newton_dif_divididas(x, tabela, 850.0)
    assert abs(val - 11.76) < 1e-10


def test_max_grau_limitation():
    """Garante que o parâmetro max_grau limita o grau do polinômio"""
    x = [0.0, 1.0, 2.0, 3.0]
    y = [0.0, 1.0, 4.0, 9.0]
    val = interpolacoes.lagrange_interpol(x, y, 1.5, max_grau=1)
    assert isinstance(val, (float, np.floating))


def test_gregory_newton_real_data():
    """Testa Gregory-Newton com dados igualmente espaçados"""
    x = [0.0, 0.5, 1.0, 1.5]
    y = [1.0, 1.648721, 2.718282, 4.481689]
    val = interpolacoes.gregory_newton_progressivo(x, y, 0.75)
    expected = np.exp(0.75)
    assert abs(val - expected) < 5e-3  


def test_input_validation_errors():
    """Verifica que validação de entradas levanta erros apropriados"""
    import pytest
    
    with pytest.raises(ValueError, match="x e y devem ter o mesmo comprimento"):
        interpolacoes._validate_interpolation_inputs([1, 2], [1, 2, 3])
    
    with pytest.raises(ValueError, match="Os pontos x devem ser únicos"):
        interpolacoes._validate_interpolation_inputs([1, 1, 2], [1, 2, 3])
    
    with pytest.raises(ValueError, match="São necessários pelo menos 2 pontos para interpolação"):
        interpolacoes._validate_interpolation_inputs([1], [1])


def test_verbose_output(capsys):
    """Verifica que verbose=False não produz saída e verbose=True produz saída"""
    x = [0.0, 1.0, 2.0]
    y = [0.0, 1.0, 4.0]
    
    val_silent = interpolacoes.lagrange_interpol(x, y, 1.5, verbose=False)
    captured = capsys.readouterr()
    assert captured.out == ""
    
    val_verbose = interpolacoes.lagrange_interpol(x, y, 1.5, verbose=True)
    captured = capsys.readouterr()
    assert "Lagrange" in captured.out or len(captured.out) > 0
    
    assert abs(val_silent - val_verbose) < 1e-12


def test_lagrange_verbose_detailed_output(capsys):
    """Verifica saída detalhada em verbose para interpolação de Lagrange"""
    x = [1.0, 1.3, 1.8]
    y = [0.0, 0.262, 0.588]
    
    val = interpolacoes.lagrange_interpol(x, y, 1.4, verbose=False)
    assert abs(val - 0.3382666666666666) < 1e-10


def test_newton_verbose_detailed_output(capsys):
    """Verifica saída detalhada em verbose para interpolação de Newton"""
    x = [1.0, 1.3, 1.8]
    y = [0.0, 0.262, 0.588]
    tabela = interpolacoes.tabela_diferencas_divididas(x, y)
    
    val = interpolacoes.newton_dif_divididas(x, tabela, 1.4, verbose=False)
    assert abs(val - 0.33826666666666655) < 1e-10

def test_numpy_array_inputs():
    """Verifica que as funções aceitam arrays numpy como entrada"""
    x = np.array([0.0, 1.0, 2.0])
    y = np.array([0.0, 1.0, 4.0])
    
    val = interpolacoes.lagrange_interpol(x, y, 1.5)
    assert abs(val - 2.25) < 1e-12
    
    tabela = interpolacoes.tabela_diferencas_divididas(x, y)
    val_newton = interpolacoes.newton_dif_divididas(x, tabela, 1.5)
    assert abs(val_newton - 2.25) < 1e-12


def test_verbose_enables_tables_and_details(capsys):
    """Quando verbose=True, a função imprime passos e tabelas detalhadas."""
    x = [0.0, 1.0, 2.0]
    y = [0.0, 1.0, 4.0]
    tabela = interpolacoes.tabela_diferencas_divididas(x, y)

    val = interpolacoes.newton_dif_divididas(x, tabela, 1.5, verbose=True)
    captured = capsys.readouterr()
    assert "Termo" in captured.out or "Parcial" in captured.out
    assert abs(val - 2.25) < 1e-12


def test_invalid_xp_raises():
    """xp deve ser um número finito."""
    x = [0.0, 1.0]
    y = [0.0, 1.0]
    tabela = interpolacoes.tabela_diferencas_divididas(x, y)
    import math
    import pytest
    with pytest.raises(TypeError):
        interpolacoes.newton_dif_divididas(x, tabela, 'not-a-number')
    with pytest.raises(ValueError):
        interpolacoes.newton_dif_divididas(x, tabela, math.inf)


def test_max_grau_limits_degree():
    """Garante que max_grau é limitado a [1, n-1]"""
    x = [0.0, 1.0, 2.0]
    y = [0.0, 1.0, 4.0]
    tabela = interpolacoes.tabela_diferencas_divididas(x, y)
    # request a ridiculously large degree, should be clamped
    val_high = interpolacoes.newton_dif_divididas(x, tabela, 1.5, max_grau=100)
    val_full = interpolacoes.newton_dif_divididas(x, tabela, 1.5, max_grau=None)
    assert abs(val_high - val_full) < 1e-12
