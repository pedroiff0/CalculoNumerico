from math import factorial, isclose # isclose é só pro gregory newton
import sympy as sp # pro erro e truncamento

def ler_pontos_interpolacao():
    n = int(input("\nDigite o número de pontos (n): "))
    x_vals = []
    y_vals = []
    for i in range(n):
        x = float(input(f"x[{i}] = "))
        y = float(input(f"y[{i}] = "))
        x_vals.append(x)
        y_vals.append(y)
    x_interp = float(input("Digite o valor de x para interpolar: "))
    return x_vals, y_vals, x_interp

def obter_max_grau(n):
    try:
        val = input(f"Digite o grau máximo desejado (máximo {n-1}), ou deixe vazio para usar o máximo: ")
        if val.strip() == '':
            return None
        grau = int(val)
        if grau < 1 or grau > n - 1:
            print("Após limite, usando o máximo possível.")
            return None
        return grau
    except:
        print("Entrada inválida, usando o máximo possível.")
        return None

# tolerencia muito alta (15 casa decimal)
def verifica_espaçamento_uniforme(x, tol=1e-15):
    h = x[1] - x[0]
    return all(isclose(x[i+1] - x[i], h, abs_tol=tol) for i in range(len(x)-1)), h

# lagrange
def tabela_diferencas_divididas(x, y):
    n = len(x)
    tabela = [y.copy()]
    for j in range(1, n):
        coluna = []
        for i in range(n - j):
            numerador = tabela[j - 1][i + 1] - tabela[j - 1][i]
            denominador = x[i + j] - x[i]
            coluna.append(numerador / denominador)
        tabela.append(coluna)
    return tabela

# impressao de tabela 
def imprimir_tabela_diferencas_divididas(tabela):
    print("\nTabela de Diferenças Divididas:")
    for i in range(len(tabela[0])):
        linha = [f"{tabela[j][i]:>12.6f}" if i < len(tabela[j]) else " " * 12 for j in range(len(tabela))]
        print(" ".join(linha))

def tabela_diferencas_finitas(y):
    n = len(y)
    tabela = [y.copy()]
    for j in range(1, n):
        coluna = []
        for i in range(n - j):
            coluna.append(tabela[j-1][i+1] - tabela[j-1][i])
        tabela.append(coluna)
    return tabela

def imprimir_tabela_diferencas_finitas(tabela):
    print("\nTabela de Diferenças Finitas Progressivas:")
    for i in range(len(tabela[0])):
        linha = [f"{tabela[j][i]:>12.6f}" if i < len(tabela[j]) else " " * 12 for j in range(len(tabela))]
        print(" ".join(linha))


def perguntar_erro(x_vals, x_interp, grau, valor_interpolado):
    resposta = input("Deseja calcular erro truncamento e erro real? (s/n) ").strip().lower()
    if resposta == 's':
        func_str = input("Digite a função f(x) em Python (ex: exp(x)): ").strip()
        return calcular_erro(func_str, x_vals, x_interp, grau, valor_interpolado)
    else:
        print("Cálculo de erro não realizado.")
        return None, None

def calcular_erro(func_str, x_vals, x_interp, grau, valor_interpolado):
    x = sp.Symbol('x')
    f = sp.sympify(func_str)
    try:
        # derivada de ordem n+1 para estimar erro máximo (limitante superior)
        f_deriv = f.diff(x, grau + 1)

        # determina o ponto de máximo do valor da derivada no intervalo (aproximação)
        x_max = max(x_vals)
        f_deriv_max = abs(f_deriv.evalf(subs={x: x_max}))

        # produtorio dos termos (x - xi)
        produto = 1.0
        for xi in x_vals:
            produto *= (x_interp - xi)

        # erro de truncamento máximo
        erro_trunc_max = (f_deriv_max / factorial(grau + 1)) * abs(produto)

        # Exibe informações e valores
        # print(f"\nFunção: {func_str}")
        # print(f"Derivada de ordem {grau+1} máxima em x = {x_max}: {f_deriv_max}")
        #print(f"Produto dos termos (x_interp - xi): {produto}")
        print(f"Erro de truncamento máximo): {erro_trunc_max}") # deixar so o erro truncamento, q é o ideal é necessário (prática 21/10)
        
        return erro_trunc_max, None

    except Exception as e:
        print(f"Erro ao calcular erro truncamento máximo: {e}")
        return None, None

#metodo de newton
def newton_dif_divididas(x, tabela, xp, max_grau=None):
    n = len(x)
    if max_grau is None or max_grau > n - 1:
        max_grau = n - 1
    resultado = tabela[0][0]
    termo = 1.0
    print("\nCálculo passo a passo (Newton Diferenças Divididas):")
    print(f"P0 = {resultado}")
    for i in range(1, max_grau + 1):
        termo *= (xp - x[i - 1])
        print(f"Termo {i}: (xp - x[{i-1}]) = ({xp} - {x[i-1]}) = {xp - x[i-1]}")
        print(f"Δ^{i} f = {tabela[i][0]}") # Δ é o operador da dif dividida
        resultado += tabela[i][0] * termo
        print(f"Parcial após termo {i}: {resultado}")
    return resultado

def gregory_newton_progressivo(x, y, xp, max_grau=None):
    n = len(x)
    if max_grau is None or max_grau > n - 1:
        max_grau = n - 1
    dx = x[1] - x[0]
    s = (xp - x[0]) / dx  # variável u
    tabela = tabela_diferencas_finitas(y)
    resultado = y[0]
    termo = 1.0

    print(f"\nPasso h = {dx}")
    print(f"Valor de u (s) = (xp - x[0]) / h = ({xp} - {x[0]}) / {dx} = {s}")
    print("\nCálculo passo a passo (Gregory-Newton Progressivo):")
    print(f"y[0] = {y[0]}")

    for k in range(1, max_grau + 1):
        termo *= (s - (k - 1)) / k
        delta = tabela[k][0]
        resultado += delta * termo
        print(f"Δ^{k} y[0] = {delta}, termo: {termo}, parcial: {resultado}")

    return resultado

def lagrange_interpol(x, y, xp, max_grau=None):
    n = len(x)
    if max_grau is None or max_grau > n - 1:
        max_grau = n - 1
    yp = 0.0
    print("\nCálculos detalhados do polinômio de Lagrange:")

    for i in range(max_grau + 1):
        li = 1.0
        print(f"\nTermo {i}: L{i}(xp) = ", end="")
        for j in range(n):
            if i != j:
                li *= (xp - x[j]) / (x[i] - x[j])
                print(f"(({xp} - {x[j]}) / ({x[i]} - {x[j]})) ", end="")
        termo = y[i] * li
        yp += termo
        print(f"= {li}")
        print(f"y[{i}] * L{i} = {y[i]} * {li} = {termo}")

    return yp

def dispositivo_pratico_lagrange(x, y, xp, max_grau=None):
    n = len(x)
    if max_grau is None or max_grau > n - 1:
        max_grau = n - 1
    resultado = 0.0
    G = []
    for i in range(n):
        linha = []
        for j in range(n):
            if i == j:
                linha.append(xp - x[j])
            else:
                linha.append(x[i] - x[j])
        G.append(linha)

    print("\nDispositivo Prático de Lagrange:")
    print(f"{'i':>2} {'x[i]':>10} {'y[i]':>10} {'L[i](xp)':>15}")

    for i in range(max_grau + 1):
        numerador = 1.0
        denominador = 1.0
        for j in range(n):
            if i != j:
                numerador *= (xp - x[j])
                denominador *= (x[i] - x[j])
        Li = numerador / denominador
        termo = y[i] * Li
        resultado += termo
        print(f"{i:2d} {x[i]:10} {y[i]:10} {Li:15}")

    print("\nMatriz G (x[i] - x[j], diagonal = xp - x[i]):")
    for linha in G:
        print("[ " + " ".join(str(v) for v in linha) + " ]")

    Gi = []
    Gd = 1.0
    for i in range(max_grau + 1):
        prod = 1.0
        for j in range(n):
            prod *= G[i][j]
        Gi.append(prod)
        Gd *= G[i][i]

    print(f"\nProduto da diagonal Gd = {Gd}")
    for i, val in enumerate(Gi):
        print(f"Produto da linha G[{i}] = {val}")

    soma_serie = 0.0
    for i in range(max_grau + 1):
        soma_serie += y[i] / Gi[i]
    print(f"\nCálculo final: Gd * sum(y[i]/Gi[i]) = {Gd} * {soma_serie} = {Gd * soma_serie}")
    print(f"\nValor interpolado em x = {xp} é: {resultado}")

    return resultado

def menu():
    while True:
        print("\n================ MENU DE INTERPOLAÇÃO ================")
        print("1. Polinômio de Lagrange")
        print("2. Dispositivo Prático de Lagrange")
        print("3. Polinômio de Newton (Diferenças Divididas)")
        print("4. Polinômio Gregory-Newton Progressivo")
        print("0. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == '0':
            print("Encerrando o programa...")
            break
        
        x_vals, y_vals, x_interp = ler_pontos_interpolacao()

        max_grau = obter_max_grau(n)

        if opcao == '1':
            resultado = lagrange_interpol(x_vals, y_vals, x_interp, max_grau=max_grau)
            if resultado is not None:
                erro_trunc, erro_real = perguntar_erro(x_vals[:max_grau+1], x_interp, max_grau, resultado)
            print(f"\nResultado final (Lagrange): {resultado}")

        elif opcao == '2':
            resultado = dispositivo_pratico_lagrange(x_vals, y_vals, x_interp, max_grau=max_grau)
            if resultado is not None:
                erro_trunc, erro_real = perguntar_erro(x_vals[:max_grau+1], x_interp, max_grau, resultado)
            print(f"\nResultado final (Dispositivo Prático de Lagrange): {resultado}")

        elif opcao == '3':
            tabela = tabela_diferencas_divididas(x_vals, y_vals)
            imprimir_tabela_diferencas_divididas(tabela)
            resultado = newton_dif_divididas(x_vals, tabela, x_interp, max_grau=max_grau)
            if resultado is not None:
                erro_trunc, erro_real = perguntar_erro(x_vals[:max_grau+1], x_interp, max_grau, resultado)
            print(f"\nResultado final (Newton Diferenças Divididas): {resultado}")

        elif opcao == '4':
            uniforme, h = verifica_espaçamento_uniforme(x_vals)
            if not uniforme:
                print("Erro: Os pontos x não têm espaçamento uniforme! Gregory-Newton requer x igualmente espaçados.")
                continue
            tabela = tabela_diferencas_finitas(y_vals)
            imprimir_tabela_diferencas_finitas(tabela)
            resultado = gregory_newton_progressivo(x_vals, y_vals, x_interp, max_grau=max_grau)
            if resultado is not None:
                erro_trunc, erro_real = perguntar_erro(x_vals[:max_grau+1], x_interp, max_grau, resultado)
            print(f"\nResultado final (Gregory-Newton Progressivo): {resultado}")

        else:
            print("Opção inválida, tente novamente.")

if __name__ == '__main__':
    menu()