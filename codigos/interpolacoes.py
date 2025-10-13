#polinomio newton


def diferencas_divididas(x, y):
    n = len(x)
    tabela = [y.copy()]  # primeira coluna é y

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

    for i in range(1, n):
        termo *= (xp - x[i - 1])
        resultado += tabela[i][0] * termo

    return resultado

def imprimir_tabela(tabela):
    print("\nTabela de Diferenças Divididas:")
    for i in range(len(tabela[0])):
        linha = [f"{tabela[j][i]:10.6f}" if i < len(tabela[j]) else " " * 10 for j in range(len(tabela))]
        print(" ".join(linha))


# Entrada de dados
n = int(input("Digite o número de pontos (n): "))

x_vals = []
y_vals = []

print("Digite os pares (x, y):")
for i in range(n):
    x = float(input(f"x[{i}] = "))
    y = float(input(f"y[{i}] = "))
    x_vals.append(x)
    y_vals.append(y)

x_interp = float(input("Digite o valor de x para interpolar: "))

# Cálculos
tabela = diferencas_divididas(x_vals, y_vals)
imprimir_tabela(tabela)
resultado = newton_interpolacao(x_vals, tabela, x_interp)

print(f"\nValor interpolado em x = {x_interp:.4f} é: {resultado:.6f}")