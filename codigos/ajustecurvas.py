#auhtor: pedro h r andrade
#pip3 install numpy, matplotlib, pandas

import numpy as np #opcional, apenas para simplificar os somatórios, vetores, etc...
import matplotlib.pyplot as plt #opcional, apenas para exibir os gráficos
from codigos.sistemaslineares import eliminacao_gauss_com_pivotamento
import pandas as pd

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

## VARIÁVEIS GLOBAIS DE CONTROLE PARA GRÁFICOS, LOGS E TABELAS.

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

    # Resolver sistema pelo método de pivotamento (retornar apenas o vetor solução)
    sol = eliminacao_gauss_com_pivotamento(ATA, ATy)
    if sol is None:
        raise RuntimeError("Falha ao resolver sistema normal para mínimos quadrados de ordem n")
    # eliminacao_gauss_com_pivotamento pode retornar (x, A, b) ou apenas x
    if isinstance(sol, (tuple, list)):
        candidate = sol[0]
    else:
        candidate = sol
    coef = np.asarray(candidate, dtype=float).ravel()

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

#resolução específica da questão 1c (para as estimatias, só substituir!)
# para utilizar, descomente a chamada na função minquadrados()
def questao1c(b0,b1):
    print("\nQuestão 1c):")
    altura_est = 175 # (x)
    peso_est = b0 + b1 * altura_est
    print(f"Peso estimado para altura {altura_est:.2f} cm: {peso_est:.2f} kg")
    
    # Estimativa de altura para peso 80 kg (inverter a equação)
    peso_ref = 80 # (y)
    altura_est_inv = (peso_ref - b0) / b1
    print(f"Altura estimada para peso {peso_ref:.2f} kg: {altura_est_inv:.2f} cm")

# resolução específica da questão 1e pois os eixos estão invertidos, as contas mudam
# para utilizar, descomente a chamada na função minquadrados()
def questao1e(b0,b1):
    print("\nQuestão 1e):")
    peso_est = 80 # (x)
    altura_est = b0 + b1 * peso_est
    print(f"Altura estimada para peso {peso_est:.2f} kg: {altura_est:.2f} cm")
        
    altura_est = 175 # (y)
    peso_est = (altura_est - b0) / b1
    print(f"Peso estimado para altura {altura_est:.2f} cm: {peso_est:.2f} kg")     

# //TODO: Adicionar FIT POLINOMIAL de grau n, sem usar numpy.polyfit
# //TODO: Adicionar FIT EXPONENCIAL, LOGARÍTMICO, TRIGONOMÉTRICO

def menu():
    """Menu interativo de demonstração para Ajustes de Curvas.

    Fornece opções para regressão linear, mínimos quadrados (linear) e ajuste
    polinomial de ordem n. Este docstring foi simplificado para evitar problemas
    de formatação no Sphinx e melhorar a legibilidade.
    """
    x = []
    y = []
    
    #questão 1a,b,c)
    # x = [183, 173, 168, 188, 158, 163, 193, 163, 178] # altura
    # y = [79, 69, 70, 81, 61, 63, 79, 71, 73] # peso
    
    #questão 1d,e)
    # x = [79, 69, 70, 81, 61, 63, 79, 71, 73] # peso
    # y = [183, 173, 168, 188, 158, 163, 193, 163, 178] # altura
    
    # x_val = np.array(x)
    # y_val = np.array(y)    
    
    while True:
        print("\n================ MENU DE REGRESSÕES ================")
        print("1. Regressão Linear Simples (Polinômio de grau 1)")
        print("2. Regressão Linear No Intervalo (Polinômio de grau 1)")
        print("3. Método dos Quadrados Mínimos")
        print("0. Sair")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == '0':
            print("Saindo do programa.")
            break
        elif opcao == "1":
            x, y = dados()
            regressaolinear(x, y)
            # regressaolinear(x_val, y_val) # para usar essa função, utilize os dados prontos, e comente as linhas de obtenção de dados
        elif opcao == "2":
            x, y = dados()
            regressaolinear_intervalo(x, y)
            # regressaolinear_intervalo(x_val, y_val) # para usar essa função, utilize os dados prontos, e comente as linhas de obtenção de dados
        elif opcao == "3":
            x, y = dados()
            minquadrados(x, y)
            # minquadrados(x_val, y_val) # para usar essa função, utilize os dados prontos, e comente as linhas de obtenção de dados
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    menu()