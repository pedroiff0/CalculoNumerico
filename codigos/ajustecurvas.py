#author: pedro h r andrade
#pip3 install numpy, matplotlib, pandas

import numpy as np #opcional, apenas para simplificar os somatórios, vetores, etc...

# Configurações base para plotagem (aproveitamento codigo do projeto da bolsa)
plotpars_1x1 = {'axes.linewidth': 1.0,
                'axes.labelsize': 18,
                'xtick.labelsize': 18,
                'ytick.labelsize': 18,
                'legend.frameon': True,
                'legend.framealpha': 0.65,
                'legend.edgecolor': 'black',
                'legend.loc': 'upper right',
                'legend.fontsize': 12,
                'font.size': 12,
                'figure.figsize': (7., 5.),
                'image.cmap': 'ocean_r'
               }

## VARIÁVEIS GLOBAIS DE CONTROLE PARA GRÁFICOS, LOGS E TABELAS.

tabela = False
grafico = True

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
    # msg = (df.to_string(index=False))
    # log_output(msg)

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

    """
    msg = (f"\n=========================\nEstatísticas\n========================="
           f"\nDesvio D(a0,a1) = {desvio:.6f}"
           f"\nChi² = {chi2:.6f}"
           f"\nSQT = {SQT:.6f}"
           f"\nSQRes = {SQRes:.6f}"
           f"\nSQReg = {SQReg:.6f}"
           f"\nR² = {r2:.6f}"
           )
    log_output(msg)
    """
    
    return {
        'Chi2': chi2,
        'R2': r2,
        'Desvio': desvio,
        'SQT': SQT,
        'SQRes': SQRes,
        'SQReg': SQReg,
        'Ui': Ui
    }

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
    
    """
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
    """
    
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

def menu():
    x = []
    y = []
    
    # Questão 1:
    # x = [183, 173, 168, 188, 158, 163, 193, 163, 178] # altura
    # y = [79, 69, 70, 81, 61, 63, 79, 71, 73] # peso
    
    # Questão 2:
    # x = [1,2,3,4,5,6,7,8]
    # y = [0.5, 0.6, 0.9, 0.8, 1.2, 1.5, 1.7, 2.0]
    
    # x_val = np.array(x)
    # y_val = np.array(y)    
    
    x, y = dados()
    minquadrados(x, y)
    # minquadrados(x_val, y_val) # para usar essa função, utilize os dados prontos, e comente as linhas de obtenção de dados

if __name__ == '__main__':
    menu()