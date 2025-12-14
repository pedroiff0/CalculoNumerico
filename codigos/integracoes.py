import math
from sympy import symbols, integrate, sympify

# === Funções para integração com dados em tabela (x, y) ===

def trapezio_tabela():
    print("[DEBUG] Iniciando Trapézio com tabela...")
    print("\n--- Regra do Trapézio com dados em tabela ---")
    n = int(input("Digite o número de pontos (n >= 2): "))
    if n < 2:
        print("Número de pontos deve ser pelo menos 2.")
        return

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
    print("[DEBUG] Iniciando Simpson 1/3 com tabela...")
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

    print(f"\nResultado da integral pela Regra de Simpson 1/3 com dados discretos: {integral:.6f}\n")


def simpson_3_8_tabela():
    print("[DEBUG] Iniciando Simpson 3/8 com tabela...")
    print("\n--- Regra de Simpson 3/8 com dados em tabela ---")
    n = int(input("Digite o número de pontos (n deve ser múltiplo de 3 mais 1, ex: 4, 7, 10): "))
    if (n - 1) % 3 != 0 or n < 4:
        print("Número de pontos inválido. Deve ser 3k + 1 e pelo menos 4.")
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
    for i in range(1, n - 1):
        if i % 3 == 0:
            integral += 2 * y[i]
        else:
            integral += 3 * y[i]

    integral *= 3 * h / 8

    print(f"\nResultado da integral pela Regra de Simpson 3/8 com dados discretos: {integral:.6f}\n")
    return


def calcular_integral_analitica():
    print("[DEBUG] Iniciando cálculo analítico (simbólico)...")
    print("\n--- Cálculo Analítico da Integral ---")
    expressao = input("Digite a função f(x): ")
    a = float(input("Limite inferior (a): "))
    b = float(input("Limite superior (b): "))

    x = symbols('x')
    try:
        funcao = sympify(expressao)
        integral_exata = integrate(funcao, (x, a, b))
        print(f"\nResultado exato da integral de {expressao} de {a} a {b}: {integral_exata.evalf():.6f}\n")
        return integral_exata.evalf()
    except Exception as e:
        print("\nErro ao calcular a integral simbolicamente:", e)
        return None

def newton_cotes(func, a, b, ordem):
    print(f"[DEBUG] Newton-Cotes ordem {ordem}, intervalo: [{a}, {b}], função: {func}")
    """Newton-Cotes de ordem 1 a 4 (sem subdivisões compostas)"""
    h = (b - a) / ordem
    x = [a + i * h for i in range(ordem + 1)]
    y = []
    for xi in x:
        # Define x para eval
        global_vars = {"x": xi, "math": math}
        try:
            yi = eval(func, {"__builtins__": None}, global_vars)
        except Exception as e:
            print(f"Erro na avaliação da função: {e}")
            return None
        y.append(yi)

    if ordem == 1:
        resultado = h * (y[0] + y[1]) / 2
        metodo_nome = "Regra do Trapézio"
    elif ordem == 2:
        resultado = (h/3) * (y[0] + 4*y[1] + y[2])
        metodo_nome = "Regra de Simpson 1/3"
    elif ordem == 3:
        resultado = (3*h/8) * (y[0] + 3*y[1] + 3*y[2] + y[3])
        metodo_nome = "Regra de Simpson 3/8"
    elif ordem == 4:
        resultado = (2*h/45) * (7*y[0] + 32*y[1] + 12*y[2] + 32*y[3] + 7*y[4])
        metodo_nome = "Newton-Cotes ordem 4"
    else:
        print("Ordem inválida para Newton-Cotes.")
        return None

    print(f"\nResultado pela {metodo_nome}: {resultado:.6f}\n")
    return resultado


def simpson_1_3_composta(func, a, b, n):
    print(f"[DEBUG] Simpson 1/3 composta, n={n}, intervalo: [{a}, {b}], função: {func}")
    if n % 2 != 0:
        print("Número de subintervalos deve ser par para Simpson 1/3 composta.")
        return None
    h = (b - a) / n
    soma = 0.0
    for i in range(1, n):
        x_i = a + i * h
        global_vars = {"x": x_i, "math": math}
        try:
            f_x = eval(func, {"__builtins__": None}, global_vars)
        except Exception as e:
            print(f"Erro na avaliação da função: {e}")
            return None

        if i % 2 == 0:
            soma += 2 * f_x
        else:
            soma += 4 * f_x

    f_a = eval(func, {"__builtins__": None}, {"x": a, "math": math})
    f_b = eval(func, {"__builtins__": None}, {"x": b, "math": math})

    resultado = (h / 3) * (f_a + soma + f_b)
    print(f"\nResultado pela Regra de Simpson 1/3 composta: {resultado:.6f}\n")
    return resultado


def simpson_3_8_composta(func, a, b, n):
    print(f"[DEBUG] Simpson 3/8 composta, n={n}, intervalo: [{a}, {b}], função: {func}")
    if n % 3 != 0:
        print("Número de subintervalos deve ser múltiplo de 3 para Simpson 3/8 composta.")
        return None
    h = (b - a) / n
    soma = 0.0
    for i in range(1, n):
        x_i = a + i * h
        global_vars = {"x": x_i, "math": math}
        try:
            f_x = eval(func, {"__builtins__": None}, global_vars)
        except Exception as e:
            print(f"Erro na avaliação da função: {e}")
            return None

        if i % 3 == 0:
            soma += 2 * f_x
        else:
            soma += 3 * f_x

    f_a = eval(func, {"__builtins__": None}, {"x": a, "math": math})
    f_b = eval(func, {"__builtins__": None}, {"x": b, "math": math})

    resultado = (3 * h / 8) * (f_a + soma + f_b)
    print(f"\nResultado pela Regra de Simpson 3/8 composta: {resultado:.6f}\n")
    return resultado


def trapezio_composta(func, a, b, n):
    print(f"[DEBUG] Trapézio composta, n={n}, intervalo: [{a}, {b}], função: {func}")
    h = (b - a) / n
    soma = 0.0
    for i in range(1, n):
        x_i = a + i * h
        global_vars = {"x": x_i, "math": math}
        try:
            f_x = eval(func, {"__builtins__": None}, global_vars)
        except Exception as e:
            print(f"Erro na avaliação da função: {e}")
            return None
        soma += f_x

    f_a = eval(func, {"__builtins__": None}, {"x": a, "math": math})
    f_b = eval(func, {"__builtins__": None}, {"x": b, "math": math})

    resultado = (h / 2) * (f_a + 2 * soma + f_b)
    print(f"\nResultado pela Regra do Trapézio composta: {resultado:.6f}\n")
    return resultado




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


        # Pergunta se deseja tabela primeiro
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

        # Só pede função e limites se NÃO for tabela
        func = input("Digite a função f(x) (use math. para funções trigonométricas, etc): ")
        a = float(input("Limite inferior (a): "))
        b = float(input("Limite superior (b): "))

        composta = input("Deseja usar a versão composta? (s/n): ").strip().lower() == 's'

        resultado = None
        if opcao == '1':
            if composta:
                n = int(input("Digite o número de subintervalos (n): "))
                resultado = trapezio_composta(func, a, b, n)
            else:
                resultado = newton_cotes(func, a, b, 1)
        elif opcao == '2':
            if composta:
                n = int(input("Digite um número PAR de subintervalos: "))
                resultado = simpson_1_3_composta(func, a, b, n)
            else:
                resultado = newton_cotes(func, a, b, 2)
        elif opcao == '3':
            if composta:
                n = int(input("Digite um número MÚLTIPLO DE 3 de subintervalos: "))
                resultado = simpson_3_8_composta(func, a, b, n)
            else:
                resultado = newton_cotes(func, a, b, 3)
        else:
            print("Opção inválida. Tente novamente.")
            continue

        # Após calcular a integral, perguntar se deseja calcular o erro
        if resultado is not None:
            # Perguntar se deseja calcular a integral exata (simbólica) primeiro
            valor_exato = None
            calc_exata = input("Deseja calcular a integral exata (simbólica)? (s/n): ").strip().lower() == 's'
            if calc_exata:
                from sympy import symbols, integrate, sympify
                x = symbols('x')
                # Converter math. para vazio e funções para nomes do SymPy
                func_sympy = func.replace('math.', '')
                func_sympy = func_sympy.replace('log10', 'log')
                func_sympy = func_sympy.replace('log', 'ln')
                func_sympy = func_sympy.replace('ln', 'log')
                func_sympy = func_sympy.replace('sqrt', 'sqrt')
                func_sympy = func_sympy.replace('exp', 'exp')
                try:
                    funcao = sympify(func_sympy, locals={'sqrt':sympify('sqrt'), 'log':sympify('log'), 'exp':sympify('exp')})
                    integral_exata = integrate(funcao, (x, a, b))
                    valor_exato = float(integral_exata.evalf())
                    print(f"\nResultado exato da integral de {func_sympy} de {a} a {b}: {valor_exato:.6f}\n")
                except Exception as e:
                    print("\nErro ao calcular a integral simbolicamente:", e)
            # Perguntar se deseja calcular o erro de truncamento
            calc_erro = input("Deseja calcular o erro de truncamento? (s/n): ").strip().lower() == 's'
            if calc_erro:
                if valor_exato is None:
                    valor_exato = float(input("Digite o valor EXATO da integral (analítico): "))
                erro = abs(valor_exato - resultado)
                print(f"\nValor exato informado: {valor_exato}")
                print(f"Resultado numérico: {resultado}")
                print(f"Erro de truncamento: {erro}\n")

if __name__ == "__main__":
    menu()