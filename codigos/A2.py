

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

# Constantes locais (copiadas para esta versão — não usar import de `codigos.constants`)
# Mantém mapeamento padrão para uso com sympify
SYMPY_LOCALS = {
    'sin': sin, 'cos': cos, 'tan': tan,
    'asin': asin, 'acos': acos, 'atan': atan,
    'sinh': sinh, 'cosh': cosh, 'tanh': tanh,
    'exp': exp, 'sqrt': sqrt, 'log': log, 'abs': Abs,
    'pi': pi, 'e': E, 'E': E
}

# SAFE_MATH: funções do módulo math expostas para fallbacks com eval
SAFE_MATH = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}


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

"""
Módulo para solução numérica de equações diferenciais ordinárias.

Este módulo implementa métodos numéricos para EDOs:
Euler, Runge-Kutta (1ª a 4ª ordem) e diferenças finitas.

Author: Pedro Henrique Rocha de Andrade
Date: Dezembro 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import math
import sympy as sp
from sympy import sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, exp, sqrt, log, Abs, pi, E
import re

def _validate_edo_inputs(func_input, x0, y0, h, xn, ordem=None):
    """Valida entradas para funções de resolução de EDOs.

    Esta função realiza validações abrangentes dos dados de entrada para garantir
    que a resolução de EDO possa ser realizada corretamente.

    Parameters
    ----------
    func_input : str
        Expressão da função f(x, y) como string.
    x0, y0 : float
        Condições iniciais: ponto inicial x0 e valor y(x0).
    h : float
        Tamanho do passo de integração. Deve ser positivo.
    xn : float
        Ponto final de integração. Deve ser diferente de x0.
    ordem : int or None, optional
        Ordem do método Runge-Kutta (1, 2, 3, 4). Se None, não valida.

    Returns
    -------
    func_input_valid, x0_valid, y0_valid, h_valid, xn_valid : str, float, float, float, float
        Entradas validadas e convertidas para tipos apropriados.

    Raises
    ------
    TypeError
        Se os tipos de entrada não forem adequados.
    ValueError
        Se os valores não forem válidos (passo negativo, pontos iguais, etc.).
    """
    # Validação da função de entrada
    if not isinstance(func_input, str):
        raise TypeError(f"func_input deve ser uma string. Recebido: {type(func_input)}")

    func_input = func_input.strip()
    if not func_input:
        raise ValueError("A expressão da função f(x,y) não pode estar vazia")

    # Validação e conversão dos valores numéricos
    try:
        x0 = float(x0)
        y0 = float(y0)
        h = float(h)
        xn = float(xn)
    except (ValueError, TypeError) as e:
        raise TypeError(f"Todos os parâmetros numéricos devem ser números. Erro: {e}")

    # Validação de valores finitos
    if not np.isfinite(x0):
        raise ValueError("O ponto inicial x0 deve ser finito (não NaN ou infinito)")
    if not np.isfinite(y0):
        raise ValueError("O valor inicial y0 deve ser finito (não NaN ou infinito)")
    if not np.isfinite(h):
        raise ValueError("O passo h deve ser finito (não NaN ou infinito)")
    if not np.isfinite(xn):
        raise ValueError("O ponto final xn deve ser finito (não NaN ou infinito)")

    # Validação do passo
    if h <= 0:
        raise ValueError(f"O passo h deve ser positivo. Recebido: {h}")

    # Validação do intervalo
    if abs(xn - x0) < 1e-15:
        raise ValueError(f"Os pontos inicial e final devem ser diferentes. x0={x0}, xn={xn}")

    # Validação da ordem (se fornecida)
    if ordem is not None:
        try:
            ordem = int(ordem)
        except (ValueError, TypeError):
            raise TypeError(f"A ordem deve ser um inteiro. Recebido: {type(ordem)}")

        if ordem not in [1, 2, 3, 4]:
            raise ValueError(f"A ordem deve ser 1, 2, 3 ou 4. Recebido: {ordem}")

    return func_input, x0, y0, h, xn

def _validate_sistema_edo_inputs(funcs_input, y0, t0, tf, h, ordem=None):
    """Valida entradas para resolução de sistemas de EDOs.

    Parameters
    ----------
    funcs_input : list of str
        Lista de expressões das funções f_i(t, y) como strings.
    y0 : array_like
        Condições iniciais y(t0) como array ou lista.
    t0, tf : float
        Pontos inicial e final de integração.
    h : float
        Tamanho do passo de integração. Deve ser positivo.
    ordem : int or None, optional
        Ordem do método Runge-Kutta (1, 2, 3, 4). Se None, não valida.

    Returns
    -------
    funcs_valid, y0_valid, t0_valid, tf_valid, h_valid : list, np.ndarray, float, float, float
        Entradas validadas e convertidas.

    Raises
    ------
    TypeError
        Se os tipos de entrada não forem adequados.
    ValueError
        Se os valores não forem válidos.
    """
    # Validação das funções
    if not isinstance(funcs_input, (list, tuple)):
        raise TypeError(f"funcs_input deve ser uma lista ou tupla. Recebido: {type(funcs_input)}")

    if len(funcs_input) == 0:
        raise ValueError("Deve haver pelo menos uma função no sistema")

    funcs_valid = []
    for i, func in enumerate(funcs_input):
        if not isinstance(func, str):
            raise TypeError(f"Todas as funções devem ser strings. Função {i}: {type(func)}")
        func = func.strip()
        if not func:
            raise ValueError(f"A função {i} não pode estar vazia")
        funcs_valid.append(func)

    # Validação das condições iniciais
    try:
        y0 = np.asarray(y0, dtype=float)
    except (ValueError, TypeError) as e:
        raise TypeError(f"y0 deve ser conversível para array numérico. Erro: {e}")

    if y0.ndim != 1:
        raise ValueError(f"y0 deve ser um array 1D. Recebido: {y0.ndim}D com shape {y0.shape}")

    if len(y0) != len(funcs_input):
        raise ValueError(f"Número de condições iniciais ({len(y0)}) deve corresponder ao "
                        f"número de funções ({len(funcs_input)})")

    if not np.all(np.isfinite(y0)):
        raise ValueError("Todas as condições iniciais em y0 devem ser finitas")

    # Validação dos pontos temporais e passo
    try:
        t0 = float(t0)
        tf = float(tf)
        h = float(h)
    except (ValueError, TypeError) as e:
        raise TypeError(f"t0, tf e h devem ser números. Erro: {e}")

    if not np.isfinite(t0):
        raise ValueError("O ponto inicial t0 deve ser finito")
    if not np.isfinite(tf):
        raise ValueError("O ponto final tf deve ser finito")
    if not np.isfinite(h):
        raise ValueError("O passo h deve ser finito")

    if h <= 0:
        raise ValueError(f"O passo h deve ser positivo. Recebido: {h}")

    if abs(tf - t0) < 1e-15:
        raise ValueError(f"Os pontos inicial e final devem ser diferentes. t0={t0}, tf={tf}")

    # Validação da ordem (se fornecida)
    if ordem is not None:
        try:
            ordem = int(ordem)
        except (ValueError, TypeError):
            raise TypeError(f"A ordem deve ser um inteiro. Recebido: {type(ordem)}")

        if ordem not in [1, 2, 3, 4]:
            raise ValueError(f"A ordem deve ser 1, 2, 3 ou 4. Recebido: {ordem}")

    return funcs_valid, y0, t0, tf, h

def _create_function_from_string(func_str, variables, verbose=False):
    """Cria uma função callable a partir de uma string matemática.

    Esta função tenta múltiplas abordagens para converter uma expressão
    matemática em string para uma função Python callable, com fallbacks
    para máxima compatibilidade.

    Parameters
    ----------
    func_str : str
        Expressão matemática como string (ex.: 'y - x**2').
    variables : list of str
        Nomes das variáveis na expressão (ex.: ['x', 'y']).
    verbose : bool, optional
        Se True, imprime informações sobre o processo de criação.

    Returns
    -------
    callable
        Função que pode ser chamada com os argumentos correspondentes.

    Raises
    ------
    ValueError
        Se não for possível criar uma função válida da string.
    """
    if verbose:
        print(f"Criando função a partir de: {func_str}")

    # Preparar a string: remover espaços, corrigir notação
    func_str = func_str.replace(' ', '').replace('^', '**')

    # Corrigir multiplicação implícita (ex.: 2x -> 2*x)
    func_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_str)

    # Criar símbolos do SymPy
    symbols = sp.symbols(variables)
    symbols_dict = dict(zip(variables, symbols))

    try:
        # Tentar primeiro com SymPy (mais robusto)
        expr = sp.sympify(func_str, locals={**SYMPY_LOCALS, **symbols_dict})
        func = sp.lambdify(symbols, expr, modules=['numpy'])

        # Teste rápido da função
        test_args = [1.0] * len(variables)
        test_result = func(*test_args)
        if not np.isfinite(test_result):
            raise ValueError("Função produz resultado não-finito no teste")

        if verbose:
            print("Função criada com sucesso usando SymPy")

        return func

    except Exception as e:
        if verbose:
            print(f"Falhou com SymPy: {e}. Tentando fallback com eval...")

        # Fallback: usar eval com ambiente restrito
        try:
            def func(*args):
                if len(args) != len(variables):
                    raise ValueError(f"Número incorreto de argumentos. Esperado: {len(variables)}, "
                                   f"recebido: {len(args)}")

                local_vars = dict(zip(variables, args))
                local_vars.update({'np': np, 'math': math, **SAFE_MATH})

                try:
                    return eval(func_str, {"__builtins__": None}, local_vars)
                except Exception as eval_error:
                    raise ValueError(f"Erro na avaliação da função: {eval_error}")

            # Teste da função
            test_args = [1.0] * len(variables)
            test_result = func(*test_args)
            if not np.isfinite(test_result):
                raise ValueError("Função produz resultado não-finito no teste")

            if verbose:
                print("Função criada com sucesso usando eval")

            return func

        except Exception as fallback_error:
            raise ValueError(f"Não foi possível criar função a partir de '{func_str}'. "
                           f"Erro SymPy: {e}. Erro fallback: {fallback_error}")

def coletar_dados_edo():
    """Obtém entradas do usuário para resolução de EDOs com validação robusta.

    Esta função solicita interativamente ao usuário os dados necessários para
    resolver uma equação diferencial ordinária: a função f(x,y), o intervalo
    de integração [a,b], as condições iniciais (x0,y0), e o passo de integração.
    Também permite especificar uma solução exata opcional para comparação.

    A função inclui validações abrangentes para garantir que os dados sejam
    adequados para a resolução numérica da EDO.

    Returns
    -------
    dict
        Dicionário contendo todos os dados validados com as seguintes chaves:
        - 'func_input': str, expressão da função f(x,y)
        - 'a': float, limite inferior do intervalo
        - 'b': float, limite superior do intervalo
        - 'x0': float, ponto inicial das condições iniciais
        - 'y0': float, valor inicial y(x0)
        - 'h': float, tamanho do passo de integração
        - 'm': int or None, número de subintervalos (se especificado)
        - 'xn': float, ponto final (sempre igual a b)
        - 'solucao_exata': callable or None, função da solução exata
        - 'sol_exata_expr': str, expressão da solução exata

    Raises
    ------
    ValueError
        Se os dados inseridos forem inválidos ou inconsistentes.
    KeyboardInterrupt
        Se o usuário interromper a entrada (Ctrl+C).
    """
    try:
        # Entrada da função f(x,y) com validação
        while True:
            print("\nDigite a função f(x,y) em notação matemática simples:")
            print("Exemplo: y - x**2  (será interpretado como y - x²)")
            print("Funções disponíveis: sin, cos, tan, exp, log, sqrt, pi, e, etc.")
            func_input = input("f(x,y) = ").strip()

            if not func_input:
                print("Erro: A expressão da função não pode estar vazia. Tente novamente.")
                continue

            # Teste básico da função
            try:
                test_func = _create_function_from_string(func_input, ['x', 'y'], verbose=False)
                # Teste numérico rápido
                test_result = test_func(1.0, 1.0)
                if not np.isfinite(test_result):
                    print("Erro: A função produz resultado não-finito. Verifique a expressão.")
                    continue
                break
            except Exception as e:
                print(f"Erro na expressão da função: {e}")
                print("Tente novamente.")
                continue

        # Entrada do intervalo [a,b] com validação
        while True:
            try:
                print("\nIntervalo de integração [a,b]:")
                a_str = input("a = ").strip()
                a = float(a_str)
                b_str = input("b = ").strip()
                b = float(b_str)

                if not (np.isfinite(a) and np.isfinite(b)):
                    print("Erro: Os limites devem ser finitos. Tente novamente.")
                    continue

                if abs(b - a) < 1e-15:
                    print("Erro: Os limites a e b devem ser diferentes. Tente novamente.")
                    continue

                break
            except ValueError:
                print("Erro: Digite números válidos. Tente novamente.")

        # Entrada das condições iniciais com validação
        while True:
            try:
                print("\nCondições iniciais:")
                x0_str = input("x0 = ").strip()
                x0 = float(x0_str)
                y0_str = input("y0 = ").strip()
                y0 = float(y0_str)

                if not (np.isfinite(x0) and np.isfinite(y0)):
                    print("Erro: As condições iniciais devem ser finitas. Tente novamente.")
                    continue

                # Verificar se x0 está no intervalo [a,b]
                if not (min(a, b) <= x0 <= max(a, b)):
                    print(f"Aviso: x0 = {x0} está fora do intervalo [{a}, {b}]")

                break
            except ValueError:
                print("Erro: Digite números válidos. Tente novamente.")

        # Escolha do passo: h ou m
        h = None
        m = None
        while True:
            try:
                escolha = input("\nDeseja informar o passo por:\n"
                              "  h - tamanho do passo diretamente\n"
                              "  m - número de subintervalos\n"
                              "Escolha [h/m]: ").strip().lower()

                if escolha == 'h':
                    h_str = input("h = ").strip()
                    h = float(h_str)
                    if h <= 0:
                        print("Erro: O passo h deve ser positivo. Tente novamente.")
                        continue
                    if h > abs(b - a):
                        print(f"Aviso: h = {h} é maior que o intervalo |b-a| = {abs(b-a)}")
                    m = None
                    break

                elif escolha == 'm':
                    m_str = input("m = ").strip()
                    m = int(m_str)
                    if m <= 0:
                        print("Erro: O número de subintervalos m deve ser positivo. Tente novamente.")
                        continue
                    if m > 10000:  # Limite razoável
                        print("Erro: Número máximo de subintervalos é 10000. Tente novamente.")
                        continue
                    h = abs(b - a) / m
                    print(f"Calculado h = {h:.8e}")
                    break

                else:
                    print("Erro: Escolha 'h' ou 'm'. Tente novamente.")
                    continue

            except ValueError:
                print("Erro: Digite um valor numérico válido. Tente novamente.")
            except ZeroDivisionError:
                print("Erro: Intervalo [a,b] tem comprimento zero. Tente novamente.")
                continue

        xn = b

        # Solução exata opcional
        solucao_exata = None
        sol_exata_expr = ''

        while True:
            s = input("\nSolução exata y(x) (pressione Enter se não houver): ").strip()
            if not s:
                break

            sol_exata_expr = s
            try:
                # Criar função da solução exata
                x_sym = sp.symbols('x')
                expr_sol = sp.sympify(sol_exata_expr, locals=SYMPY_LOCALS)
                lam_sol = sp.lambdify(x_sym, expr_sol, modules=['numpy'])

                def solucao_exata(x):
                    try:
                        val = lam_sol(x)
                        # Converter para float se possível
                        if hasattr(val, 'item'):
                            val = val.item()
                        return float(val)
                    except Exception:
                        return float(sp.N(expr_sol.subs(x_sym, x)))

                # Teste da função
                test_val = solucao_exata(x0)
                if not np.isfinite(test_val):
                    print("Erro: A solução exata produz valor não-finito em x0. Tente novamente.")
                    continue

                print("Solução exata aceita.")
                break

            except Exception as e:
                print(f"Erro na expressão da solução exata: {e}")
                print("Tente novamente ou pressione Enter para pular.")
                continue

        return {
            'func_input': func_input,
            'a': a,
            'b': b,
            'x0': x0,
            'y0': y0,
            'h': h,
            'm': m,
            'xn': xn,
            'solucao_exata': solucao_exata,
            'sol_exata_expr': sol_exata_expr,
        }

    except KeyboardInterrupt:
        print("\n\nEntrada interrompida pelo usuário.")
        raise
    except Exception as e:
        print(f"\nErro inesperado na leitura dos dados: {e}")
        raise


def passos_edo(a, b, x0, h=None, m=None):
    """Normaliza e retorna (h, xn) dado h ou m. xn é sempre b."""
    if m is not None:
        if m <= 0:
            raise ValueError('m deve ser > 0')
        h = (b - a) / m
        xn = b
        return h, xn
    if h is None:
        raise ValueError('h ou m deve ser fornecido')
    xn = b
    return h, xn


def plotar_grafico_edo(x_vals, y_vals, solucao_exata=None, titulo='Solução da EDO'):
    try:
        import matplotlib.pyplot as plt
    except Exception:
        print("matplotlib não está disponível. Instale com 'pip install matplotlib'.")
        return
    plt.figure(figsize=(8, 4))
    plt.plot(x_vals, y_vals, marker='o', label='Aproximação')
    if solucao_exata is not None:
        xs = np.array(x_vals)
        ys_ex = [solucao_exata(x) for x in xs]
        plt.plot(xs, ys_ex, linestyle='--', label='Solução exata')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(titulo)
    plt.legend()
    plt.grid(True)
    plt.show()


def mostrar_tabela_e_grafico_edo(x_vals, y_vals, solucao_exata=None, titulo='Solução da EDO', plotar=True):
    """Mostra a tabela de pontos (x, y) e chama o plot se `plotar` for True."""
    print("\n--- Tabela de resultados ---")
    if solucao_exata is not None:
        print(f"{'x':>10} {'y_aprox':>18} {'y_exato':>18} {'erro':>12}")
        print('-' * 60)
        for xi, yi in zip(x_vals, y_vals):
            try:
                y_real = solucao_exata(xi)
                erro = abs(y_real - yi)
                print(f"{xi:10.6f} {yi:18.10f} {y_real:18.10f} {erro:12.4e}")
            except Exception:
                print(f"{xi:10.6f} {yi:18.10f} {'N/A':>18} {'N/A':>12}")
    else:
        print(f"{'x':>10} {'y':>18}")
        print('-' * 30)
        for xi, yi in zip(x_vals, y_vals):
            print(f"{xi:10.6f} {yi:18.10f}")

    # Plot opcional
    if plotar:
        plotar_grafico_edo(x_vals, y_vals, solucao_exata, titulo)


def resolver_edo_2ordem():
    print("\n=== Resolução de EDO de 2ª ordem: y'' = f(x, y, y') ===")
    print("Digite f(x, y, yp) usando x, y, yp (exemplo: yp + 2*y - x**2)")
    f_input = input("f(x, y, yp) = ").strip().replace('^', '**')
    x0 = float(input("x inicial: "))
    xf = float(input("x final: "))
    # Permitir expressões numéricas (ex: 1/2, pi/4) usando sympy
    y0_str = input("y(x0): ").strip()
    yp0_str = input("y'(x0): ").strip()
    try:
        y0 = float(sp.N(sp.sympify(y0_str)))
    except Exception:
        y0 = float(y0_str)
    try:
        yp0 = float(sp.N(sp.sympify(yp0_str)))
    except Exception:
        yp0 = float(yp0_str)
    
    print("\nComo deseja especificar o passo?")
    
    print("1 - Inserir h diretamente")
    print("2 - Inserir número de subintervalos m")
    escolha_h = input("Escolha (1 ou 2): ").strip()
    if escolha_h == '1':
        h = float(input("Digite o passo h: "))
    elif escolha_h == '2':
        m = int(input("Digite o número de subintervalos m: "))
        h = (xf - x0) / m
        print(f"Calculado h = {h}")
    else:
        print("Opção inválida. Encerrando")

    # Montar sistema equivalente: y1' = y2, y2' = f(x, y1, y2)
    # Converter y[1] -> y[0], y[2] -> y[1] na string "y[2]"
    def convert_indices(expr):
        def repl_idx(m):
            idx = int(m.group(1))
            return f'y[{idx-1}]'
        return re.sub(r'y\[(\d+)\]', repl_idx, expr)

    # Compilar f(x,y,yp) com sympy -> lambdify
    x_sym, y_sym, yp_sym = sp.symbols('x y yp')
    try:
        expr_f = sp.sympify(f_input)
        lam_f = sp.lambdify((x_sym, y_sym, yp_sym), expr_f, modules=['numpy'])
        def f2(x, y):
            return lam_f(x, y[0], y[1])
    except Exception:
        # fallback: usar eval em namespace restrito
        def f2(x, y):
            local = {"x": x, "y": y[0], "yp": y[1], "np": np, "math": math, **SAFE_MATH}
            try:
                return eval(f_input, {"__builtins__": None}, local)
            except Exception:
                return eval(f_input)

    # Montar as funções do sistema: y1' = y2, y2' = f(x,y,yp)
    funcs_input = [lambda x, y: y[1], f2]
    # y[1] = y, y[2] = y'
    y_ini = [y0, yp0]
    # Adaptar runge_kutta_sistema para aceitar função direta no segundo termo
    def runge_kutta_sistema_2ordem(funcs_input, y0, x0, xf, h, ordem):
        n = len(y0)
        t_vals = [x0]
        u_vals = [np.array(y0)]
        # preparar func0 (caso seja string) para avaliação segura
        if isinstance(funcs_input[0], str):
            expr0 = funcs_input[0].strip().replace('^', '**').replace(' ', '')
            expr0_named = re.sub(r'y\[(\d+)\]', lambda m: f'y{m.group(1)}', expr0)
            y_symbols0 = sp.symbols(' '.join([f'y{i+1}' for i in range(n)]))
            x_sym0 = sp.symbols('x')
            locals_map0 = {'x': x_sym0}
            for i, ys in enumerate(y_symbols0):
                locals_map0[f'y{i+1}'] = ys
            try:
                expr0_sym = sp.sympify(expr0_named, locals=locals_map0)
                lam0 = sp.lambdify((x_sym0, ) + tuple(y_symbols0), expr0_sym, modules=['numpy'])
                def func0_callable(x, y):
                    return lam0(x, *tuple(y.tolist() if hasattr(y, 'tolist') else list(y)))
            except Exception:
                def func0_callable(x, y):
                    local = {'x': x, 'y': y, 'np': np, 'math': math, **SAFE_MATH}
                    try:
                        return eval(expr0, {"__builtins__": None}, local)
                    except Exception:
                        return eval(expr0)
        else:
            func0_callable = funcs_input[0]

        while t_vals[-1] < xf:
            x = t_vals[-1]
            y = u_vals[-1]
            step = min(h, xf - x)
            # Evitar passo nulo que causaria loop infinito
            if step <= 0:
                print("Passo nulo ou intervalo concluído; interrompendo resolução do sistema de 2ª ordem.")
                break
            if ordem == 1:
                k1 = np.array([
                        func0_callable(x, y),
                    funcs_input[1](x, y)
                ])
                y_new = y + step * k1
            elif ordem == 2:
                k1 = np.array([func0_callable(x, y), funcs_input[1](x, y)])
                k2 = np.array([
                    func0_callable(x+step, y+step*k1), funcs_input[1](x+step, y+step*k1)
                ])
                y_new = y + 0.5 * step * (k1 + k2)
            elif ordem == 3:
                k1 = np.array([func0_callable(x, y), funcs_input[1](x, y)])
                k2 = np.array([
                    func0_callable(x+step/2, y+step*k1/2), funcs_input[1](x+step/2, y+step*k1/2)
                ])
                k3 = np.array([
                    func0_callable(x+step, y-step*k1+2*step*k2), funcs_input[1](x+step, y-step*k1+2*step*k2)
                ])
                y_new = y + (step/6) * (k1 + 4*k2 + k3)
            elif ordem == 4:
                k1 = np.array([func0_callable(x, y), funcs_input[1](x, y)])
                k2 = np.array([
                    func0_callable(x+step/2, y+step*k1/2), funcs_input[1](x+step/2, y+step*k1/2)
                ])
                k3 = np.array([
                    func0_callable(x+step/2, y+step*k2/2), funcs_input[1](x+step/2, y+step*k2/2)
                ])
                k4 = np.array([
                    func0_callable(x+step, y+step*k3), funcs_input[1](x+step, y+step*k3)
                ])
                y_new = y + (step/6) * (k1 + 2*k2 + 2*k3 + k4)
            x_next = x + step
            t_vals.append(x_next)
            u_vals.append(y_new)
        return t_vals, np.array(u_vals)

    print("\nEscolha a ordem do método de Runge-Kutta:")
    print("1 - Euler (RK1)")
    print("2 - RK2")
    print("3 - RK3")
    print("4 - RK4")
    ordem = int(input("Ordem (1-4): "))
    t_vals, u_vals = runge_kutta_sistema_2ordem(funcs_input, y_ini, x0, xf, h, ordem)
    print("\nTabela de resultados:")
    print("x\ty(x)\ty'(x)")
    for i in range(len(t_vals)):
        print(f"{t_vals[i]:.6f}\t{u_vals[i][0]:.6f}\t{u_vals[i][1]:.6f}")
    # Perguntar se o usuário deseja ver o gráfico
    try:
        resp = input("Deseja plotar o gráfico da solução? [s/n]: ").strip().lower()
        if resp.startswith('s'):
            plt.figure(figsize=(10, 5))
            plt.plot(t_vals, u_vals[:, 0], label="y(x)", marker='o')
            plt.plot(t_vals, u_vals[:, 1], label="y'(x)", marker='s')
            plt.xlabel('x')
            plt.ylabel('Soluções')
            plt.title('Solução da EDO de 2ª ordem')
            plt.legend()
            plt.grid(True)
            plt.show()
    except Exception:
        # Se houver erro na leitura (por ex. EOF em testes), não plotar por padrão
        pass
        plt.show()



def runge_kutta(func_input, x0, y0, h, xn, ordem):
    """Resolve EDOs escalares usando métodos de Runge-Kutta de ordem 1 a 4.

    Esta função implementa os métodos de Runge-Kutta para resolver numericamente
    equações diferenciais ordinárias da forma dy/dx = f(x,y). Os métodos
    implementados vão da ordem 1 (Euler) até a ordem 4 (Runge-Kutta clássico).

    Parameters
    ----------
    func_input : str
        Expressão matemática para f(x, y) como string. Deve ser uma função
        válida das variáveis x e y. Exemplos: 'y', 'y - x**2', 'sin(x)*y'.
        Espaços são ignorados e '^' é convertido para '**'.
    x0 : float
        Ponto inicial da integração (condição inicial para x).
        Deve ser um número finito.
    y0 : float
        Valor inicial y(x0). Deve ser um número finito.
    h : float
        Tamanho do passo de integração. Deve ser positivo e dividir
        exatamente o intervalo (xn - x0), caso contrário será truncado.
    xn : float
        Ponto final da integração. Deve ser diferente de x0.
    ordem : int
        Ordem do método Runge-Kutta. Deve ser 1, 2, 3 ou 4:
        - 1: Método de Euler (primeira ordem)
        - 2: Euler modificado (segunda ordem)
        - 3: Runge-Kutta de terceira ordem
        - 4: Runge-Kutta clássico (quarta ordem)

    Returns
    -------
    x_vals : list of float
        Lista dos pontos x onde a solução foi calculada, incluindo x0 e xn.
    y_vals : list of float
        Lista dos valores aproximados y(x) correspondentes aos pontos em x_vals.

    Raises
    ------
    ValueError
        Se os parâmetros forem inválidos (ver _validate_edo_inputs).
    TypeError
        Se os tipos de entrada não forem adequados.
    RuntimeError
        Se ocorrer erro durante a avaliação da função f(x,y).

    Notes
    -----
    Os métodos de Runge-Kutta seguem as fórmulas clássicas (Euler, Euler modificado e RK4).
    Por exemplo, para Euler: ``y_{n+1} = y_n + h * f(x_n, y_n)``.
    Para RK4: ``y_{n+1} = y_n + (h/6) * (k1 + 2*k2 + 2*k3 + k4)``, onde ``k1``..``k4``
    são os incrementos padrões do método.
    A estabilidade e precisão aumentam com a ordem do método, mas também
    o custo computacional.

    Examples
    --------
    >>> # Resolver dy/dx = y com y(0) = 1 no intervalo [0, 1]
    >>> x_vals, y_vals = runge_kutta('y', 0, 1, 0.1, 1, 4)
    >>> print(f"Solução em x=1: {y_vals[-1]:.6f}")  # Aproxima e^1 ≈ 2.718282

    >>> # EDO não-linear: dy/dx = y - x²
    >>> x_vals, y_vals = runge_kutta('y - x**2', 0, 1, 0.1, 1, 2)
    """
    # Validações de entrada
    func_input, x0, y0, h, xn = _validate_edo_inputs(func_input, x0, y0, h, xn, ordem)

    # Preparar a expressão da função
    func_input = func_input.replace(' ', '')  # Remove espaços
    func_input = re.sub(r'(\d)([xy])', r'\1*\2', func_input)  # Corrigir multiplicação implícita

    # Criar função f(x,y) com fallbacks robustos
    try:
        f = _create_function_from_string(func_input, ['x', 'y'], verbose=False)
    except Exception as e:
        raise ValueError(f"Não foi possível criar a função f(x,y) a partir de '{func_input}': {e}")

    # Calcular número de passos
    n_steps = int((xn - x0) / h)

    # Avisar se o passo não divide exatamente o intervalo
    remainder = abs(xn - x0) - n_steps * h
    if remainder > 1e-10:
        print(f"Aviso: O passo h={h} não divide exatamente o intervalo [{x0}, {xn}]. "
              f"Será integrado até x={x0 + n_steps * h:.6f} em {n_steps} passos.")

    # Inicializar listas de resultados
    x_vals = []
    y_vals = []
    x = float(x0)
    y = float(y0)
    x_vals.append(x)
    y_vals.append(y)

    # Loop principal de integração
    for step in range(n_steps):
        try:
            if ordem == 1:
                # Método de Euler
                y_new = y + h * f(x, y)

            elif ordem == 2:
                # Euler Modificado (Runge-Kutta 2ª ordem)
                k1 = h * f(x, y)
                k2 = h * f(x + h, y + k1)
                y_new = y + 0.5 * (k1 + k2)

            elif ordem == 3:
                # Runge-Kutta 3ª ordem
                k1 = h * f(x, y)
                k2 = h * f(x + h/2, y + k1/2)
                k3 = h * f(x + h, y - k1 + 2*k2)
                y_new = y + (1/6) * (k1 + 4*k2 + k3)

            elif ordem == 4:
                # Runge-Kutta 4ª ordem (clássico)
                k1 = h * f(x, y)
                k2 = h * f(x + h/2, y + k1/2)
                k3 = h * f(x + h/2, y + k2/2)
                k4 = h * f(x + h, y + k3)
                y_new = y + (1/6) * (k1 + 2*k2 + 2*k3 + k4)

            # Verificar se o resultado é finito
            if not np.isfinite(y_new):
                raise RuntimeError(f"Resultado não-finito no passo {step+1}: y = {y_new}")

            # Atualizar valores
            y = y_new
            x += h

            x_vals.append(x)
            y_vals.append(y)

        except Exception as e:
            raise RuntimeError(f"Erro na integração no passo {step+1} (x={x:.6f}, y={y:.6f}): {e}")

    return x_vals, y_vals

def executar_runge_kutta(ordem):
    nomes = {
        1: "Runge-Kutta 1ª ordem (Euler)",
        2: "Runge-Kutta 2ª ordem (Euler Modificado)",
        3: "Runge-Kutta 3ª ordem",
        4: "Runge-Kutta 4ª ordem (Euler Melhorado)"
    }
    print(f"\n--- {nomes.get(ordem, 'Runge-Kutta')} ---")
    try:
        dados = coletar_dados_edo()
        func_input = dados['func_input']
        a = dados['a']
        b = dados['b']
        x0 = dados['x0']
        y0 = dados['y0']
        h = dados['h']
        m = dados['m']
        xn = dados['xn']
        solucao_exata = dados['solucao_exata']
        h, xn = passos_edo(a, b, x0, h=h, m=m)
        x_vals, y_vals = runge_kutta(func_input, x0, y0, h, xn, ordem)

        # Perguntar ao usuário se deseja plotar
        plotar = False
        try:
            resp = input("Deseja plotar os gráficos? [s/n]: ").strip().lower()
            plotar = resp.startswith('s')
        except Exception:
            # Em ambiente sem stdin/EOF (ex.: testes automatizados), não plotar
            plotar = False

        # Exibir tabela e (opcionalmente) gráfico
        titulo = nomes.get(ordem, 'Runge-Kutta')
        mostrar_tabela_e_grafico_edo(x_vals, y_vals, solucao_exata, titulo, plotar=plotar)

    except Exception as e:
        print(f"Erro: {e}")

# === NOVAS FUNÇÕES PARA SISTEMAS DE EDOS ===

def runge_kutta_sistema(funcs_input, u0, t0, tf, h, ordem):
    """Resolve sistemas de EDOs usando métodos de Runge-Kutta vetoriais.

    Esta função resolve numericamente sistemas de equações diferenciais ordinárias
    da forma dy/dt = f(t,y), onde y é um vetor de variáveis dependentes.
    Implementa os métodos de Runge-Kutta de ordem 1 a 4 para sistemas.

    Parameters
    ----------
    funcs_input : list of str
        Lista de expressões matemáticas para as funções f_i(t, y) do sistema.
        Cada string deve usar notação y[1], y[2], ... para as variáveis
        (indexação 1-based). Exemplo: ['y[2]', 'y[1] - y[2]'].
    u0 : array_like
        Vetor de condições iniciais y(t0). Deve ter o mesmo comprimento
        que funcs_input. Todos os valores devem ser finitos.
    t0 : float
        Tempo inicial da integração. Deve ser finito.
    tf : float
        Tempo final da integração. Deve ser diferente de t0.
    h : float
        Tamanho do passo de integração. Deve ser positivo.
    ordem : int
        Ordem do método Runge-Kutta (1, 2, 3 ou 4).

    Returns
    -------
    t_vals : list of float
        Lista dos pontos temporais onde a solução foi calculada,
        incluindo t0 e tf (aproximadamente).
    u_vals : ndarray
        Array de shape (n_pontos, n_equacoes) contendo os valores
        da solução em cada ponto temporal.

    Raises
    ------
    ValueError
        Se as entradas não forem válidas (ver _validate_sistema_edo_inputs).
    TypeError
        Se os tipos de entrada não forem adequados.
    RuntimeError
        Se ocorrer erro durante a integração do sistema.

    Notes
    -----
    O sistema é resolvido usando a formulação vetorial dos métodos de Runge-Kutta.
    Em termos práticos, aplica-se a versão vetorial das fórmulas escalares (Euler,
    RK2/3/4). Por exemplo, em RK4 cada :math:`k_i` é um vetor de incrementos e
    a combinação final segue a soma ponderada usual: ``y_{n+1} = y_n + (h/6)*(k1+2*k2+2*k3+k4)``.

    Examples
    --------
    >>> # Sistema linear: dy1/dt = y2, dy2/dt = -y1
    >>> funcs = ['y[2]', '-y[1]']
    >>> y0 = [1, 0]  # y1(0)=1, y2(0)=0
    >>> t_vals, y_vals = runge_kutta_sistema(funcs, y0, 0, 2*np.pi, 0.1, 4)
    >>> # y_vals[-1] ≈ [cos(2π), -sin(2π)] ≈ [1, 0]
    """
    # Validações de entrada
    funcs_input, u0, t0, tf, h = _validate_sistema_edo_inputs(funcs_input, u0, t0, tf, h, ordem)

    n_equacoes = len(u0)

    # Preparar funções do sistema
    funcs = []
    for i, func_input in enumerate(funcs_input):
        expr = func_input.strip().replace('^', '**').replace(' ', '')

        # Substituir y[1], y[2], ... por y1, y2, ... (variáveis simbólicas)
        def repl_idx_name(m):
            idx = int(m.group(1))
            if idx < 1 or idx > n_equacoes:
                raise ValueError(f"Índice y[{idx}] fora do intervalo válido [1, {n_equacoes}]")
            return f'y{idx}'

        expr_named = re.sub(r'y\[(\d+)\]', repl_idx_name, expr)

        # Expressão preparada para compilação (não imprimir em execução normal)

        # Criar símbolos: x (tempo) e y1, y2, ... (variáveis do sistema)
        y_symbols = sp.symbols(' '.join([f'y{j+1}' for j in range(n_equacoes)]))
        x_sym = sp.symbols('x')

        # Mapear nomes para símbolos
        locals_map = {'x': x_sym}
        for j, ys in enumerate(y_symbols):
            locals_map[f'y{j+1}'] = ys

        try:
            # Tentar criar função com SymPy
            expr_sym = sp.sympify(expr_named, locals=locals_map)
            lam = sp.lambdify((x_sym,) + tuple(y_symbols), expr_sym, modules=['numpy'])

            def func(x, y, lam=lam, idx=i):
                # y é array-like; passar cada componente como argumento
                return lam(x, *tuple(y.tolist() if hasattr(y, 'tolist') else list(y)))

            funcs.append(func)

        except Exception as e:
            # Fallback para eval com ambiente restrito
            try:
                def func(x, y, expr_str=expr_named, idx=i):
                    # Criar dicionário local com x e componentes de y
                    local_vars = {'x': x, 'np': np, 'math': math, **SAFE_MATH}
                    for j in range(n_equacoes):
                        local_vars[f'y{j+1}'] = y[j]

                    try:
                        return eval(expr_str, {"__builtins__": None}, local_vars)
                    except Exception:
                        return eval(expr_str)

                funcs.append(func)

            except Exception as fallback_error:
                raise ValueError(f"Não foi possível criar função {i+1} a partir de '{func_input}': "
                               f"SymPy: {e}, Fallback: {fallback_error}")

    # Inicializar resultados
    t_vals = [float(t0)]
    u_vals = [u0.copy()]

    # Loop de integração
    t_current = float(t0)
    u_current = u0.copy()

    while t_current < tf:
        # Calcular passo atual (último passo pode ser menor)
        step = min(h, tf - t_current)

        # Evitar passo nulo
        if step <= 1e-15:
            break

        try:
            if ordem == 1:
                # Método de Euler
                k1 = np.array([f(t_current, u_current) for f in funcs])
                u_new = u_current + step * k1

            elif ordem == 2:
                # Runge-Kutta 2ª ordem
                k1 = np.array([f(t_current, u_current) for f in funcs])
                k2 = np.array([f(t_current + step, u_current + step * k1) for f in funcs])
                u_new = u_current + 0.5 * step * (k1 + k2)

            elif ordem == 3:
                # Runge-Kutta 3ª ordem
                k1 = np.array([f(t_current, u_current) for f in funcs])
                k2 = np.array([f(t_current + step/2, u_current + step*k1/2) for f in funcs])
                k3 = np.array([f(t_current + step, u_current - step*k1 + 2*step*k2) for f in funcs])
                u_new = u_current + (step/6) * (k1 + 4*k2 + k3)

            elif ordem == 4:
                # Runge-Kutta 4ª ordem
                k1 = np.array([f(t_current, u_current) for f in funcs])
                k2 = np.array([f(t_current + step/2, u_current + step*k1/2) for f in funcs])
                k3 = np.array([f(t_current + step/2, u_current + step*k2/2) for f in funcs])
                k4 = np.array([f(t_current + step, u_current + step*k3) for f in funcs])
                u_new = u_current + (step/6) * (k1 + 2*k2 + 2*k3 + k4)

            # Verificar se os resultados são finitos
            if not np.all(np.isfinite(u_new)):
                raise RuntimeError(f"Resultado não-finito no tempo t={t_current:.6f}")

            # Atualizar valores
            t_current += step
            u_current = u_new

            t_vals.append(t_current)
            u_vals.append(u_current.copy())

        except Exception as e:
            raise RuntimeError(f"Erro na integração em t={t_current:.6f}: {e}")

    return t_vals, np.array(u_vals)

def executar_sistema_edos():
    """
    Interface para resolução de sistemas de EDOs usando Runge-Kutta.
    """
    try:
        # Pedir ordem do método RK
        ordem = int(input("Digite a ordem do método de Runge-Kutta (1-4): "))
        if not 1 <= ordem <= 4:
            print("Ordem deve estar entre 1 e 4.")
            return
        
        # Pedir número de equações
        n = int(input("Digite o número de equações no sistema: "))
        if n < 1:
            print("Número de equações deve ser pelo menos 1.")
            return
        
        # Pedir as funções do sistema
        print(f"\nDigite as {n} funções do sistema dy[i]/dx = f_i(x, y)")
        print("Exemplo: 2*y[1] - y[2] - x  (use y[1] para a primeira variável, y[2] para a segunda, etc.)")
        funcs_input = []
        for i in range(n):
            func = input(f"f{i}(x, y) = ")
            funcs_input.append(func)
        
        # Pedir condições iniciais
        print(f"\nDigite as {n} condições iniciais y[i](0):")
        y0 = []
        for i in range(n):
            yi = float(input(f"y[{i+1}](0) = "))
            y0.append(yi)
        y0 = np.array(y0)
        
        # Pedir intervalo temporal
        x0 = float(input("Digite o valor inicial de x (x0): "))
        xf = float(input("Digite o valor final de x (xf): "))
        print("\nComo deseja especificar o passo?")
        print("1 - Inserir h diretamente")
        print("2 - Inserir número de subintervalos m")
        escolha_h = input("Escolha (1 ou 2): ").strip()
        if escolha_h == '1':
            h = float(input("Digite o passo h: "))
            if h <= 0:
                print("Passo h inválido (<=0). Encerrando esta execução.")
                return
        elif escolha_h == '2':
            m = int(input("Digite o número de subintervalos m: "))
            if m <= 0:
                print("Número de subintervalos inválido (<=0). Encerrando esta execução.")
                return
            h = (xf - x0) / m
            print(f"Calculado h = {h}")
        else:
            print("Opção inválida, usando h=0.1")
            h = 0.1
        
        
        # Resolver o sistema
        t_vals, u_vals = runge_kutta_sistema(funcs_input, y0, x0, xf, h, ordem)
        u_vals = np.array(u_vals)
        n = u_vals.shape[1] if len(u_vals.shape) > 1 else 1
        # Exibir resultados em tabela
        print(f"\nMétodo: Runge-Kutta {ordem}ª ordem")
        header = "x\t" + "\t".join([f"y[{i+1}]" for i in range(n)])
        print(header)
        for i in range(len(t_vals)):
            linha = f"{t_vals[i]:.6f}"
            for j in range(n):
                linha += f"\t{u_vals[i][j]:.6f}"
            print(linha)
        
        
        # Perguntar se deseja plotar os gráficos do sistema
        try:
            resp = input("Deseja plotar os gráficos do sistema? [s/n]: ").strip().lower()
            if resp.startswith('s'):
                plt.figure(figsize=(10, 6))
                for j in range(n):
                    plt.plot(t_vals, u_vals[:, j], label=f'y[{j+1}](x)', marker='o', markersize=2)
                plt.xlabel('x')
                plt.ylabel('y[j]')
                plt.title(f'Solução do Sistema de EDOs - RK{ordem}')
                plt.legend()
                plt.grid(True)
                plt.show()
        except Exception:
            # Em ambiente não-interativo, não mostrar gráficos por padrão
            pass
        
    except Exception as e:
        print(f"Erro: {e}")

def executar_edo_2ordem():
    """
    Interface para resolução de EDOs de 2ª ordem convertidas em sistemas.
    """
    try:
        # Pedir ordem do método RK
        ordem = int(input("Digite a ordem do método de Runge-Kutta (1-4): "))
        if not 1 <= ordem <= 4:
            print("Ordem deve estar entre 1 e 4.")
            return
        
        print("\n--- EDO de 2ª Ordem ---")
        print("Digite a EDO na forma: d²y/dx² = f(x, y, y')")
        
        # Entrada da função
        print("Digite f(x, y, y') (use y para y e yp para y'):")
        f_input = input("f(x, y, yp) = ").strip()
        
        # Preprocessar: substituir y por u[0], yp por u[1]
        f_input = f_input.replace('y', 'u[0]').replace('yp', 'u[1]')
        
        # Condições iniciais
        x0 = float(input("Digite x inicial: "))
        y0 = float(input("Digite y(x0): "))
        yp0 = float(input("Digite y'(x0): "))
        
        # Intervalo temporal
        xf = float(input("Digite x final: "))
        h = float(input("Digite o passo h: "))
        if h <= 0:
            print("Passo h inválido (<=0). Encerrando esta execução.")
            return
        
        # Converter para sistema
        funcs_input = ['u[1]', f_input]  # dy1/dx = y2, dy2/dx = f
        u0 = [y0, yp0]
        
        # Resolver usando o método de sistemas
        t_vals, u_vals = runge_kutta_sistema(funcs_input, u0, x0, xf, h, ordem)
        
        # Exibir resultados
        print(f"\nSolução da EDO de 2ª ordem:")
        # Use double-quoted string literal inside f-string expression to avoid backslash in expressions
        print(f"{'x':>10} {'y':>15} {"y'":>15}")
        print("-" * 40)
        
        for i, (x, u) in enumerate(zip(t_vals, u_vals)):
            print(f"{x:10.4f} {u[0]:15.8f} {u[1]:15.8f}")
        
        # Perguntar se deseja plotar os gráficos
        try:
            resp = input("Deseja plotar os gráficos? [s/n]: ").strip().lower()
            if resp.startswith('s'):
                plt.figure(figsize=(12, 5))
                plt.subplot(1, 2, 1)
                plt.plot(t_vals, u_vals[:, 0], 'b-', marker='o', markersize=3, label='y(x)')
                plt.xlabel('x')
                plt.ylabel('y')
                plt.title('Solução y(x)')
                plt.grid(True)
                plt.legend()

                plt.subplot(1, 2, 2)
                plt.plot(t_vals, u_vals[:, 1], 'r-', marker='s', markersize=3, label='y\'(x)')
                plt.xlabel('x')
                plt.ylabel("y'")
                plt.title("Derivada y'(x)")
                plt.grid(True)
                plt.legend()

                plt.tight_layout()
                plt.show()
        except Exception:
            # Em ambiente não-interativo (tests), não plotar por padrão
            pass
        
    except Exception as e:
        print(f"Erro: {e}")

def menu_principal():
    while True:
        print("\n===== MENU DE EQUAÇÕES DIFERENCIAIS =====")
        print("1 - Método de Euler (Runge-Kutta 1ª ordem)")
        print("2 - Método de Runge-Kutta (2ª, 3ª ou 4ª ordem)")
        print("3 - Sistemas de EDOs")
        print("4 - Equações Diferenciais de 2ª Ordem")
        print("0 - Sair")   

        opcao = input("Escolha uma opção: ")
        if opcao == '0':
            print("Encerrando o programa.")
            break
        
        if opcao == '1':
            executar_runge_kutta(1)
        elif opcao == '2':
            try:
                ordem = int(input("Digite a ordem do método de Runge-Kutta (2-4): "))
                if 2 <= ordem <= 4:
                    executar_runge_kutta(ordem)
                else:
                    print("Ordem deve estar entre 2 e 4.")
            except ValueError:
                print("Entrada inválida. Digite um número inteiro.")
        elif opcao == '3':
            executar_sistema_edos()
        elif opcao == '4':
            resolver_edo_2ordem()
        else:
            print("Opção inválida.")


def dados():
    """Menu interativo para métodos de resolução de EDOs."""
    print("\n===== MENU DE EQUAÇÕES DIFERENCIAIS =====")
    print("1 - Método de Euler (Runge-Kutta 1ª ordem)")
    print("2 - Método de Runge-Kutta (2ª, 3ª ou 4ª ordem)")
    print("3 - Sistemas de EDOs")
    print("4 - Equações Diferenciais de 2ª Ordem")
    print("0 - Voltar ao menu principal")
    opcao = input("Escolha uma opção: ")
    return opcao


if __name__ == "__main__":
    # Entrada principal deslocada para o menu global no final do arquivo
    pass

"""
Módulo para métodos de busca de raízes de equações.

Este módulo implementa algoritmos numéricos para encontrar raízes de
funções: bisseção, Newton-Raphson e secante.

Author: Pedro Henrique Rocha de Andrade
Date: Fevereiro 2026
"""

import matplotlib.pyplot as plt
import numpy as np
import math

# Função para converter a string em função executável (avaliação segura, restrita)
def f(x, func_str):
    """Avalia `func_str` em `x` com ambiente seguro (sem builtins).

    Parameters
    ----------
    x : float
        Valor de avaliação.
    func_str : str
        Expressão Python da função em x (ex.: 'x**2 - 4').

    Returns
    -------
    float
        Valor de f(x).

    Raises
    ------
    ValueError
        Em caso de erro na avaliação.
    """
    # Funções matemáticas permitidas (do módulo math)
    safe_math = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
    try:
        return eval(func_str, {"__builtins__": None}, {"x": x, "math": math, **safe_math})
    except Exception as e:
        raise ValueError(f"Erro ao avaliar função em x={x}: {e}")

# Função para plotar gráfico
def plotar_funcao(func_str, a=None, b=None, raiz=None, grafico=None, verbose=False, title=None):
    """Plota a função `f(x)` opcionalmente mostrando a raiz.

    Parameters
    ----------
    func_str : str
        Expressão Python de ``f(x)``.
    a, b : float, optional
        Intervalo de plotagem (padrão: [-10, 10] se None).
    raiz : float, optional
        Ponto da raiz a ser destacado.
    grafico : bool or None, optional
        Controla se o gráfico será exibido. Se None, segue ``verbose`` (True mostra o gráfico).
    verbose : bool, optional
        Habilita saídas e, por padrão, ativa o gráfico.
    """
    if grafico is None:
        grafico = bool(verbose)

    if a is None or b is None:
        a, b = -10, 10

    if not grafico:
        return

    x_vals = np.linspace(a, b, 400)
    # avalia ponto-a-ponto usando nossa função segura
    y_vals = []
    for xv in x_vals:
        try:
            y_vals.append(f(xv, func_str))
        except Exception:
            y_vals.append(float('nan'))

    plt.figure()
    plt.axhline(0, color="black", linewidth=1)
    plt.axvline(0, color="black", linewidth=1)
    # Ajusta legenda para não cortar
    label_fx = f"f(x) = {func_str}"
    if len(label_fx) > 40:
        label_fx = "f(x)"
    # Plota apenas a função
    plt.plot(x_vals, y_vals, label=label_fx)

    # Adiciona tracejado e ponto na raiz, ambos com a mesma label
    if raiz is not None:
        try:
            y_raiz = f(raiz, func_str)
            plt.axvline(raiz, color="red", linestyle="--", linewidth=1, label=f"Raiz ≈ {str(raiz)}")
            plt.scatter(raiz, y_raiz, color="red", zorder=5)
        except Exception:
            pass

    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend(loc='best')
    # Título customizável vindo do menu
    if title is not None:
        try:
            plt.title(title)
        except Exception:
            pass
    plt.grid(True)
    try:
        plt.show()
    except Exception:
        if verbose:
            print("Aviso: matplotlib não conseguiu exibir o gráfico.")

# Método da Bisseção
def bissecao(func_str, a, b, tol, max_iter, verbose=False, grafico=None):
    """Método da bisseção para encontrar raiz de uma função dada por string.

    Parameters
    ----------
    func_str : str
        Expressão Python de ``f(x)`` (ex.: ``'x**2 - 4'``).
    a, b : float
        Intervalo inicial [a, b] com sinais opostos.
    tol : float
        Tolerância para critério de parada.
    max_iter : int
        Número máximo de iterações.
    verbose : bool, optional
        Se ``True``, imprime detalhes de cada iteração e ativa o gráfico por padrão.
    grafico : bool or None, optional
        Controla plotagem: se ``None`` e ``verbose`` for True, o gráfico é mostrado.

    Returns
    -------
    (float, int)
        Tupla (raiz_aproximada, n_iter) ou (None, 0) se os sinais em a/b não forem opostos.
    """
    # Validação básica de tipos/valores
    try:
        a = float(a); b = float(b); tol = float(tol); max_iter = int(max_iter)
    except Exception:
        raise TypeError("a, b, tol devem ser numéricos e max_iter deve ser inteiro")
    if verbose:
        print(f"\nCritério de parada: b-a < {tol}")

    if grafico is None:
        grafico = bool(verbose)

    try:
        fa = f(a, func_str)
        fb = f(b, func_str)
    except Exception as e:
        print(f"Erro na avaliação nos extremos: {e}")
        return None, 0

    if fa * fb >= 0:
        print("Erro: f(a) e f(b) devem ter sinais opostos.")
        return None, 0

    iteracoes = []
    c_ant = None
    a_atual, b_atual = a, b
    for i in range(max_iter):
        intervalo = abs(b_atual - a_atual)
        # calcula o ponto médio e seu f antes de verificar critério
        c = (a_atual + b_atual) / 2
        try:
            fc = f(c, func_str)
        except Exception as e:
            print(f"Erro ao avaliar f(c): {e}")
            return None, i
        iteracoes.append((i, c, fc, intervalo))
        if verbose:
            print(f"[Bisseção] Iter {i}: x = {str(c)}, f(x) = {str(fc)}, b-a = {str(intervalo)}")
        # Se f(c) for praticamente zero, encontramos a raiz exata
        try:
            is_zero = abs(float(fc)) < 1e-12
        except Exception:
            is_zero = False
        if is_zero:
            if verbose:
                print("\nTabela de iterações (Bisseção):")
                print(f"{'i':>3} {'xi':>24} {'f(xi)':>24} {'b-a':>24}")
                for it in iteracoes:
                    print(f"{it[0]:3d} {str(it[1]):>24} {str(it[2]):>24} {str(it[3]):>24}")
                print(f"\nRaiz aproximada: {str(c)}")
                print(f"Iterações realizadas: {i+1}")
            return c, i+1
        # Critério: apenas o tamanho do intervalo
        if intervalo < tol:
            if verbose:
                print("\nTabela de iterações (Bisseção):")
                print(f"{'i':>3} {'xi':>24} {'f(xi)':>24} {'b-a':>24}")
                for it in iteracoes:
                    print(f"{it[0]:3d} {str(it[1]):>24} {str(it[2]):>24} {str(it[3]):>24}")
                print(f"\nRaiz aproximada: {c}")
                print(f"Iterações realizadas: {i+1}")
            return c, i+1
        # atualiza intervalo para próxima iteração
        if fa * fc < 0:
            b_atual = c
            fb = fc
        else:
            a_atual = c
            fa = fc
        c_ant = c
    if verbose:
        print("\nTabela de iterações (Bisseção):")
        print(f"{'i':>3} {'xi':>12} {'f(xi)':>12} {'b-a':>12}")
        for it in iteracoes:
            intervalo_str = f"{it[3]:.8f}"
            print(f"{it[0]:3d} {it[1]:12.6f} {it[2]:12.6f} {intervalo_str:>12}")
        print(f"\nRaiz aproximada: {c}")
        print(f"Iterações realizadas: {max_iter}")
    return c, max_iter

# Método de Newton-Raphson
def newton(func_str, x0, tol, max_iter, verbose=False, a=None, b=None):
    """Método de Newton-Raphson para encontrar raiz de função dada por string.

    Parameters
    ----------
    func_str : str
        Expressão Python de ``f(x)``.
    x0 : float
        Chute inicial.
    tol : float
        Tolerância para critério de parada.
    max_iter : int
        Número máximo de iterações.
    verbose : bool, optional
        Se True imprime detalhes de cada iteração.

    Returns
    -------
    (float, int)
        Tupla (raiz_aproximada, n_iter) ou (None, n_iter) se houver erro.
    """
    try:
        x0 = float(x0); tol = float(tol); max_iter = int(max_iter)
    except Exception:
        raise TypeError("x0 and tol must be numeric, max_iter integer")
    if verbose:
        print(f"\nCritério de parada: |xi-xi-1| < {tol}")

    h = 1e-6
    iteracoes = []
    x_ant = x0
    for i in range(1, max_iter + 1):
        try:
            fx = f(x0, func_str)
            dfx = (f(x0 + h, func_str) - f(x0 - h, func_str)) / (2 * h)
        except Exception as e:
            print(f"Erro ao avaliar função/derivada: {e}")
            return None, i
        if dfx == 0:
            print("Erro: derivada zero.")
            return None, i
        x1 = x0 - fx / dfx
        delta = abs(x1 - x0)
        iteracoes.append((i-1, x0, fx, delta))
        if verbose:
            try:
                print(f"[Newton] Iter {i-1}: x = {str(x0)}, f(x) = {str(fx)}, |xi-xi-1| = {str(delta)}")
            except Exception:
                print(f"[Newton] Iter {i-1}: x = {str(x0)}, f(x) = <erro na avaliação>")
        if delta < tol:
            if verbose:
                print("\nTabela de iterações (Newton-Raphson):")
                print(f"{'i':>3} {'xi':>24} {'f(xi)':>24} {'|xi-xi-1|':>24}")
                for it in iteracoes:
                    print(f"{it[0]:3d} {str(it[1]):>24} {str(it[2]):>24} {str(it[3]):>24}")
                print(f"\nRaiz aproximada: {str(x1)}")
                print(f"Iterações realizadas: {i}")
            return x1, i
        x0 = x1
    if verbose:
        print("\nTabela de iterações (Newton-Raphson):")
        print(f"{'i':>3} {'xi':>24} {'f(xi)':>24} {'|xi-xi-1|':>24}")
        for it in iteracoes:
            print(f"{it[0]:3d} {str(it[1]):>24} {str(it[2]):>24} {str(it[3]):>24}")
        print(f"\nRaiz aproximada: {str(x0)}")
        print(f"Iterações realizadas: {max_iter}")
    return x0, max_iter

# Método da Secante
def secante(func_str, x0, x1, tol, max_iter, verbose=False, a=None, b=None):
    """Método da secante para encontrar raiz de função dada por string.

    Parameters
    ----------
    func_str : str
        Expressão Python de ``f(x)``.
    x0, x1 : float
        Dois chutes iniciais.
    tol : float
        Tolerância para critério de parada.
    max_iter : int
        Número máximo de iterações.
    verbose : bool, optional
        Se True imprime detalhes de cada iteração.

    Returns
    -------
    (float, int)
        Tupla (raiz_aproximada, n_iter) ou (None, n_iter) em caso de erro.
    """
    try:
        x0 = float(x0); x1 = float(x1); tol = float(tol); max_iter = int(max_iter)
    except Exception:
        raise TypeError("x0, x1, tol devem ser numéricos e max_iter deve ser inteiro")
    if verbose:
        print(f"\nCritério de parada: |xi-xi-1| < {tol}")

    iteracoes = []
    fx0 = f(x0, func_str)
    fx1 = f(x1, func_str)
    iteracoes.append((0, x0, fx0, float('nan')))
    iteracoes.append((1, x1, fx1, abs(x1 - x0)))
    # Começa as iterações a partir do terceiro valor (índice 2)
    for iter_count in range(2, max_iter + 1):
        # atualiza checagem de divisão por zero
        if fx1 - fx0 == 0:
            print("Erro: divisão por zero.")
            return None, iter_count - 1
        x2 = (x0 * fx1 - x1 * fx0) / (fx1 - fx0)
        fx2 = f(x2, func_str)
        delta = abs(x2 - x1)
        iteracoes.append((iter_count, x2, fx2, delta))
        if verbose:
            try:
                print(f"[Secante] Iter {iter_count-2}: x = {x2}, f(x) = {fx2}, |xi-xi-1| = {delta}")
            except Exception:
                print(f"[Secante] Iter {iter_count-2}: x = {x2}, f(x) = <erro na avaliação>")
        if delta < tol:
            if verbose:
                print("\nTabela de iterações (Secante):")
                print(f"{'i':>3} {'xi':>24} {'f(xi)':>24} {'|xi-xi-1|':>24}")
                for it in iteracoes:
                    delta_str = str(it[3]) if not np.isnan(it[3]) else "-"
                    print(f"{it[0]:3d} {str(it[1]):>24} {str(it[2]):>24} {delta_str:>24}")
                print(f"\nRaiz aproximada: {x2}")
                print(f"Iterações realizadas: {iter_count-1}")
            return x2, iter_count-1
        # atualiza pontos e valores de f para próxima iteração
        x0, fx0 = x1, fx1
        x1, fx1 = x2, fx2
    if verbose:
        print("\nTabela de iterações (Secante):")
        print(f"{'i':>3} {'xi':>24} {'f(xi)':>24} {'|xi-xi-1|':>24}")
        for it in iteracoes:
            delta_str = str(it[3]) if not np.isnan(it[3]) else "-"
            print(f"{it[0]:3d} {str(it[1]):>24} {str(it[2]):>24} {delta_str:>24}")
        print(f"\nRaiz aproximada: {x1}")
        print(f"Iterações realizadas: {max_iter}")
    return x1, max_iter

# Menu principal
def pedir_dados_raizes(metodo=None):
    """Lê os dados necessários para o método de raízes.

    Se ``metodo`` for ``None``, comporta-se como modo interativo completo
    (executa o método e plota o resultado). Se ``metodo`` for uma das strings
    ``'bissecao'``, ``'newton'`` ou ``'secante'``, apenas lê os parâmetros e
    retorna uma tupla ``(func_str, tol, max_iter, params)`` para uso por
    menus externos (compatibilidade com `menu_raizes`).

    Em modo interativo, protege contra EOFError para permitir execuções em
    ambientes não interativos (scripts/tests).
    """
    if metodo is None:
        # modo interativo (executa e plota)
        try:
            print("Métodos de Cálculo Numérico")
            print("1 - Método da Bisseção")
            print("2 - Método de Newton-Raphson (Tangente)")
            print("3 - Método da Secante")

            escolha = int(input("Escolha o método: "))
            func_str = input("Digite a função f(x) (ex: x**2 - 4): ")
            # Verificação para evitar '=' na expressão
            if '=' in func_str:
                print("Erro: Digite apenas a expressão igualada a zero, por exemplo: x**4 - 2*x**3 - 2*x + 1")
                return None
            tol_str = input("Digite a tolerância: ")
            try:
                tol = float(tol_str)
            except Exception:
                print("Erro: Tolerância deve ser um número (ex: 0.0001 ou 1e-4)")
                return None
            max_iter_str = input("Digite o número máximo de iterações [padrão: 100]: ")
            if max_iter_str.strip() == "":
                max_iter = 100
            else:
                try:
                    max_iter = int(max_iter_str)
                except Exception:
                    print("Erro: Número máximo de iterações deve ser um inteiro.")
                    return None

            if escolha == 1:
                a = float(input("Digite o valor de a: "))
                b = float(input("Digite o valor de b: "))
                raiz, iters = bissecao(func_str, a, b, tol, max_iter, verbose=True)
                print("\nGráfico da função:")
                plotar_funcao(func_str, a, b, raiz, grafico=True, title="Método da Bisseção")
            elif escolha == 2:
                x0 = float(input("Digite o valor inicial x0: "))
                a = float(input("Digite o valor de a: "))
                b = float(input("Digite o valor de b: "))
                raiz, iters = newton(func_str, x0, tol, max_iter, verbose=True, a=a, b=b)
                print("\nGráfico da função:")
                plotar_funcao(func_str, a, b, raiz, grafico=True, title="Método de Newton-Raphson")
            if escolha == 3:
                x0 = float(input("Digite o valor inicial x0: "))
                x1 = float(input("Digite o valor inicial x1: "))
                # Define intervalo automaticamente para o gráfico
                a = min(x0, x1) - 2
                b = max(x0, x1) + 2
                raiz, iters = secante(func_str, x0, x1, tol, max_iter, verbose=True, a=a, b=b)
                print("\nGráfico da função:")
                plotar_funcao(func_str, a, b, raiz, grafico=True, title="Método da Secante")
            else:
                print("Opção inválida.")
                return
            return
        except EOFError:
            # Em execução não interativa, retorna sem exceção
            return None
        except Exception as e:
            print(f"Erro ao ler parâmetros: {e}")
            return None

    # Modo de leitura para menu externo: não executar, apenas retornar parâmetros
    try:
        func_str = input("Digite a função f(x) (ex: x**2 - 4): ")
        if '=' in func_str:
            print("Erro: Digite apenas a expressão igualada a zero, por exemplo: x**4 - 2*x**3 - 2*x + 1")
            return None, None, None, ()
        tol_str = input("Digite a tolerância: ")
        try:
            tol = float(tol_str)
        except Exception:
            print("Erro: Tolerância deve ser um número (ex: 0.0001 ou 1e-4)")
            return None, None, None, ()
        max_iter_str = input("Digite o número máximo de iterações [padrão: 100]: ")
        if max_iter_str.strip() == "":
            max_iter = 100
        else:
            try:
                max_iter = int(max_iter_str)
            except Exception:
                print("Erro: Número máximo de iterações deve ser um inteiro.")
                return None, None, None, ()

        if metodo == 'bissecao':
            a = float(input("Digite o valor de a: "))
            b = float(input("Digite o valor de b: "))
            params = (a, b)
        elif metodo == 'newton':
            x0 = float(input("Digite o valor inicial x0: "))
            params = (x0,)
        elif metodo == 'secante':
            x0 = float(input("Digite o valor inicial x0: "))
            x1 = float(input("Digite o valor inicial x1: "))
            params = (x0, x1)
        else:
            print("Método desconhecido para leitura de parâmetros.")
            return None, None, None, ()

        return func_str, tol, max_iter, params
    except EOFError:
        return None, None, None, ()
    except Exception as e:
        print(f"Erro ao ler parâmetros: {e}")
        return None, None, None, ()


def dados():
    """Menu interativo para métodos de busca de raízes."""
    print("\n=== Métodos de Busca de Raízes ===")
    print("1 - Método da Bissecção")
    print("2 - Método do Ponto Fixo")
    print("3 - Método de Newton-Raphson")
    print("4 - Método da Secante")
    print("0 - Sair")
    opcao = input("Escolha o método desejado: ")
    return opcao

def menu_principal_global():
    """Menu principal que encaminha para os menus específicos.

    Opções:
    1 - Integrações (chama `menu()` definido na seção de integrações)
    2 - EDOs (chama `menu_principal()` definido na seção de EDOs)
    3 - Raízes (chama `pedir_dados_raizes()` da seção de raízes)
    0 - Sair
    """
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1 - Integrações")
        print("2 - EDOs")
        print("3 - Raízes")
        print("0 - Sair")
        opc = input("Escolha uma opção: ").strip()
        if opc == '0':
            print("Saindo.")
            break
        elif opc == '1':
            try:
                menu()
            except Exception as e:
                print(f"Erro ao executar menu de Integrações: {e}")
        elif opc == '2':
            try:
                menu_principal()
            except Exception as e:
                print(f"Erro ao executar menu de EDOs: {e}")
        elif opc == '3':
            try:
                pedir_dados_raizes()
            except Exception as e:
                print(f"Erro ao executar menu de Raízes: {e}")
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_principal_global()