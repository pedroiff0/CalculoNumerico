import numpy as np

def imprimir_sistema_linear(A, b, titulo="Sistema de Equações"):
    n = len(A)
    largura = 24
    print(f"\n{titulo}:")
    total_largura = (largura + 1) * A.shape[1] + largura + 2
    print("-" * total_largura)
    for i in range(n):
        linha = ""
        for j in range(A.shape[1]):
            linha += f"{A[i,j]:>{largura}} "
        linha += f"|{b[i]:>{largura}}"
        print(linha)
    print("-" * total_largura)
    print()

def montar_sistema_valores():
    n = int(input("Digite o número de variáveis (sistema quadrado): "))
    print(f"Insira os coeficientes da matriz A ({n} linhas), cada linha com {n} valores separados por espaço:")
    A = []
    for i in range(n):
        linha = list(map(float, input(f"Linha {i+1}: ").split()))
        if len(linha) != n:
            raise ValueError("Número de coeficientes deve ser igual ao número de variáveis!")
        A.append(linha)
    print(f"Insira os termos independentes do vetor b em uma única linha, {n} valores separados por espaço:")
    b = list(map(float, input("b: ").split()))
    if len(b) != n:
        raise ValueError("Número de termos independentes deve ser igual ao número de variáveis!")
    return np.array(A, dtype=float), np.array(b, dtype=float), [f"x{i+1}" for i in range(n)]

def eliminacao_gauss_sem_pivotamento(A, b):
    n = len(A)
    A = A.copy()
    b = b.copy()
    imprimir_sistema_linear(A, b, "Sistema inicial")
    for k in range(n-1):
        if abs(A[k,k]) < 1e-15:
            print(f"Pivô zero detectado na linha {k+1} no método sem pivotamento.")
            resp = input("Deseja trocar para o método com pivotamento? (s/n): ").strip().lower()
            if resp == 's':
                return None, None, None, True
            else:
                raise ZeroDivisionError("Pivô zero no método sem pivotamento e usuário optou por não trocar.")
        for i in range(k+1, n):
            fator = A[i,k] / A[k,k]
            A[i,k:] -= fator * A[k,k:]
            b[i] -= fator * b[k]
            print(f"Eliminando elemento A[{i+1},{k+1}], multiplicando linha {k+1} por {fator} e subtraindo da linha {i+1}:")
            imprimir_sistema_linear(A, b, f"Sistema após eliminar entrada A[{i+1},{k+1}]")
    if any(abs(A[i,i]) < 1e-15 for i in range(n)):
        print("Sistema impossível (pivô zero na diagonal após eliminação).")
        return None, None, None, False
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        soma = np.dot(A[i,i+1:], x[i+1:])
        x[i] = (b[i] - soma) / A[i,i]
    return x, A, b, False

def eliminacao_gauss_com_pivotamento(A, b):
    n = len(A)
    A = A.copy()
    b = b.copy()
    imprimir_sistema_linear(A, b, "Sistema inicial")
    for k in range(n):
        pivo_linha = max(range(k, n), key=lambda i: abs(A[i,k]))
        if abs(A[pivo_linha,k]) < 1e-15:
            print("Sistema impossível (pivô zero detectado).")
            return None, None, None
        if pivo_linha != k:
            A[[k,pivo_linha]] = A[[pivo_linha,k]]
            b[[k,pivo_linha]] = b[[pivo_linha,k]]
            print(f"Trocando linha {k+1} com linha {pivo_linha+1} (pivoteamento):")
            imprimir_sistema_linear(A, b, f"Sistema após troca das linhas {k+1} e {pivo_linha+1}")
        for i in range(k+1, n):
            fator = A[i,k] / A[k,k]
            A[i,k:] -= fator * A[k,k:]
            b[i] -= fator * b[k]
            print(f"Eliminando elemento A[{i+1},{k+1}], multiplicando linha {k+1} por {fator} e subtraindo da linha {i+1}:")
            imprimir_sistema_linear(A, b, f"Sistema após eliminar entrada A[{i+1},{k+1}]")
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        soma = np.dot(A[i,i+1:], x[i+1:])
        x[i] = (b[i] - soma) / A[i,i]
    return x, A, b

def lu_sem_pivot(A):
    n = len(A)
    U = A.astype(float).copy()
    L = np.eye(n)
    imprimir_sistema_linear(U, np.zeros(n), "Matriz U inicial")
    imprimir_sistema_linear(L, np.zeros(n), "Matriz L inicial")
    for k in range(n-1):
        if abs(U[k,k]) < 1e-15:
            print(f"Pivô zero detectado na etapa {k+1} da decomposição LU sem pivotamento.")
            raise ZeroDivisionError("Pivô zero na LU sem pivotamento - sistema pode ser impossível ou indeterminado.")
        print(f'Etapa {k+1} da decomposição LU sem pivotamento:')
        for i in range(k+1, n):
            m = U[i,k] / U[k,k]
            L[i,k] = m
            U[i,:] = U[i,:] - m * U[k,:]
            print(f"m_{{{i+1},{k+1}}} = {m}")
            imprimir_sistema_linear(L, np.zeros(n), "Matriz L após etapa")
            imprimir_sistema_linear(U, np.zeros(n), "Matriz U após etapa")
    return L, U

def lu_com_pivot(A):
    n = len(A)
    U = A.astype(float).copy()
    L = np.eye(n)
    P = np.eye(n)
    imprimir_sistema_linear(U, np.zeros(n), "Matriz U inicial")
    imprimir_sistema_linear(L, np.zeros(n), "Matriz L inicial")
    imprimir_sistema_linear(P, np.zeros(n), "Matriz P inicial")
    for k in range(n-1):
        pivo_linha = max(range(k, n), key=lambda i: abs(U[i,k]))
        if abs(U[pivo_linha,k]) < 1e-15:
            print("Sistema impossível (pivô zero detectado na LU com pivotamento).")
            return None
        if pivo_linha != k:
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

def forward_solve(L, b):
    n = len(L)
    y = np.zeros(n)
    for i in range(n):
        y[i] = (b[i] - np.dot(L[i,:i], y[:i])) / L[i,i]
    return y

def backward_solve(U, y):
    n = len(U)
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - np.dot(U[i,i+1:], x[i+1:])) / U[i,i]
    return x

def calcular_residuo(A, x, b):
    r = b - A @ x
    return r

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
                x, Atri, bmod, deseja_pivot = eliminacao_gauss_sem_pivotamento(A, b)
                if deseja_pivot:
                    x, Atri, bmod = eliminacao_gauss_com_pivotamento(A, b)
                    print("\nSolução pelo método de Gauss com pivotamento (alternativo):")
                elif x is None:
                    print("Sistema impossível pelo método sem pivotamento.")
                    continue
                else:
                    print("\nSolução pelo método de Gauss sem pivotamento:")
                for var, val in zip(vars, x):
                    print(f"{var} = {val}")
                residuo = calcular_residuo(A, x, b)
                print("\nResíduo (Ax - b):")
                for i, r in enumerate(residuo):
                    print(f"r{i+1} = {r}")
            elif opcao == '2':
                x, Atri, bmod = eliminacao_gauss_com_pivotamento(A, b)
                if x is None:
                    print("Sistema impossível pelo método com pivotamento.")
                    continue
                print("\nSolução pelo método de Gauss com pivotamento:")
                for var, val in zip(vars, x):
                    print(f"{var} = {val}")
                residuo = calcular_residuo(A, x, b)
                print("\nResíduo (Ax - b):")
                for i, r in enumerate(residuo):
                    print(f"r{i+1} = {r}")
            elif opcao == '3':
                L, U = lu_sem_pivot(A)
                y = forward_solve(L, b)
                x = backward_solve(U, y)
                print("\nSolução pela decomposição LU sem pivotamento:")
                for var, val in zip(vars, x):
                    print(f"{var} = {val}")
                residuo = calcular_residuo(A, x, b)
                print("\nResíduo (Ax - b):")
                for i, r in enumerate(residuo):
                    print(f"r{i+1} = {r}")
            elif opcao == '4':
                result = lu_com_pivot(A)
                if result is None:
                    print("Sistema impossível pela decomposição LU com pivotamento.")
                    continue
                P, L, U = result
                b_mod = P @ b
                y = forward_solve(L, b_mod)
                x = backward_solve(U, y)
                print("\nSolução pela decomposição LU com pivotamento:")
                for var, val in zip(vars, x):
                    print(f"{var} = {val}")
                residuo = calcular_residuo(A, x, b)
                print("\nResíduo (Ax - b):")
                for i, r in enumerate(residuo):
                    print(f"r{i+1} = {r}")
            else:
                print("Opção inválida. Tente novamente.")
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    menu()