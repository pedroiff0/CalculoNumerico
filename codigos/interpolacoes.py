from math import factorial, isclose
import sympy as sp 
import numpy as np

def _validate_interpolation_inputs(x, y, xp=None):
    """Valida entradas para funções de interpolação.

    Esta função realiza validações abrangentes dos dados de entrada para garantir
    que a interpolação possa ser realizada corretamente.

    Parameters
    ----------
    x, y : array_like
        Nós e valores correspondentes. Devem ser sequências de números reais.
    xp : float, optional
        Ponto de interpolação. Deve estar dentro do intervalo dos nós x para
        melhores resultados, embora extrapolações sejam permitidas.

    Returns
    -------
    x_valid, y_valid : np.ndarray
        Entradas validadas e convertidas para arrays NumPy de ponto flutuante.

    Raises
    ------
    ValueError
        Se as entradas não forem válidas (dimensões incorretas, comprimentos
        diferentes, pontos x duplicados, etc.).
    TypeError
        Se os dados não puderem ser convertidos para números reais.
    """
    # Validação de tipo e conversão
    try:
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
    except (ValueError, TypeError) as e:
        raise TypeError(f"Os dados de entrada devem ser numéricos. Erro: {e}")

    # Validação de dimensionalidade
    if x.ndim != 1:
        raise ValueError(f"x deve ser um array 1D. Recebido: {x.ndim}D com shape {x.shape}")
    if y.ndim != 1:
        raise ValueError(f"y deve ser um array 1D. Recebido: {y.ndim}D com shape {y.shape}")

    # Validação de comprimento
    if len(x) != len(y):
        raise ValueError(f"x e y devem ter o mesmo comprimento. x: {len(x)}, y: {len(y)}")
    if len(x) < 2:
        raise ValueError(f"São necessários pelo menos 2 pontos para interpolação. Recebidos: {len(x)}")

    # Validação de pontos x únicos
    unique_x = np.unique(x)
    if len(unique_x) != len(x):
        duplicates = x[np.where(np.diff(np.sort(x)) == 0)[0]]
        raise ValueError(f"Os pontos x devem ser únicos. Pontos duplicados encontrados: {duplicates}")

    # Validação de valores finitos (não NaN ou infinito)
    if not np.all(np.isfinite(x)):
        raise ValueError("Todos os valores em x devem ser finitos (não NaN ou infinito)")
    if not np.all(np.isfinite(y)):
        raise ValueError("Todos os valores em y devem ser finitos (não NaN ou infinito)")

    # Validação opcional do ponto de interpolação
    if xp is not None:
        try:
            xp = float(xp)
        except (ValueError, TypeError):
            raise TypeError(f"O ponto de interpolação xp deve ser um número. Recebido: {type(xp)}")

    return x, y

def _validate_max_grau(n, max_grau):
    """Valida e ajusta o grau máximo para interpolação polinomial.

    Esta função garante que o grau do polinômio interpolador seja válido
    dado o número de pontos disponíveis. O grau máximo possível é n-1,
    onde n é o número de pontos.

    Parameters
    ----------
    n : int
        Número de pontos de dados disponíveis. Deve ser >= 2.
    max_grau : int or None
        Grau máximo solicitado. Se None, usa o máximo possível (n-1).
        Deve ser um inteiro não-negativo.

    Returns
    -------
    int
        Grau máximo válido para interpolação. Sempre estará no intervalo [1, n-1].

    Raises
    ------
    TypeError
        Se max_grau não for None, int ou conversível para int.
    ValueError
        Se n for menor que 2 ou max_grau for negativo.
    """
    # Validação do número de pontos
    if not isinstance(n, int) or n < 2:
        raise ValueError(f"Número de pontos deve ser um inteiro >= 2. Recebido: {n}")

    # Caso padrão: usar grau máximo possível
    if max_grau is None:
        return n - 1

    # Validação e conversão do tipo
    try:
        max_grau = int(max_grau)
    except (ValueError, TypeError):
        raise TypeError(f"max_grau deve ser um inteiro ou None. Recebido: {type(max_grau)}")

    # Validação do valor
    if max_grau < 0:
        raise ValueError(f"max_grau deve ser não-negativo. Recebido: {max_grau}")

    # Ajuste automático se fora do limite
    if max_grau > n - 1:
        return n - 1
    elif max_grau < 1:
        return 1

    return max_grau

def dados_interpolacao():
    """Lê interativamente pontos para interpolação com validação robusta.

    Esta função solicita ao usuário os dados necessários para interpolação:
    número de pontos, coordenadas x e y, e ponto de interpolação.
    Inclui validações para garantir que os dados sejam adequados.

    Returns
    -------
    tuple
        Tupla (x_vals, y_vals, x_interp) onde:
        - x_vals: list of float, coordenadas x dos pontos
        - y_vals: list of float, coordenadas y dos pontos
        - x_interp: float, ponto onde avaliar a interpolação

    Raises
    ------
    ValueError
        Se os dados inseridos forem inválidos.
    KeyboardInterrupt
        Se o usuário interromper a entrada (Ctrl+C).
    """
    try:
        # Leitura e validação do número de pontos
        while True:
            try:
                n_str = input("\nDigite o número de pontos (n >= 2): ").strip()
                n = int(n_str)
                if n < 2:
                    print("Erro: São necessários pelo menos 2 pontos. Tente novamente.")
                    continue
                if n > 100:  # Limite razoável para evitar entrada excessiva
                    print("Erro: Número máximo de pontos é 100. Tente novamente.")
                    continue
                break
            except ValueError:
                print("Erro: Digite um número inteiro válido. Tente novamente.")

        x_vals = []
        y_vals = []

        # Leitura dos pontos com validação
        print(f"\nDigite as coordenadas para {n} pontos:")
        for i in range(n):
            while True:
                try:
                    x_str = input(f"x[{i}] = ").strip()
                    x = float(x_str)
                    y_str = input(f"y[{i}] = ").strip()
                    y = float(y_str)

                    # Verificação de valores finitos
                    if not (np.isfinite(x) and np.isfinite(y)):
                        print("Erro: Valores devem ser finitos (não NaN ou infinito). Tente novamente.")
                        continue

                    x_vals.append(x)
                    y_vals.append(y)
                    break
                except ValueError:
                    print("Erro: Digite números válidos. Tente novamente.")

        # Validação adicional: pontos x únicos
        if len(set(x_vals)) != len(x_vals):
            print("Aviso: Alguns pontos x são duplicados. A interpolação pode não funcionar corretamente.")

        # Leitura do ponto de interpolação
        while True:
            try:
                x_interp_str = input("Digite o valor de x para interpolar: ").strip()
                x_interp = float(x_interp_str)

                if not np.isfinite(x_interp):
                    print("Erro: O ponto de interpolação deve ser finito. Tente novamente.")
                    continue

                break
            except ValueError:
                print("Erro: Digite um número válido. Tente novamente.")

        return x_vals, y_vals, x_interp

    except KeyboardInterrupt:
        print("\n\nEntrada interrompida pelo usuário.")
        raise
    except Exception as e:
        print(f"\nErro inesperado na leitura dos dados: {e}")
        raise

def obter_max_grau(n):
    """Solicita ao usuário o grau máximo para interpolação.

    Parameters
    ----------
    n : int
        Número de pontos disponíveis.

    Returns
    -------
    int or None
        Grau máximo escolhido ou ``None`` para usar o máximo disponível.
    """
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

def verifica_espaçamento_uniforme(x, tol=1e-15):
    """Verifica se os pontos x possuem espaçamento uniforme.

    Parameters
    ----------
    x : sequence of float
        Pontos x ordenados.
    tol : float, optional
        Tolerância absoluta para comparação (padrão 1e-15).

    Returns
    -------
    (bool, float)
        Tupla (eh_uniforme, h) onde h é o passo estimado entre pontos.
    """
    h = x[1] - x[0]
    return all(isclose(x[i+1] - x[i], h, abs_tol=tol) for i in range(len(x)-1)), h

def tabela_diferencas_divididas(x, y):
    """Calcula a tabela de diferenças divididas (Newton).

    Parameters
    ----------
    x, y : sequence of float
        Nós e valores correspondentes.

    Returns
    -------
    list of lists
        Tabela em que cada linha j contém as diferenças divididas de ordem j.
    """
    x, y = _validate_interpolation_inputs(x, y)
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
def imprimir_tabela_diferencas_divididas(tabela, verbose=True):
    if not verbose:
        return
    print("\nTabela de Diferenças Divididas:")
    for i in range(len(tabela[0])):
        linha = [f"{tabela[j][i]:>12.6f}" if i < len(tabela[j]) else " " * 12 for j in range(len(tabela))]
        print(" ".join(linha))

def tabela_diferencas_finitas(y):
    """Calcula tabela de diferenças finitas progressivas.

    Parameters
    ----------
    y : sequence of float
        Valores y nos nós igualmente espaçados.

    Returns
    -------
    list of lists
        Tabela de diferenças finitas progressivas.
    """
    y = np.asarray(y, dtype=float)
    if y.ndim != 1:
        raise ValueError("y deve ser um array 1D.")
    if len(y) < 2:
        raise ValueError("São necessários pelo menos 2 pontos para diferenças finitas.")
    n = len(y)
    tabela = [y.copy()]
    for j in range(1, n):
        coluna = []
        for i in range(n - j):
            coluna.append(tabela[j-1][i+1] - tabela[j-1][i])
        tabela.append(coluna)
    return tabela

def imprimir_tabela_diferencas_finitas(tabela, verbose=True):
    if not verbose:
        return
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
    """Calcula estimativa do erro de truncamento do polinômio interpolador.

    Parameters
    ----------
    func_str : str
        Expressão simbólica de f(x).
    x_vals : sequence
        Nós usados na interpolação.
    x_interp : float
        Ponto em que a interpolação foi avaliada.
    grau : int
        Grau do polinômio usado.
    valor_interpolado : float
        Valor interpolado (não usado diretamente no cálculo aqui).

    Returns
    -------
    (float, None)
        Erro de truncamento máximo estimado e None (placeholder para erro real).
    """
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

def newton_dif_divididas(x, tabela_diferencas, xp, max_grau=None, verbose=False, tabela=None, grafico=None):
    """Avalia o polinômio interpolador de Newton usando diferenças divididas.

    Esta função implementa o método de interpolação polinomial de Newton baseado
    em diferenças divididas, que é numericamente mais estável que o método de
    Lagrange para avaliação em múltiplos pontos.

    Parameters
    ----------
    x : array_like
        Nós (pontos x) onde os valores são conhecidos. Devem ser números reais
        únicos e finitos.
    tabela_diferencas : list of lists
        Tabela de diferenças divididas calculada previamente (como retornada
        por tabela_diferencas_divididas). Cada linha j contém as diferenças
        divididas de ordem j.
    xp : float
        Ponto onde avaliar o polinômio interpolador. Deve ser um número finito.
    max_grau : int or None, optional
        Grau máximo do polinômio interpolador. Se None (padrão), usa o grau
        máximo possível (n-1, onde n é o número de pontos). Deve estar no
        intervalo [1, n-1].
    verbose : bool, optional
        Se True, imprime os cálculos detalhados do processo de interpolação.
        Se False (padrão), executa silenciosamente.
    tabela : bool or None, optional
        Se True, mostra a tabela de diferenças divididas utilizada.
        Se None (padrão), usa o valor da variável global 'tabela' ou False.
    grafico : bool or None, optional
        Se True, gera um gráfico mostrando os pontos originais, a curva
        interpolada e o ponto de interpolação. Se None (padrão), usa o valor
        da variável global 'grafico' ou False. Requer matplotlib instalado.

    Returns
    -------
    float
        Valor interpolado do polinômio de Newton no ponto xp.

    Raises
    ------
    ValueError
        Se as entradas não forem válidas ou se a tabela de diferenças não
        for consistente com os pontos x.
    TypeError
        Se os tipos de entrada não forem adequados.
    RuntimeError
        Se ocorrer erro na avaliação do polinômio.

    Notes
    -----
    O método de Newton com diferenças divididas é definido pela fórmula:

    .. math::
        P_n(x) = f[x_0] + f[x_0,x_1](x-x_0) + f[x_0,x_1,x_2](x-x_0)(x-x_1) + \\cdots

    onde :math:`f[x_0,x_1,\\dots,x_k]` são as diferenças divididas de ordem k.

    A complexidade computacional é O(n) para avaliação em um ponto, após
    a pré-computação da tabela de diferenças divididas O(n²).

    Examples
    --------
    >>> x = [0, 1, 2]
    >>> y = [0, 1, 4]
    >>> tabela = tabela_diferencas_divididas(x, y)
    >>> newton_dif_divididas(x, tabela, 1.5)
    2.25

    >>> # Interpolação quadrática
    >>> newton_dif_divididas(x, tabela, 1.5, max_grau=2)
    2.25
    """
    # Validações de entrada
    x = np.asarray(x, dtype=float)
    if x.ndim != 1:
        raise ValueError(f"x deve ser um array 1D. Recebido: {x.ndim}D")

    n = len(x)
    if n < 2:
        raise ValueError(f"São necessários pelo menos 2 pontos para interpolação. Recebidos: {n}")

    # Validação da tabela de diferenças divididas
    if not isinstance(tabela_diferencas, (list, tuple)):
        raise TypeError("tabela_diferencas deve ser uma lista de listas")

    if len(tabela_diferencas) == 0:
        raise ValueError("tabela_diferencas não pode estar vazia")

    if len(tabela_diferencas[0]) != n:
        raise ValueError(f"A primeira linha da tabela deve ter {n} elementos. "
                        f"Recebidos: {len(tabela_diferencas[0])}")

    # Validação do grau máximo
    max_grau = _validate_max_grau(n, max_grau)

    # Conversão e validação do ponto de interpolação
    try:
        xp = float(xp)
    except (ValueError, TypeError):
        raise TypeError(f"O ponto de interpolação xp deve ser um número. Recebido: {type(xp)}")

    if not np.isfinite(xp):
        raise ValueError("O ponto de interpolação xp deve ser finito (não NaN ou infinito)")

    # Configuração dos flags de saída
    if tabela is None:
        tabela = globals().get('tabela', False)
    if grafico is None:
        grafico = globals().get('grafico', False)

    # Exibição da tabela se solicitado
    if tabela:
        imprimir_tabela_diferencas_divididas(tabela_diferencas, verbose=verbose)

    # Cálculo da interpolação usando diferenças divididas
    resultado = float(tabela_diferencas[0][0])
    termo = 1.0

    if verbose:
        print(f"\nCálculo passo a passo - Newton Diferenças Divididas (grau {max_grau}):")
        print(f"P({xp}) = f[x₀] = {resultado:.8f}")

    termos = [resultado]
    for i in range(1, max_grau + 1):
        # Cálculo do termo (xp - x[j]) para j = 0 até i-1
        termo_parcial = 1.0
        termo_str = ""

        for j in range(i):
            termo_parcial *= (xp - x[j])
            if verbose:
                termo_str += f"(xp - x[{j}])" if j == 0 else f" · (xp - x[{j}])"
                if j < i - 1:
                    termo_str += " · "

        # Adição do termo da diferença dividida
        diferenca_dividida = float(tabela_diferencas[i][0])
        termo_completo = diferenca_dividida * termo_parcial
        resultado += termo_completo
        termos.append(termo_completo)

        if verbose:
            print(f"Termo {i}: f[x₀,x₁,...,x_{i}] = {diferenca_dividida:.8f}")
            print(f"         {termo_str} = {termo_parcial:.8f}")
            print(f"         Contribuição: {diferenca_dividida:.8f} × {termo_parcial:.8f} = {termo_completo:.8f}")
            print(f"         Parcial: {resultado:.8f}")

    if verbose:
        termos_str = " + ".join([f"{t:.6f}" for t in termos])
        print(f"\nP({xp}) = {termos_str} = {resultado:.8f}")

    # Geração do gráfico se solicitado
    if grafico and verbose:
        try:
            import matplotlib.pyplot as plt

            # Criação da figura
            plt.figure(figsize=(10, 6))

            # Plot dos pontos originais
            plt.plot(x, tabela_diferencas[0], 'ro-', markersize=8, linewidth=2,
                    label='Pontos de interpolação')

            # Plot da curva interpolada
            x_min, x_max = min(x), max(x)
            margem = 0.1 * (x_max - x_min) if x_max != x_min else 1.0
            x_interp = np.linspace(x_min - margem, x_max + margem, 200)
            y_interp = [newton_dif_divididas(x, tabela_diferencas, xi, max_grau,
                                           verbose=False, tabela=False, grafico=False)
                       for xi in x_interp]
            plt.plot(x_interp, y_interp, 'b-', linewidth=2,
                    label=f'Polinômio interpolador (grau {max_grau})')

            # Destaque do ponto interpolado
            plt.plot([xp], [resultado], 'gx', markersize=12, markeredgewidth=2,
                    label=f'Ponto interpolado ({xp:.3f}, {resultado:.3f})')

            # Configurações do gráfico
            plt.xlabel('x', fontsize=12)
            plt.ylabel('y', fontsize=12)
            plt.title(f'Interpolação Newton - Diferenças Divididas (grau {max_grau})',
                     fontsize=14, fontweight='bold')
            plt.legend(fontsize=10)
            plt.grid(True, alpha=0.3)
            plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)

            # Ajuste dos limites se necessário
            y_min, y_max = min(y_interp), max(y_interp)
            y_margem = 0.1 * (y_max - y_min) if y_max != y_min else 1.0
            plt.ylim(y_min - y_margem, y_max + y_margem)

            plt.tight_layout()
            plt.show()

        except ImportError:
            if verbose:
                print("Aviso: Matplotlib não está instalado. Não foi possível gerar o gráfico.")
        except Exception as e:
            if verbose:
                print(f"Aviso: Erro ao gerar gráfico: {e}")

    return resultado

def gregory_newton_progressivo(x, y, xp, max_grau=None, verbose=False, tabela=None, grafico=None):
    """Avalia o polinômio interpolador de Gregory-Newton progressivo.

    Esta função implementa o método de interpolação polinomial de Gregory-Newton
    progressivo, que utiliza diferenças finitas para interpolação em pontos
    igualmente espaçados. É uma variante do método de Newton otimizada para
    nós com espaçamento uniforme.

    Parameters
    ----------
    x, y : array_like
        Nós (pontos x) e valores correspondentes (pontos y). Os pontos x devem
        estar igualmente espaçados e ser únicos. Ambos devem ser sequências
        de números reais finitos.
    xp : float
        Ponto onde avaliar o polinômio interpolador. Deve ser um número finito.
    max_grau : int or None, optional
        Grau máximo do polinômio interpolador. Se None (padrão), usa o grau
        máximo possível (n-1, onde n é o número de pontos). Deve estar no
        intervalo [1, n-1].
    verbose : bool, optional
        Se True, imprime os cálculos detalhados do processo de interpolação.
        Se False (padrão), executa silenciosamente.
    tabela : bool or None, optional
        Se True, mostra a tabela de diferenças finitas utilizada.
        Se None (padrão), usa o valor da variável global 'tabela' ou False.
    grafico : bool or None, optional
        Se True, gera um gráfico mostrando os pontos originais, a curva
        interpolada e o ponto de interpolação. Se None (padrão), usa o valor
        da variável global 'grafico' ou False. Requer matplotlib instalado.

    Returns
    -------
    float
        Valor interpolado do polinômio de Gregory-Newton no ponto xp.

    Raises
    ------
    ValueError
        Se as entradas não forem válidas ou se os pontos x não estiverem
        igualmente espaçados.
    TypeError
        Se os tipos de entrada não forem adequados.

    Notes
    -----
    O método de Gregory-Newton progressivo é definido pela fórmula:

    .. math::
        P_n(x) = y_0 + \\binom{s}{1} \\Delta y_0 + \\binom{s}{2} \\Delta^2 y_0 + \\cdots + \\binom{s}{n} \\Delta^n y_0

    onde :math:`s = (x - x_0)/h` é a variável reduzida, :math:`h` é o passo
    entre pontos, e :math:`\\Delta^k y_0` são as diferenças finitas progressivas.

    Este método requer que os pontos x estejam igualmente espaçados. Para
    pontos não-uniformemente espaçados, use newton_dif_divididas.

    A complexidade computacional é O(n) para avaliação em um ponto, após
    a pré-computação da tabela de diferenças finitas O(n²).

    Examples
    --------
    >>> x = [0, 1, 2, 3]
    >>> y = [1, 3, 7, 13]  # y = x² + 1
    >>> gregory_newton_progressivo(x, y, 1.5)
    3.25

    >>> # Interpolação cúbica
    >>> gregory_newton_progressivo(x, y, 1.5, max_grau=3)
    3.25
    """
    # Validações de entrada
    x, y = _validate_interpolation_inputs(x, y, xp)
    n = len(x)
    max_grau = _validate_max_grau(n, max_grau)

    # Verificação de espaçamento uniforme
    espacamento_uniforme, h = verifica_espaçamento_uniforme(x)
    if not espacamento_uniforme:
        raise ValueError("Os pontos x devem estar igualmente espaçados para "
                        "o método Gregory-Newton progressivo. Use newton_dif_divididas "
                        "para pontos não-uniformemente espaçados.")

    if abs(h) < 1e-15:
        raise ValueError("O espaçamento entre pontos x é muito pequeno ou zero.")

    # Conversão e validação do ponto de interpolação
    try:
        xp = float(xp)
    except (ValueError, TypeError):
        raise TypeError(f"O ponto de interpolação xp deve ser um número. Recebido: {type(xp)}")

    if not np.isfinite(xp):
        raise ValueError("O ponto de interpolação xp deve ser finito (não NaN ou infinito)")

    # Cálculo da variável reduzida s = (xp - x[0]) / h
    s = (xp - x[0]) / h

    # Cálculo da tabela de diferenças finitas
    tabela_dif_finitas = tabela_diferencas_finitas(y)

    # Configuração dos flags de saída
    if tabela is None:
        tabela = globals().get('tabela', False)
    if grafico is None:
        grafico = globals().get('grafico', False)

    # Exibição da tabela se solicitado
    if tabela:
        imprimir_tabela_diferencas_finitas(tabela_dif_finitas, verbose=verbose)

    # Cálculo da interpolação usando Gregory-Newton progressivo
    resultado = float(y[0])
    termo = 1.0

    if verbose:
        print(f"\nCálculo passo a passo - Gregory-Newton Progressivo (grau {max_grau}):")
        print(f"Passo h = {h:.8f}")
        print(f"Variável reduzida s = (xp - x[0]) / h = ({xp:.6f} - {x[0]:.6f}) / {h:.8f} = {s:.8f}")
        print(f"P({xp:.6f}) = y[0] = {resultado:.8f}")

    termos = [resultado]
    for k in range(1, max_grau + 1):
        # Cálculo do termo binomial: termo *= (s - (k-1)) / k
        termo *= (s - (k - 1)) / k

        # Diferença finita de ordem k
        delta_k = float(tabela_dif_finitas[k][0])

        # Contribuição do termo
        termo_completo = delta_k * termo
        resultado += termo_completo
        termos.append(termo_completo)

        if verbose:
            print(f"Termo {k}: Δ^{k} y[0] = {delta_k:.8f}")
            print(f"         Binomial: s(s-1)...(s-{k-1})/{k}! = {termo:.8f}")
            print(f"         Contribuição: {delta_k:.8f} × {termo:.8f} = {termo_completo:.8f}")
            print(f"         Parcial: {resultado:.8f}")

    if verbose:
        termos_str = " + ".join([f"{t:.6f}" for t in termos])
        print(f"\nP({xp:.6f}) = {termos_str} = {resultado:.8f}")

    # Geração do gráfico se solicitado
    if grafico and verbose:
        try:
            import matplotlib.pyplot as plt

            # Criação da figura
            plt.figure(figsize=(10, 6))

            # Plot dos pontos originais
            plt.plot(x, y, 'ro-', markersize=8, linewidth=2,
                    label='Pontos de interpolação')

            # Plot da curva interpolada
            x_min, x_max = min(x), max(x)
            margem = 0.1 * (x_max - x_min) if x_max != x_min else 1.0
            x_interp = np.linspace(x_min - margem, x_max + margem, 200)
            y_interp = [gregory_newton_progressivo(x, y, xi, max_grau,
                                                  verbose=False, tabela=False, grafico=False)
                       for xi in x_interp]
            plt.plot(x_interp, y_interp, 'b-', linewidth=2,
                    label=f'Polinômio interpolador (grau {max_grau})')

            # Destaque do ponto interpolado
            plt.plot([xp], [resultado], 'gx', markersize=12, markeredgewidth=2,
                    label=f'Ponto interpolado ({xp:.3f}, {resultado:.3f})')

            # Configurações do gráfico
            plt.xlabel('x', fontsize=12)
            plt.ylabel('y', fontsize=12)
            plt.title(f'Interpolação Gregory-Newton Progressivo (grau {max_grau})',
                     fontsize=14, fontweight='bold')
            plt.legend(fontsize=10)
            plt.grid(True, alpha=0.3)
            plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)

            # Ajuste dos limites se necessário
            y_min, y_max = min(y_interp), max(y_interp)
            y_margem = 0.1 * (y_max - y_min) if y_max != y_min else 1.0
            plt.ylim(y_min - y_margem, y_max + y_margem)

            plt.tight_layout()
            plt.show()

        except ImportError:
            if verbose:
                print("Aviso: Matplotlib não está instalado. Não foi possível gerar o gráfico.")
        except Exception as e:
            if verbose:
                print(f"Aviso: Erro ao gerar gráfico: {e}")

    return resultado

def lagrange_interpol(x, y, xp, max_grau=None, verbose=False, tabela=None, grafico=None):
    """Avalia o polinômio interpolador de Lagrange em um ponto específico.

    Esta função implementa o método de interpolação polinomial de Lagrange,
    que constrói um polinômio que passa exatamente pelos pontos dados.
    O método é numericamente estável e não requer ordenação prévia dos pontos.

    Parameters
    ----------
    x, y : array_like
        Nós (pontos x) e valores correspondentes (pontos y). Devem ser sequências
        de números reais com o mesmo comprimento. Os pontos x devem ser únicos.
    xp : float
        Ponto onde avaliar o polinômio interpolador. Deve ser um número finito.
    max_grau : int or None, optional
        Grau máximo do polinômio interpolador. Se None (padrão), usa o grau
        máximo possível (n-1, onde n é o número de pontos). Deve estar no
        intervalo [1, n-1].
    verbose : bool, optional
        Se True, imprime os cálculos detalhados do processo de interpolação.
        Se False (padrão), executa silenciosamente.
    tabela : bool or None, optional
        Se True, mostra tabela com os pontos de interpolação utilizados.
        Se None (padrão), usa o valor da variável global 'tabela' ou False.
    grafico : bool or None, optional
        Se True, gera um gráfico mostrando os pontos originais, a curva
        interpolada e o ponto de interpolação. Se None (padrão), usa o valor
        da variável global 'grafico' ou False. Requer matplotlib instalado.

    Returns
    -------
    float
        Valor interpolado do polinômio de Lagrange no ponto xp.

    Raises
    ------
    ValueError
        Se as entradas não forem válidas (ver _validate_interpolation_inputs).
    TypeError
        Se os tipos de entrada não forem adequados.
    RuntimeError
        Se ocorrer divisão por zero durante o cálculo (pontos x duplicados).

    Notes
    -----
    O método de Lagrange é definido pela fórmula:

    .. math::
        P(x) = \\sum_{i=0}^{n-1} y_i \\cdot L_i(x)

    onde :math:`L_i(x)` são os polinômios base de Lagrange:

    .. math::
        L_i(x) = \\prod_{j=0, j\\neq i}^{n-1} \\frac{x - x_j}{x_i - x_j}

    A complexidade computacional é O(n²) para avaliação em um ponto.

    Examples
    --------
    >>> x = [0, 1, 2]
    >>> y = [0, 1, 4]
    >>> lagrange_interpol(x, y, 1.5)
    2.25

    >>> # Interpolação quadrática
    >>> lagrange_interpol(x, y, 1.5, max_grau=2)
    2.25
    """
    # Validações de entrada
    x, y = _validate_interpolation_inputs(x, y, xp)
    n = len(x)
    max_grau = _validate_max_grau(n, max_grau)

    # Conversão do ponto de interpolação
    try:
        xp = float(xp)
    except (ValueError, TypeError):
        raise TypeError(f"O ponto de interpolação xp deve ser um número. Recebido: {type(xp)}")

    if not np.isfinite(xp):
        raise ValueError("O ponto de interpolação xp deve ser finito (não NaN ou infinito)")

    # Inicialização do resultado
    yp = 0.0

    # Configuração dos flags de saída
    if tabela is None:
        tabela = globals().get('tabela', False)
    if grafico is None:
        grafico = globals().get('grafico', False)

    # Exibição da tabela de pontos se solicitado
    if tabela and verbose:
        print("\nTabela de pontos de interpolação:")
        print(" i |   x[i]   |   y[i]   ")
        print("---|----------|----------")
        for i in range(min(max_grau + 1, n)):
            print("2d")

    # Cálculo da interpolação
    if verbose:
        print(f"\nCálculos detalhados do polinômio de Lagrange (grau {max_grau}):")
        print(f"P({xp}) = ", end="")

    termos = []
    for i in range(max_grau + 1):
        # Cálculo do polinômio base de Lagrange L_i(xp)
        li = 1.0
        denominadores = []

        if verbose:
            print(f"\n  Termo {i}: y[{i}] * L{i}({xp})")
            print(f"    L{i}({xp}) = ", end="")

        for j in range(n):
            if i != j:
                # Verificação de divisão por zero
                denominador = x[i] - x[j]
                if abs(denominador) < 1e-15:
                    raise RuntimeError(f"Divisão por zero detectada: x[{i}] - x[{j}] = {denominador}. "
                                     f"Pontos x duplicados ou muito próximos.")

                li *= (xp - x[j]) / denominador
                denominadores.append(denominador)

                if verbose:
                    print(f"(({xp} - {x[j]:.6f}) / ({x[i]:.6f} - {x[j]:.6f})) ", end="")

        # Cálculo do termo completo
        termo = y[i] * li
        yp += termo
        termos.append(termo)

        if verbose:
            print(f"= {li:.8f}")
            print(f"    y[{i}] * L{i}({xp}) = {y[i]:.6f} * {li:.8f} = {termo:.8f}")

    if verbose:
        print(f"\nP({xp}) = {' + '.join([f'{t:.6f}' for t in termos])} = {yp:.8f}")

    # Geração do gráfico se solicitado
    if grafico and verbose:
        try:
            import matplotlib.pyplot as plt

            # Criação da figura
            plt.figure(figsize=(10, 6))

            # Plot dos pontos originais
            plt.plot(x[:max_grau+1], y[:max_grau+1], 'ro-', markersize=8, linewidth=2,
                    label='Pontos de interpolação')

            # Plot da curva interpolada
            x_min, x_max = min(x), max(x)
            margem = 0.1 * (x_max - x_min) if x_max != x_min else 1.0
            x_interp = np.linspace(x_min - margem, x_max + margem, 200)
            y_interp = [lagrange_interpol(x, y, xi, max_grau, verbose=False,
                                         tabela=False, grafico=False)
                       for xi in x_interp]
            plt.plot(x_interp, y_interp, 'b-', linewidth=2,
                    label=f'Polinômio interpolador (grau {max_grau})')

            # Destaque do ponto interpolado
            plt.plot([xp], [yp], 'gx', markersize=12, markeredgewidth=2,
                    label=f'Ponto interpolado ({xp:.3f}, {yp:.3f})')

            # Configurações do gráfico
            plt.xlabel('x', fontsize=12)
            plt.ylabel('y', fontsize=12)
            plt.title(f'Interpolação de Lagrange (grau {max_grau})', fontsize=14, fontweight='bold')
            plt.legend(fontsize=10)
            plt.grid(True, alpha=0.3)
            plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)

            # Ajuste dos limites se necessário
            y_min, y_max = min(y_interp), max(y_interp)
            y_margem = 0.1 * (y_max - y_min) if y_max != y_min else 1.0
            plt.ylim(y_min - y_margem, y_max + y_margem)

            plt.tight_layout()
            plt.show()

        except ImportError:
            if verbose:
                print("Aviso: Matplotlib não está instalado. Não foi possível gerar o gráfico.")
        except Exception as e:
            if verbose:
                print(f"Aviso: Erro ao gerar gráfico: {e}")

    return yp

def dispositivo_pratico_lagrange(x, y, xp, max_grau=None, verbose=False, tabela=None, grafico=None):
    x, y = _validate_interpolation_inputs(x, y)
    n = len(x)
    max_grau = _validate_max_grau(n, max_grau)
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

    if tabela is None:
        tabela = globals().get('tabela', False)
    if tabela and verbose:
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
            print("2d")

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

    if verbose and tabela:
        print("\nMatriz G (x[i] - x[j], diagonal = xp - x[i]):")
        for linha in G:
            print("[ " + " ".join(str(v) for v in linha) + " ]")

    if grafico is None:
        grafico = globals().get('grafico', False)
    if grafico and verbose:
        try:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(10, 6))
            plt.plot(x, y, 'ro-', label='Pontos originais')
            x_interp = np.linspace(min(x), max(x), 100)
            y_interp = [dispositivo_pratico_lagrange(x, y, xi, max_grau, verbose=False, tabela=False, grafico=False) for xi in x_interp]
            plt.plot(x_interp, y_interp, 'b-', label=f'Interpolação grau {max_grau}')
            plt.plot([xp], [resultado], 'gx', markersize=10, label=f'Ponto interpolado ({xp:.3f}, {resultado:.3f})')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title(f'Dispositivo Prático de Lagrange (grau {max_grau})')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.show()
        except ImportError:
            if verbose:
                print("Matplotlib não disponível para plotar gráfico.")
    
    return resultado

def menu():
    while True:
        print("\n================ MENU DE INTERPOLAÇÃO ================")
        print("1. Polinômio de Lagrange")
        print("2. Dispositivo Prático de Lagrange")
        print("3. Polinômio de Newton (Diferenças Divididas)")
        print("4. Polinômio Gregory-Newton Progressivo")
        print("0. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == '0':
            print("Encerrando o programa...")
            break
        
        x_vals, y_vals, x_interp = dados_interpolacao()

        n = len(x_vals)
        max_grau = obter_max_grau(n)

        if opcao == '1':
            resultado = lagrange_interpol(x_vals, y_vals, x_interp, max_grau=max_grau, verbose=False)
            if resultado is not None:
                erro_trunc, erro_real = perguntar_erro(x_vals[:max_grau+1], x_interp, max_grau, resultado)
            print(f"\nResultado final (Lagrange): {resultado}")

        elif opcao == '2':
            resultado = dispositivo_pratico_lagrange(x_vals, y_vals, x_interp, max_grau=max_grau, verbose=False)
            if resultado is not None:
                erro_trunc, erro_real = perguntar_erro(x_vals[:max_grau+1], x_interp, max_grau, resultado)
            print(f"\nResultado final (Dispositivo Prático de Lagrange): {resultado}")

        elif opcao == '3':
            tabela = tabela_diferencas_divididas(x_vals, y_vals)
            imprimir_tabela_diferencas_divididas(tabela, verbose=True)
            resultado = newton_dif_divididas(x_vals, tabela, x_interp, max_grau=max_grau, verbose=False)
            if resultado is not None:
                erro_trunc, erro_real = perguntar_erro(x_vals[:max_grau+1], x_interp, max_grau, resultado)
            print(f"\nResultado final (Newton Diferenças Divididas): {resultado}")

        elif opcao == '4':
            uniforme, h = verifica_espaçamento_uniforme(x_vals)
            if not uniforme:
                print("Erro: Os pontos x não têm espaçamento uniforme! Gregory-Newton requer x igualmente espaçados.")
                continue
            tabela = tabela_diferencas_finitas(y_vals)
            imprimir_tabela_diferencas_finitas(tabela, verbose=False)
            resultado = gregory_newton_progressivo(x_vals, y_vals, x_interp, max_grau=max_grau, verbose=False)
            if resultado is not None:
                erro_trunc, erro_real = perguntar_erro(x_vals[:max_grau+1], x_interp, max_grau, resultado)
            print(f"\nResultado final (Gregory-Newton Progressivo): {resultado}")

        else:
            print("Opção inválida, tente novamente.")

if __name__ == '__main__':
    menu()