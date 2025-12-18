import matplotlib.pyplot as plt
import numpy as np

# Função para converter a string em função executável
def f(x, func_str):
    return eval(func_str)

# Função para plotar gráfico
def plotar_funcao(func_str, a=None, b=None, raiz=None):
    if a is None or b is None:
        a, b = -10, 10
    x_vals = np.linspace(a, b, 400)
    y_vals = [f(x, func_str) for x in x_vals]

    plt.figure()
    plt.axhline(0, color="black", linewidth=1)
    plt.axvline(0, color="black", linewidth=1)
    plt.plot(x_vals, y_vals, label=f"f(x) = {func_str}")
    
    if raiz is not None:
        plt.scatter(raiz, f(raiz, func_str), color="red", zorder=5, label=f"Raiz ≈ {raiz:.6f}")
    
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid(True)
    plt.show()  # Mostra gráfico interativo

# Método da Bisseção
def bissecao(func_str, a, b, tol, max_iter):
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

    Returns
    -------
    (float, int)
        Tupla (raiz_aproximada, n_iter) ou (None, 0) se os sinais em a/b não forem opostos.
    """
    if f(a, func_str) * f(b, func_str) >= 0:
        print("Erro: f(a) e f(b) devem ter sinais opostos.")
        return None, 0

    for i in range(1, max_iter + 1):
        c = (a + b) / 2
        print(f"[Bisseção] Iter {i}: x = {c:.6f}, f(x) = {f(c, func_str):.6f}")
        if abs(f(c, func_str)) < tol or abs(b - a) < tol:
            return c, i
        if f(a, func_str) * f(c, func_str) < 0:
            b = c
        else:
            a = c
    return c, max_iter

# Método de Newton-Raphson
def newton(func_str, x0, tol, max_iter):
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

    Returns
    -------
    (float, int)
        Tupla (raiz_aproximada, n_iter) ou (None, n_iter) se houver erro.
    """
    h = 1e-6
    for i in range(1, max_iter + 1):
        fx = f(x0, func_str)
        dfx = (f(x0 + h, func_str) - f(x0 - h, func_str)) / (2 * h)
        if dfx == 0:
            print("Erro: derivada zero.")
            return None, i
        x1 = x0 - fx / dfx
        print(f"[Newton] Iter {i}: x = {x1:.6f}, f(x) = {f(x1, func_str):.6f}")
        if abs(x1 - x0) < tol:
            return x1, i
        x0 = x1
    return x0, max_iter

# Método da Secante
def secante(func_str, x0, x1, tol, max_iter):
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

    Returns
    -------
    (float, int)
        Tupla (raiz_aproximada, n_iter) ou (None, n_iter) em caso de erro.
    """
    for i in range(1, max_iter + 1):
        fx0 = f(x0, func_str)
        fx1 = f(x1, func_str)
        if fx1 - fx0 == 0:
            print("Erro: divisão por zero.")
            return None, i
        x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        print(f"[Secante] Iter {i}: x = {x2:.6f}, f(x) = {f(x2, func_str):.6f}")
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
    """
    if metodo is None:
        # modo interativo antigo (executa e plota)
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
                plotar_funcao(func_str, a, b, raiz)

        elif escolha == 2:
            x0 = float(input("Digite o valor inicial x0: "))
            raiz, iters = newton(func_str, x0, tol, max_iter)
            if raiz is not None:
                plotar_funcao(func_str, x0 - 5, x0 + 5, raiz)

        elif escolha == 3:
            x0 = float(input("Digite o valor inicial x0: "))
            x1 = float(input("Digite o valor inicial x1: "))
            raiz, iters = secante(func_str, x0, x1, tol, max_iter)
            if raiz is not None:
                plotar_funcao(func_str, min(x0, x1) - 5, max(x0, x1) + 5, raiz)

        else:
            print("Opção inválida.")
            return

        if raiz is not None:
            print(f"\nA raiz encontrada é: {raiz:.6f}")
            print(f"Número total de iterações: {iters}")
        return

    # Modo de leitura para menu externo: não executar, apenas retornar parâmetros
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
if __name__ == "__main__":
    pedir_dados_raizes()