import numpy as np

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
def lu_sem_pivot(A):
    n = len(A)
    U = A.astype(float).copy() # matriz superior
    L = np.eye(n) # matriz inferior
    imprimir_sistema_linear(U, np.zeros(n), "Matriz U inicial")
    imprimir_sistema_linear(L, np.zeros(n), "Matriz L inicial")
    for k in range(n-1):
        if abs(U[k,k]) < 1e-20:
            print(f"Pivô zero detectado na etapa {k+1} da decomposição LU sem pivotamento.")
            raise ZeroDivisionError("Pivô zero na LU sem pivotamento - sistema pode ser impossível ou indeterminado.")
        print(f'Etapa {k+1} da decomposição LU sem pivotamento:')
        for i in range(k+1, n):
            m = U[i,k] / U[k,k] # fator multiplicador
            L[i,k] = m # armazena o fator em L
            U[i,:] = U[i,:] - m * U[k,:] # elimina o elemento abaixo do pivô
            print(f"m_{{{i+1},{k+1}}} = {m}")
            imprimir_sistema_linear(L, np.zeros(n), "Matriz L após etapa")
            imprimir_sistema_linear(U, np.zeros(n), "Matriz U após etapa")
    return L, U

# Decomposição LU com pivotamento parcial
def lu_com_pivot(A):
    n = len(A)
    U = A.astype(float).copy()
    L = np.eye(n)
    P = np.eye(n)
    imprimir_sistema_linear(U, np.zeros(n), "Matriz U inicial")
    imprimir_sistema_linear(L, np.zeros(n), "Matriz L inicial")
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
            imprimir_sistema_linear(U, np.zeros(n), "Matriz U após permutação")
            imprimir_sistema_linear(L, np.zeros(n), "Matriz L após permutação")
            imprimir_sistema_linear(P, np.zeros(n), "Matriz P após permutação")
        print(f'Etapa {k+1} da decomposição LU com pivotamento:')
        for i in range(k+1, n):
            m = U[i,k] / U[k,k]
            L[i,k] = m
            U[i,:] = U[i,:] - m * U[k,:]
            print(f"m_{{{i+1},{k+1}}} = {m}")
            imprimir_sistema_linear(L, np.zeros(n), "Matriz L após atualização")
            imprimir_sistema_linear(U, np.zeros(n), "Matriz U após atualização")
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

def menu():
    while True:
        print("\nMenu de métodos para resolver sistemas lineares:")
        print("1 - Método de Gauss sem pivotamento")
        print("2 - Método de Gauss com pivotamento")
        print("3 - Decomposição LU sem pivotamento")
        print("4 - Decomposição LU com pivotamento")
        print("0 - Sair")
        opcao = input("Escolha a opção desejada: ")

        if opcao == '0':
            print("Encerrando o programa.")
            break

        try:
            A, b, vars = montar_sistema_valores()
            if opcao == '1':
                x, Atri, bmod, _ = eliminacao_gauss_sem_pivotamento(A, b) # variavel, a trinangular, b _ era uma opcao para trocar q removi
                if x is None:
                    print("Sistema impossível pelo método sem pivotamento.") # se der algum 0 diagonal, ou encontrar pivo 0.
                    continue
                print("\nSolução pelo método de Gauss sem pivotamento:")
                for var, val in zip(vars, x):
                    print(f"{var} = {val}") # exibir a solução
                exibir_residuo_detalhado(A, x, b) # resíduo mostrando Ax - b = r
            elif opcao == '2':
                x, Atri, bmod = eliminacao_gauss_com_pivotamento(A, b) # variavel, a tringualar, b
                if x is None:
                    print("Sistema impossível pelo método com pivotamento.") # se o pivotamento ainda assim der 0 na diagonal.
                    continue
                print("\nSolução pelo método de Gauss com pivotamento:")
                for var, val in zip(vars, x):
                    print(f"{var} = {val}") # exibir solução
                exibir_residuo_detalhado(A, x, b) # resíduo mostrando Ax - b = r 
            elif opcao == '3':
                L, U = lu_sem_pivot(A)
                y = forward_solve(L, b) # resolve em baixo Ly = b
                x = backward_solve(U, y) # resolve em cima = Ux = y
                print("\nSolução pela decomposição LU sem pivotamento:")
                for var, val in zip(vars, x):
                    print(f"{var} = {val}") # exibir solução
                exibir_residuo_detalhado(A, x, b) # resíduo mostrando Ax - b = r
            elif opcao == '4':
                result = lu_com_pivot(A)
                if result is None:
                    print("Sistema impossível pela decomposição LU com pivotamento.")
                    continue
                P, L, U = result # P (matriz Identidade), L = Lower, U = Upper
                b_mod = P @ b # operação para multiplicar as duas matrizes 
                y = forward_solve(L, b_mod) # resolve em baixo Ly = b
                x = backward_solve(U, y) # resolve em cima = Ux = y
                print("\nSolução pela decomposição LU com pivotamento:")
                for var, val in zip(vars, x):
                    print(f"{var} = {val}") # exibir solução
                exibir_residuo_detalhado(A, x, b) # resíduo mostrando Ax - b = r
            else:
                print("Opção inválida. Tente novamente.")
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    menu()