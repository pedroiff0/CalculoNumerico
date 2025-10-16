from math import exp, factorial

def diferencas_divididas(x, y):
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

def newton_interpolacao(x, tabela, xp):
    n = len(x)
    resultado = tabela[0][0]
    termo = 1.0
    print("\nCálculo passo a passo do polinômio de Newton:")
    print(f"P0 = {resultado:.6f}")
    for i in range(1, n):
        termo *= (xp - x[i - 1])
        print(f"Termo {i}: (xp - x[{i-1}]) = ({xp} - {x[i-1]}) = {xp - x[i-1]:.6f}")
        print(f"Δ^{i} f = {tabela[i][0]:.6f}")
        resultado += tabela[i][0] * termo
        print(f"Parcial após termo {i}: {resultado:.6f}")
    return resultado

def erro_truncamento_exp3x(x_vals, x_interp):
    f3_max = 27 * exp(3 * max(x_vals))
    produto = 1
    for xi in x_vals:
        produto *= (x_interp - xi)
    erro = (f3_max / factorial(3)) * produto
    return erro

def dispositivo_pratico_lagrange(x, y, xp):
    n = len(x)
    resultado = 0.0
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
    print(f"\nValor interpolado em x = {xp:.4f} é: {resultado:.6f}")
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

def menu():
    while True:
        print("\n================ MENU DE INTERPOLAÇÃO ================")
        print("1. Polinômio de Lagrange")
        print("2. Dispositivo Prático de Lagrange")
        print("3. Polinômio de Newton")
        print("4. Polinômio Gregory-Newton")
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
            tabela = diferencas_divididas(x_vals, y_vals)
            resultado = newton_interpolacao(x_vals, tabela, x_interp)
            erro = erro_truncamento_exp3x(x_vals, x_interp)
            print(f"\nResultado final (Newton): {resultado:.6f}")
            print(f"Erro estimado: {erro:.7f}")

        elif opcao == '4':
            tabela = diferencas_divididas(x_vals, y_vals)
            resultado = newton_interpolacao(x_vals, tabela, x_interp)
            erro = erro_truncamento_exp3x(x_vals, x_interp)
            print(f"\nResultado final (Gregory-Newton): {resultado:.6f}")
            print(f"Erro estimado: {erro:.7f}")
        else:
            print("Opção inválida, tente novamente.")
            
if __name__ == "__main__":
    menu()