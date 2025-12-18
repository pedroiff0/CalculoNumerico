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

def pedir_dados_edo():
    """Obtém entradas do usuário para resolução de EDOs (RK/Euler).

    A função solicita interativamente a função ``f(x, y)``, intervalo de integração,
    condições iniciais e passo (``h``) ou número de subintervalos (``m``). Também
    permite informar uma solução exata opcional.

    Returns
    -------
    dict
        Dicionário com chaves: 'func_input', 'a', 'b', 'x0', 'y0', 'h', 'm', 'xn',
        'solucao_exata' (callable ou None) e 'sol_exata_expr' (string).
    """
    print("Digite a função f(x,y) em notação matemática simples:")
    print("Exemplo: y - x  (será interpretado como y - x)")
    func_input = input("f(x,y) = ").strip()

    print("\nIntervalo de integração [a,b]:")
    a = float(input("a = "))
    b = float(input("b = "))

    print("\nCondições iniciais:")
    x0 = float(input("x0 = "))
    y0 = float(input("y0 = "))

    # passo: h ou m
    while True:
        escolha = input("Deseja informar passo por h ou por número de subintervalos m? [h/m]: ").strip().lower()
        if escolha == 'h':
            try:
                h = float(input("h = "))
                m = None
                break
            except Exception:
                print("Valor de h inválido. Tente novamente.")
                continue
        elif escolha == 'm':
            try:
                m = int(input("m = "))
                if m <= 0:
                    print("m deve ser inteiro positivo. Tente novamente.")
                    continue
                h = (b - a) / m
                print(f"Calculado h = {h}")
                break
            except Exception:
                print("Valor de m inválido. Tente novamente.")
                continue
        else:
            print("Escolha inválida. Digite 'h' ou 'm'.")

    xn = b

    # solução exata opcional
    solucao_exata = None
    sol_exata_expr = ''
    s = input("Solução exata (y(x))? (pressione Enter se não houver): ").strip()
    if s:
        sol_exata_expr = s.replace(' ', '').replace('^', '**')
        try:
            x_sym = sp.symbols('x')
            # usar o mapeamento global `SYMPY_LOCALS` (define sin, cos, pi, e, etc.)
            expr_sol = sp.sympify(sol_exata_expr, locals=SYMPY_LOCALS)
            lam_sol = sp.lambdify(x_sym, expr_sol, modules=['numpy'])
            def solucao_exata(x):
                val = lam_sol(x)
                # tentar converter de numpy/sympy para float
                try:
                    return float(val)
                except Exception:
                    try:
                        return float(np.asarray(val).item())
                    except Exception:
                        return float(sp.N(val))
        except Exception:
            print("Expressão da solução exata inválida; ignorando solução exata.")
            sol_exata_expr = ''
            solucao_exata = None

    return {
        'func_input': func_input,
        'a': a,
        'b': b,
        'x0': x0,
        'y0': y0,
        'h': h,
        'm': m if 'm' in locals() else None,
        'xn': xn,
        'solucao_exata': solucao_exata if 'solucao_exata' in locals() and sol_exata_expr else None,
        'sol_exata_expr': sol_exata_expr,
    }


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

    Parameters
    ----------
    func_input : str
        Expressão para f(x, y) como string (ex.: ``'y'`` para dy/dx = y).
    x0 : float
        Ponto inicial.
    y0 : float
        Valor inicial y(x0).
    h : float
        Tamanho do passo (deve dividir o intervalo (xn-x0)).
    xn : float
        Ponto final onde se integra até (xn > x0 esperado).
    ordem : int
        Ordem do método (1, 2, 3 ou 4).

    Returns
    -------
    (list, list)
        Tupla ``(x_vals, y_vals)`` com os pontos de amostragem e as aproximações y.
    """
    func_input = func_input.replace(' ', '')  # Remove espaços
    func_input = re.sub(r'(\d)([xy])', r'\1*\2', func_input)
    # Usar sympy para avaliar a função f(x,y)
    x_sym, y_sym = sp.symbols('x y')
    try:
        expr = sp.sympify(func_input)
        f = sp.lambdify((x_sym, y_sym), expr, modules=['numpy'])
    except Exception:
        # fallback simples: usar eval em ambiente restrito com safe_math
        def f(x, y):
            local_vars = {"x": x, "y": y, "math": math, **safe_math}
            try:
                return eval(func_input, {"__builtins__": None}, local_vars)
            except Exception:
                # última tentativa: avaliar com python direto
                return eval(func_input)

    if h <= 0:
        raise ValueError('h deve ser > 0')
    if ordem not in [1, 2, 3, 4]:
        raise ValueError('ordem deve ser 1, 2, 3 ou 4')
    n = int((xn - x0) / h)
    x_vals = []
    y_vals = []
    x = x0
    y = y0
    x_vals.append(x)
    y_vals.append(y)
    
    for _ in range(n):
        if ordem == 1:
            y = y + h * f(x, y)
        elif ordem == 2:
            k1 = h * f(x, y)
            k2 = h * f(x + h, y + k1)
            y = y + 0.5 * (k1 + k2)
        elif ordem == 3:
            k1 = h * f(x, y)
            k2 = h * f(x + h / 2, y + k1 / 2)
            k3 = h * f(x + h, y - k1 + 2 * k2)
            y = y + (1/6) * (k1 + 4 * k2 + k3)
        elif ordem == 4:
            k1 = h * f(x, y)
            k2 = h * f(x + h / 2, y + k1 / 2)
            k3 = h * f(x + h / 2, y + k2 / 2)
            k4 = h * f(x + h, y + k3)
            y = y + (1 / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

        x += h
        x_vals.append(x)
        y_vals.append(y)

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
    """Resolve sistemas de EDOs usando Runge-Kutta (vetorial).

    Parameters
    ----------
    funcs_input : list of str or callables
        Lista de expressões/funcões que descrevem cada componente do sistema. Use a notação
        ``y[1]``, ``y[2]`` etc. quando passar strings (1-based index).
    u0 : array_like
        Vetor de condições iniciais (tamanho n, onde n é número de equações).
    t0 : float
        Tempo inicial.
    tf : float
        Tempo final para integração.
    h : float
        Passo de tempo.
    ordem : int
        Ordem do método de Runge-Kutta (1-4).

    Returns
    -------
    (list, ndarray)
        Tupla ``(t_vals, u_vals)`` onde ``t_vals`` é lista de tempos e ``u_vals`` é array (m x n)
        com as soluções em cada tempo.
    """
    # Preprocessar cada função do sistema para aceitar y[1], y[2], ... (1-based)
    funcs = []
    n = len(u0)
    for func_input in funcs_input:
        expr = func_input.strip().replace('^', '**').replace(' ', '')
        # Substituir y[1] por y1, y[2] por y2, etc. (variáveis simbólicas)
        def repl_idx_name(m):
            idx = int(m.group(1))
            return f'y{idx}'
        expr_named = re.sub(r'y\[(\d+)\]', repl_idx_name, expr)

        # Criar símbolos x, y1, y2, ... conforme o número de equações
        y_symbols = sp.symbols(' '.join([f'y{i+1}' for i in range(n)]))
        x_sym = sp.symbols('x')
        # mapear nomes para símbolos
        locals_map = {'x': x_sym}
        for i, ys in enumerate(y_symbols):
            locals_map[f'y{i+1}'] = ys

        try:
            expr_sym = sp.sympify(expr_named, locals=locals_map)
            # lambdify aceita (x, y1, y2, ...)
            lam = sp.lambdify((x_sym, ) + tuple(y_symbols), expr_sym, modules=['numpy'])
            def make_func_from_lam(lf):
                def f(x, y):
                    # y é array-like; passar cada componente como argumento
                    return lf(x, *tuple(y.tolist() if hasattr(y, 'tolist') else list(y)))
                return f
            funcs.append(make_func_from_lam(lam))
        except Exception:
            # fallback para compatibilidade com código anterior
            def make_func(e):
                def f(x, y):
                    local = {'x': x, 'y': y, 'np': np, 'math': math, **safe_math}
                    try:
                        return eval(e, {"__builtins__": None}, local)
                    except Exception:
                        return eval(e)
                return f
            funcs.append(make_func(expr))
    
    if h <= 0:
        raise ValueError('h deve ser > 0')
    t_vals = [t0]
    u_vals = [u0.copy()]
    n = len(u0)  # número de equações
    
    while t0 < tf:
        step = min(h, tf - t0)  # last step may be smaller than h
        # Evitar passo nulo que causaria loop infinito
        if step <= 0:
            print("Passo nulo ou intervalo concluído; interrompendo resolução do sistema.")
            break
        if ordem == 1:
            # Euler
            k1 = np.array([f(t0, u_vals[-1]) for f in funcs])
            u_new = u_vals[-1] + step * k1
        elif ordem == 2:
            # RK2
            k1 = np.array([f(t0, u_vals[-1]) for f in funcs])
            k2 = np.array([f(t0 + step, u_vals[-1] + step * k1) for f in funcs])
            u_new = u_vals[-1] + 0.5 * step * (k1 + k2)
        elif ordem == 3:
            # RK3
            k1 = np.array([f(t0, u_vals[-1]) for f in funcs])
            k2 = np.array([f(t0 + step/2, u_vals[-1] + step*k1/2) for f in funcs])
            k3 = np.array([f(t0 + step, u_vals[-1] - step*k1 + 2*step*k2) for f in funcs])
            u_new = u_vals[-1] + (step/6) * (k1 + 4*k2 + k3)
        elif ordem == 4:
            # RK4
            k1 = np.array([f(t0, u_vals[-1]) for f in funcs])
            k2 = np.array([f(t0 + step/2, u_vals[-1] + step*k1/2) for f in funcs])
            k3 = np.array([f(t0 + step/2, u_vals[-1] + step*k2/2) for f in funcs])
            k4 = np.array([f(t0 + step, u_vals[-1] + step*k3) for f in funcs])
            u_new = u_vals[-1] + (step/6) * (k1 + 2*k2 + 2*k3 + k4)
        
        t0 += step
        # append new time and value (ensures final tf is included)
        t_vals.append(t0)
        u_vals.append(u_new)
    
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
