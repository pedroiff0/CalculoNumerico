"""Testes para o módulo `codigos.raizes`.

- Bisseção: validade do intervalo, comportamento em intervalos inválidos e saída em verbose
- Newton: convergência básica e comportamento quando a derivada é nula
- Secante: convergência básica
- `pedir_dados_raizes`: valida leitura de parâmetros no modo de menu
"""

import math
from codigos import raizes

def test_bissecao_basic():
    """Verifica a convergência básica do método da bisseção.

    - Função: f(x) = x**2 - 4
    - Intervalo: [0, 3]
    - Critério: raiz aproximada ~ 2.0 dentro da tolerância fornecida e >0 iterações
    """
    raiz, iters = raizes.bissecao('x**2 - 4', 0.0, 3.0, 1e-8, 100)
    assert raiz is not None
    assert abs(raiz - 2.0) < 1e-8
    assert iters > 0

def test_bissecao_invalid_interval():
    """Confirma que bisseção detecta intervalo inválido (mesmo sinal em extremidades).

    - Função: f(x) = x**2 + 1 (sempre positiva)
    - Intervalo: [-1, 1]
    - Resultado esperado: (None, 0) e mensagem de erro
    """
    raiz, iters = raizes.bissecao('x**2 + 1', -1.0, 1.0, 1e-8, 10)
    assert raiz is None
    assert iters == 0

def test_newton_basic():
    """Verifica convergência do método de Newton-Raphson para raiz sqrt(2).

    - Função: f(x) = x**2 - 2
    - Chute: x0 = 1.5
    - Critério: aproxima sqrt(2) dentro do limiar pedido
    """
    raiz, iters = raizes.newton('x**2 - 2', 1.5, 1e-12, 50)
    assert raiz is not None
    assert abs(raiz - math.sqrt(2.0)) < 1e-10

def test_newton_derivative_zero():
    """Testa o comportamento de Newton quando a derivada é zero no ponto inicial.

    - Função: f(x) = x**3, chute x0 = 0 (derivada nula)
    - Aceita-se raiz 0.0 como comportamento válido (método pode retornar None ou a raiz)
    """
    raiz, iters = raizes.newton('x**3', 0.0, 1e-12, 10)
    assert raiz is not None
    assert abs(raiz - 0.0) < 1e-12

def test_secante_basic():
    """Verifica que o método da secante convergente para uma raiz em (0,1).

    - Função: f(x) = x**3 - 0.5
    - Chutes: x0 = 0.0, x1 = 1.0
    - Verifica resíduo pequeno em função da raiz encontrada
    """
    raiz, iters = raizes.secante('x**3 - 0.5', 0.0, 1.0, 1e-10, 100)
    assert raiz is not None
    # verify residual is small
    fval = (raiz**3 - 0.5)
    assert abs(fval) < 1e-8

def test_pedir_dados_raizes_for_menu(monkeypatch):
    """Simula a leitura de parâmetros no modo de menu para a bisseção.

    - Garante que os valores retornados pelo helper sejam corretamente tipados e ordenados
    """
    # Simulate inputs for bissecao: func, tol, max_iter, a, b
    inputs = iter(['x**2 - 4', '1e-8', '100', '0', '3'])
    monkeypatch.setattr('builtins.input', lambda prompt='': next(inputs))
    func_str, tol, max_iter, params = raizes.pedir_dados_raizes('bissecao')
    assert func_str == 'x**2 - 4'
    assert abs(float(tol) - 1e-8) < 1e-20
    assert int(max_iter) == 100
    assert params == (0.0, 3.0)

def test_plotar_funcao_grafico_false(monkeypatch):
    called = {"show": False}
    monkeypatch.setattr('matplotlib.pyplot.show', lambda: called.__setitem__('show', True))
    raizes.plotar_funcao('x**2 - 4', a=-1, b=3, grafico=False)
    assert called['show'] is False


def test_plotar_funcao_grafico_true(monkeypatch):
    called = {"show": False}
    monkeypatch.setattr('matplotlib.pyplot.show', lambda: called.__setitem__('show', True))
    raizes.plotar_funcao('x**2 - 4', a=-1, b=3, grafico=True)
    assert called['show'] is True


def test_bissecao_with_verbose():
    raiz, iters = raizes.bissecao('x**2 - 4', 0.0, 3.0, 1e-8, 100, verbose=True)
    assert raiz is not None
    assert abs(raiz - 2.0) < 1e-8
    assert iters > 0

def test_plotar_funcao_grafico_false(monkeypatch):
    """Garante que `plotar_funcao(..., grafico=False)` não chama `plt.show()`.

    - Substitui `plt.show` por stub e verifica que não foi invocado
    """
    called = {"show": False}
    monkeypatch.setattr('matplotlib.pyplot.show', lambda: called.__setitem__('show', True))
    # Deve retornar sem chamar show
    raizes.plotar_funcao('x**2 - 4', a=-1, b=3, grafico=False)
    assert called['show'] is False


def test_plotar_funcao_grafico_true(monkeypatch):
    """Garante que `plotar_funcao(..., grafico=True)` chama `plt.show()`.

    - Substitui `plt.show` e verifica invocação para gráficos ativos
    """
    called = {"show": False}
    monkeypatch.setattr('matplotlib.pyplot.show', lambda: called.__setitem__('show', True))
    raizes.plotar_funcao('x**2 - 4', a=-1, b=3, grafico=True)
    assert called['show'] is True


def test_bissecao_with_verbose():
    """Verifica que `bissecao` funciona corretamente em modo `verbose`.

    - Assegura que a execução verbose não altera a solução encontrada
    """
    raiz, iters = raizes.bissecao('x**2 - 4', 0.0, 3.0, 1e-8, 100, verbose=True)
    assert raiz is not None
    assert abs(raiz - 2.0) < 1e-8
    assert iters > 0
