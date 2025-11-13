import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def eliminacao_gauss(a, b):
    """
    Função Solução Sistema de Matrizes por Eliminação de Gauss:
    Aproveitado do Código de Matrizes (Primeira etapa do curso) e adaptado
    
    Saídas:
    Solução dos valores de X
    """
    n = len(a)
    A = a.copy() # para não alterar a matriz original
    b = b.copy()
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
    # Verifica se algum pivô ficou zero após a eliminação
    if any(abs(A[i,i]) < 1e-20 for i in range(n)):
        print("Sistema impossível (pivô zero na diagonal após eliminação).")
        return None, None, None, False
    # Substituição regressiva para encontrar a solução x
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        soma = np.dot(A[i,i+1:], x[i+1:])
        x[i] = (b[i] - soma) / A[i,i]
    return x

def dados():
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
        return np.array(x), np.array(y)
    except ValueError:
        print("Entrada inválida. Retornando arrays vazios.")
        return np.array([]), np.array([])

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
    coef = eliminacao_gauss(ATA, ATy)

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

def menu():
    """
    Menu contendo a função pra pedir os dados, ou opcionalmente ja inserir manualmente (não ter que redigitar toda vez!)
    """
    
    x = []
    y = []
    
    # x = [0,2,4,6,9,11,12,15,17,19] # altura
    # y = [5,6,7,6,9,8,7,10,12,12] # peso
    
    # x = [1,2,3,4,5,6,7,8]
    # y = [0.5, 0.6, 0.9, 0.8, 1.2, 1.5, 1.7, 2.0]
    
    # x_val = np.array(x)
    # y_val = np.array(y)    
    
    x, y = dados()
    
    #pedir ordem 
    if len(x) == 0:
        return
    ordem_str = input("Ordem do polinômio para ajuste (ex: 1 para linear): ")
    try:
        ordem = int(ordem_str)
    except ValueError:
        print("Ordem inválida, usando 1 (linear).")
        ordem = 1
    minquadrados_ordem_n_manual(x, y, ordem=ordem, tabela=True, grafico=True) # usar aqui com os dados da função de pedir dados
    # minquadrados_ordem_n_manual(x_val, y_val, ordem=ordem, tabela=True, grafico=True) # usar aqui com os valores diretamente inseridos.

if __name__ == '__main__':
    menu()