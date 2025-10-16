from math import exp, factorial, isclose

def verifica_espaçamento_uniforme(x, tol=1e-6):
    h = x[1] - x[0]
    return all(isclose(x[i+1] - x[i], h, abs_tol=tol) for i in range(len(x)-1)), h

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

def newton_dif_divididas(x, tabela, xp):
    n = len(x)
    resultado = tabela[0][0]
    termo = 1.0
    print("\nCálculo passo a passo (Newton Diferenças Divididas):")
    print(f"P0 = {resultado:.6f}")
    for i in range(1, n):
        termo *= (xp - x[i - 1])
        print(f"Termo {i}: (xp - x[{i-1}]) = ({xp} - {x[i-1]}) = {xp - x[i-1]:.6f}")
        print(f"Δ^{i} f = {tabela[i][0]:.6f}")
        resultado += tabela[i][0] * termo
        print(f"Parcial após termo {i}: {resultado:.6f}")
    return resultado

def gregory_newton_progressivo(x, y, xp):
    n = len(x)
    dx = x[1] - x[0]
    s = (xp - x[0]) / dx  # variável u na fórmula
    tabela = tabela_diferencas_finitas(y)
    resultado = y[0]
    termo = 1.0

    print(f"\nPasso h = {dx:.6f}")
    print(f"Valor de u (s) = (xp - x[0]) / h = ({xp} - {x[0]}) / {dx:.6f} = {s:.6f}")

    print("\nCálculo passo a passo (Gregory-Newton Progressivo):")
    print(f"y[0] = {y[0]:.6f}")

    for k in range(1, n):
        termo *= (s - (k - 1)) / k
        delta = tabela[k][0]
        resultado += delta * termo
        print(f"Δ^{k} y[0] = {delta:.6f}, termo: {termo:.6f}, parcial: {resultado:.6f}")

    return resultado

def lagrange_interpol(x, y, xp):
    n = len(x)
    yp = 0.0
    print("\nCálculos detalhados do polinômio de Lagrange:")
    for i in range(n):
        li = 1.0
        print(f"\nTermo {i}: L{i}(xp) = ", end="")
        for j in range(n):
            if i != j:
                li *= (xp - x[j]) / (x[i] - x[j])
                print(f"(({xp} - {x[j]}) / ({x[i]} - {x[j]})) ", end="")
        termo = y[i] * li
        yp += termo
        print(f"= {li:.6f}")
        print(f"y[{i}] * L{i} = {y[i]} * {li:.6f} = {termo:.6f}")
    return yp

def dispositivo_pratico_lagrange(x, y, xp):
    n = len(x)
    resultado = 0.0

    # Construção da matriz G conforme definição:
    # diagonal: xp - x[i]
    # outros elementos: x[i] - x[j]
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

    for i in range(n):
        numerador = 1.0
        denominador = 1.0
        for j in range(n):
            if i != j:
                numerador *= (xp - x[j])
                denominador *= (x[i] - x[j])
        Li = numerador / denominador
        termo = y[i] * Li
        resultado += termo
        print(f"{i:2d} {x[i]:10.4f} {y[i]:10.4f} {Li:15.6f}")

    print("\nMatriz G (x[i] - x[j], diagonal = xp - x[i]):")
    for i in range(n):
        linha = [f"{G[i][j]:10.6f}" for j in range(n)]
        print("[ " + " ".join(linha) + " ]")

    # Produto por linha (incluindo diagonal)
    Gi = []
    Gd = 1.0
    for i in range(n):
        prod = 1.0
        for j in range(n):
            prod *= G[i][j]
        Gi.append(prod)
        Gd *= G[i][i]  # produto dos elementos na diagonal com xp

    print(f"\nProduto da diagonal Gd = {Gd:.6f}")
    for i, val in enumerate(Gi):
        print(f"Produto da linha G[{i}] = {val:.6f}")

    soma_serie = 0.0
    for i in range(n):
        soma_serie += y[i] / Gi[i]
    print(f"\nCálculo final: Gd * sum(y[i]/Gi[i]) = {Gd:.6f} * {soma_serie:.6f} = {Gd * soma_serie:.6f}")

    print(f"\nValor interpolado em x = {xp:.4f} é: {resultado:.6f}")

    return resultado

def erro_truncamento_exp3x(x_vals, x_interp):
    f3_max = 27 * exp(3 * max(x_vals))
    produto = 1
    for xi in x_vals:
        produto *= (x_interp - xi)
    erro = (f3_max / factorial(3)) * produto
    return erro

def menu():
    while True:
        print("\n================ MENU DE INTERPOLAÇÃO ================")
        print("1. Polinômio de Lagrange")
        print("2. Dispositivo Prático de Lagrange")
        print("3. Polinômio de Newton (Diferenças Divididas)")
        print("4. Polinômio Gregory-Newton Progressivo")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '5':
            print("Encerrando o programa...")
            break

        n = int(input("\nDigite o número de pontos (n): "))
        x_vals = []
        y_vals = []
        for i in range(n):
            x = float(input(f"x[{i}] = "))
            y = float(input(f"y[{i}] = "))
            x_vals.append(x)
            y_vals.append(y)
        x_interp = float(input("Digite o valor de x para interpolar: "))

        if opcao == '1':
            resultado = lagrange_interpol(x_vals, y_vals, x_interp)
            erro = erro_truncamento_exp3x(x_vals, x_interp)
            print(f"\nResultado final (Lagrange): {resultado:.6f}")
            print(f"Erro estimado: {erro:.7f}")

        elif opcao == '2':
            resultado = dispositivo_pratico_lagrange(x_vals, y_vals, x_interp)
            erro = erro_truncamento_exp3x(x_vals, x_interp)
            print(f"\nErro estimado: {erro:.7f}")

        elif opcao == '3':
            tabela = tabela_diferencas_divididas(x_vals, y_vals)
            imprimir_tabela_diferencas_divididas(tabela)
            resultado = newton_dif_divididas(x_vals, tabela, x_interp)
            erro = erro_truncamento_exp3x(x_vals, x_interp)
            print(f"\nResultado final (Newton Diferenças Divididas): {resultado:.6f}")
            print(f"Erro estimado: {erro:.7f}")

        elif opcao == '4':
            uniforme, h = verifica_espaçamento_uniforme(x_vals)
            if not uniforme:
                print("Erro: Os pontos x não têm espaçamento uniforme! Gregory-Newton requer x igualmente espaçados.")
                continue
            tabela = tabela_diferencas_finitas(y_vals)
            imprimir_tabela_diferencas_finitas(tabela)
            resultado = gregory_newton_progressivo(x_vals, y_vals, x_interp)
            erro = erro_truncamento_exp3x(x_vals, x_interp)
            print(f"\nResultado final (Gregory-Newton Progressivo): {resultado:.6f}")
            print(f"Erro estimado: {erro:.7f}")
        else:
            print("Opção inválida, tente novamente.")

if __name__ == '__main__':
    menu()