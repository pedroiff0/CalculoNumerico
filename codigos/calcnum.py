"""
Requirements do projeto:

matplotlib==3.10.7
numpy==2.3.4
sympy==1.14.0
pandas==2.3.3
mpmath==1.3.0

"""
from math import factorial, isclose # isclose é só pro gregory newton
import sympy as sp # pro erro e truncamento
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""

Projeto de Cálculo Numérico:
Autor: Pedro Henrique Rocha de Andrade
Orientador: Rodrigo Lacerda da Silva
Ano Início: 2025.2

Paper:
Documentação:
Tutoriais:

% pip3 install calculonumiff
"""

"""
Sistema de Conversão de Bases - Parte 0 (Teórica)

    Funções:
    
    Funções Auxiliares:

"""

def dados_bases():
    print("\n=== Conversor de Bases ===")
    print("1 - Binário para Decimal")
    print("2 - Decimal para Binário")
    print("3 - Binário para Hexadecimal")
    print("4 - Hexadecimal para Binário")
    print("5 - Decimal para Hexadecimal")
    print("6 - Hexadecimal para Decimal")
    print("0 - Sair")
    opcao = input("Escolha a conversão desejada: ")
    return opcao

def binario_para_decimal(bin_str):
    """
    Cálculo: Soma dos dígitos binários multiplicados pelas potências de 2 conforme posição.
    Para cada dígito (d) na posição i (contando da direita para esquerda), soma-se d * 2^i.
    
    Exemplo: bin_str = '1011'
    1*2^0 + 1*2^1 + 0*2^2 + 1*2^3 = 1 + 2 + 0 + 8 = 11 decimal
    """
    decimal = 0
    for i, digito in enumerate(reversed(bin_str)):
        decimal += int(digito) * (2 ** i)
    return decimal

def decimal_para_binario(numDecimal):
    """
    Cálculo: Divisões sucessivas por 2, coletando os restos.
    O número decimal é dividido por 2 repetidamente, e os restos (0 ou 1) formam o número binário do último para o primeiro.
    
    Exemplo: numDecimal = 11
    11/2 = 5 resto 1
    5/2 = 2 resto 1
    2/2 = 1 resto 0
    1/2 = 0 resto 1
    Lendo os restos de baixo para cima: 1011 binário
    """
    if numDecimal == 0:
        return "0"
    binario = ""
    while numDecimal > 0:
        binario = str(numDecimal % 2) + binario
        numDecimal = numDecimal // 2
    return binario

def decimal_para_hexadecimal(numDecimal):
    """
    Cálculo: Divisões sucessivas por 16, coletando restos que representam dígitos hexadecimais.
    Usa tabela '0123456789ABCDEF' para representar restos >= 10.
    
    Exemplo: numDecimal = 254
    254/16 = 15 resto 14 (E)
    15/16 = 0 resto 15 (F)
    Resultado: FE hexadecimal
    """
    if numDecimal == 0:
        return "0"
    digitos = "0123456789ABCDEF"
    hexa = ""
    while numDecimal > 0:
        hexa = digitos[numDecimal % 16] + hexa
        numDecimal = numDecimal // 16
    return hexa

def hexadecimal_para_decimal(hex_str):
    """
    Cálculo: Soma dos dígitos hexadecimais multiplicados por potências de 16 conforme posição.
    Cada caracter é convertido para seu valor decimal e multiplicado por 16^i (contando da direita para esquerda).
    
    Exemplo: hex_str = '1A3'
    3*16^0 + 10*16^1 + 1*16^2 = 3 + 160 + 256 = 419 decimal
    """
    hex_str = hex_str.upper()
    digitos = "0123456789ABCDEF"
    decimal = 0
    for i, digito in enumerate(reversed(hex_str)):
        valor = digitos.index(digito)
        decimal += valor * (16 ** i)
    return decimal

def binario_para_hexadecimal(bin_str):
    """
    Cálculo: Primeiro converte binário para decimal;
    Depois converte o decimal para hexadecimal usando o método das divisões sucessivas.
    
    Exemplo: bin_str = '1111'
    Binário para decimal: 15
    Decimal para hexadecimal: F
    """
    decimal = binario_para_decimal(bin_str)
    return decimal_para_hexadecimal(decimal)

def hexadecimal_para_binario(hex_str):
    """
    Cálculo: Primeiro converte hexadecimal para decimal;
    Depois converte o decimal para binário usando divisões sucessivas por 2.
    
    Exemplo: hex_str = 'F'
    Hexadecimal para decimal: 15
    Decimal para binário: 1111
    """
    decimal = hexadecimal_para_decimal(hex_str)
    return decimal_para_binario(decimal)

"""

Sistemas Lineares - Parte 1

    Funções:
    - eliminacao_gauss_sem_pivotamento(A, b)
    - eliminacao_gauss_com_pivotamento(A, b)
    - lu_sem_pivot(A,b)
    - lu_com_pivot(A,b)
    - forward_solve(L, b)
    - backward_solve(U, y)
    - calcular_residuo(A, x, b)
    
    Funções Auxiliares:
    - imprimir_sistema_linear()
    - montar_sistema_valores() # (pedir dados ao usuario)
    - exibir_residuo_detalhado(A, x, b)
    - matriz_zeros_manual(n) # opcional
    - multiplicar_matrizes(A, B) # opcional
    - matriz_identidade(n) # opcional
"""

# Exibe o sistema linear A|b de forma alinhada no terminal
def imprimir_sistema_linear(A, b, titulo="Sistema de Equações"):
    n = len(A) # número de linhas
    largura = 24 # largura de cada coluna para alinhamento
    print(f"\n{titulo}:")
    for i in range(n):
        linha = ""
        for j in range(A.shape[1]):
            linha += f"{A[i,j]:>{largura}} " # exibe cada elemento de A com espaçamento
        linha += f"|{b[i]:>{largura}}" # exibe o termo independente b ao lado
        print(linha)
    print()

# Lê o sistema do usuário, garantindo matriz quadrada e entrada correta de b
def montar_sistema_valores():
    n = int(input("Digite o número de variáveis (sistema quadrado): ")) # só pode ser matrizes quadradas
    print(f"Insira os coeficientes da matriz A ({n} linhas), cada linha com {n} valores separados por espaço:")
    A = []
    for i in range(n):
        linha = list(map(float, input(f"Linha {i+1}: ").split())) # lê e converte para float
        if len(linha) != n:
            raise ValueError("Número de coeficientes deve ser igual ao número de variáveis!") # validação
        A.append(linha)
    print(f"Insira os termos independentes do vetor b em uma única linha, {n} valores separados por espaço:")
    b = list(map(float, input("b: ").split()))
    if len(b) != n:
        raise ValueError("Número de termos independentes deve ser igual ao número de variáveis!")
    return np.array(A, dtype=float), np.array(b, dtype=float), [f"x{i+1}" for i in range(n)] # retorna A, b, variáveis

# Eliminação de Gauss sem pivotamento parcial
def eliminacao_gauss_sem_pivotamento(A, b):
    n = len(A)
    A = A.copy() # para não alterar a matriz original
    b = b.copy()
    imprimir_sistema_linear(A, b, "Sistema inicial") # mostra o sistema inicial
    for k in range(n-1):
        # Verifica se o pivô é zero (ou muito próximo)
        # se precisar de ser apenas 0 é só colocar para = 0, e ai nao tem a verificação e fica MENOS preciso
        if abs(A[k,k]) < 1e-20:
            print(f"Pivô zero detectado na linha {k+1} no método sem pivotamento. Não é possível continuar.")
            return None, None, None, False
        for i in range(k+1, n):
            # Calcula o fator de eliminação para zerar A[i,k]
            fator = -A[i,k] / A[k,k] # m_ik = -A_ik / A_kk
            # Atualiza a linha i da matriz A e o termo b
            A[i,k:] += fator * A[k,k:]
            b[i] += fator * b[k]
            print(f"Eliminando elemento A[{i+1},{k+1}], multiplicando linha {k+1} por {fator} e subtraindo da linha {i+1}:")
            imprimir_sistema_linear(A, b, f"Sistema após eliminar entrada A[{i+1},{k+1}]")
    # Verifica se algum pivô ficou zero após a eliminação
    if any(abs(A[i,i]) < 1e-20 for i in range(n)):
        print("Sistema impossível (pivô zero na diagonal após eliminação).")
        return None, None, None, False
    # Substituição regressiva para encontrar a solução x
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        soma = np.dot(A[i,i+1:], x[i+1:])
        x[i] = (b[i] - soma) / A[i,i]
    return x, A, b, False

# Eliminação de Gauss com pivotamento parcial
def eliminacao_gauss_com_pivotamento(A, b):
    n = len(A)
    A = A.copy()
    b = b.copy()
    imprimir_sistema_linear(A, b, "Sistema inicial")
    for k in range(n):
        # Escolhe o maior pivô na coluna k a partir da linha k
        pivo_linha = max(range(k, n), key=lambda i: abs(A[i,k]))
        print(f"Pivô escolhido: {pivo_linha}")
        if abs(A[pivo_linha,k]) < 1e-20:
            print("Sistema impossível (pivô zero detectado).")
            return None, None, None
        if pivo_linha != k:
            # Troca as linhas de A e b
            A[[k,pivo_linha]] = A[[pivo_linha,k]]
            b[[k,pivo_linha]] = b[[pivo_linha,k]]
            print(f"Trocando linha {k+1} com linha {pivo_linha+1} (pivoteamento):")
            imprimir_sistema_linear(A, b, f"Sistema após troca das linhas {k+1} e {pivo_linha+1}")
        for i in range(k+1, n):
            # faz as operações padrões de gauss m_kk = - a_ik / a_kk e L_i = m_ik * L_k + L_i
            fator = -A[i,k] / A[k,k]
            A[i,k:] += fator * A[k,k:]
            b[i] += fator * b[k]
            print(f"Eliminando elemento A[{i+1},{k+1}], multiplicando linha {k+1} por {fator} e subtraindo da linha {i+1}:")
            imprimir_sistema_linear(A, b, f"Sistema após eliminar entrada A[{i+1},{k+1}]")
    # Substituição regressiva
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        soma = np.dot(A[i,i+1:], x[i+1:])
        x[i] = (b[i] - soma) / A[i,i]
    return x, A, b

# Decomposição LU sem pivotamento
def lu_sem_pivot(A,b):
    n = len(A)
    U = A.astype(float).copy() # matriz superior
    L = np.eye(n) # matriz inferior
    imprimir_sistema_linear(U, b, "Matriz U inicial")
    imprimir_sistema_linear(L, b, "Matriz L inicial")
    for k in range(n-1):
        if abs(U[k,k]) < 1e-20:
            print(f"Pivô zero detectado na etapa {k+1} da decomposição LU sem pivotamento.")
            raise ZeroDivisionError("Pivô zero na LU sem pivotamento - sistema pode ser impossível ou indeterminado.")
        print(f'Etapa {k+1} da decomposição LU sem pivotamento:')
        for i in range(k+1, n):
            m = - U[i,k] / U[k,k] # fator multiplicador
            L[i,k] = - m # armazena o fator em L
            U[i,:] += m * U[k,:] # elimina o elemento abaixo do pivô
            print(f"m_{{{i+1},{k+1}}} = {m}")
            imprimir_sistema_linear(L, b, "Matriz L após etapa")
            imprimir_sistema_linear(U, b, "Matriz U após etapa")
    return L, U

# Decomposição LU com pivotamento parcial
def lu_com_pivot(A,b):
    n = len(A)
    U = A.astype(float).copy()
    L = np.eye(n)
    P = np.eye(n) # aqui cria a matriz identidade usando o numpy, que zera e mantem apenas a diagonal.
    imprimir_sistema_linear(U, b, "Matriz U inicial")
    imprimir_sistema_linear(L, b, "Matriz L inicial")
    imprimir_sistema_linear(P, np.zeros(n), "Matriz P inicial")
    for k in range(n-1):
        # Escolhe o maior pivô na coluna k
        pivo_linha = max(range(k, n), key=lambda i: abs(U[i,k]))
        if abs(U[pivo_linha,k]) < 1e-20:
            print("Sistema impossível (pivô zero detectado na LU com pivotamento).")
            return None
        if pivo_linha != k:
            # Troca linhas em U, P e L (até coluna k)
            U[[k, pivo_linha], :] = U[[pivo_linha, k], :]
            P[[k, pivo_linha], :] = P[[pivo_linha, k], :]
            if k > 0:
                L[[k, pivo_linha], :k] = L[[pivo_linha, k], :k]
            print(f"Trocando linha {k+1} com linha {pivo_linha+1} na matriz U (pivotamento):")
            imprimir_sistema_linear(U, b, "Matriz U após permutação")
            imprimir_sistema_linear(L, b, "Matriz L após permutação")
            imprimir_sistema_linear(P, np.zeros(n), "Matriz P após permutação")
        print(f'Etapa {k+1} da decomposição LU com pivotamento:')
        for i in range(k+1, n):
            m = -U[i,k] / U[k,k]   # fator negativo da eliminação de Gauss
            L[i,k] = -m             # matriz L armazena esse fator negativo
            U[i,:] += m * U[k,:]   # soma em U para zerar o elemento U[i,k]
            print(f"m_{{{i+1},{k+1}}} = {m}")
            imprimir_sistema_linear(L, np.zeros(n), "Matriz L após etapa")
            imprimir_sistema_linear(U, np.zeros(n), "Matriz U após etapa")
    return P, L, U

# stackoverflow progressiva 
# resolve Ly = b (decomp. LU)
def forward_solve(L, b):
    """
    Percorre as linhas de cima para baixo, resolvendo y[i] a cada passo.
    """
    n = len(L)
    y = np.zeros(n)
    for i in range(n):
        # y[i] depende apenas dos y já calculados (j < i)
        y[i] = (b[i] - np.dot(L[i,:i], y[:i])) / L[i,i]
    return y # retorna o vetor solução intermediário y

# stackoverflow regressiva
# resolve Ux = y (decomp. LU)
def backward_solve(U, y):
    """
    Percorre as linhas de baixo para cima, resolvendo x[i] a cada passo.
    """
    n = len(U)
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        # x[i] depende apenas dos x já calculados (j > i)
        x[i] = (y[i] - np.dot(U[i,i+1:], x[i+1:])) / U[i,i]
    return x # retorna o vetor solução x

# calcula o resíduo r = b - Ax
# se nao quiser ver o detalhe, é só trocar no menu para essa funcao direto
def calcular_residuo(A, x, b):
    """
    calcula o resíduo r = b - Ax, que indica o erro de solução x
    em relação ao sistema original Ax = b.
    """
    r = b - A @ x # Produto d matriz A*x e subtração de b
    return r

# só pra poder mostrar o resíduo bonitinho
def exibir_residuo_detalhado(A, x, b):
    """
    mostra as matrizes do resíduo r = b - Ax para cada linha do sistema
    """
    n = len(A)
    largura = 18
    print("\nMatrizes do cálculo do resíduo:")
    print("A:") # matriz A
    for i in range(n):
        print(" ".join(f"{A[i,j]:>{largura}}" for j in range(n)))
    print("\nx:") # matriz x
    for j in range(n):
        print(f"{x[j]:>{largura}}")
    print("\nb:") # matriz b
    for i in range(n):
        print(f"{b[i]:>{largura}}")
    r = b - A @ x
    print("\nr = b - A x:") # residuo r
    for i in range(n):
        print(f"{r[i]:>{largura}}")
    print()

# # pra substituir o np.zeros()
# def matriz_zeros_manual(n):
#     matriz = []
#     m = n
#     for i in range(m):
#         linha = []
#         for j in range(n):
#             linha.append(0)
#         matriz.append(linha)
#     return matriz

# # para criar matriz identidade  (seja pra L ou U na decomposição) pode usar o np.eye ou fazer manual:
# def matriz_identidade(n):
#     identidade = []
#     for i in range(n):
#         linha = []
#         for j in range(n):
#             if i == j:
#                 linha.append(1)
#             else:
#                 linha.append(0)
#         identidade.append(linha)
#     return identidade

# # pra multiplicar duas matrizes a e b (subsituindo o @ que é o operador padrão disso no python)
# def multiplicar_matrizes(A, B):
#     n_linhas_A, n_colunas_A = A.shape
#     n_linhas_B, n_colunas_B = B.shape
#     if n_colunas_A != n_linhas_B:
#         raise ValueError("Número de colunas de A deve ser igual ao número de linhas de B para multiplicar.")

#     resultado = np.zeros((n_linhas_A, n_colunas_B))

#     for i in range(n_linhas_A):
#         for j in range(n_colunas_B):
#             soma = 0
#             for k in range(n_colunas_A):
#                 soma += A[i, k] * B[k, j]
#             resultado[i, j] = soma
#     return resultado


"""
Interpolações - Parte 2

    Funções:
    - newton_dif_divididas(x, tabela, xp, max_grau=None)
    - gregory_newton_progressivo(x, y, xp, max_grau=None)
    - lagrange_interpol(x, y, xp, max_grau=None)
    - dispositivo_pratico_lagrange(x, y, xp, max_grau=None)
    - calcular_erro(func_str, x_vals, x_interp, grau, valor_interpolado)
    
    Funções Auxiliares:
    - dados_interpolacao()
    - obter_max_grau(n):
    - verifica_espaçamento_uniforme(x, tol=1e-15)
    - tabela_diferencas_divididas(x, y)
    - imprimir_tabela_diferencas_divididas(tabela)
    - tabela_diferencas_finitas(y)
    - imprimir_tabela_diferencas_finitas(tabela)
    - perguntar_erro(x_vals, x_interp, grau, valor_interpolado)
    
"""

def dados_interpolacao():
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


"""
Ajustes de Curvas - Parte 3

    Funções:
    - regressaolinear(x, y) # opcional!
    - regressaolinear_intervalo(x, y) # opcional!
    - minquadrados(x, y)
    - minquadrados_ordem_n_manual(x, y, ordem=1, tabela=True, grafico=True)
    - calcula_chi_e_r2(x, y, b0, b1, n_params=2)
    
    Funções Auxiliares:
    - log_output(message, logfile='log_resultados.txt') # opcional
    - dados() # especificamente  (pode ser para Interpolações e Ajustes de Curvas)
    - tabela_interpolador(x, y, p1x) # opcional
    - tabela_minimos_quadrados(x, y) # opcional

"""

# Configurações base para plotagem (aproveitamento codigo do projeto da bolsa)
plotpars_1x1 = {'axes.linewidth': 1.0,
                'axes.labelsize': 14,
                'xtick.labelsize': 14,
                'ytick.labelsize': 14,
                'legend.frameon': True,
                'legend.framealpha': 1,
                'legend.edgecolor': 'black',
                'legend.loc': 'upper right',
                'legend.fontsize': 12,
                'font.size': 14,
                'figure.figsize': (10, 8),
                'image.cmap': 'ocean_r'
               }

log = False
tabela = False
grafico = True

# reutilizado de outro codigo!
def log_output(message, logfile='log_resultados.txt'):
    """
    Função para registrar logs em arquivo com timestamp
    
    Parâmetros:
    - message: string com o conteúdo a ser registrado (pode conter múltiplas linhas)
    - logfile: nome do arquivo de log (padrão 'log_resultados.txt')
    
    O arquivo é aberto em modo append e cada chamada adiciona a mensagem com a data/hora corrente
    """
    if log==True:
        import datetime
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(logfile, 'a', encoding='utf-8') as f:
            f.write(f'[{timestamp}]\n{message}\n')
    else:
        pass

def dados_ajustes():
    """
    Função de entrada de dados:
    
    - Tratamento de zeros e entradas inválidas
    
    Saídas:     
    - Vetor x
    - Vetor y
    """
    
    try:
        n_str = input("Quantos pontos de dados? ")
        if not n_str.strip(): return np.array([]), np.array([])
        n = int(n_str)
        x = []
        y = []
        print("Digite os valores de x e y para o conjunto de dados:")
        for i in range(n):
            x_v = float(input(f"x[{i+1}] = "))
            y_v = float(input(f"y[{i+1}] = "))
            x.append(x_v)
            y.append(y_v)
            msg = (f"\n=========================\nPontos Inseridos\n=========================",
                   np.array(x),
                   np.array(y)
                   )
            log_output(msg)
        return np.array(x), np.array(y)
    except ValueError:
        print("Entrada inválida. Retornando arrays vazios.")
        return np.array([]), np.array([])

def tabela_interpolador(x, y, p1x):
    """
    Tabela para exibição dos cálculos pelo método dos mínimos quadrados:

    Entradas/Parâmetros: 
    - x (vetor de pontos em x)
    - y (vetor de pontos em y)
    - p1x (valores do polinomio interpolador de x)
    
    Fórmulas
    di = yi - p1(xi)
    
    Saídas:     
    - Tabela com i,xi,yi,p_1(xi),di,di**2 
    """
    import pandas as pd #opcional, apenas se quiser mostrar as tabelas formatadas

    di = y - p1x
    # di2 = di ** 2
    n = len(x)

    dados = {
        'i': np.arange(1, n + 1),
        'x': x,
        'y': y,
        'p1(x)': p1x,
        'di': di,
        # 'di^2': di2
    }
    df = pd.DataFrame(dados)
    soma = df[['x', 
               'y', 
               'p1(x)', 
               'di',
               #'di^2'
               ]].sum()
    soma['i'] = ''
    df = pd.concat([df, pd.DataFrame([soma])], ignore_index=True)
    print(df.to_string(index=False))
    msg = (f"\n=========================\nTabela Interpolador\n=========================\n",
           df.to_string(index=False))
    log_output(msg)


def tabela_minimos_quadrados(x, y):
    """
    Tabela para exibição dos cálculos pelo método dos mínimos quadrados:

    Entradas/Parâmetros: 
    - x (vetor de pontos em x)
    - y (vetor de pontos em y)

    Fórmulas
    b1 = (sum_xi * sum_yi - n * sum_xiyi) / (sum_xi ** 2 - n * sum_xi**2)
    b0 = (sum_yi - b1 * sum_xi) / n
    
    Saídas:     
    - Tabela com i,xi,yi,xi**2,yi**2,xiyi,ui,di,di**2
    """
    import pandas as pd #opcional, apenas se quiser mostrar as tabelas formatadas

    n = len(x)
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_x2 = np.sum(x ** 2)
    sum_xy = np.sum(x * y)
    # sum_y2 = np.sum(y ** 2)

    b1 = (sum_x * sum_y - n * sum_xy) / (sum_x ** 2 - n * sum_x2)
    b0 = (sum_y - b1 * sum_x) / n

    Ui = b0 + b1 * x
    d = y - Ui
    d2 = d ** 2

    data = {
        'i': np.arange(1, n + 1),
        'xi': x,
        'yi': y,
        'xi^2': x ** 2,
        'xiyi': x * y,
        'yi^2': y ** 2,
        'Ui': Ui,
        'di': d,
        'di^2': d2
    }

    df = pd.DataFrame(data)
    soma = df.sum(numeric_only=True)
    df = pd.concat([df, pd.DataFrame([soma])], ignore_index=True)
    print(df.to_string(index=False))
    msg = (df.to_string(index=False))
    log_output(msg)

def calcula_chi_e_r2(x, y, b0, b1, n_params=2):
    """
    Calcula chi-quadrado (ajustado), soma dos quadrados dos resíduos (desvio) e coeficiente de determinação R^2,
    recebendo explicitamente os coeficientes da reta (b0, b1) e os pontos (x, y).

    Parâmetros:
    x (np.array): valores de x
    y (np.array): valores observados
    b0 (float): coeficiente linear da reta
    b1 (float): coeficiente angular da reta
    n_params (int): número de parâmetros do modelo (p), padrão 2 para regressão linear

    Fórmulas:
    D(a0,a1) = sum((y_i - b0 - b1*x_i)^2)
    SQT = sum((y_i - y_media)^2)
    SQRes = sum((y_i - Ui)^2) onde Ui = b0 + b1 * x_i
    SQReg = sum((Ui - y_media)^2)
    R^2 = 1 - (SQRes / SQT)
    Chi^2 = D(a0,a1) / (n - p) (n = número de pontos, p = número de parâmetros do modelo)
    
    Retorna:
        chi2, r2, Desvio, SQT, SQRes, SQReg, Ui
    """
    x = np.array(x)
    y = np.array(y)
    n = len(y)

    Ui = b0 + b1 * x
    y_media = np.mean(y)

    # Soma total dos quadrados
    SQT = np.sum((y - y_media) ** 2)

    # Soma dos quadrados dos resíduos (Desvio)
    SQRes = np.sum((y - Ui) ** 2)

    # Soma dos quadrados da regressão
    SQReg = np.sum((Ui - y_media) ** 2)

    # Coeficiente de determinação R²
    r2 = 1 - (SQRes / SQT) if SQT != 0 else float('nan')

    # Chi-quadrado
    chi2 = SQRes / (n - n_params) if (n - n_params) > 0 else float('nan')

    desvio = SQRes

    print(f"Desvio D(a0,a1) = {desvio:.6f}")
    print(f"Chi² = {chi2:.6f}")
    print(f"SQT = {SQT:.6f}")
    print(f"SQRes = {SQRes:.6f}")
    print(f"SQReg = {SQReg:.6f}")
    print(f"R² = {r2:.6f}")

    msg = (f"\n=========================\nEstatísticas\n========================="
           f"\nDesvio D(a0,a1) = {desvio:.6f}"
           f"\nChi² = {chi2:.6f}"
           f"\nSQT = {SQT:.6f}"
           f"\nSQRes = {SQRes:.6f}"
           f"\nSQReg = {SQReg:.6f}"
           f"\nR² = {r2:.6f}"
           )
    log_output(msg)

    return {
        'Chi2': chi2,
        'R2': r2,
        'Desvio': desvio,
        'SQT': SQT,
        'SQRes': SQRes,
        'SQReg': SQReg,
        'Ui': Ui
    }

def regressaolinear(x, y):
    """
    Método 1: Polinômio interpolador de ordem 1
    - Escolhendo o primeiro e o último ponto, ou qualquer outro par de pontos inserido previamente pelo usuário.

    Entradas/Parâmetros: 
    - x (vetor de pontos em x)
    - y (vetor de pontos em y)
    - x0,y0; x1,y1 (pares de pontos escolhidos por indice)

    Fórmulas
    b1 = (y1 - y0) / (x1 - x0)         # Coeficiente angular (m)
    b0 = y0 - b1 * x0                  # Coeficiente linear (y)
    P_1(x) = y0 - ((y1 - y0)/(x1 - x0))*(x-x0)
    D(a0,a1) = sum((yi - p1(xi))^2)
    
    
    Saídas:     
    - Tabela com i,xi,yi,p_1(xi),di
    - Equação da reta
    - Desvio D(a0,a1)
    - Chi2, R2
    - Gráfico ilustrativo
    """
    
    n = len(x)
    if n < 2:
        print("São necessários pelo menos 2 pontos para esta operação.")
        return

    print("\n--- Seleção de Pontos para Interpolação ---")
    print("Pontos disponíveis:")
    for i in range(n):
        print(f" [{i+1}] -> (x: {x[i]:.2f}, y: {y[i]:.2f})")
    
    while True:
        try:
            p1 = int(input(f"Escolha o índice do 1o ponto (1 a {n}): ")) - 1
            p2 = int(input(f"Escolha o índice do 2o ponto (1 a {n}): ")) - 1
            
            if p1 == p2:
                print("Erro: Os pontos devem ser diferentes. Tente novamente.")
                continue
            if 0 <= p1 < n and 0 <= p2 < n:
                # Verifica se os valores de x são iguais (reta vertical, divisão por zero)
                if x[p1] == x[p2]:
                     print("Erro: Pontos com mesmo valor de X causam divisão por zero. Escolha outros.")
                     continue
                break
            else:
                print(f"Erro: Índices fora do intervalo (1 a {n}). Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite números inteiros.")

    x0, y0 = x[p1], y[p1]
    x1, y1 = x[p2], y[p2]

    # Eq. Reta: y - y0 = m * (x- x0)
    # Cálculo dos coeficientes da reta: y = b0 + b1*x
    b1 = (y1 - y0) / (x1 - x0)         # Coeficiente angular (m)
    b0 = y0 - b1 * x0                  # Coeficiente linear (y)
    
    print(f"\nPontos escolhidos: P{p1+1}({x0}, {y0}) e P{p2+1}({x1}, {y1})")

    # Calcula as estatísticas usando a reta definida pelos 2 pontos
    estatisticas = calcula_chi_e_r2(x, y, b0, b1)
    p1x = estatisticas['Ui']
    funcao = 'b0 + b1*x'

    msg = (f"\n=========================\nResultados\n========================="
           f"\nMétodo 1: Regressão Linear Simples"
           f"\nFunção: {funcao}"
           f"\nPolinômio interpolador: p1(x) = {b0:.4f} + {b1:.4f} * x"
           f"\nDesvio D(a0,a1) (SQRes) = {estatisticas['Desvio']:.4f}"
           f"\nChi² = {estatisticas['Chi2']:.4f}"
           f"\nR² = {estatisticas['R2']:.4f}"
           f"\n=========================\nTabela p1(x)\n========================="
           )
    log_output(msg)
    
    # Exibe tabela e resultados
    if tabela==True:
        tabela_interpolador(x, y, p1x)
    else:
        pass
    
    print(f"\nFunção: {funcao}")
    print(f"Polinômio interpolador: p1(x) = {b0:.4f} + {b1:.4f} * x")
    print(f"Desvio D(a0,a1) (SQRes) = {estatisticas['Desvio']:.4f}")
    print(f"Chi² = {estatisticas['Chi2']:.4f}")
    print(f"R² = {estatisticas['R2']:.4f}")

    if grafico==True:
        import matplotlib.pyplot as plt #opcional, apenas para exibir os gráficos 
        plt.rcParams.update(plotpars_1x1)  # atualizar parâmetros do plt
        # Plotagem
        legenda = (f'Função = {funcao}\n'
                f'y = {b1:.6f}x + {b0:.6f}\n'
                f'b1 = {b1:.6f}\n'
                f'b0 = {b0:.6f}\n'
                f'Desvio = {estatisticas["Desvio"]:.6f}\n'
                f'Chi² = {estatisticas["Chi2"]:.6f}\n'
                f'R² = {estatisticas["R2"]:.6f}')
        
        plt.scatter(x, y, color='green', s=50, label='Dados originais', zorder=3)
        
        # Destacar os pontos escolhidos
        plt.scatter([x0, x1], [y0, y1], color='purple', s=50, marker='o', label='Pontos Escolhidos', zorder=4)
        
        plt.plot(x, p1x, color='red', linestyle='-', label='Regressão Linear', linewidth=2)
        
        plt.title('Regressão Linear (Método 1)')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend(title=legenda, loc='upper left', fontsize=10, title_fontsize=10)
        plt.show()
    else:
        pass
   
def regressaolinear_intervalo(x, y):
    """
    Método 2: Polinômio interpolador de ordem 1 dentro do intervalo (x.min(x), x.max(x))
    - Inserindo pontos manualmente dentro do intervalo previamente definido com os dados da funcao dados()

    Entradas/Parâmetros: 
    - x (vetor de pontos em x)
    - y (vetor de pontos em y)

    Fórmulas
    P_1(x) = y0 - ((y1 - y0)/(x1 - x0))*(x-x0)
    D(a0,a1) = sum((yi - p1(xi))^2)
    
    Saídas:     
    - Tabela com i,xi,yi,p_1(xi),di
    - Equação da reta
    - Desvio D(a0,a1)
    - Chi2, R2
    - Gráfico ilustrativo
    """
    n = len(x)
    if n < 2:
        print("São necessários pelo menos 2 pontos no conjunto de dados para definir o intervalo.")
        return

    x_min = np.min(x)
    x_max = np.max(x)

    print("Informe dois pontos P1(x1,y1) e P2(x2,y2).")
    print(f"Restrição: Os valores de X devem estar entre [{x_min:.2f}, {x_max:.2f}]")

    while True:
        try:
            print("\nPonto 1:")
            x1 = float(input(" x1: "))
            if not (x_min <= x1 <= x_max):
                 print(f" Erro: x1 deve estar entre {x_min:.2f} e {x_max:.2f}.")
                 continue
            y1 = float(input(" y1: "))

            print("\nPonto 2:")
            x2 = float(input('x2: '))
            if not (x_min <= x2 <= x_max):
                 print(f" Erro: x2 deve estar entre {x_min:.2f} e {x_max:.2f}.")
                 continue
            if x1 == x2:
                print(" Erro: x2 deve ser diferente de x1 para não gerar uma reta vertical (divisão por zero).")
                continue
            y2 = float(input(" y2: "))
            
            break # Se chegou aqui, tudo válido
        except ValueError:
            print(" Entrada inválida. Digite números válidos.")

    # Eq. Reta: y - y1 = m * (x- x1)
    # Cálculo dos coeficientes da reta definida pelos pontos manuais
    b1 = (y2 - y1) / (x2 - x1) # (m)
    b0 = y1 - b1 * x1 # (y)

    # Calcula as estatísticas para os dados ORIGINAIS usando essa reta
    estatisticas = calcula_chi_e_r2(x, y, b0, b1)
    p1x = estatisticas['Ui']
    funcao = 'b0 + b1*x'

    msg = (f"\n=========================\nResultados\n========================="
           f"\nMétodo 2: Regressão Linear Intervalo"
           f"\nFunção: {funcao}"
           f"\nPolinômio interpolador: p1(x) = {b0:.4f} + {b1:.4f} * x"
           f"\nDesvio D(a0,a1) (SQRes) = {estatisticas['Desvio']:.4f}"
           f"\nChi² = {estatisticas['Chi2']:.4f}"
           f"\nR² = {estatisticas['R2']:.4f}"
           f"\n=========================\nTabela p1(x)\n========================="
           )
    log_output(msg)
    
    if tabela==True:
        tabela_interpolador(x, y, p1x)
    else:
        pass
    
    print(f"\nFunção: {funcao}")
    print(f"Polinômio Interpolador: p_1(x) = {b0:.6f} + {b1:.6f} * x")
    print(f"Desvio D(a0,a1) (SQRes) = {estatisticas['Desvio']:.6f}")
    print(f"Chi² = {estatisticas['Chi2']:.6f}")
    print(f"R² = {estatisticas['R2']:.6f}")

    if grafico==True:
        import matplotlib.pyplot as plt #opcional, apenas para exibir os gráficos 
        plt.rcParams.update(plotpars_1x1)  # atualizar parâmetros do plt
        # Plotagem
        legenda = (f'Função = {funcao}\n'
                f'y = {b1:.6f}x + {b0:.6f}\n'
                f'b1 = {b1:.6f}\n'
                f'b0 = {b0:.6f}\n'
                f'Desvio = {estatisticas["Desvio"]:.6f}\n'
                f'Chi² = {estatisticas["Chi2"]:.6f}\n'
                f'R² = {estatisticas["R2"]:.6f}')

        # Dados originais
        plt.scatter(x, y, color='green', s=50, label='Dados originais', zorder=3)
        
        # Pontos manuais que definiram a reta
        plt.scatter([x1, x2], [y1, y2], color='purple', s=50, marker='o', label='Pontos Escolhidos', zorder=4)
        
        # Para plotar a reta estendida por todo o gráfico
        x_plot = np.linspace(x_min, x_max, 100)
        y_plot = b0 + b1 * x_plot
        
        plt.plot(x_plot, y_plot, color='red', linestyle='-', label='Regressão Linear', linewidth=1)
        plt.title('Regressão Linear (Método 2)')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend(title=legenda, loc='upper left', fontsize=10, title_fontsize=10)
        plt.show()   
    else:
        pass   

def minquadrados(x, y):
    """
    Método 3: Mínimos Quadrados
    - É a derivada do desvio igualada a 0 com respeito a b0 e b1 (parciais)

    Entradas/Parâmetros: 
    - x (vetor de pontos em x)
    - y (vetor de pontos em y)

    Fórmulas:
    b0 = (sum(yi) - b1*sum(xi)) / n
    b1 = (sum(xi)*sum(yi) - n*sum(xiyi))/((sum(xi)**2) - n*sum(xi**2))
    D(b0,b1) = sum((yi - (b0 + b1*xi))^2)
    
    Saídas:     
    - Tabela com i,xi,yi,xi**2,yi**2,xiyi,ui,di,di**2
    - Equação da reta
    - Desvio D(b0,b1)
    - Chi2, R2
    - Gráfico ilustrativo
    """
    n = len(x)
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_xy = np.sum(x * y)
    sum_x2 = np.sum(x ** 2)
    sum_y2 = np.sum(y ** 2)

    b1 = (sum_x * sum_y - n * sum_xy) / ((sum_x) ** 2 - n * sum_x2)
    b0 = (sum_y - b1 * sum_x) / n

    estatisticas = calcula_chi_e_r2(x, y, b0, b1, n_params=2)
    funcao = 'b0+b1*x'
    
    msg = (f"\n=========================\nResultados\n========================="
           f"\nMétodo 3: Mínimos Quadrados"
           f"\nFunção: {funcao}"
           f"\nPolinômio interpolador: p1(x) = {b0:.4f} + {b1:.4f} * x"
           f"\nDesvio D(a0,a1) (SQRes) = {estatisticas['Desvio']:.4f}"
           f"\nChi² = {estatisticas['Chi2']:.4f}"
           f"\nR² = {estatisticas['R2']:.4f}"
           f"\n=========================\nTabela Mínimos Quadrados\n========================="
           )
    log_output(msg)
    
    #criação da tabela de mínimos quadrados
    if tabela==True:
        tabela_minimos_quadrados(x, y)
    else:
        pass
    
    print(f"\nFunção: {funcao}")
    print(f"Equação da reta: y = {b1:.6f}x + {b0:.6f}")
    print(f"Desvio D(a0,a1) (SQRes) = {estatisticas['Desvio']:.6f}")
    print(f"Chi² = {estatisticas['Chi2']:.6f}")
    print(f"R²: {estatisticas['R2']:.6f}")
 
    # Resoluções específicas da questão 1c e 1e
    # questao1c(b0,b1)
    # questao1e(b0,b1)
    
    if grafico==True:
        import matplotlib.pyplot as plt #opcional, apenas para exibir os gráficos 
        # Plotagem
        legenda = (f'Função = {funcao}\n'
                f'y = {b1:.6f}x + {b0:.6f}\n'
                f'b1 = {b1:.6f}\n'
                f'b0 = {b0:.6f}\n'
                f'Desvio = {estatisticas["Desvio"]:.6f}\n'
                f'Chi² = {estatisticas["Chi2"]:.6f}\n'
                f'R² = {estatisticas["R2"]:.6f}')

        plt.scatter(x, y, color='purple', label='Pontos originais')
        plt.plot(x, estatisticas['Ui'], color='red', label='Ajuste - Mínimos Quadrados')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Regressão Linear (Método 3. - Mínimos Quadrados)')
        plt.legend(title=legenda, loc='upper left', fontsize=10, title_fontsize=10)
        plt.show()
    else:
        pass  

def minquadrados_ordem_n_manual(x, y, ordem=1, tabela=True, grafico=True):
    """
    Método 3: Mínimos Quadrados

    Entradas/Parâmetros: 
    - x (vetor de pontos em x)
    - y (vetor de pontos em y)
    - ordem (1,n)
    - tabela (pra mostrar x,ui,di,di**2)
    - gráfico com legenda mostrando as infos calculadas.

    Fórmulas:
    basicamente montar um sistema e resolver por Gauss (poderia ser por decomposição LU tb)
    
    Saídas:     
    - Equação da reta
    - Desvio
    - Chi2, R2
    - Gráfico ilustrativo
    """
    n = len(x)
    if n == 0 or ordem < 0:
        print("Dados insuficientes ou ordem inválida.")
        return None

    # Somatórios S_x^k para k=0..2*ordem
    Sx = [np.sum(x ** k) for k in range(2 * ordem + 1)]
    # Somatórios S_x^k y para k=0..ordem
    Sxy = [np.sum((x ** k) * y) for k in range(ordem + 1)]

    # Montar matriz do sistema normal (seria o equivalente a usar a funcao de montar sistema que fiz em sistemaslineares.py)
    ATA = np.zeros((ordem+1, ordem+1))
    for i in range(ordem + 1):
        for j in range(ordem + 1):
            ATA[i, j] = Sx[i + j]
    # Lado direito
    ATy = np.array(Sxy)

    # Resolver sistema pelo método manual
    coef = eliminacao_gauss_sem_pivotamento(ATA, ATy)

    # Calcular valores ajustados
    Ui = np.zeros(n)
    for k in range(ordem + 1):
        Ui += coef[k] * (x ** k)

    """
    Estatísticas calculadas internamente direto, poderia ter usado a função, mas como é só um método não achei necessário
    """
    y_media = np.mean(y)
    SQT = np.sum((y - y_media) ** 2)
    SQRes = np.sum((y - Ui) ** 2)
    SQReg = np.sum((Ui - y_media) ** 2)
    r2 = 1 - (SQRes / SQT) if SQT != 0 else float('nan')
    chi2 = SQRes / (n - (ordem + 1)) if (n - (ordem + 1)) > 0 else float('nan')

    # equação da reta
    termos = [f"({coef[i]:.6f})x^{i}" if i > 0 else f"({coef[i]:.6f})" for i in range(ordem + 1)]
    equacao = " + ".join(termos)
    print("\nEquação ajustada:")
    print("p(x) = " + equacao)

    # Coeficientes
    print("\nCoeficientes:")
    for i, c in enumerate(coef):
        print(f"a{i} = {c:.6f}")

    print(f"\nEstatísticas do ajuste:")
    print(f"Desvio (SQRes) = {SQRes:.6f}")
    print(f"Chi² ajustado = {chi2:.6f}")
    print(f"R² = {r2:.6f}")


    # Tabela contendo os dados assim como para o MMQ de ordem 1 (reaproveitado, apenas fiz direto aqui pra poupar linhas de código)
    if tabela:
        data = {
            'i': np.arange(1, n+1),
            'xi': x,
            'yi': y,
        }
        for k in range(ordem + 1):
            data[f'x^{k}'] = x ** k
        data['Ui'] = Ui
        data['di'] = y - Ui
        data['di^2'] = (y - Ui) ** 2

        df = pd.DataFrame(data)
        soma = df.sum(numeric_only=True)
        df = pd.concat([df, pd.DataFrame([soma])], ignore_index=True)
        print("\nTabela de cálculos intermediários:")
        print(df.to_string(index=False))

    if grafico:
        xp = np.linspace(np.min(x), np.max(x), 500)
        yp = np.zeros_like(xp)
        for k in range(ordem + 1):
            yp += coef[k] * (xp ** k)

        legenda = (f'y = {equacao}\n'
                f'Desvio = {SQRes:.6f}\n'
                f'Chi² = {chi2:.6f}\n'
                f'R² = {r2:.6f}')
        plt.scatter(x, y, color='purple', label='Pontos originais')
        plt.plot(xp, yp, color='red', label=f'Ajuste - Polinômio grau {ordem}')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(f'Regressão Mínimos Quadrados - Grau {ordem}')
        plt.legend(title=legenda, loc='upper left', fontsize=10, title_fontsize=10)
        plt.show()

    return coef

def menu_bases():
    while True:
        opcao = dados_bases()
        if opcao == '0':
            return
        if opcao == '1':
            s = input("Digite o número binário (ex: 1011): ").strip()
            print(f"Decimal: {binario_para_decimal(s)}")
        elif opcao == '2':
            try:
                n = int(input("Digite o número decimal (inteiro): "))
                print(f"Binário: {decimal_para_binario(n)}")
            except ValueError:
                print("Entrada inválida. Digite um inteiro.")
        elif opcao == '3':
            s = input("Digite o número binário (ex: 1111): ").strip()
            print(f"Hexadecimal: {binario_para_hexadecimal(s)}")
        elif opcao == '4':
            s = input("Digite o número hexadecimal (ex: FE): ").strip()
            print(f"Binário: {hexadecimal_para_binario(s)}")
        elif opcao == '5':
            try:
                n = int(input("Digite o número decimal (inteiro): "))
                print(f"Hexadecimal: {decimal_para_hexadecimal(n)}")
            except ValueError:
                print("Entrada inválida. Digite um inteiro.")
        elif opcao == '6':
            s = input("Digite o número hexadecimal (ex: 1A3): ").strip()
            print(f"Decimal: {hexadecimal_para_decimal(s)}")
        else:
            print("Opção inválida. Tente novamente.")

def menu_sistemas():
    while True:
        print("\n=== Sistemas Lineares ===")
        print("1 - Eliminação de Gauss (sem pivotamento)")
        print("2 - Eliminação de Gauss (com pivotamento parcial)")
        print("3 - Decomposição LU (sem pivotamento)")
        print("4 - Decomposição LU (com pivotamento)")
        print("5 - Calcular resíduo (b - A x)")
        print("0 - Voltar")
        op = input("Escolha uma opção: ").strip()
        if op == '0':
            return
        try:
            A, b, vars = montar_sistema_valores()
        except Exception as e:
            print(f"Erro ao montar o sistema: {e}")
            continue

        if op == '1':
            x, Atri, btri, flag = eliminacao_gauss_sem_pivotamento(A, b)
            if x is None:
                print("Não foi possível obter solução.")
            else:
                print(f"Solução x = {x}")
        elif op == '2':
            x, Atri, btri = eliminacao_gauss_com_pivotamento(A, b)
            if x is None:
                print("Não foi possível obter solução.")
            else:
                print(f"Solução x = {x}")
        elif op == '3':
            try:
                L, U = lu_sem_pivot(A, b)
                y = forward_solve(L, b)
                x = backward_solve(U, y)
                print(f"Solução x = {x}")
            except Exception as e:
                print(f"Erro na LU sem pivotamento: {e}")
        elif op == '4':
            res = lu_com_pivot(A, b)
            if res is None:
                print("LU com pivotamento falhou.")
            else:
                P, L, U = res
                # aplica permutação P ao vetor b
                try:
                    Pb = P @ b
                    y = forward_solve(L, Pb)
                    x = backward_solve(U, y)
                    print(f"Solução x = {x}")
                except Exception as e:
                    print(f"Erro ao resolver após pivotamento: {e}")
        elif op == '5':
            # pede sistema e solução do usuário ou resolver pelo próprio método
            escolha = input("Deseja inserir solução x manualmente? (s/n): ").strip().lower()
            if escolha == 's':
                try:
                    x_vals = list(map(float, input("Digite x separados por espaço: ").split()))
                    x = np.array(x_vals, dtype=float)
                    r = calcular_residuo(A, x, b)
                    print(f"Resíduo r = {r}")
                except Exception as e:
                    print(f"Entrada inválida: {e}")
            else:
                # tenta resolver por gauss com pivot
                x, *_ = eliminacao_gauss_com_pivotamento(A, b)
                if x is None:
                    print("Não foi possível resolver o sistema para calcular resíduo.")
                else:
                    r = calcular_residuo(A, x, b)
                    print(f"Solução x = {x}")
                    print(f"Resíduo r = {r}")
        else:
            print("Opção inválida.")

def menu_interpolacao():
    while True:
        print("\n=== Interpolações ===")
        print("1 - Newton (diferenças divididas)")
        print("2 - Gregory-Newton progressivo")
        print("3 - Lagrange")
        print("4 - Dispositivo prático Lagrange")
        print("0 - Voltar")
        op = input("Escolha uma opção: ").strip()
        if op == '0':
            return
        try:
            x_vals, y_vals, xp = dados_interpolacao()
        except Exception as e:
            print(f"Erro na leitura dos pontos: {e}")
            continue

        max_grau = obter_max_grau(len(x_vals))

        if op == '1':
            tabela = tabela_diferencas_divididas(x_vals, y_vals)
            resultado = newton_dif_divididas(x_vals, tabela, xp, max_grau)
            print(f"Resultado (Newton): {resultado}")
        elif op == '2':
            uniforme, h = verifica_espaçamento_uniforme(x_vals)
            if not uniforme:
                print("Atenção: pontos não têm espaçamento uniforme. Gregory-Newton pode ser impreciso.")
            resultado = gregory_newton_progressivo(np.array(x_vals), np.array(y_vals), xp, max_grau)
            print(f"Resultado (Gregory-Newton): {resultado}")
        elif op == '3':
            resultado = lagrange_interpol(np.array(x_vals), np.array(y_vals), xp, max_grau)
            print(f"Resultado (Lagrange): {resultado}")
        elif op == '4':
            resultado = dispositivo_pratico_lagrange(np.array(x_vals), np.array(y_vals), xp, max_grau)
            print(f"Resultado (Dispositivo de Lagrange): {resultado}")
        else:
            print("Opção inválida.")

def menu_ajustes():
    while True:
        print("\n=== Ajustes de Curvas ===")
        print("1 - Regressão linear (método 1)")
        print("2 - Regressão linear por intervalo (método 2)")
        print("3 - Mínimos quadrados (linear)")
        print("4 - Mínimos quadrados (ordem n)")
        print("0 - Voltar")
        op = input("Escolha uma opção: ").strip()
        if op == '0':
            return
        x, y = dados_ajustes()
        if x.size == 0:
            print("Nenhum dado fornecido.")
            continue

        if op == '1':
            regressaolinear(x, y)
        elif op == '2':
            regressaolinear_intervalo(x, y)
        elif op == '3':
            minquadrados(x, y)
        elif op == '4':
            try:
                ordem = int(input("Digite a ordem do polinômio (inteiro >=0): "))
            except ValueError:
                print("Ordem inválida. Usando ordem 1.")
                ordem = 1
            minquadrados_ordem_n_manual(x, y, ordem=ordem)
        else:
            print("Opção inválida.")

def menu_principal():
    while True:
        print("\n=== Cálculo Numérico - Menu Principal ===")
        print("1 - Conversão de Bases")
        print("2 - Sistemas Lineares")
        print("3 - Interpolações")
        print("4 - Ajustes de Curvas")
        print("0 - Sair")
        escolha = input("Escolha uma opção: ").strip()
        if escolha == '0':
            print("Saindo...")
            break
        elif escolha == '1':
            menu_bases()
        elif escolha == '2':
            menu_sistemas()
        elif escolha == '3':
            menu_interpolacao()
        elif escolha == '4':
            menu_ajustes()
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    menu_principal()