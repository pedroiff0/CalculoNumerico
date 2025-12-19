import numpy as np
import matplotlib.pyplot as plt
import math
import sympy as sp
from sympy import sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, exp, sqrt, log, Abs, pi, E
import re

# mapa seguro com funções do math (para uso em fallbacks com eval)
safe_math = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}

# Mapeamento padrão para uso com sympify (padroniza nomes de funções/constantes)
SYMPY_LOCALS = {
    'sin': sin, 'cos': cos, 'tan': tan,
    'asin': asin, 'acos': acos, 'atan': atan,
    'sinh': sinh, 'cosh': cosh, 'tanh': tanh,
    'exp': exp, 'sqrt': sqrt, 'log': log, 'abs': Abs,
    'pi': pi, 'e': E, 'E': E
}

def _validate_edo_inputs(func_input, x0, y0, h, xn, ordem=None):
    """Valida entradas para funções de resolução de EDOs.

    Esta função realiza validações abrangentes dos dados de entrada para garantir
    que a resolução de EDO possa ser realizada corretamente.

    Parameters
    ----------
    func_input : str
        Expressão da função f(x, y) como string.
    x0, y0 : float
        Condições iniciais: ponto inicial x0 e valor y(x0).
    h : float
        Tamanho do passo de integração. Deve ser positivo.
    xn : float
        Ponto final de integração. Deve ser diferente de x0.
    ordem : int or None, optional
        Ordem do método Runge-Kutta (1, 2, 3, 4). Se None, não valida.

    Returns
    -------
    func_input_valid, x0_valid, y0_valid, h_valid, xn_valid : str, float, float, float, float
        Entradas validadas e convertidas para tipos apropriados.

    Raises
    ------
    TypeError
        Se os tipos de entrada não forem adequados.
    ValueError
        Se os valores não forem válidos (passo negativo, pontos iguais, etc.).
    """
    # Validação da função de entrada
    if not isinstance(func_input, str):
        raise TypeError(f"func_input deve ser uma string. Recebido: {type(func_input)}")

    func_input = func_input.strip()
    if not func_input:
        raise ValueError("A expressão da função f(x,y) não pode estar vazia")

    # Validação e conversão dos valores numéricos
    try:
        x0 = float(x0)
        y0 = float(y0)
        h = float(h)
        xn = float(xn)
    except (ValueError, TypeError) as e:
        raise TypeError(f"Todos os parâmetros numéricos devem ser números. Erro: {e}")

    # Validação de valores finitos
    if not np.isfinite(x0):
        raise ValueError("O ponto inicial x0 deve ser finito (não NaN ou infinito)")
    if not np.isfinite(y0):
        raise ValueError("O valor inicial y0 deve ser finito (não NaN ou infinito)")
    if not np.isfinite(h):
        raise ValueError("O passo h deve ser finito (não NaN ou infinito)")
    if not np.isfinite(xn):
        raise ValueError("O ponto final xn deve ser finito (não NaN ou infinito)")

    # Validação do passo
    if h <= 0:
        raise ValueError(f"O passo h deve ser positivo. Recebido: {h}")

    # Validação do intervalo
    if abs(xn - x0) < 1e-15:
        raise ValueError(f"Os pontos inicial e final devem ser diferentes. x0={x0}, xn={xn}")

    # Validação da ordem (se fornecida)
    if ordem is not None:
        try:
            ordem = int(ordem)
        except (ValueError, TypeError):
            raise TypeError(f"A ordem deve ser um inteiro. Recebido: {type(ordem)}")

        if ordem not in [1, 2, 3, 4]:
            raise ValueError(f"A ordem deve ser 1, 2, 3 ou 4. Recebido: {ordem}")

    return func_input, x0, y0, h, xn

def _validate_sistema_edo_inputs(funcs_input, y0, t0, tf, h, ordem=None):
    """Valida entradas para resolução de sistemas de EDOs.

    Parameters
    ----------
    funcs_input : list of str
        Lista de expressões das funções f_i(t, y) como strings.
    y0 : array_like
        Condições iniciais y(t0) como array ou lista.
    t0, tf : float
        Pontos inicial e final de integração.
    h : float
        Tamanho do passo de integração. Deve ser positivo.
    ordem : int or None, optional
        Ordem do método Runge-Kutta (1, 2, 3, 4). Se None, não valida.

    Returns
    -------
    funcs_valid, y0_valid, t0_valid, tf_valid, h_valid : list, np.ndarray, float, float, float
        Entradas validadas e convertidas.

    Raises
    ------
    TypeError
        Se os tipos de entrada não forem adequados.
    ValueError
        Se os valores não forem válidos.
    """
    # Validação das funções
    if not isinstance(funcs_input, (list, tuple)):
        raise TypeError(f"funcs_input deve ser uma lista ou tupla. Recebido: {type(funcs_input)}")

    if len(funcs_input) == 0:
        raise ValueError("Deve haver pelo menos uma função no sistema")

    funcs_valid = []
    for i, func in enumerate(funcs_input):
        if not isinstance(func, str):
            raise TypeError(f"Todas as funções devem ser strings. Função {i}: {type(func)}")
        func = func.strip()
        if not func:
            raise ValueError(f"A função {i} não pode estar vazia")
        funcs_valid.append(func)

    # Validação das condições iniciais
    try:
        y0 = np.asarray(y0, dtype=float)
    except (ValueError, TypeError) as e:
        raise TypeError(f"y0 deve ser conversível para array numérico. Erro: {e}")

    if y0.ndim != 1:
        raise ValueError(f"y0 deve ser um array 1D. Recebido: {y0.ndim}D com shape {y0.shape}")

    if len(y0) != len(funcs_input):
        raise ValueError(f"Número de condições iniciais ({len(y0)}) deve corresponder ao "
                        f"número de funções ({len(funcs_input)})")

    if not np.all(np.isfinite(y0)):
        raise ValueError("Todas as condições iniciais em y0 devem ser finitas")

    # Validação dos pontos temporais e passo
    try:
        t0 = float(t0)
        tf = float(tf)
        h = float(h)
    except (ValueError, TypeError) as e:
        raise TypeError(f"t0, tf e h devem ser números. Erro: {e}")

    if not np.isfinite(t0):
        raise ValueError("O ponto inicial t0 deve ser finito")
    if not np.isfinite(tf):
        raise ValueError("O ponto final tf deve ser finito")
    if not np.isfinite(h):
        raise ValueError("O passo h deve ser finito")

    if h <= 0:
        raise ValueError(f"O passo h deve ser positivo. Recebido: {h}")

    if abs(tf - t0) < 1e-15:
        raise ValueError(f"Os pontos inicial e final devem ser diferentes. t0={t0}, tf={tf}")

    # Validação da ordem (se fornecida)
    if ordem is not None:
        try:
            ordem = int(ordem)
        except (ValueError, TypeError):
            raise TypeError(f"A ordem deve ser um inteiro. Recebido: {type(ordem)}")

        if ordem not in [1, 2, 3, 4]:
            raise ValueError(f"A ordem deve ser 1, 2, 3 ou 4. Recebido: {ordem}")

    return funcs_valid, y0, t0, tf, h

def _create_function_from_string(func_str, variables, verbose=False):
    """Cria uma função callable a partir de uma string matemática.

    Esta função tenta múltiplas abordagens para converter uma expressão
    matemática em string para uma função Python callable, com fallbacks
    para máxima compatibilidade.

    Parameters
    ----------
    func_str : str
        Expressão matemática como string (ex.: 'y - x**2').
    variables : list of str
        Nomes das variáveis na expressão (ex.: ['x', 'y']).
    verbose : bool, optional
        Se True, imprime informações sobre o processo de criação.

    Returns
    -------
    callable
        Função que pode ser chamada com os argumentos correspondentes.

    Raises
    ------
    ValueError
        Se não for possível criar uma função válida da string.
    """
    if verbose:
        print(f"Criando função a partir de: {func_str}")

    # Preparar a string: remover espaços, corrigir notação
    func_str = func_str.replace(' ', '').replace('^', '**')

    # Corrigir multiplicação implícita (ex.: 2x -> 2*x)
    func_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func_str)

    # Criar símbolos do SymPy
    symbols = sp.symbols(variables)
    symbols_dict = dict(zip(variables, symbols))

    try:
        # Tentar primeiro com SymPy (mais robusto)
        expr = sp.sympify(func_str, locals={**SYMPY_LOCALS, **symbols_dict})
        func = sp.lambdify(symbols, expr, modules=['numpy'])

        # Teste rápido da função
        test_args = [1.0] * len(variables)
        test_result = func(*test_args)
        if not np.isfinite(test_result):
            raise ValueError("Função produz resultado não-finito no teste")

        if verbose:
            print("Função criada com sucesso usando SymPy")

        return func

    except Exception as e:
        if verbose:
            print(f"Falhou com SymPy: {e}. Tentando fallback com eval...")

        # Fallback: usar eval com ambiente restrito
        try:
            def func(*args):
                if len(args) != len(variables):
                    raise ValueError(f"Número incorreto de argumentos. Esperado: {len(variables)}, "
                                   f"recebido: {len(args)}")

                local_vars = dict(zip(variables, args))
                local_vars.update({'np': np, 'math': math, **safe_math})

                try:
                    return eval(func_str, {"__builtins__": None}, local_vars)
                except Exception as eval_error:
                    raise ValueError(f"Erro na avaliação da função: {eval_error}")

            # Teste da função
            test_args = [1.0] * len(variables)
            test_result = func(*test_args)
            if not np.isfinite(test_result):
                raise ValueError("Função produz resultado não-finito no teste")

            if verbose:
                print("Função criada com sucesso usando eval")

            return func

        except Exception as fallback_error:
            raise ValueError(f"Não foi possível criar função a partir de '{func_str}'. "
                           f"Erro SymPy: {e}. Erro fallback: {fallback_error}")

def pedir_dados_edo():
    """Obtém entradas do usuário para resolução de EDOs com validação robusta.

    Esta função solicita interativamente ao usuário os dados necessários para
    resolver uma equação diferencial ordinária: a função f(x,y), o intervalo
    de integração [a,b], as condições iniciais (x0,y0), e o passo de integração.
    Também permite especificar uma solução exata opcional para comparação.

    A função inclui validações abrangentes para garantir que os dados sejam
    adequados para a resolução numérica da EDO.

    Returns
    -------
    dict
        Dicionário contendo todos os dados validados com as seguintes chaves:
        - 'func_input': str, expressão da função f(x,y)
        - 'a': float, limite inferior do intervalo
        - 'b': float, limite superior do intervalo
        - 'x0': float, ponto inicial das condições iniciais
        - 'y0': float, valor inicial y(x0)
        - 'h': float, tamanho do passo de integração
        - 'm': int or None, número de subintervalos (se especificado)
        - 'xn': float, ponto final (sempre igual a b)
        - 'solucao_exata': callable or None, função da solução exata
        - 'sol_exata_expr': str, expressão da solução exata

    Raises
    ------
    ValueError
        Se os dados inseridos forem inválidos ou inconsistentes.
    KeyboardInterrupt
        Se o usuário interromper a entrada (Ctrl+C).
    """
    try:
        # Entrada da função f(x,y) com validação
        while True:
            print("\nDigite a função f(x,y) em notação matemática simples:")
            print("Exemplo: y - x**2  (será interpretado como y - x²)")
            print("Funções disponíveis: sin, cos, tan, exp, log, sqrt, pi, e, etc.")
            func_input = input("f(x,y) = ").strip()

            if not func_input:
                print("Erro: A expressão da função não pode estar vazia. Tente novamente.")
                continue

            # Teste básico da função
            try:
                test_func = _create_function_from_string(func_input, ['x', 'y'], verbose=False)
                # Teste numérico rápido
                test_result = test_func(1.0, 1.0)
                if not np.isfinite(test_result):
                    print("Erro: A função produz resultado não-finito. Verifique a expressão.")
                    continue
                break
            except Exception as e:
                print(f"Erro na expressão da função: {e}")
                print("Tente novamente.")
                continue

        # Entrada do intervalo [a,b] com validação
        while True:
            try:
                print("\nIntervalo de integração [a,b]:")
                a_str = input("a = ").strip()
                a = float(a_str)
                b_str = input("b = ").strip()
                b = float(b_str)

                if not (np.isfinite(a) and np.isfinite(b)):
                    print("Erro: Os limites devem ser finitos. Tente novamente.")
                    continue

                if abs(b - a) < 1e-15:
                    print("Erro: Os limites a e b devem ser diferentes. Tente novamente.")
                    continue

                break
            except ValueError:
                print("Erro: Digite números válidos. Tente novamente.")

        # Entrada das condições iniciais com validação
        while True:
            try:
                print("\nCondições iniciais:")
                x0_str = input("x0 = ").strip()
                x0 = float(x0_str)
                y0_str = input("y0 = ").strip()
                y0 = float(y0_str)

                if not (np.isfinite(x0) and np.isfinite(y0)):
                    print("Erro: As condições iniciais devem ser finitas. Tente novamente.")
                    continue

                # Verificar se x0 está no intervalo [a,b]
                if not (min(a, b) <= x0 <= max(a, b)):
                    print(f"Aviso: x0 = {x0} está fora do intervalo [{a}, {b}]")

                break
            except ValueError:
                print("Erro: Digite números válidos. Tente novamente.")

        # Escolha do passo: h ou m
        h = None
        m = None
        while True:
            try:
                escolha = input("\nDeseja informar o passo por:\n"
                              "  h - tamanho do passo diretamente\n"
                              "  m - número de subintervalos\n"
                              "Escolha [h/m]: ").strip().lower()

                if escolha == 'h':
                    h_str = input("h = ").strip()
                    h = float(h_str)
                    if h <= 0:
                        print("Erro: O passo h deve ser positivo. Tente novamente.")
                        continue
                    if h > abs(b - a):
                        print(f"Aviso: h = {h} é maior que o intervalo |b-a| = {abs(b-a)}")
                    m = None
                    break

                elif escolha == 'm':
                    m_str = input("m = ").strip()
                    m = int(m_str)
                    if m <= 0:
                        print("Erro: O número de subintervalos m deve ser positivo. Tente novamente.")
                        continue
                    if m > 10000:  # Limite razoável
                        print("Erro: Número máximo de subintervalos é 10000. Tente novamente.")
                        continue
                    h = abs(b - a) / m
                    print(f"Calculado h = {h:.8e}")
                    break

                else:
                    print("Erro: Escolha 'h' ou 'm'. Tente novamente.")
                    continue

            except ValueError:
                print("Erro: Digite um valor numérico válido. Tente novamente.")
            except ZeroDivisionError:
                print("Erro: Intervalo [a,b] tem comprimento zero. Tente novamente.")
                continue

        xn = b

        # Solução exata opcional
        solucao_exata = None
        sol_exata_expr = ''

        while True:
            s = input("\nSolução exata y(x) (pressione Enter se não houver): ").strip()
            if not s:
                break

            sol_exata_expr = s
            try:
                # Criar função da solução exata
                x_sym = sp.symbols('x')
                expr_sol = sp.sympify(sol_exata_expr, locals=SYMPY_LOCALS)
                lam_sol = sp.lambdify(x_sym, expr_sol, modules=['numpy'])

                def solucao_exata(x):
                    try:
                        val = lam_sol(x)
                        # Converter para float se possível
                        if hasattr(val, 'item'):
                            val = val.item()
                        return float(val)
                    except Exception:
                        return float(sp.N(expr_sol.subs(x_sym, x)))

                # Teste da função
                test_val = solucao_exata(x0)
                if not np.isfinite(test_val):
                    print("Erro: A solução exata produz valor não-finito em x0. Tente novamente.")
                    continue

                print("Solução exata aceita.")
                break

            except Exception as e:
                print(f"Erro na expressão da solução exata: {e}")
                print("Tente novamente ou pressione Enter para pular.")
                continue

        return {
            'func_input': func_input,
            'a': a,
            'b': b,
            'x0': x0,
            'y0': y0,
            'h': h,
            'm': m,
            'xn': xn,
            'solucao_exata': solucao_exata,
            'sol_exata_expr': sol_exata_expr,
        }

    except KeyboardInterrupt:
        print("\n\nEntrada interrompida pelo usuário.")
        raise
    except Exception as e:
        print(f"\nErro inesperado na leitura dos dados: {e}")
        raise


def passos_edo(a, b, x0, h=None, m=None):
    """Normaliza e retorna (h, xn) dado h ou m. xn é sempre b."""
    if m is not None:
        if m <= 0:
            raise ValueError('m deve ser > 0')
        h = (b - a) / m
        xn = b
        return h, xn
    if h is None:
        raise ValueError('h ou m deve ser fornecido')
    xn = b
    return h, xn


def plotar_grafico_edo(x_vals, y_vals, solucao_exata=None, titulo='Solução da EDO'):
    try:
        import matplotlib.pyplot as plt
    except Exception:
        print("matplotlib não está disponível. Instale com 'pip install matplotlib'.")
        return
    plt.figure(figsize=(8, 4))
    plt.plot(x_vals, y_vals, marker='o', label='Aproximação')
    if solucao_exata is not None:
        xs = np.array(x_vals)
        ys_ex = [solucao_exata(x) for x in xs]
        plt.plot(xs, ys_ex, linestyle='--', label='Solução exata')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(titulo)
    plt.legend()
    plt.grid(True)
    plt.show()


def mostrar_tabela_e_grafico_edo(x_vals, y_vals, solucao_exata=None, titulo='Solução da EDO', plotar=True):
    """Mostra a tabela de pontos (x, y) e chama o plot se `plotar` for True."""
    print("\n--- Tabela de resultados ---")
    if solucao_exata is not None:
        print(f"{'x':>10} {'y_aprox':>18} {'y_exato':>18} {'erro':>12}")
        print('-' * 60)
        for xi, yi in zip(x_vals, y_vals):
            try:
                y_real = solucao_exata(xi)
                erro = abs(y_real - yi)
                print(f"{xi:10.6f} {yi:18.10f} {y_real:18.10f} {erro:12.4e}")
            except Exception:
                print(f"{xi:10.6f} {yi:18.10f} {'N/A':>18} {'N/A':>12}")
    else:
        print(f"{'x':>10} {'y':>18}")
        print('-' * 30)
        for xi, yi in zip(x_vals, y_vals):
            print(f"{xi:10.6f} {yi:18.10f}")

    # Plot opcional
    if plotar:
        plotar_grafico_edo(x_vals, y_vals, solucao_exata, titulo)


def resolver_edo_2ordem():
    print("\n=== Resolução de EDO de 2ª ordem: y'' = f(x, y, y') ===")
    print("Digite f(x, y, yp) usando x, y, yp (exemplo: yp + 2*y - x**2)")
    f_input = input("f(x, y, yp) = ").strip().replace('^', '**')
    x0 = float(input("x inicial: "))
    xf = float(input("x final: "))
    # Permitir expressões numéricas (ex: 1/2, pi/4) usando sympy
    y0_str = input("y(x0): ").strip()
    yp0_str = input("y'(x0): ").strip()
    try:
        y0 = float(sp.N(sp.sympify(y0_str)))
    except Exception:
        y0 = float(y0_str)
    try:
        yp0 = float(sp.N(sp.sympify(yp0_str)))
    except Exception:
        yp0 = float(yp0_str)
    
    print("\nComo deseja especificar o passo?")
    
    print("1 - Inserir h diretamente")
    print("2 - Inserir número de subintervalos m")
    escolha_h = input("Escolha (1 ou 2): ").strip()
    if escolha_h == '1':
        h = float(input("Digite o passo h: "))
    elif escolha_h == '2':
        m = int(input("Digite o número de subintervalos m: "))
        h = (xf - x0) / m
        print(f"Calculado h = {h}")
    else:
        print("Opção inválida. Encerrando")

    # Montar sistema equivalente: y1' = y2, y2' = f(x, y1, y2)
    # Converter y[1] -> y[0], y[2] -> y[1] na string "y[2]"
    def convert_indices(expr):
        def repl_idx(m):
            idx = int(m.group(1))
            return f'y[{idx-1}]'
        return re.sub(r'y\[(\d+)\]', repl_idx, expr)

    # Compilar f(x,y,yp) com sympy -> lambdify
    x_sym, y_sym, yp_sym = sp.symbols('x y yp')
    try:
        expr_f = sp.sympify(f_input)
        lam_f = sp.lambdify((x_sym, y_sym, yp_sym), expr_f, modules=['numpy'])
        def f2(x, y):
            return lam_f(x, y[0], y[1])
    except Exception:
        # fallback: usar eval em namespace restrito
        def f2(x, y):
            local = {"x": x, "y": y[0], "yp": y[1], "np": np, "math": math, **safe_math}
            try:
                return eval(f_input, {"__builtins__": None}, local)
            except Exception:
                return eval(f_input)

    # Montar as funções do sistema: y1' = y2, y2' = f(x,y,yp)
    funcs_input = [lambda x, y: y[1], f2]
    # y[1] = y, y[2] = y'
    y_ini = [y0, yp0]
    # Adaptar runge_kutta_sistema para aceitar função direta no segundo termo
    def runge_kutta_sistema_2ordem(funcs_input, y0, x0, xf, h, ordem):
        n = len(y0)
        t_vals = [x0]
        u_vals = [np.array(y0)]
        # preparar func0 (caso seja string) para avaliação segura
        if isinstance(funcs_input[0], str):
            expr0 = funcs_input[0].strip().replace('^', '**').replace(' ', '')
            expr0_named = re.sub(r'y\[(\d+)\]', lambda m: f'y{m.group(1)}', expr0)
            y_symbols0 = sp.symbols(' '.join([f'y{i+1}' for i in range(n)]))
            x_sym0 = sp.symbols('x')
            locals_map0 = {'x': x_sym0}
            for i, ys in enumerate(y_symbols0):
                locals_map0[f'y{i+1}'] = ys
            try:
                expr0_sym = sp.sympify(expr0_named, locals=locals_map0)
                lam0 = sp.lambdify((x_sym0, ) + tuple(y_symbols0), expr0_sym, modules=['numpy'])
                def func0_callable(x, y):
                    return lam0(x, *tuple(y.tolist() if hasattr(y, 'tolist') else list(y)))
            except Exception:
                def func0_callable(x, y):
                    local = {'x': x, 'y': y, 'np': np, 'math': math, **safe_math}
                    try:
                        return eval(expr0, {"__builtins__": None}, local)
                    except Exception:
                        return eval(expr0)
        else:
            func0_callable = funcs_input[0]

        while t_vals[-1] < xf:
            x = t_vals[-1]
            y = u_vals[-1]
            step = min(h, xf - x)
            # Evitar passo nulo que causaria loop infinito
            if step <= 0:
                print("Passo nulo ou intervalo concluído; interrompendo resolução do sistema de 2ª ordem.")
                break
            if ordem == 1:
                k1 = np.array([
                        func0_callable(x, y),
                    funcs_input[1](x, y)
                ])
                y_new = y + step * k1
            elif ordem == 2:
                k1 = np.array([func0_callable(x, y), funcs_input[1](x, y)])
                k2 = np.array([
                    func0_callable(x+step, y+step*k1), funcs_input[1](x+step, y+step*k1)
                ])
                y_new = y + 0.5 * step * (k1 + k2)
            elif ordem == 3:
                k1 = np.array([func0_callable(x, y), funcs_input[1](x, y)])
                k2 = np.array([
                    func0_callable(x+step/2, y+step*k1/2), funcs_input[1](x+step/2, y+step*k1/2)
                ])
                k3 = np.array([
                    func0_callable(x+step, y-step*k1+2*step*k2), funcs_input[1](x+step, y-step*k1+2*step*k2)
                ])
                y_new = y + (step/6) * (k1 + 4*k2 + k3)
            elif ordem == 4:
                k1 = np.array([func0_callable(x, y), funcs_input[1](x, y)])
                k2 = np.array([
                    func0_callable(x+step/2, y+step*k1/2), funcs_input[1](x+step/2, y+step*k1/2)
                ])
                k3 = np.array([
                    func0_callable(x+step/2, y+step*k2/2), funcs_input[1](x+step/2, y+step*k2/2)
                ])
                k4 = np.array([
                    func0_callable(x+step, y+step*k3), funcs_input[1](x+step, y+step*k3)
                ])
                y_new = y + (step/6) * (k1 + 2*k2 + 2*k3 + k4)
            x_next = x + step
            t_vals.append(x_next)
            u_vals.append(y_new)
        return t_vals, np.array(u_vals)

    print("\nEscolha a ordem do método de Runge-Kutta:")
    print("1 - Euler (RK1)")
    print("2 - RK2")
    print("3 - RK3")
    print("4 - RK4")
    ordem = int(input("Ordem (1-4): "))
    t_vals, u_vals = runge_kutta_sistema_2ordem(funcs_input, y_ini, x0, xf, h, ordem)
    print("\nTabela de resultados:")
    print("x\ty(x)\ty'(x)")
    for i in range(len(t_vals)):
        print(f"{t_vals[i]:.6f}\t{u_vals[i][0]:.6f}\t{u_vals[i][1]:.6f}")
    # Perguntar se o usuário deseja ver o gráfico
    try:
        resp = input("Deseja plotar o gráfico da solução? [s/n]: ").strip().lower()
        if resp.startswith('s'):
            plt.figure(figsize=(10, 5))
            plt.plot(t_vals, u_vals[:, 0], label="y(x)", marker='o')
            plt.plot(t_vals, u_vals[:, 1], label="y'(x)", marker='s')
            plt.xlabel('x')
            plt.ylabel('Soluções')
            plt.title('Solução da EDO de 2ª ordem')
            plt.legend()
            plt.grid(True)
            plt.show()
    except Exception:
        # Se houver erro na leitura (por ex. EOF em testes), não plotar por padrão
        pass
        plt.show()



def runge_kutta(func_input, x0, y0, h, xn, ordem):
    """Resolve EDOs escalares usando métodos de Runge-Kutta de ordem 1 a 4.

    Esta função implementa os métodos de Runge-Kutta para resolver numericamente
    equações diferenciais ordinárias da forma dy/dx = f(x,y). Os métodos
    implementados vão da ordem 1 (Euler) até a ordem 4 (Runge-Kutta clássico).

    Parameters
    ----------
    func_input : str
        Expressão matemática para f(x, y) como string. Deve ser uma função
        válida das variáveis x e y. Exemplos: 'y', 'y - x**2', 'sin(x)*y'.
        Espaços são ignorados e '^' é convertido para '**'.
    x0 : float
        Ponto inicial da integração (condição inicial para x).
        Deve ser um número finito.
    y0 : float
        Valor inicial y(x0). Deve ser um número finito.
    h : float
        Tamanho do passo de integração. Deve ser positivo e dividir
        exatamente o intervalo (xn - x0), caso contrário será truncado.
    xn : float
        Ponto final da integração. Deve ser diferente de x0.
    ordem : int
        Ordem do método Runge-Kutta. Deve ser 1, 2, 3 ou 4:
        - 1: Método de Euler (primeira ordem)
        - 2: Euler modificado (segunda ordem)
        - 3: Runge-Kutta de terceira ordem
        - 4: Runge-Kutta clássico (quarta ordem)

    Returns
    -------
    x_vals : list of float
        Lista dos pontos x onde a solução foi calculada, incluindo x0 e xn.
    y_vals : list of float
        Lista dos valores aproximados y(x) correspondentes aos pontos em x_vals.

    Raises
    ------
    ValueError
        Se os parâmetros forem inválidos (ver _validate_edo_inputs).
    TypeError
        Se os tipos de entrada não forem adequados.
    RuntimeError
        Se ocorrer erro durante a avaliação da função f(x,y).

    Notes
    -----
    Os métodos de Runge-Kutta seguem as fórmulas clássicas (Euler, Euler modificado e RK4).
    Por exemplo, para Euler: ``y_{n+1} = y_n + h * f(x_n, y_n)``.
    Para RK4: ``y_{n+1} = y_n + (h/6) * (k1 + 2*k2 + 2*k3 + k4)``, onde ``k1``..``k4``
    são os incrementos padrões do método.
    A estabilidade e precisão aumentam com a ordem do método, mas também
    o custo computacional.

    Examples
    --------
    >>> # Resolver dy/dx = y com y(0) = 1 no intervalo [0, 1]
    >>> x_vals, y_vals = runge_kutta('y', 0, 1, 0.1, 1, 4)
    >>> print(f"Solução em x=1: {y_vals[-1]:.6f}")  # Aproxima e^1 ≈ 2.718282

    >>> # EDO não-linear: dy/dx = y - x²
    >>> x_vals, y_vals = runge_kutta('y - x**2', 0, 1, 0.1, 1, 2)
    """
    # Validações de entrada
    func_input, x0, y0, h, xn = _validate_edo_inputs(func_input, x0, y0, h, xn, ordem)

    # Preparar a expressão da função
    func_input = func_input.replace(' ', '')  # Remove espaços
    func_input = re.sub(r'(\d)([xy])', r'\1*\2', func_input)  # Corrigir multiplicação implícita

    # Criar função f(x,y) com fallbacks robustos
    try:
        f = _create_function_from_string(func_input, ['x', 'y'], verbose=False)
    except Exception as e:
        raise ValueError(f"Não foi possível criar a função f(x,y) a partir de '{func_input}': {e}")

    # Calcular número de passos
    n_steps = int((xn - x0) / h)

    # Avisar se o passo não divide exatamente o intervalo
    remainder = abs(xn - x0) - n_steps * h
    if remainder > 1e-10:
        print(f"Aviso: O passo h={h} não divide exatamente o intervalo [{x0}, {xn}]. "
              f"Será integrado até x={x0 + n_steps * h:.6f} em {n_steps} passos.")

    # Inicializar listas de resultados
    x_vals = []
    y_vals = []
    x = float(x0)
    y = float(y0)
    x_vals.append(x)
    y_vals.append(y)

    # Loop principal de integração
    for step in range(n_steps):
        try:
            if ordem == 1:
                # Método de Euler
                y_new = y + h * f(x, y)

            elif ordem == 2:
                # Euler Modificado (Runge-Kutta 2ª ordem)
                k1 = h * f(x, y)
                k2 = h * f(x + h, y + k1)
                y_new = y + 0.5 * (k1 + k2)

            elif ordem == 3:
                # Runge-Kutta 3ª ordem
                k1 = h * f(x, y)
                k2 = h * f(x + h/2, y + k1/2)
                k3 = h * f(x + h, y - k1 + 2*k2)
                y_new = y + (1/6) * (k1 + 4*k2 + k3)

            elif ordem == 4:
                # Runge-Kutta 4ª ordem (clássico)
                k1 = h * f(x, y)
                k2 = h * f(x + h/2, y + k1/2)
                k3 = h * f(x + h/2, y + k2/2)
                k4 = h * f(x + h, y + k3)
                y_new = y + (1/6) * (k1 + 2*k2 + 2*k3 + k4)

            # Verificar se o resultado é finito
            if not np.isfinite(y_new):
                raise RuntimeError(f"Resultado não-finito no passo {step+1}: y = {y_new}")

            # Atualizar valores
            y = y_new
            x += h

            x_vals.append(x)
            y_vals.append(y)

        except Exception as e:
            raise RuntimeError(f"Erro na integração no passo {step+1} (x={x:.6f}, y={y:.6f}): {e}")

    return x_vals, y_vals

def executar_runge_kutta(ordem):
    nomes = {
        1: "Runge-Kutta 1ª ordem (Euler)",
        2: "Runge-Kutta 2ª ordem (Euler Modificado)",
        3: "Runge-Kutta 3ª ordem",
        4: "Runge-Kutta 4ª ordem (Euler Melhorado)"
    }
    print(f"\n--- {nomes.get(ordem, 'Runge-Kutta')} ---")
    try:
        dados = pedir_dados_edo()
        func_input = dados['func_input']
        a = dados['a']
        b = dados['b']
        x0 = dados['x0']
        y0 = dados['y0']
        h = dados['h']
        m = dados['m']
        xn = dados['xn']
        solucao_exata = dados['solucao_exata']
        h, xn = passos_edo(a, b, x0, h=h, m=m)
        x_vals, y_vals = runge_kutta(func_input, x0, y0, h, xn, ordem)

        # Perguntar ao usuário se deseja plotar
        plotar = False
        try:
            resp = input("Deseja plotar os gráficos? [s/n]: ").strip().lower()
            plotar = resp.startswith('s')
        except Exception:
            # Em ambiente sem stdin/EOF (ex.: testes automatizados), não plotar
            plotar = False

        # Exibir tabela e (opcionalmente) gráfico
        titulo = nomes.get(ordem, 'Runge-Kutta')
        mostrar_tabela_e_grafico_edo(x_vals, y_vals, solucao_exata, titulo, plotar=plotar)

    except Exception as e:
        print(f"Erro: {e}")

# === NOVAS FUNÇÕES PARA SISTEMAS DE EDOS ===

def runge_kutta_sistema(funcs_input, u0, t0, tf, h, ordem):
    """Resolve sistemas de EDOs usando métodos de Runge-Kutta vetoriais.

    Esta função resolve numericamente sistemas de equações diferenciais ordinárias
    da forma dy/dt = f(t,y), onde y é um vetor de variáveis dependentes.
    Implementa os métodos de Runge-Kutta de ordem 1 a 4 para sistemas.

    Parameters
    ----------
    funcs_input : list of str
        Lista de expressões matemáticas para as funções f_i(t, y) do sistema.
        Cada string deve usar notação y[1], y[2], ... para as variáveis
        (indexação 1-based). Exemplo: ['y[2]', 'y[1] - y[2]'].
    u0 : array_like
        Vetor de condições iniciais y(t0). Deve ter o mesmo comprimento
        que funcs_input. Todos os valores devem ser finitos.
    t0 : float
        Tempo inicial da integração. Deve ser finito.
    tf : float
        Tempo final da integração. Deve ser diferente de t0.
    h : float
        Tamanho do passo de integração. Deve ser positivo.
    ordem : int
        Ordem do método Runge-Kutta (1, 2, 3 ou 4).

    Returns
    -------
    t_vals : list of float
        Lista dos pontos temporais onde a solução foi calculada,
        incluindo t0 e tf (aproximadamente).
    u_vals : ndarray
        Array de shape (n_pontos, n_equacoes) contendo os valores
        da solução em cada ponto temporal.

    Raises
    ------
    ValueError
        Se as entradas não forem válidas (ver _validate_sistema_edo_inputs).
    TypeError
        Se os tipos de entrada não forem adequados.
    RuntimeError
        Se ocorrer erro durante a integração do sistema.

    Notes
    -----
    O sistema é resolvido usando a formulação vetorial dos métodos de Runge-Kutta.
    Em termos práticos, aplica-se a versão vetorial das fórmulas escalares (Euler,
    RK2/3/4). Por exemplo, em RK4 cada :math:`k_i` é um vetor de incrementos e
    a combinação final segue a soma ponderada usual: ``y_{n+1} = y_n + (h/6)*(k1+2*k2+2*k3+k4)``.

    Examples
    --------
    >>> # Sistema linear: dy1/dt = y2, dy2/dt = -y1
    >>> funcs = ['y[2]', '-y[1]']
    >>> y0 = [1, 0]  # y1(0)=1, y2(0)=0
    >>> t_vals, y_vals = runge_kutta_sistema(funcs, y0, 0, 2*np.pi, 0.1, 4)
    >>> # y_vals[-1] ≈ [cos(2π), -sin(2π)] ≈ [1, 0]
    """
    # Validações de entrada
    funcs_input, u0, t0, tf, h = _validate_sistema_edo_inputs(funcs_input, u0, t0, tf, h, ordem)

    n_equacoes = len(u0)

    # Preparar funções do sistema
    funcs = []
    for i, func_input in enumerate(funcs_input):
        expr = func_input.strip().replace('^', '**').replace(' ', '')

        # Substituir y[1], y[2], ... por y1, y2, ... (variáveis simbólicas)
        def repl_idx_name(m):
            idx = int(m.group(1))
            if idx < 1 or idx > n_equacoes:
                raise ValueError(f"Índice y[{idx}] fora do intervalo válido [1, {n_equacoes}]")
            return f'y{idx}'

        expr_named = re.sub(r'y\[(\d+)\]', repl_idx_name, expr)

        # Expressão preparada para compilação (não imprimir em execução normal)

        # Criar símbolos: x (tempo) e y1, y2, ... (variáveis do sistema)
        y_symbols = sp.symbols(' '.join([f'y{j+1}' for j in range(n_equacoes)]))
        x_sym = sp.symbols('x')

        # Mapear nomes para símbolos
        locals_map = {'x': x_sym}
        for j, ys in enumerate(y_symbols):
            locals_map[f'y{j+1}'] = ys

        try:
            # Tentar criar função com SymPy
            expr_sym = sp.sympify(expr_named, locals=locals_map)
            lam = sp.lambdify((x_sym,) + tuple(y_symbols), expr_sym, modules=['numpy'])

            def func(x, y, lam=lam, idx=i):
                # y é array-like; passar cada componente como argumento
                return lam(x, *tuple(y.tolist() if hasattr(y, 'tolist') else list(y)))

            funcs.append(func)

        except Exception as e:
            # Fallback para eval com ambiente restrito
            try:
                def func(x, y, expr_str=expr_named, idx=i):
                    # Criar dicionário local com x e componentes de y
                    local_vars = {'x': x, 'np': np, 'math': math, **safe_math}
                    for j in range(n_equacoes):
                        local_vars[f'y{j+1}'] = y[j]

                    try:
                        return eval(expr_str, {"__builtins__": None}, local_vars)
                    except Exception:
                        return eval(expr_str)

                funcs.append(func)

            except Exception as fallback_error:
                raise ValueError(f"Não foi possível criar função {i+1} a partir de '{func_input}': "
                               f"SymPy: {e}, Fallback: {fallback_error}")

    # Inicializar resultados
    t_vals = [float(t0)]
    u_vals = [u0.copy()]

    # Loop de integração
    t_current = float(t0)
    u_current = u0.copy()

    while t_current < tf:
        # Calcular passo atual (último passo pode ser menor)
        step = min(h, tf - t_current)

        # Evitar passo nulo
        if step <= 1e-15:
            break

        try:
            if ordem == 1:
                # Método de Euler
                k1 = np.array([f(t_current, u_current) for f in funcs])
                u_new = u_current + step * k1

            elif ordem == 2:
                # Runge-Kutta 2ª ordem
                k1 = np.array([f(t_current, u_current) for f in funcs])
                k2 = np.array([f(t_current + step, u_current + step * k1) for f in funcs])
                u_new = u_current + 0.5 * step * (k1 + k2)

            elif ordem == 3:
                # Runge-Kutta 3ª ordem
                k1 = np.array([f(t_current, u_current) for f in funcs])
                k2 = np.array([f(t_current + step/2, u_current + step*k1/2) for f in funcs])
                k3 = np.array([f(t_current + step, u_current - step*k1 + 2*step*k2) for f in funcs])
                u_new = u_current + (step/6) * (k1 + 4*k2 + k3)

            elif ordem == 4:
                # Runge-Kutta 4ª ordem
                k1 = np.array([f(t_current, u_current) for f in funcs])
                k2 = np.array([f(t_current + step/2, u_current + step*k1/2) for f in funcs])
                k3 = np.array([f(t_current + step/2, u_current + step*k2/2) for f in funcs])
                k4 = np.array([f(t_current + step, u_current + step*k3) for f in funcs])
                u_new = u_current + (step/6) * (k1 + 2*k2 + 2*k3 + k4)

            # Verificar se os resultados são finitos
            if not np.all(np.isfinite(u_new)):
                raise RuntimeError(f"Resultado não-finito no tempo t={t_current:.6f}")

            # Atualizar valores
            t_current += step
            u_current = u_new

            t_vals.append(t_current)
            u_vals.append(u_current.copy())

        except Exception as e:
            raise RuntimeError(f"Erro na integração em t={t_current:.6f}: {e}")

    return t_vals, np.array(u_vals)

def executar_sistema_edos():
    """
    Interface para resolução de sistemas de EDOs usando Runge-Kutta.
    """
    try:
        # Pedir ordem do método RK
        ordem = int(input("Digite a ordem do método de Runge-Kutta (1-4): "))
        if not 1 <= ordem <= 4:
            print("Ordem deve estar entre 1 e 4.")
            return
        
        # Pedir número de equações
        n = int(input("Digite o número de equações no sistema: "))
        if n < 1:
            print("Número de equações deve ser pelo menos 1.")
            return
        
        # Pedir as funções do sistema
        print(f"\nDigite as {n} funções do sistema dy[i]/dx = f_i(x, y)")
        print("Exemplo: 2*y[1] - y[2] - x  (use y[1] para a primeira variável, y[2] para a segunda, etc.)")
        funcs_input = []
        for i in range(n):
            func = input(f"f{i}(x, y) = ")
            funcs_input.append(func)
        
        # Pedir condições iniciais
        print(f"\nDigite as {n} condições iniciais y[i](0):")
        y0 = []
        for i in range(n):
            yi = float(input(f"y[{i+1}](0) = "))
            y0.append(yi)
        y0 = np.array(y0)
        
        # Pedir intervalo temporal
        x0 = float(input("Digite o valor inicial de x (x0): "))
        xf = float(input("Digite o valor final de x (xf): "))
        print("\nComo deseja especificar o passo?")
        print("1 - Inserir h diretamente")
        print("2 - Inserir número de subintervalos m")
        escolha_h = input("Escolha (1 ou 2): ").strip()
        if escolha_h == '1':
            h = float(input("Digite o passo h: "))
            if h <= 0:
                print("Passo h inválido (<=0). Encerrando esta execução.")
                return
        elif escolha_h == '2':
            m = int(input("Digite o número de subintervalos m: "))
            if m <= 0:
                print("Número de subintervalos inválido (<=0). Encerrando esta execução.")
                return
            h = (xf - x0) / m
            print(f"Calculado h = {h}")
        else:
            print("Opção inválida, usando h=0.1")
            h = 0.1
        
        
        # Resolver o sistema
        t_vals, u_vals = runge_kutta_sistema(funcs_input, y0, x0, xf, h, ordem)
        u_vals = np.array(u_vals)
        n = u_vals.shape[1] if len(u_vals.shape) > 1 else 1
        # Exibir resultados em tabela
        print(f"\nMétodo: Runge-Kutta {ordem}ª ordem")
        header = "x\t" + "\t".join([f"y[{i+1}]" for i in range(n)])
        print(header)
        for i in range(len(t_vals)):
            linha = f"{t_vals[i]:.6f}"
            for j in range(n):
                linha += f"\t{u_vals[i][j]:.6f}"
            print(linha)
        
        
        # Perguntar se deseja plotar os gráficos do sistema
        try:
            resp = input("Deseja plotar os gráficos do sistema? [s/n]: ").strip().lower()
            if resp.startswith('s'):
                plt.figure(figsize=(10, 6))
                for j in range(n):
                    plt.plot(t_vals, u_vals[:, j], label=f'y[{j+1}](x)', marker='o', markersize=2)
                plt.xlabel('x')
                plt.ylabel('y[j]')
                plt.title(f'Solução do Sistema de EDOs - RK{ordem}')
                plt.legend()
                plt.grid(True)
                plt.show()
        except Exception:
            # Em ambiente não-interativo, não mostrar gráficos por padrão
            pass
        
    except Exception as e:
        print(f"Erro: {e}")

def executar_edo_2ordem():
    """
    Interface para resolução de EDOs de 2ª ordem convertidas em sistemas.
    """
    try:
        # Pedir ordem do método RK
        ordem = int(input("Digite a ordem do método de Runge-Kutta (1-4): "))
        if not 1 <= ordem <= 4:
            print("Ordem deve estar entre 1 e 4.")
            return
        
        print("\n--- EDO de 2ª Ordem ---")
        print("Digite a EDO na forma: d²y/dx² = f(x, y, y')")
        
        # Entrada da função
        print("Digite f(x, y, y') (use y para y e yp para y'):")
        f_input = input("f(x, y, yp) = ").strip()
        
        # Preprocessar: substituir y por u[0], yp por u[1]
        f_input = f_input.replace('y', 'u[0]').replace('yp', 'u[1]')
        
        # Condições iniciais
        x0 = float(input("Digite x inicial: "))
        y0 = float(input("Digite y(x0): "))
        yp0 = float(input("Digite y'(x0): "))
        
        # Intervalo temporal
        xf = float(input("Digite x final: "))
        h = float(input("Digite o passo h: "))
        if h <= 0:
            print("Passo h inválido (<=0). Encerrando esta execução.")
            return
        
        # Converter para sistema
        funcs_input = ['u[1]', f_input]  # dy1/dx = y2, dy2/dx = f
        u0 = [y0, yp0]
        
        # Resolver usando o método de sistemas
        t_vals, u_vals = runge_kutta_sistema(funcs_input, u0, x0, xf, h, ordem)
        
        # Exibir resultados
        print(f"\nSolução da EDO de 2ª ordem:")
        # Use double-quoted string literal inside f-string expression to avoid backslash in expressions
        print(f"{'x':>10} {'y':>15} {"y'":>15}")
        print("-" * 40)
        
        for i, (x, u) in enumerate(zip(t_vals, u_vals)):
            print(f"{x:10.4f} {u[0]:15.8f} {u[1]:15.8f}")
        
        # Perguntar se deseja plotar os gráficos
        try:
            resp = input("Deseja plotar os gráficos? [s/n]: ").strip().lower()
            if resp.startswith('s'):
                plt.figure(figsize=(12, 5))
                plt.subplot(1, 2, 1)
                plt.plot(t_vals, u_vals[:, 0], 'b-', marker='o', markersize=3, label='y(x)')
                plt.xlabel('x')
                plt.ylabel('y')
                plt.title('Solução y(x)')
                plt.grid(True)
                plt.legend()

                plt.subplot(1, 2, 2)
                plt.plot(t_vals, u_vals[:, 1], 'r-', marker='s', markersize=3, label='y\'(x)')
                plt.xlabel('x')
                plt.ylabel("y'")
                plt.title("Derivada y'(x)")
                plt.grid(True)
                plt.legend()

                plt.tight_layout()
                plt.show()
        except Exception:
            # Em ambiente não-interativo (tests), não plotar por padrão
            pass
        
    except Exception as e:
        print(f"Erro: {e}")

def menu_principal():
    while True:
        print("\n===== MENU DE EQUAÇÕES DIFERENCIAIS =====")
        print("1 - Método de Euler (Runge-Kutta 1ª ordem)")
        print("2 - Método de Runge-Kutta (2ª, 3ª ou 4ª ordem)")
        print("3 - Sistemas de EDOs")
        print("4 - Equações Diferenciais de 2ª Ordem")
        print("0 - Sair")   

        opcao = input("Escolha uma opção: ")
        if opcao == '0':
            print("Encerrando o programa.")
            break
        
        if opcao == '1':
            executar_runge_kutta(1)
        elif opcao == '2':
            try:
                ordem = int(input("Digite a ordem do método de Runge-Kutta (2-4): "))
                if 2 <= ordem <= 4:
                    executar_runge_kutta(ordem)
                else:
                    print("Ordem deve estar entre 2 e 4.")
            except ValueError:
                print("Entrada inválida. Digite um número inteiro.")
        elif opcao == '3':
            executar_sistema_edos()
        elif opcao == '4':
            resolver_edo_2ordem()
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu_principal()
