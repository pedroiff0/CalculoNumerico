import numpy as np

"""Utilitários para resolução de sistemas lineares.

Módulo contendo funções para montagem e exibição de sistemas lineares,
eliminação de Gauss (com e sem pivotamento), decomposição LU (com e sem
pivotamento), forward/backward solves e cálculo do resíduo.

Todas as funções aceitam entradas ``array_like`` (listas, arrays numpy, etc.),
convertem internamente para ``numpy.ndarray`` quando necessário, e retornam
estruturas numpy compatíveis para fácil integração com demais rotinas.
"""

def _validate_linear_system_inputs(A, b):
    """Valida e converte entradas para funções de sistemas lineares.
    
    Parameters
    ----------
    A : array_like
        Matriz dos coeficientes.
    b : array_like
        Vetor dos termos independentes.
        
    Returns
    -------
    A_valid, b_valid : np.ndarray
        Entradas validadas e convertidas para float.
        
    Raises
    ------
    ValueError
        Se as entradas não forem válidas.
    """
    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float)
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("A deve ser uma matriz quadrada 2D.")
    if b.ndim != 1 or b.shape[0] != A.shape[0]:
        raise ValueError("b deve ser um vetor 1D com comprimento igual ao número de linhas de A.")
    return A, b

def _validate_lu_inputs(A, b):
    """Valida entradas para funções de decomposição LU.
    
    Parameters
    ----------
    A : array_like
        Matriz a ser decomposta.
    b : array_like or None
        Vetor opcional para exibição.
        
    Returns
    -------
    A_valid, b_valid : np.ndarray
        Entradas validadas.
    """
    A = np.asarray(A, dtype=float)
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("A deve ser uma matriz quadrada 2D.")
    if b is not None:
        b = np.asarray(b, dtype=float)
        if b.ndim != 1 or b.shape[0] != A.shape[0]:
            raise ValueError("b deve ser um vetor 1D com comprimento igual ao número de linhas de A.")
    return A, b

def imprimir_sistema_linear(A, b, titulo="Sistema de Equações", verbose=True):
    """Exibe um sistema linear A|b formatado no terminal.

    Parameters
    ----------
    A : np.ndarray
        Matriz de coeficientes (n x n).
    b : np.ndarray or None
        Vetor dos termos independentes (n,), ou None se não houver.
    titulo : str, optional
        Título a ser exibido antes do sistema (default: ``'Sistema de Equações'``).
    verbose : bool, optional
        Se True, imprime o sistema; se False, não imprime nada (default: True).
    """
    if not verbose:
        return
    n = len(A)
    largura = 24 
    print(f"\n{titulo}:")
    for i in range(n):
        linha = ""
        for j in range(A.shape[1]):
            linha += f"{A[i,j]:>{largura}} "
        if b is not None:
            linha += f"|{b[i]:>{largura}}"
        print(linha)
    print()
    
def montar_sistema_valores():
    """Lê interativamente os coeficientes de um sistema linear quadrado.

    Solicita ao usuário o número de variáveis ``n``, em seguida lê ``n`` linhas
    com ``n`` coeficientes cada e um vetor ``b`` com ``n`` termos. Faz validações
    simples de comprimento e converte para ``numpy.ndarray``.

    Returns
    -------
    A : np.ndarray
        Matriz dos coeficientes (n x n).
    b : np.ndarray
        Vetor dos termos independentes (n,).
    vars : list
        Lista de nomes das variáveis (ex.: ['x1','x2', ...]).

    Raises
    ------
    ValueError
        Se o número de elementos fornecidos por linha não corresponder a ``n``.
    """
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

def eliminacao_gauss_sem_pivotamento(A, b, verbose=False):
    """Executa a eliminação de Gauss sem pivotamento parcial.

    Triangulariza a matriz ``A`` e aplica substituição regressiva para
    obter a solução ``x``. Esta versão não realiza trocas de linha, por
    isso pode falhar para matrizes que exigem pivotamento.

    Parameters
    ----------
    A : array_like, shape (n, n)
        Matriz dos coeficientes do sistema linear.
    b : array_like, shape (n,)
        Vetor dos termos independentes.
    verbose : bool, optional
        Se True, imprime os passos da eliminação; se False, executa silenciosamente (default: False).

    Returns
    -------
    tuple
        ``(x, A_triangular, b_modificado, erro_flag)`` onde ``x`` é o vetor
        solução (ou ``None`` em caso de falha), ``A_triangular`` é a matriz A
        após eliminação e ``b_modificado`` o vetor b modificado. ``erro_flag`` é
        ``False`` em execução bem-sucedida ou ``True`` em caso de erro.
    """
    A, b = _validate_linear_system_inputs(A, b)
    n = A.shape[0]
    A = A.copy()
    b = b.copy()
    imprimir_sistema_linear(A, b, "Sistema inicial", verbose)
    for k in range(n-1):
        if abs(A[k,k]) < 1e-20:
            if verbose:
                print(f"Pivô zero detectado na linha {k+1} no método sem pivotamento. Não é possível continuar.")
            return None, None, None, True
        for i in range(k+1, n):
            fator = -A[i,k] / A[k,k] 
            A[i,k:] += fator * A[k,k:]
            b[i] += fator * b[k]
            if verbose:
                print(f"Eliminando elemento A[{i+1},{k+1}], multiplicando linha {k+1} por {fator} e subtraindo da linha {i+1}:")
                imprimir_sistema_linear(A, b, f"Sistema após eliminar entrada A[{i+1},{k+1}]", verbose)
    if any(abs(A[i,i]) < 1e-20 for i in range(n)):
        if verbose:
            print("Sistema impossível (pivô zero na diagonal após eliminação).")
        return None, None, None, True
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        soma = np.dot(A[i,i+1:], x[i+1:])
        x[i] = (b[i] - soma) / A[i,i]
    return x, A, b, False

def eliminacao_gauss_com_pivotamento(A, b, verbose=False):
    """Executa a eliminação de Gauss com pivotamento parcial.

    Triangulariza a matriz ``A`` com trocas de linha para escolher o melhor pivô,
    e aplica substituição regressiva para obter a solução ``x``.

    Parameters
    ----------
    A : array_like, shape (n, n)
        Matriz dos coeficientes do sistema linear.
    b : array_like, shape (n,)
        Vetor dos termos independentes.
    verbose : bool, optional
        Se True, imprime os passos da eliminação; se False, executa silenciosamente (default: False).

    Returns
    -------
    tuple
        ``(x, A_triangular, b_modificado, erro_flag)`` onde ``x`` é o vetor
        solução (ou ``None`` em caso de falha), ``A_triangular`` é a matriz A
        após eliminação e ``b_modificado`` o vetor b modificado. ``erro_flag`` é
        ``False`` em execução bem-sucedida ou ``True`` em caso de erro.
    """
    A, b = _validate_linear_system_inputs(A, b)
    n = A.shape[0]
    A = A.copy()
    b = b.copy()
    imprimir_sistema_linear(A, b, "Sistema inicial", verbose)
    for k in range(n):
        pivo_linha = max(range(k, n), key=lambda i: abs(A[i,k]))
        if verbose:
            print(f"Pivô escolhido: {pivo_linha}")
        if abs(A[pivo_linha,k]) < 1e-20:
            if verbose:
                print("Sistema impossível (pivô zero detectado).")
            return None, None, None, True
        if pivo_linha != k:
            A[[k,pivo_linha]] = A[[pivo_linha,k]]
            b[[k,pivo_linha]] = b[[pivo_linha,k]]
            if verbose:
                print(f"Trocando linha {k+1} com linha {pivo_linha+1} (pivoteamento):")
                imprimir_sistema_linear(A, b, f"Sistema após troca das linhas {k+1} e {pivo_linha+1}", verbose)
        for i in range(k+1, n):
            fator = -A[i,k] / A[k,k]
            A[i,k:] += fator * A[k,k:]
            b[i] += fator * b[k]
            if verbose:
                print(f"Eliminando elemento A[{i+1},{k+1}], multiplicando linha {k+1} por {fator} e subtraindo da linha {i+1}:")
                imprimir_sistema_linear(A, b, f"Sistema após eliminar entrada A[{i+1},{k+1}]", verbose)
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        soma = np.dot(A[i,i+1:], x[i+1:])
        x[i] = (b[i] - soma) / A[i,i]
    return x, A, b, False

def lu_sem_pivot(A, b, verbose=False):
    """Decomposição LU sem pivotamento.

    Calcula matrizes ``L`` (inferior) e ``U`` (superior) tais que
    ``A = L @ U`` quando possível. Não realiza pivotamento; um pivô zero
    provoca exceção ``ZeroDivisionError``.

    Parameters
    ----------
    A : array_like, shape (n, n)
        Matriz a ser decomposta.
    b : array_like
        (opcional) vetor usado apenas para exibição durante passos (pode ser
        ``None`` quando não for necessário).
    verbose : bool, optional
        Se True, imprime os passos da decomposição; se False, executa silenciosamente (default: False).

    Returns
    -------
    L, U : np.ndarray
        Matrizes inferior e superior da decomposição LU.
    """
    A, b = _validate_lu_inputs(A, b)
    n = A.shape[0]
    U = A.astype(float).copy()
    L = np.eye(n)
    if verbose:
        imprimir_sistema_linear(U, b, "Matriz U inicial", verbose)
        imprimir_sistema_linear(L, b, "Matriz L inicial", verbose)
    for k in range(n-1):
        if abs(U[k,k]) < 1e-20:
            if verbose:
                print(f"Pivô zero detectado na etapa {k+1} da decomposição LU sem pivotamento.")
            raise ZeroDivisionError("Pivô zero na LU sem pivotamento - sistema pode ser impossível ou indeterminado.")
        if verbose:
            print(f'Etapa {k+1} da decomposição LU sem pivotamento:')
        for i in range(k+1, n):
            m = - U[i,k] / U[k,k]
            L[i,k] = - m 
            U[i,:] += m * U[k,:]
            if verbose:
                print(f"m_{{{i+1},{k+1}}} = {m}")
                imprimir_sistema_linear(L, b, "Matriz L após etapa", verbose)
                imprimir_sistema_linear(U, b, "Matriz U após etapa", verbose)
    return L, U

def lu_com_pivot(A, b, verbose=False):
    """Decomposição LU com pivotamento parcial.

    Retorna a tripla ``P, L, U`` tal que ``P @ A = L @ U``.

    Parameters
    ----------
    A : array_like, shape (n, n)
        Matriz a ser decomposta.
    b : array_like
        (opcional) vetor usado apenas para exibição durante passos.
    verbose : bool, optional
        Se True, imprime os passos da decomposição; se False, executa silenciosamente (default: False).

    Returns
    -------
    P, L, U : np.ndarray
        ``P`` matriz de permutação, ``L`` inferior, ``U`` superior.
    """
    A, b = _validate_lu_inputs(A, b)
    n = A.shape[0]
    U = A.astype(float).copy()
    L = np.eye(n)
    P = np.eye(n)
    if verbose:
        imprimir_sistema_linear(U, b, "Matriz U inicial", verbose)
        imprimir_sistema_linear(L, b, "Matriz L inicial", verbose)
        imprimir_sistema_linear(P, np.zeros(n), "Matriz P inicial", verbose)
    for k in range(n-1):
        pivo_linha = max(range(k, n), key=lambda i: abs(U[i,k]))
        if abs(U[pivo_linha,k]) < 1e-20:
            if verbose:
                print("Sistema impossível (pivô zero detectado na LU com pivotamento).")
            return None
        if pivo_linha != k:
            U[[k, pivo_linha], :] = U[[pivo_linha, k], :]
            P[[k, pivo_linha], :] = P[[pivo_linha, k], :]
            if k > 0:
                L[[k, pivo_linha], :k] = L[[pivo_linha, k], :k]
            if verbose:
                print(f"Trocando linha {k+1} com linha {pivo_linha+1} na matriz U (pivotamento):")
                imprimir_sistema_linear(U, b, "Matriz U após permutação", verbose)
                imprimir_sistema_linear(L, b, "Matriz L após permutação", verbose)
                imprimir_sistema_linear(P, np.zeros(n), "Matriz P após permutação", verbose)
        if verbose:
            print(f'Etapa {k+1} da decomposição LU com pivotamento:')
        for i in range(k+1, n):
            m = -U[i,k] / U[k,k]   
            L[i,k] = -m             
            U[i,:] += m * U[k,:]   
            if verbose:
                print(f"m_{{{i+1},{k+1}}} = {m}")
                imprimir_sistema_linear(L, np.zeros(n), "Matriz L após etapa", verbose)
                imprimir_sistema_linear(U, np.zeros(n), "Matriz U após etapa", verbose)
    return P, L, U

def forward_solve(L, b):
    """Resolve o sistema triangular inferior L y = b por substituição progressiva.

    Parameters
    ----------
    L : array_like, shape (n, n)
        Matriz triangular inferior (diagonal não-nula esperada).
    b : array_like, shape (n,)
        Vetor de termos independentes.

    Returns
    -------
    y : np.ndarray
        Solução do sistema triangular inferior.
    """
    L = np.asarray(L, dtype=float)
    b = np.asarray(b, dtype=float)
    if L.ndim != 2 or L.shape[0] != L.shape[1]:
        raise ValueError("L deve ser uma matriz quadrada 2D.")
    if b.ndim != 1 or b.shape[0] != L.shape[0]:
        raise ValueError("b deve ser um vetor 1D com comprimento igual ao número de linhas de L.")
    n = L.shape[0]
    y = np.zeros(n)
    for i in range(n):
        y[i] = (b[i] - np.dot(L[i,:i], y[:i])) / L[i,i]
    return y

def backward_solve(U, y):
    """Resolve o sistema triangular superior U x = y por substituição regressiva.

    Parameters
    ----------
    U : array_like, shape (n, n)
        Matriz triangular superior.
    y : array_like, shape (n,)
        Vetor do lado direito (resultado da forward_solve).

    Returns
    -------
    x : np.ndarray
        Solução do sistema triangular superior.
    """
    U = np.asarray(U, dtype=float)
    y = np.asarray(y, dtype=float)
    if U.ndim != 2 or U.shape[0] != U.shape[1]:
        raise ValueError("U deve ser uma matriz quadrada 2D.")
    if y.ndim != 1 or y.shape[0] != U.shape[0]:
        raise ValueError("y deve ser um vetor 1D com comprimento igual ao número de linhas de U.")
    n = U.shape[0]
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - np.dot(U[i,i+1:], x[i+1:])) / U[i,i]
    return x

def calcular_residuo(A, x, b):
    """Calcula o resíduo r = b - A x.

    Parameters
    ----------
    A : array_like
        Matriz dos coeficientes.
    x : array_like
        Solução candidata do sistema.
    b : array_like
        Vetor do lado direito.

    Returns
    -------
    r : np.ndarray
        Vetor resíduo (b - A x).
    """
    A = np.asarray(A, dtype=float)
    x = np.asarray(x, dtype=float)
    b = np.asarray(b, dtype=float)
    if A.ndim != 2:
        raise ValueError("A deve ser uma matriz 2D.")
    if x.ndim != 1 or x.shape[0] != A.shape[1]:
        raise ValueError("x deve ser um vetor 1D com comprimento igual ao número de colunas de A.")
    if b.ndim != 1 or b.shape[0] != A.shape[0]:
        raise ValueError("b deve ser um vetor 1D com comprimento igual ao número de linhas de A.")
    r = b - A @ x
    return r

def exibir_residuo_detalhado(A, x, b):
    """Exibe detalhadamente as matrizes A, x, b e o resíduo r = b - A x.

    Útil para depuração e apresentação passo a passo da solução do sistema.
    """
    n = len(A)
    largura = 18
    print("\nMatrizes do cálculo do resíduo:")
    print("A:")
    for i in range(n):
        print(" ".join(f"{A[i,j]:>{largura}}" for j in range(n)))
    print("\nx:")
    for j in range(n):
        print(f"{x[j]:>{largura}}")
    print("\nb:")
    for i in range(n):
        print(f"{b[i]:>{largura}}")
    r = b - A @ x
    print("\nr = b - A x:")
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
                x, Atri, bmod, _ = eliminacao_gauss_sem_pivotamento(A, b) 
                if x is None:
                    print("Sistema impossível pelo método sem pivotamento.") 
                    continue
                print("\nSolução pelo método de Gauss sem pivotamento:")
                for var, val in zip(vars, x):
                    print(f"{var} = {val}") 
                exibir_residuo_detalhado(A, x, b) 
            elif opcao == '2':
                x, Atri, bmod = eliminacao_gauss_com_pivotamento(A, b)
                if x is None:
                    print("Sistema impossível pelo método com pivotamento.") 
                    continue
                print("\nSolução pelo método de Gauss com pivotamento:")
                for var, val in zip(vars, x):
                    print(f"{var} = {val}") 
                exibir_residuo_detalhado(A, x, b) 
            elif opcao == '3':
                L, U = lu_sem_pivot(A,b)
                y = forward_solve(L, b) 
                x = backward_solve(U, y) 
                print("\nSolução pela decomposição LU sem pivotamento:")
                for var, val in zip(vars, x):
                    print(f"{var} = {val}") 
                exibir_residuo_detalhado(A, x, b) 
            elif opcao == '4':
                result = lu_com_pivot(A,b)
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
                exibir_residuo_detalhado(A, x, b) 
            else:
                print("Opção inválida. Tente novamente.")
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    menu()