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
if __name__ == "__main__":
    pedir_dados_raizes()