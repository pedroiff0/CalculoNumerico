"""
Módulo para métodos de integração numérica.

Este módulo implementa algoritmos de integração numérica:
Regra dos trapézios, Simpson 1/3 e suas versões repetidas.

Author: Pedro Henrique Rocha de Andrade
Date: Dezembro 2025
"""

import math
import numpy as np
from sympy import symbols, integrate, sympify, diff, lambdify
from sympy import sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, exp, sqrt, log, Abs, pi, E
import matplotlib.pyplot as plt
from .constants import SYMPY_LOCALS


def plotar_funcoes(funcs, a, b, pontos=400):
    """Plota uma ou várias funções simbólicas no intervalo [a, b].

    Parameters
    ----------
    funcs : str
        String com expressões separadas por vírgula (ex.: ``'sin(x), cos(x)'``).
    a, b : float
        Limites do intervalo de plotagem.
    pontos : int, optional
        Número de pontos no eixo x usados para amostragem (padrão: 400).
    """
    x = symbols('x')
    lista = [f.strip() for f in funcs.split(',') if f.strip()]
    xs = np.linspace(a, b, pontos)

    plt.figure()
    any_plotted = False
    for fstr in lista:
        try:
            f_clean = fstr.replace('math.', '')
            fexpr = sympify(f_clean, locals=SYMPY_LOCALS)
            ffunc = lambdify(x, fexpr, modules=['numpy'])
            ys = ffunc(xs)
            plt.plot(xs, ys, label=fstr)
            any_plotted = True
        except Exception as e:
            print(f"Erro ao processar função '{fstr}': {e}")

    if not any_plotted:
        print("Nenhuma função pôde ser plotada.")
        return

    plt.axhline(0, color='k', linewidth=0.6)
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('f(x)')
    # plt.title('')
    plt.grid(True)
    plt.show()


def plotar_funcao_e_aproximacao(func, a, b, m, metodo=None, pontos=400):
    """Plota a função e a aproximação composta baseada em nós igualmente espaçados.

    Parameters
    ----------
    func : str
        Expressão da função em termos de ``x``.
    a, b : float
        Intervalo da integração.
    m : int
        Número de subintervalos (m > 0).
    metodo : str, optional
        Legenda para a aproximação (ex.: ``'Trapézio composta'``).
    pontos : int, optional
        Número de pontos para plotagem da função exata.
    """
    try:
        import matplotlib.pyplot as plt
    except Exception:
        print("matplotlib não está disponível. Instale com 'pip install matplotlib'.")
        return

    x = symbols('x')
    func_clean = func.replace('math.', '')
    xs = np.linspace(a, b, pontos)

    # tenta criar função vetorizada via sympy
    try:
        fexpr = sympify(func_clean, locals=SYMPY_LOCALS)
        ffunc = lambdify(x, fexpr, modules=['numpy'])
        ys = ffunc(xs)
    except Exception:
        # fallback para eval ponto-a-ponto
        ys = []
        safe_math = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
        for xv in xs:
            try:
                yv = eval(func, {"__builtins__": None}, {"x": xv, "math": math, **safe_math})
            except Exception:
                yv = float('nan')
            ys.append(yv)
        ys = np.array(ys, dtype=float)

    # calcula nós de aproximação
    try:
        m_int = int(m)
        if m_int <= 0:
            raise ValueError("m deve ser positivo")
    except Exception:
        print("Valor de m inválido para plotar aproximação.")
        return

    h = (b - a) / m_int
    xi = np.array([a + i * h for i in range(m_int + 1)], dtype=float)

    # avalia a função nos nós (tenta lambdify, senão eval)
    try:
        if 'ffunc' in locals():
            yi = ffunc(xi)
        else:
            raise Exception()
    except Exception:
        yi = []
        safe_math = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
        for xv in xi:
            try:
                yv = eval(func, {"__builtins__": None}, {"x": xv, "math": math, **safe_math})
            except Exception:
                yv = float('nan')
            yi.append(yv)
        yi = np.array(yi, dtype=float)

    plt.figure()
    plt.plot(xs, ys, label='f(x) exata', linewidth=2)
    # desenha a aproximação através dos nós conectados
    plt.plot(xi, yi, '--o', color='orange', label=f'Aproximação ({metodo or "composta"})')

    # Desenhar polinômios locais usados pela fórmula composta (Lagrange)
    def lagrange_eval(x_nodes, y_nodes, x_eval):
        x_nodes = np.asarray(x_nodes, dtype=float)
        y_nodes = np.asarray(y_nodes, dtype=float)
        x_eval = np.asarray(x_eval, dtype=float)
        P = np.zeros_like(x_eval, dtype=float)
        n = len(x_nodes)
        for j in range(n):
            # compute L_j(x) basis
            lj = np.ones_like(x_eval, dtype=float)
            for k in range(n):
                if k == j:
                    continue
                lj *= (x_eval - x_nodes[k]) / (x_nodes[j] - x_nodes[k])
            P += y_nodes[j] * lj
        return P

    method_lower = (metodo or '').lower()
    # Trapezio: a linha conectando nós já representa o polinômio de grau 1 por segmento
    if 'simpson 1/3' in method_lower or 'simpson13' in method_lower:
        # para cada par de subintervalos (2 subintervalos, 3 nós), desenha o polinômio quadrático
        for i in range(0, m_int, 2):
            if i + 2 > m_int:
                break
            nodes_x = xi[i:i+3]
            nodes_y = yi[i:i+3]
            xs_local = np.linspace(nodes_x[0], nodes_x[-1], max(50, int(pontos*(len(nodes_x)/len(xs)))))
            try:
                ys_local = lagrange_eval(nodes_x, nodes_y, xs_local)
                plt.plot(xs_local, ys_local, color='red', linewidth=1.8, alpha=0.9)
            except Exception:
                # ignora se algo falhar na interpolação local
                pass
    elif 'simpson 3/8' in method_lower or 'simpson38' in method_lower:
        # para cada bloco de 3 subintervalos (4 nós), desenha o polinômio cúbico
        for i in range(0, m_int, 3):
            if i + 3 > m_int:
                break
            nodes_x = xi[i:i+4]
            nodes_y = yi[i:i+4]
            xs_local = np.linspace(nodes_x[0], nodes_x[-1], max(60, int(pontos*(len(nodes_x)/len(xs)))))
            try:
                ys_local = lagrange_eval(nodes_x, nodes_y, xs_local)
                plt.plot(xs_local, ys_local, color='green', linewidth=1.8, alpha=0.9)
            except Exception:
                pass
    plt.axhline(0, color='k', linewidth=0.6)
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Função e aproximação')
    plt.grid(True)
    plt.show()

def pedir_dados_integral():
    """Lê interativamente a função e limites para integração.

    Returns
    -------
    (func, a, b, composta)
        func : str ou None - expressão da função
        a, b : float - limites do intervalo
        composta : bool - se deve usar regra composta
        Retorna (None, None, None, None) em caso de erro de parsing.
    """
    func = input("Digite a função f(x) (ex: sin(x), log(x), exp(x), etc): ")
    a_str = input("Limite inferior (a): ")
    b_str = input("Limite superior (b): ")
    try:
        a = float(sympify(a_str, locals=SYMPY_LOCALS))
        b = float(sympify(b_str, locals=SYMPY_LOCALS))
    except Exception as e:
        print(f"Erro ao interpretar os limites: {e}")
        return None, None, None, None
    composta = input("Deseja usar a versão composta? (s/n): ").strip().lower() == 's'
    return func, a, b, composta

def pedir_m_ou_h(a, b, regra):
    """Auxiliar que solicita ``m`` (número de subintervalos) ou ``h`` (tamanho do passo).

    Parameters
    ----------
    a, b : float
        Intervalo de integração.
    regra : str
        Identificador da regra ('trapezio', 'simpson13', 'simpson38') usado para validar requisitos (paridade, múltiplos).

    Returns
    -------
    (int, float) or (None, None)
        Tupla (m, h) calculada, ou (None, None) em caso de entrada inválida.
    """
    escolha = input("Deseja informar o número de subintervalos (m) ou o tamanho do passo (h)? [m/h]: ").strip().lower()
    if escolha == 'h':
        try:
            h = float(input("Digite o valor de h (tamanho do passo): "))
            if h == 0:
                print("O passo h não pode ser zero.")
                return None, None
        except Exception:
            print("Valor de h inválido.")
            return None, None
        m = (b - a) / h
        m_int = int(round(m))
        if regra == 'simpson13' and m_int % 2 != 0:
            print("Número de subintervalos calculado não é par para Simpson 1/3 composta. Retornando ao menu.")
            return None, None
        if regra == 'simpson38' and m_int % 3 != 0:
            print("Número de subintervalos calculado não é múltiplo de 3 para Simpson 3/8 composta. Retornando ao menu.")
            return None, None
        m = m_int
        if m <= 0:
            print("Número de subintervalos inválido calculado (<=0). Retornando ao menu.")
            return None, None
        h = (b - a) / m
        print(f"Número de subintervalos ajustado (m): {m}")
        print(f"Tamanho do passo ajustado (h): {h}")
    else:
        try:
            m = int(input("Digite o número de subintervalos (m): "))
            if m <= 0:
                print("Número de subintervalos deve ser maior que zero. Retornando ao menu.")
                return None, None
        except Exception:
            print("Valor de m inválido. Retornando ao menu.")
            return None, None
        if regra == 'simpson13' and m % 2 != 0:
            print("Número de subintervalos deve ser par para Simpson 1/3 composta. Retornando ao menu.")
            return None, None
        if regra == 'simpson38' and m % 3 != 0:
            print("Número de subintervalos deve ser múltiplo de 3 para Simpson 3/8 composta. Retornando ao menu.")
            return None, None
        h = (b - a) / m
    return m, h

def erro_truncamento_composta(a, b, m, derivada_max, metodo):
    """Estimativa do erro de truncamento para regras compostas.

    Parameters
    ----------
    a, b : float
        Intervalo de integração.
    m : int
        Número de subintervalos.
    derivada_max : float
        Valor máximo estimado da derivada relevante no intervalo (ex.: segunda derivada para trapézio).
    metodo : str
        'trapezio', 'simpson13' ou 'simpson38'.

    Returns
    -------
    float or None
        Estimativa do erro de truncamento (pode ser negativa conforme fórmula) ou None se método desconhecido.
    """
    if metodo == 'trapezio':
        return -((b-a)**3) / (12 * m**2) * derivada_max
    elif metodo == 'simpson13':
        return -((b-a)**5) / (180 * m**4) * derivada_max
    elif metodo == 'simpson38':
        return -((b-a)**5) / (80 * m**4) * derivada_max
    else:
        return None

def trapezio_tabela():
    '''
    Regra do Trapézio para dados em tabela (x, y).
    
    Requer que o número de pontos seja pelo menos 2
    Fórmula: int_a^b f(x) dx ≈ (h/2) * [f(x0) + f(xn)]
    '''
    print("\n--- Regra do Trapézio com dados em tabela ---")
    n = int(input("Digite o número de pontos (n >= 2): "))
    if n < 2:
        print("Número de pontos deve ser pelo menos 2.")
        return None

    x = []
    y = []
    print("Digite os valores de x em ordem crescente:")
    for i in range(n):
        x.append(float(input(f"x[{i}]: ")))
    print("Digite os valores correspondentes de y = f(x):")
    for i in range(n):
        y.append(float(input(f"y[{i}]: ")))

    integral = 0.0
    for i in range(n - 1):
        h = x[i+1] - x[i]
        integral += (h * (y[i] + y[i+1]) / 2)

    print(f"\nResultado da integral pelo Trapézio com dados discretos: {integral}\n")


def simpson_1_3_tabela():
    '''
    Regra de Simpson 1/3 para dados em tabela (x, y).
    
    Requer que o número de pontos seja ímpar
    Fórmula: int_a^b f(x) dx ≈ (h/3) * [f(x0) + 4f(x1) + 2f(x2) + ... + 4f(xn-1) + f(xn)]
    '''
    print("\n--- Regra de Simpson 1/3 com dados em tabela ---")
    n = int(input("Digite o número de pontos (n deve ser ímpar, pelo menos 3): "))
    if n < 3 or n % 2 == 0:
        print("Número de pontos inválido. Deve ser ímpar e pelo menos 3.")
        return

    x = []
    y = []
    print("Digite os valores de x em ordem crescente:")
    for i in range(n):
        x.append(float(input(f"x[{i}]: ")))
    print("Digite os valores correspondentes de y = f(x):")
    for i in range(n):
        y.append(float(input(f"y[{i}]: ")))

    h = (x[-1] - x[0]) / (n - 1)

    integral = y[0] + y[-1]
    for i in range(1, n-1):
        if i % 2 == 0:
            integral += 2 * y[i]
        else:
            integral += 4 * y[i]
    integral *= h / 3

    print(f"\nResultado da integral pela Regra de Simpson 1/3 com dados discretos: {integral}\n")


def simpson_3_8_tabela():
    ''''
    Regra de Simpson 3/8 para dados em tabela (x, y).
    
    Requer que os intervalos sejam multiplo de 3
    Fórmula: int_a^b f(x) dx ≈ (3h/8) * [f(x0) + 3f(x1) + 3f(x2) + 2f(x3) + ... + 3f(xn-1) + f(xn)]
    '''
    print("\n--- Regra de Simpson 3/8 com dados em tabela ---")
    n = int(input("Digite o número de pontos (n deve ser múltiplo de 3 mais 1, ex: 4, 7, 10): "))
    if (n - 1) % 3 != 0 or n < 4:
        print("Número de pontos inválido. Deve ser 3k + 1 e pelo menos 4.")
        return None

    x = []
    y = []
    print("Digite os valores de x em ordem crescente:")
    for i in range(n):
        x.append(float(input(f"x[{i}]: ")))
    print("Digite os valores correspondentes de y = f(x):")
    for i in range(n):
        y.append(float(input(f"y[{i}]: ")))

    h = (x[-1] - x[0]) / (n - 1)

    integral = y[0] + y[-1]
    for i in range(1, n - 1):
        if i % 3 == 0:
            integral += 2 * y[i]
        else:
            integral += 3 * y[i]

    integral *= 3 * h / 8

    print(f"\nResultado da integral pela Regra de Simpson 3/8 com dados discretos: {integral}\n")
    return

def calcular_integral_analitica():
    '''
    Calcula a integral de uma função simbolicamente usando SymPy.
    
    Requer a função e os limites de integração.    
    Fórmula: int_a^b f(x) dx
    '''
    
    print("\nCálculo Integral")
    expressao = input("Digite a função f(x): ")
    a_str = input("Limite inferior (a): ")
    b_str = input("Limite superior (b): ")
    try:
        a = float(sympify(a_str, locals=SYMPY_LOCALS))
        b = float(sympify(b_str, locals=SYMPY_LOCALS))
    except Exception as e:
        print(f"Erro ao interpretar os limites: {e}")
        return None

    x = symbols('x')
    try:
        funcao = sympify(expressao, locals=SYMPY_LOCALS)
        integral_exata = integrate(funcao, (x, a, b))
        print(f"\nResultado exato da integral de {expressao} de {a} a {b}: {integral_exata.evalf()}\n")
        return integral_exata.evalf()
    except Exception as e:
        print("\nErro ao calcular a integral simbolicamente:", e)
        return None

def newton_cotes(func, a, b, ordem, verbose=False, grafico=None):
    """Newton-Cotes para integração numérica (ordens 1,2,3).

    Otimizações
    -----------
    - Tenta usar `sympy.lambdify` para avaliar a função de forma vetorizada quando possível.

    Verbose & Gráficos
    ------------------
    - `verbose=False` (padrão): execução silenciosa (comportamento compatível com testes automatizados).
    - `verbose=True`: imprime detalhes auxiliares e, por padrão, habilita `grafico=True`.

    Parâmetros
    ----------
    func : str
        Expressão da função em termos de ``x``.
    a, b : float
        Limites do intervalo de integração (números finitos, distintos).
    ordem : int
        Ordem da regra (1, 2 ou 3).
    verbose : bool, optional
        Habilita saídas detalhadas e gráficos (padrão: False).
    grafico : bool or None, optional
        Controla plotagem: se None e ``verbose`` for True, é habilitado; caso contrário, respeitado.

    Retorno
    -------
    float
        Aproximação da integral.

    Notas de teste
    --------------
    Os testes unitários que cobrem Newton-Cotes e regras compostas estão em ``tests/test_integracoes.py``.
    """
    # Validações básicas de entrada
    try:
        a = float(a); b = float(b)
    except Exception:
        raise TypeError("Os limites a e b devem ser numéricos e conversíveis para float.")
    if not np.isfinite(a) or not np.isfinite(b):
        raise ValueError("Os limites a e b devem ser finitos (não NaN ou infinito).")
    if a == b:
        raise ValueError("Os limites a e b não podem ser iguais.")
    if ordem not in (1, 2, 3):
        raise ValueError("Ordem inválida para Newton-Cotes. Deve ser 1, 2 ou 3.")

    if grafico is None:
        grafico = bool(verbose)

    h = (b - a) / ordem

    # Tentar avaliação vetorizada com SymPy/lambdify
    x_sym = symbols('x')
    func_clean = func.replace('math.', '')
    try:
        fexpr = sympify(func_clean, locals=SYMPY_LOCALS)
        fvec = lambdify(x_sym, fexpr, modules=['numpy'])
        x = np.linspace(a, b, ordem + 1)
        y = np.asarray(fvec(x), dtype=float)
    except Exception:
        # Fallback ponto a ponto
        x = [a + i * h for i in range(ordem + 1)]
        y = []
        safe_math = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
        for xi in x:
            try:
                yi = eval(func, {"__builtins__": None}, {"x": xi, "math": math, **safe_math})
            except Exception as e:
                if verbose:
                    print(f"Erro na avaliação da função em x={xi}: {e}")
                return None
            y.append(yi)
        y = np.asarray(y, dtype=float)

    if ordem == 1:
        resultado = h * (y[0] + y[1]) / 2
        metodo_nome = "Regra do Trapézio"
    elif ordem == 2:
        resultado = (h / 3) * (y[0] + 4 * y[1] + y[2])
        metodo_nome = "Regra de Simpson 1/3"
    else:
        resultado = (3 * h / 8) * (y[0] + 3 * y[1] + 3 * y[2] + y[3])
        metodo_nome = "Regra de Simpson 3/8"

    if verbose:
        print(f"\nResultado pela {metodo_nome}: {float(resultado)}\n")

    if grafico:
        try:
            plotar_funcao_e_aproximacao(func, a, b, ordem, metodo=metodo_nome)
        except Exception as e:
            if verbose:
                print(f"Não foi possível gerar o gráfico: {e}")

    return float(resultado)

def trapezio_composta(func, a, b, verbose=False, grafico=None):
    """Regra do Trapézio composta para integração numérica.

    Parameters
    ----------
    func : str
        Expressão da função em termos de ``x``.
    a, b : float
        Limites do intervalo de integração.
    verbose : bool, optional
        Se True, imprime detalhes e habilita (por padrão) a plotagem e estimativa de erro.
    grafico : bool or None, optional
        Controla plotagem: se None e verbose for True, habilita-a.

    Returns
    -------
    float or None
        Aproximação da integral ou ``None`` em caso de erro/entrada inválida.

    Notes
    -----
    Testes para regras compostas estão em ``tests/test_integracoes.py``.
    """
    m, h = pedir_m_ou_h(a, b, 'trapezio')
    if m is None:
        return None
    if grafico is None:
        grafico = bool(verbose)

    # Tentar vetorizar avaliação via sympy
    x_sym = symbols('x')
    func_clean = func.replace('math.', '')
    try:
        fexpr = sympify(func_clean, locals=SYMPY_LOCALS)
        fvec = lambdify(x_sym, fexpr, modules=['numpy'])
        xi = np.linspace(a, b, m + 1)
        yi = np.asarray(fvec(xi), dtype=float)
    except Exception:
        xi = np.array([a + i * h for i in range(m + 1)], dtype=float)
        yi = []
        safe_math = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
        for xv in xi:
            try:
                yv = eval(func, {"__builtins__": None}, {"x": xv, "math": math, **safe_math})
            except Exception as e:
                if verbose:
                    print(f"Erro na avaliação da função em x={xv}: {e}")
                return None
            yi.append(yv)
        yi = np.asarray(yi, dtype=float)

    # Regra composta
    resultado = (h / 2) * (yi[0] + 2 * np.sum(yi[1:-1]) + yi[-1])

    if verbose:
        print(f"\nResultado pela Regra do Trapézio composta: {float(resultado)}")
        print(f"m (subintervalos): {m}, h (passo): {h}")

    if grafico:
        try:
            plotar_funcao_e_aproximacao(func, a, b, m, metodo='Trapézio composta')
        except Exception as e:
            if verbose:
                print(f"Não foi possível gerar o gráfico: {e}")

    # Se verbose, estima erro automaticamente; caso contrário, mantém prompts interativos
    if verbose:
        try:
            x = symbols('x')
            func_expr = sympify(func_clean, locals=SYMPY_LOCALS)
            deriv2 = diff(func_expr, x, 2)
            deriv2_func = lambdify(x, deriv2, modules=["numpy"])  # vetoriza com numpy
            xs = np.linspace(a, b, 1000)
            vals = np.abs(deriv2_func(xs))
            derivada_max = float(np.nanmax(vals))
            erro = erro_truncamento_composta(a, b, m, derivada_max, 'trapezio')
            print(f"Erro de truncamento estimado (Trapézio composta): {erro}")
        except Exception as e:
            if verbose:
                print(f"Não foi possível calcular o erro automaticamente: {e}")
    else:
        # modo interativo: perguntar ao usuário se deseja plotar e estimar erro (compatibilidade)
        try:
            if input("Deseja plotar a função e a aproximação no intervalo [a,b]? (s/n): ").strip().lower() == 's':
                try:
                    plotar_funcao_e_aproximacao(func, a, b, m, metodo='Trapézio composta')
                except Exception as e:
                    print(f"Não foi possível gerar o gráfico: {e}")
        except EOFError:
            # Em ambiente não interativo, ignora
            pass

        try:
            if input("Deseja estimar o erro de truncamento? (s/n): ").strip().lower() == 's':
                try:
                    x = symbols('x')
                    func_expr = sympify(func_clean, locals=SYMPY_LOCALS)
                    deriv2 = diff(func_expr, x, 2)
                    deriv2_func = lambdify(x, deriv2, modules=["numpy"])
                    xs = np.linspace(a, b, 1000)
                    vals = np.abs(deriv2_func(xs))
                    derivada_max = float(np.nanmax(vals))
                    erro = erro_truncamento_composta(a, b, m, derivada_max, 'trapezio')
                    print(f"Erro de truncamento estimado (Trapézio composta): {erro}")
                except Exception as e:
                    print(f"Não foi possível calcular o erro automaticamente: {e}")
        except EOFError:
            pass

    print()
    return float(resultado)

def simpson_1_3_composta(func, a, b, verbose=False, grafico=None):
    """Regra de Simpson 1/3 composta para integração numérica.

    Parameters
    ----------
    func : str
        Expressão da função em termos de ``x``.
    a, b : float
        Limites do intervalo de integração.
    verbose : bool, optional
        Se True, imprime detalhes, habilita plot e estimativa de erro.
    grafico : bool or None, optional
        Controla plotagem: se None e verbose for True, habilita-a.

    Returns
    -------
    float or None
        Aproximação da integral ou ``None`` em caso de erro/entrada inválida.
    """
    m, h = pedir_m_ou_h(a, b, 'simpson13')
    if m is None:
        return None
    if grafico is None:
        grafico = bool(verbose)

    # Tentar vetorizar avaliação
    x_sym = symbols('x')
    func_clean = func.replace('math.', '')
    try:
        fexpr = sympify(func_clean, locals=SYMPY_LOCALS)
        fvec = lambdify(x_sym, fexpr, modules=['numpy'])
        xi = np.linspace(a, b, m + 1)
        yi = np.asarray(fvec(xi), dtype=float)
    except Exception:
        xi = np.array([a + i * h for i in range(m + 1)], dtype=float)
        yi = []
        safe_math = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
        for xv in xi:
            try:
                yv = eval(func, {"__builtins__": None}, {"x": xv, "math": math, **safe_math})
            except Exception as e:
                if verbose:
                    print(f"Erro na avaliação da função em x={xv}: {e}")
                return None
            yi.append(yv)
        yi = np.asarray(yi, dtype=float)

    # Aplica a regra composta (Simpson 1/3 exige m par)
    resultado = (h / 3) * (yi[0] + yi[-1] + 2 * np.sum(yi[2:-1:2]) + 4 * np.sum(yi[1::2]))

    if verbose:
        print(f"\nResultado pela Regra de Simpson 1/3 composta: {float(resultado)}")

    if grafico:
        try:
            plotar_funcao_e_aproximacao(func, a, b, m, metodo='Simpson 1/3 composta')
        except Exception as e:
            if verbose:
                print(f"Não foi possível gerar o gráfico: {e}")

    if verbose:
        try:
            x = symbols('x')
            func_expr = sympify(func_clean, locals=SYMPY_LOCALS)
            deriv4 = diff(func_expr, x, 4)
            deriv4_func = lambdify(x, deriv4, modules=["numpy"])
            xs = np.linspace(a, b, 1000)
            vals = np.abs(deriv4_func(xs))
            derivada_max = float(np.nanmax(vals))
            erro = erro_truncamento_composta(a, b, m, derivada_max, 'simpson13')
            print(f"Erro de truncamento estimado (Simpson 1/3 composta): {erro}")
        except Exception as e:
            if verbose:
                print(f"Não foi possível calcular o erro automaticamente: {e}")
    else:
        try:
            if input("Deseja plotar a função e a aproximação no intervalo [a,b]? (s/n): ").strip().lower() == 's':
                try:
                    plotar_funcao_e_aproximacao(func, a, b, m, metodo='Simpson 1/3 composta')
                except Exception as e:
                    print(f"Não foi possível gerar o gráfico: {e}")
        except EOFError:
            pass

        try:
            if input("Deseja estimar o erro de truncamento? (s/n): ").strip().lower() == 's':
                try:
                    x = symbols('x')
                    func_expr = sympify(func_clean, locals=SYMPY_LOCALS)
                    deriv4 = diff(func_expr, x, 4)
                    deriv4_func = lambdify(x, deriv4, modules=["numpy"])
                    xs = np.linspace(a, b, 1000)
                    vals = np.abs(deriv4_func(xs))
                    derivada_max = float(np.nanmax(vals))
                    erro = erro_truncamento_composta(a, b, m, derivada_max, 'simpson13')
                    print(f"Erro de truncamento estimado (Simpson 1/3 composta): {erro}")
                except Exception as e:
                    print(f"Não foi possível calcular o erro automaticamente: {e}")
        except EOFError:
            pass

    print()
    return float(resultado)


def simpson_3_8_composta(func, a, b, verbose=False, grafico=None):
    '''
    Regra de Simpson 3/8 composta para integração numérica.

    Parameters
    ----------
    func : str
        Expressão da função em termos de ``x``.
    a, b : float
        Limites do intervalo de integração.
    verbose : bool, optional
        Se True, imprime detalhes e habilita plot/estimativa de erro.
    grafico : bool or None, optional
        Controla plotagem: se None e verbose for True, habilita-a.
    '''
    m, h = pedir_m_ou_h(a, b, 'simpson38')
    if m is None:
        return None
    if grafico is None:
        grafico = bool(verbose)

    # Tentar vetorizar avaliação
    x_sym = symbols('x')
    func_clean = func.replace('math.', '')
    try:
        fexpr = sympify(func_clean, locals=SYMPY_LOCALS)
        fvec = lambdify(x_sym, fexpr, modules=['numpy'])
        xi = np.linspace(a, b, m + 1)
        yi = np.asarray(fvec(xi), dtype=float)
    except Exception:
        xi = np.array([a + i * h for i in range(m + 1)], dtype=float)
        yi = []
        safe_math = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
        for xv in xi:
            try:
                yv = eval(func, {"__builtins__": None}, {"x": xv, "math": math, **safe_math})
            except Exception as e:
                if verbose:
                    print(f"Erro na avaliação da função em x={xv}: {e}")
                return None
            yi.append(yv)
        yi = np.asarray(yi, dtype=float)

    # composição para Simpson 3/8
    soma = 0.0
    for i in range(1, m):
        if i % 3 == 0:
            soma += 2 * yi[i]
        else:
            soma += 3 * yi[i]

    resultado = (3 * h / 8) * (yi[0] + soma + yi[-1])

    if verbose:
        print(f"\nResultado pela Regra de Simpson 3/8 composta: {float(resultado)}")
        print(f"m (subintervalos): {m}, h (passo): {h}")

    if grafico:
        try:
            plotar_funcao_e_aproximacao(func, a, b, m, metodo='Simpson 3/8 composta')
        except Exception as e:
            if verbose:
                print(f"Não foi possível gerar o gráfico: {e}")

    if verbose:
        try:
            x = symbols('x')
            func_expr = sympify(func_clean, locals=SYMPY_LOCALS)
            deriv4 = diff(func_expr, x, 4)
            deriv4_func = lambdify(x, deriv4, modules=["numpy"])
            xs = np.linspace(a, b, 1000)
            vals = np.abs(deriv4_func(xs))
            derivada_max = float(np.nanmax(vals))
            erro = erro_truncamento_composta(a, b, m, derivada_max, 'simpson38')
            print(f"Erro de truncamento estimado (Simpson 3/8 composta): {erro}")
        except Exception as e:
            if verbose:
                print(f"Não foi possível calcular o erro automaticamente: {e}")
    else:
        try:
            if input("Deseja plotar a função e a aproximação no intervalo [a,b]? (s/n): ").strip().lower() == 's':
                try:
                    plotar_funcao_e_aproximacao(func, a, b, m, metodo='Simpson 3/8 composta')
                except Exception as e:
                    print(f"Não foi possível gerar o gráfico: {e}")
        except EOFError:
            pass

        try:
            if input("Deseja estimar o erro de truncamento? (s/n): ").strip().lower() == 's':
                try:
                    x = symbols('x')
                    func_expr = sympify(func_clean, locals=SYMPY_LOCALS)
                    deriv4 = diff(func_expr, x, 4)
                    deriv4_func = lambdify(x, deriv4, modules=["numpy"])
                    xs = np.linspace(a, b, 1000)
                    vals = np.abs(deriv4_func(xs))
                    derivada_max = float(np.nanmax(vals))
                    erro = erro_truncamento_composta(a, b, m, derivada_max, 'simpson38')
                    print(f"Erro de truncamento estimado (Simpson 3/8 composta): {erro}")
                except Exception as e:
                    print(f"Não foi possível calcular o erro automaticamente: {e}")
        except EOFError:
            pass

    print()
    return float(resultado)


def dados():
    """Menu interativo para métodos de integração numérica."""
    print("\n=== Métodos de Integração Numérica ===")
    print("1 - Regra do Trapézio")
    print("2 - Regra de Simpson 1/3")
    print("3 - Regra de Simpson 3/8")
    print("0 - Sair")
    opcao = input("Escolha o método desejado: ")
    return opcao


def menu():
    while True:
        print("\n--- MÉTODOS DE INTEGRAÇÃO NUMÉRICA ---")
        print("1 - Regra do Trapézio")
        print("2 - Regra de Simpson 1/3")
        print("3 - Regra de Simpson 3/8")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")
        if opcao == '0':
            print("Encerrando o programa.")
            break

        tabela = input("Deseja inserir dados em tabela (x, y)? (s/n): ").strip().lower() == 's'
        if tabela:
            if opcao == '1':
                trapezio_tabela()
            elif opcao == '2':
                simpson_1_3_tabela()
            elif opcao == '3':
                simpson_3_8_tabela()
            else:
                print("Opção inválida.")
            continue
        
        func, a, b, composta = pedir_dados_integral()
        if func is None:
            continue

        resultado = None
        if opcao == '1':
            if composta:
                resultado = trapezio_composta(func, a, b)
            else:
                resultado = newton_cotes(func, a, b, 1)
        elif opcao == '2':
            if composta:
                resultado = simpson_1_3_composta(func, a, b)
            else:
                resultado = newton_cotes(func, a, b, 2)
        elif opcao == '3':
            if composta:
                resultado = simpson_3_8_composta(func, a, b)
            else:
                resultado = newton_cotes(func, a, b, 3)
        else:
            print("Opção inválida. Tente novamente.")
            continue

        if resultado is not None:
            # Mostrar o resultado numérico no menu (útil em execução não-verbose/input-driven)
            print(f"\nResultado: {resultado}\n")
            valor_exato = None
            calc_exata = input("Deseja calcular a integral exata (simbólica)? (s/n): ").strip().lower() == 's'
            if calc_exata:
                x = symbols('x')
                func_sympy = func.replace('math.', '')
                try:
                    funcao = sympify(func_sympy, locals=SYMPY_LOCALS)
                    integral_exata = integrate(funcao, (x, a, b))
                    try:
                        valor_exato = float(integral_exata.evalf())
                    except Exception:
                        valor_exato = float(integral_exata)
                    print(f"\nResultado exato da integral de {func_sympy} de {a} a {b}: {valor_exato}\n")
                    # Se foi pedido o exato e estamos em caso composto, mostra erro relativo (módulo)
                    if composta and valor_exato is not None:
                        try:
                            erro_rel = abs(float(resultado) - float(valor_exato)) / abs(float(valor_exato)) if float(valor_exato) != 0 else float('inf')
                            print(f"Erro relativo (módulo) entre o valor numérico composto e o exato: {erro_rel}\n")
                        except Exception as _:
                            print("Não foi possível calcular o erro relativo.")
                except Exception as e:
                    print("\nErro ao calcular a integral simbolicamente:", e)
            if not composta:
                calc_erro = input("Deseja calcular o erro de truncamento? (s/n): ").strip().lower() == 's'
                if calc_erro:
                    if valor_exato is None:
                        v_str = input("Digite o valor EXATO da integral (analítico): ")
                        try:
                            valor_exato = float(sympify(v_str, locals=SYMPY_LOCALS))
                        except Exception:
                            try:
                                valor_exato = float(v_str)
                            except Exception:
                                print("Valor exato inválido.")
                                valor_exato = None
                    erro = abs(float(valor_exato) - float(resultado))
                    print(f"\nValor exato informado: {valor_exato}")
                    print(f"Resultado numérico: {resultado}")
                    print(f"Erro de truncamento: {erro}\n")

if __name__ == "__main__":
    menu()