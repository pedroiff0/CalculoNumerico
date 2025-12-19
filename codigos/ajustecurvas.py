import numpy as np
from codigos.sistemaslineares import eliminacao_gauss_com_pivotamento
import pandas as pd
import matplotlib.pyplot as plt

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

def _validate_curve_fitting_inputs(x, y):
    """
    Parameters
    ----------
    x, y : array_like
        Pontos de dados para ajuste.
    
    Returns
    -------
    x_valid, y_valid : np.ndarray
        Entradas validadas e convertidas.
    
    Raises
    ------
    ValueError
        Se as entradas não forem válidas.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 1:
        raise ValueError("x deve ser um array 1D.")
    if y.ndim != 1:
        raise ValueError("y deve ser um array 1D.")
    if len(x) != len(y):
        raise ValueError("x e y devem ter o mesmo comprimento.")
    if len(x) < 2:
        raise ValueError("São necessários pelo menos 2 pontos para ajuste de curvas.")
    return x, y

def dados():
    """
    Função de entrada de dados interativa.

    Solicita ao usuário o número de pontos e os valores de x e y,
    com validação de entrada e tratamento de erros.

    Returns:
    - Vetor x (np.ndarray)
    - Vetor y (np.ndarray)
    """
    try:
        n_str = input("Quantos pontos de dados? ")
        if not n_str.strip():
            print("Entrada vazia. Retornando arrays vazios.")
            return np.array([]), np.array([])
        n = int(n_str)
        if n < 2:
            print("São necessários pelo menos 2 pontos para ajuste de curvas.")
            return np.array([]), np.array([])

        print(f"Insira os valores de x em uma única linha, {n} valores separados por espaço:")
        x_input = input("x: ").strip()
        if not x_input:
            print("Entrada vazia para x. Retornando arrays vazios.")
            return np.array([]), np.array([])
        x = list(map(float, x_input.split()))
        if len(x) != n:
            print(f"Número de valores x ({len(x)}) deve ser igual ao número especificado ({n})!")
            return np.array([]), np.array([])

        print(f"Insira os valores de y em uma única linha, {n} valores separados por espaço:")
        y_input = input("y: ").strip()
        if not y_input:
            print("Entrada vazia para y. Retornando arrays vazios.")
            return np.array([]), np.array([])
        y = list(map(float, y_input.split()))
        if len(y) != n:
            print(f"Número de valores y ({len(y)}) deve ser igual ao número especificado ({n})!")
            return np.array([]), np.array([])

        return np.array(x), np.array(y)
    except ValueError as e:
        print(f"Entrada inválida: {e}. Retornando arrays vazios.")
        return np.array([]), np.array([])
    except Exception as e:
        print(f"Erro inesperado: {e}. Retornando arrays vazios.")
        return np.array([]), np.array([])

def tabela_interpolador(x, y, p1x, verbose=True):
    """
    Tabela para exibição dos cálculos pelo método dos mínimos quadrados.

    Parameters:
    - x, y: vetores de pontos
    - p1x: valores do polinomio interpolador
    - verbose: se True, imprime a tabela
    """
    import pandas as pd

    di = y - p1x
    n = len(x)

    dados = {
        'i': np.arange(1, n + 1),
        'x': x,
        'y': y,
        'p1(x)': p1x,
        'di': di,
    }
    df = pd.DataFrame(dados)
    soma = df[['x', 'y', 'p1(x)', 'di']].sum()
    soma['i'] = ''
    df = pd.concat([df, pd.DataFrame([soma])], ignore_index=True)
    if verbose:
        print(df.to_string(index=False))


def tabela_minimos_quadrados(x, y, verbose=True):
    """
    Tabela para exibição dos cálculos pelo método dos mínimos quadrados:

    Entradas/Parâmetros: 
    - x (vetor de pontos em x)
    - y (vetor de pontos em y)
    - verbose (bool): se True, imprime a tabela; se False, executa silenciosamente

    Fórmulas
    b1 = (sum_xi * sum_yi - n * sum_xiyi) / (sum_xi ** 2 - n * sum_xi**2)
    b0 = (sum_yi - b1 * sum_xi) / n
    
    Saídas:     
    - Tabela com i,xi,yi,xi**2,yi**2,xiyi,ui,di,di**2
    """
    import pandas as pd

    n = len(x)
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_x2 = np.sum(x ** 2)
    sum_xy = np.sum(x * y)

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
    if verbose:
        print(df.to_string(index=False))

def calcula_chi_e_r2(x, y, b0, b1, n_params=2, verbose=True):
    """
    Calcula chi-quadrado (ajustado), soma dos quadrados dos resíduos (desvio) e coeficiente de determinação R^2,
    recebendo explicitamente os coeficientes da reta (b0, b1) e os pontos (x, y).

    Parâmetros:
    x (np.array): valores de x
    y (np.array): valores observados
    b0 (float): coeficiente linear da reta
    b1 (float): coeficiente angular da reta
    n_params (int): número de parâmetros do modelo (p), padrão 2 para regressão linear
    verbose (bool): se True, imprime os resultados; se False, executa silenciosamente

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

    SQT = np.sum((y - y_media) ** 2)

    SQRes = np.sum((y - Ui) ** 2)

    SQReg = np.sum((Ui - y_media) ** 2)

    r2 = 1 - (SQRes / SQT) if SQT != 0 else float('nan')

    chi2 = SQRes / (n - n_params) if (n - n_params) > 0 else float('nan')

    desvio = SQRes

    if verbose:
        print(f"Desvio D(a0,a1) = {desvio:.6f}")
        print(f"Chi² = {chi2:.6f}")
        print(f"SQT = {SQT:.6f}")
        print(f"SQRes = {SQRes:.6f}")
        print(f"SQReg = {SQReg:.6f}")
        print(f"R² = {r2:.6f}")

    return {
        'Chi2': chi2,
        'R2': r2,
        'Desvio': desvio,
        'SQT': SQT,
        'SQRes': SQRes,
        'SQReg': SQReg,
        'Ui': Ui
    }

def regressaolinear(x, y, verbose=True, tabela=None, grafico=None):
    """
    Método 1: Polinômio interpolador de ordem 1
    - Escolhendo o primeiro e o último ponto, ou qualquer outro par de pontos inserido previamente pelo usuário.

    Entradas/Parâmetros: 
    - x (vetor de pontos em x)
    - y (vetor de pontos em y)
    - verbose (bool): se True, imprime resultados; se False, executa silenciosamente
    - tabela (bool): se True, mostra tabela; se None, usa variável global
    - grafico (bool): se True, mostra gráfico; se None, usa variável global
    - x0,y0; x1,y1 (pares de pontos escolhidos por indice)

    Fórmulas
    b1 = (y1 - y0) / (x1 - x0)        
    b0 = y0 - b1 * x0                 
    P_1(x) = y0 - ((y1 - y0)/(x1 - x0))*(x-x0)
    D(a0,a1) = sum((yi - p1(xi))^2)
    
    
    Saídas:     
    - Tabela com i,xi,yi,p_1(xi),di
    - Equação da reta
    - Desvio D(a0,a1)
    - Chi2, R2
    - Gráfico ilustrativo
    """
    x, y = _validate_curve_fitting_inputs(x, y)
    
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

    b1 = (y1 - y0) / (x1 - x0)
    b0 = y0 - b1 * x0
    
    if verbose:
        print(f"\nPontos escolhidos: P{p1+1}({x0}, {y0}) e P{p2+1}({x1}, {y1})")

    estatisticas = calcula_chi_e_r2(x, y, b0, b1, verbose=verbose)
    p1x = estatisticas['Ui']
    funcao = 'b0 + b1*x'
   
    if tabela is None:
        tabela = globals().get('tabela', True)
    if tabela:
        tabela_interpolador(x, y, p1x, verbose=verbose)
    else:
        pass
    
    if verbose:
        print(f"\nFunção: {funcao}")
        print(f"Polinômio interpolador: p1(x) = {b0:.4f} + {b1:.4f} * x")
        print(f"Desvio D(a0,a1) (SQRes) = {estatisticas['Desvio']:.4f}")
        print(f"Chi² = {estatisticas['Chi2']:.4f}")
        print(f"R² = {estatisticas['R2']:.4f}")

    if grafico is None:
        grafico = globals().get('grafico', True)
    if grafico and verbose:
        import matplotlib.pyplot as plt
        plt.rcParams.update(plotpars_1x1)
        legenda = (f'Função = {funcao}\n'
                f'y = {b1:.6f}x + {b0:.6f}\n'
                f'b1 = {b1:.6f}\n'
                f'b0 = {b0:.6f}\n'
                f'Desvio = {estatisticas["Desvio"]:.6f}\n'
                f'Chi² = {estatisticas["Chi2"]:.6f}\n'
                f'R² = {estatisticas["R2"]:.4f}')
        
        plt.scatter(x, y, color='green', s=50, label='Dados originais', zorder=3)
        
        plt.scatter([x0, x1], [y0, y1], color='purple', s=50, marker='o', label='Pontos Escolhidos', zorder=4)
        
        plt.plot(x, p1x, color='red', linestyle='-', label='Regressão Linear', linewidth=2)
        
        plt.title('Regressão Linear (Método 1)')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend(title=legenda, loc='upper left', fontsize=10, title_fontsize=10)
        plt.show()
    else:
        pass
   
def regressaolinear_intervalo(x, y, verbose=True, tabela=None, grafico=None):
    """
    Método 2: Polinômio interpolador de ordem 1 dentro do intervalo (x.min(x), x.max(x))
    - Inserindo pontos manualmente dentro do intervalo previamente definido com os dados da funcao dados()

    Entradas/Parâmetros: 
    - x (vetor de pontos em x)
    - y (vetor de pontos em y)
    - verbose (bool): se True, imprime resultados; se False, executa silenciosamente

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
    x, y = _validate_curve_fitting_inputs(x, y)
    
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
            
            break
        except ValueError:
            print(" Entrada inválida. Digite números válidos.")

    b1 = (y2 - y1) / (x2 - x1)
    b0 = y1 - b1 * x1

    estatisticas = calcula_chi_e_r2(x, y, b0, b1, verbose=verbose)
    p1x = estatisticas['Ui']
    funcao = 'b0 + b1*x'

    if verbose:
        print(f"\n=========================\nResultados\n=========================")
        print("Método 2: Regressão Linear Intervalo")
        print(f"Função: {funcao}")
        print(f"Polinômio interpolador: p1(x) = {b0:.4f} + {b1:.4f} * x")
        print(f"Desvio D(a0,a1) (SQRes) = {estatisticas['Desvio']:.4f}")
        print(f"Chi² = {estatisticas['Chi2']:.4f}")
        print(f"R² = {estatisticas['R2']:.4f}")
        print("=========================\nTabela p1(x)\n=========================")
    
    if tabela is None:
        tabela = globals().get('tabela', True)
    if tabela:
        tabela_interpolador(x, y, p1x, verbose=verbose)
    else:
        pass
    
    if verbose:
        print(f"\nFunção: {funcao}")
        print(f"Polinômio Interpolador: p_1(x) = {b0:.6f} + {b1:.6f} * x")
        print(f"Desvio D(a0,a1) (SQRes) = {estatisticas['Desvio']:.6f}")
        print(f"Chi² = {estatisticas['Chi2']:.6f}")
        print(f"R² = {estatisticas['R2']:.6f}")

    if grafico is None:
        grafico = globals().get('grafico', True)
    if grafico and verbose:
        import matplotlib.pyplot as plt
        plt.rcParams.update(plotpars_1x1)
        legenda = (f'Função = {funcao}\n'
                f'y = {b1:.6f}x + {b0:.6f}\n'
                f'b1 = {b1:.6f}\n'
                f'b0 = {b0:.6f}\n'
                f'Desvio = {estatisticas["Desvio"]:.6f}\n'
                f'Chi² = {estatisticas["Chi2"]:.6f}\n'
                f'R² = {estatisticas["R2"]:.6f}')

        plt.scatter(x, y, color='green', s=50, label='Dados originais', zorder=3)
        
        plt.scatter([x1, x2], [y1, y2], color='purple', s=50, marker='o', label='Pontos Escolhidos', zorder=4)
        
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

def minquadrados(x, y, verbose=True, tabela=None, grafico=None):
    """
    Método 3: Mínimos Quadrados
    - É a derivada do desvio igualada a 0 com respeito a b0 e b1 (parciais)

    Entradas/Parâmetros: 
    - x (vetor de pontos em x)
    - y (vetor de pontos em y)
    - verbose (bool): se True, imprime resultados; se False, executa silenciosamente
    - tabela (bool): se True, mostra tabela; se None, usa variável global
    - grafico (bool): se True, mostra gráfico; se None, usa variável global

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
    x, y = _validate_curve_fitting_inputs(x, y)
    
    n = len(x)
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_xy = np.sum(x * y)
    sum_x2 = np.sum(x ** 2)

    b1 = (sum_x * sum_y - n * sum_xy) / ((sum_x) ** 2 - n * sum_x2)
    b0 = (sum_y - b1 * sum_x) / n

    estatisticas = calcula_chi_e_r2(x, y, b0, b1, n_params=2, verbose=verbose)
    funcao = 'b0+b1*x'
    
    if verbose:
        print(f"\n=========================\nResultados\n=========================")
        print(f"Método 3: Mínimos Quadrados")
        print(f"Função: {funcao}")
        print(f"Polinômio interpolador: p1(x) = {b0:.4f} + {b1:.4f} * x")
        print(f"Desvio D(a0,a1) (SQRes) = {estatisticas['Desvio']:.4f}")
        print(f"Chi² = {estatisticas['Chi2']:.4f}")
        print(f"R² = {estatisticas['R2']:.4f}")
        print("=========================\nTabela Mínimos Quadrados\n=========================")

    if tabela is None:
        tabela = globals().get('tabela', True)
    if tabela:
        tabela_minimos_quadrados(x, y, verbose=verbose)
    else:
        pass
    
    if verbose:
        print(f"\nFunção: {funcao}")
        print(f"Equação da reta: y = {b1:.6f}x + {b0:.6f}")
        print(f"Desvio D(a0,a1) (SQRes) = {estatisticas['Desvio']:.6f}")
        print(f"Chi² = {estatisticas['Chi2']:.6f}")
        print(f"R²: {estatisticas['R2']:.6f}")

    if grafico is None:
        grafico = globals().get('grafico', True)
    if grafico and verbose:
        import matplotlib.pyplot as plt #opcional, apenas para exibir os gráficos 
       
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

    return {
        'a0': b0,
        'a1': b1,
        'equacao': f"y = {b1:.6f}x + {b0:.6f}",
        'estatisticas': estatisticas
    }

def minquadrados_ordem_n(x, y, ordem, verbose=True, tabela=None, grafico=None):
    """
    Método 3: Mínimos Quadrados

    Entradas/Parâmetros: 
    - x (vetor de pontos em x)
    - y (vetor de pontos em y)
    - ordem (inteiro >=0)
    - verbose (bool): se True, imprime resultados; se False, executa silenciosamente
    - tabela (bool): se True, mostra tabela; se None, usa variável global
    - grafico (bool): se True, mostra gráfico; se None, usa variável global

    Fórmulas:
    basicamente montar um sistema e resolver por Gauss (poderia ser por decomposição LU tb)
    
    Saídas:     
    - Equação da reta
    - Desvio
    - Chi2, R2
    - Gráfico ilustrativo
    """
    x, y = _validate_curve_fitting_inputs(x, y)
    
    n = len(x)
    if n == 0 or ordem < 0:
        print("Dados insuficientes ou ordem inválida.")
        return None

   
    Sx = [np.sum(x ** k) for k in range(2 * ordem + 1)]
   
    Sxy = [np.sum((x ** k) * y) for k in range(ordem + 1)]

   
    ATA = np.zeros((ordem+1, ordem+1))
    for i in range(ordem + 1):
        for j in range(ordem + 1):
            ATA[i, j] = Sx[i + j]
   
    ATy = np.array(Sxy)

   
    sol = eliminacao_gauss_com_pivotamento(ATA, ATy)
    if sol is None:
        raise RuntimeError("Falha ao resolver sistema normal para mínimos quadrados de ordem n")
   
    if isinstance(sol, (tuple, list)):
        candidate = sol[0]
    else:
        candidate = sol
    coef = np.asarray(candidate, dtype=float).ravel()

   
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

   
    termos = [f"({coef[i]:.6f})x^{i}" if i > 0 else f"({coef[i]:.6f})" for i in range(ordem + 1)]
    equacao = " + ".join(termos)
    if verbose:
        print("\nEquação ajustada:")
        print("p(x) = " + equacao)

       
        print("\nCoeficientes:")
        for i, c in enumerate(coef):
            print(f"a{i} = {c:.6f}")

        print(f"\nEstatísticas do ajuste:")
        print(f"Desvio (SQRes) = {SQRes:.6f}")
        print(f"Chi² ajustado = {chi2:.6f}")
        print(f"R² = {r2:.6f}")

    if tabela is None:
        tabela = globals().get('tabela', True)
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
        if verbose:
            print("\nTabela de cálculos intermediários:")
            print(df.to_string(index=False))

    if grafico is None:
        grafico = globals().get('grafico', True)
    if grafico and verbose:
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
    """Menu interativo de demonstração para Ajustes de Curvas.

    Fornece opções para regressão linear, mínimos quadrados (linear) e ajuste
    polinomial de ordem n. Este docstring foi simplificado para evitar problemas
    de formatação no Sphinx e melhorar a legibilidade.
    """
    x = []
    y = []
    
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
           
        elif opcao == "2":
            x, y = dados()
            regressaolinear_intervalo(x, y)
           
        elif opcao == "3":
            x, y = dados()
            minquadrados(x, y)
           
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    menu()