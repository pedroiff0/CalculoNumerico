"""
Módulo para métodos de busca de raízes de equações.

Este módulo implementa algoritmos numéricos para encontrar raízes de
funções: bisseção, ponto fixo, Newton-Raphson e secante.

Author: Pedro Henrique Rocha de Andrade
Date: Dezembro 2025
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
def plotar_funcao(func_str, a=None, b=None, raiz=None, grafico=None, verbose=False):
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

    # Se grafico for False, não tenta abrir janelas em ambientes não interativos
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
    plt.plot(x_vals, y_vals, label=f"f(x) = {func_str}")

    if raiz is not None:
        try:
            plt.scatter(raiz, f(raiz, func_str), color="red", zorder=5, label=f"Raiz ≈ {raiz:.6f}")
        except Exception:
            # ignora erro em ponto de plotagem
            pass

    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid(True)
    try:
        plt.show()
    except Exception:
        # Em ambientes não interativos, plt.show pode não funcionar; ignora
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

    for i in range(1, max_iter + 1):
        c = (a + b) / 2
        try:
            fc = f(c, func_str)
        except Exception as e:
            print(f"Erro ao avaliar f(c): {e}")
            return None, i
        if verbose:
            print(f"[Bisseção] Iter {i}: x = {c:.6f}, f(x) = {fc:.6f}")
        if abs(fc) < tol or abs(b - a) < tol:
            # Não plotar automaticamente aqui; quem chamou decide (interactive path pode passar grafico=True)
            return c, i
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
    return c, max_iter

# Método de Newton-Raphson
def newton(func_str, x0, tol, max_iter, verbose=False):
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

    h = 1e-6
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
        if verbose:
            try:
                print(f"[Newton] Iter {i}: x = {x1:.6f}, f(x) = {f(x1, func_str):.6f}")
            except Exception:
                print(f"[Newton] Iter {i}: x = {x1:.6f}, f(x) = <erro na avaliação>")
        if abs(x1 - x0) < tol:
            return x1, i
        x0 = x1
    return x0, max_iter

# Método da Secante
def secante(func_str, x0, x1, tol, max_iter, verbose=False):
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

    for i in range(1, max_iter + 1):
        try:
            fx0 = f(x0, func_str)
            fx1 = f(x1, func_str)
        except Exception as e:
            print(f"Erro ao avaliar função: {e}")
            return None, i
        if fx1 - fx0 == 0:
            print("Erro: divisão por zero.")
            return None, i
        x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        if verbose:
            try:
                print(f"[Secante] Iter {i}: x = {x2:.6f}, f(x) = {f(x2, func_str):.6f}")
            except Exception:
                print(f"[Secante] Iter {i}: x = {x2:.6f}, f(x) = <erro na avaliação>")
        if abs(x2 - x1) < tol:
            return x2, i
        x0, x1 = x1, x2
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
            tol = float(input("Digite a tolerância: "))
            max_iter = int(input("Digite o número máximo de iterações: "))

            if escolha == 1:
                a = float(input("Digite o valor de a: "))
                b = float(input("Digite o valor de b: "))
                raiz, iters = bissecao(func_str, a, b, tol, max_iter)
                if raiz is not None:
                    plotar_funcao(func_str, a, b, raiz, grafico=True)

            elif escolha == 2:
                x0 = float(input("Digite o valor inicial x0: "))
                raiz, iters = newton(func_str, x0, tol, max_iter)
                if raiz is not None:
                    plotar_funcao(func_str, x0 - 5, x0 + 5, raiz, grafico=True)

            elif escolha == 3:
                x0 = float(input("Digite o valor inicial x0: "))
                x1 = float(input("Digite o valor inicial x1: "))
                raiz, iters = secante(func_str, x0, x1, tol, max_iter)
                if raiz is not None:
                    plotar_funcao(func_str, min(x0, x1) - 5, max(x0, x1) + 5, raiz, grafico=True)

            else:
                print("Opção inválida.")
                return

            if raiz is not None:
                print(f"\nA raiz encontrada é: {raiz:.6f}")
                print(f"Número total de iterações: {iters}")
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
        tol = float(input("Digite a tolerância: "))
        max_iter = int(input("Digite o número máximo de iterações: "))

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
if __name__ == "__main__":
    pedir_dados_raizes()