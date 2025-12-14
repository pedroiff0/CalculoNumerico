import numpy as np
import matplotlib.pyplot as plt
import math

def resolver_edo_2ordem():
    print("\n=== Resolução de EDO de 2ª ordem: y'' = f(x, y, y') ===")
    print("Digite f(x, y, yp) usando x, y, yp (exemplo: yp + 2*y - x**2)")
    f_input = input("f(x, y, yp) = ").strip().replace('^', '**')
    x0 = float(input("x inicial: "))
    xf = float(input("x final: "))
    y0 = eval(input("y(x0): ").strip(), {"__builtins__": None, "math": math, "pi": math.pi, "e": math.e})
    yp0 = eval(input("y'(x0): ").strip(), {"__builtins__": None, "math": math, "pi": math.pi, "e": math.e})
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
        print("Opção inválida, usando h=0.1")
        h = 0.1

    # Montar sistema equivalente: y1' = y2, y2' = f(x, y1, y2)
    import re
    # Converter y[1] -> y[0], y[2] -> y[1] na string "y[2]"
    def convert_indices(expr):
        def repl_idx(m):
            idx = int(m.group(1))
            return f'y[{idx-1}]'
        return re.sub(r'y\[(\d+)\]', repl_idx, expr)

    def f2(x, y):
        local = {
            'x': x,
            'y': y[0],
            'yp': y[1],
            'np': np,
            'math': math,
            'sin': math.sin,
            'cos': math.cos,
            'exp': math.exp,
            'log': math.log,
            'sqrt': math.sqrt,
            'pi': math.pi,
            'e': math.e
        }
        return eval(f_input, {"__builtins__": None}, local)
    funcs_input = [convert_indices("y[2]"), f2]
    # y[1] = y, y[2] = y'
    y_ini = [y0, yp0]
    # Adaptar runge_kutta_sistema para aceitar função direta no segundo termo
    def runge_kutta_sistema_2ordem(funcs_input, y0, x0, xf, h, ordem):
        n = len(y0)
        t_vals = [x0]
        u_vals = [np.array(y0)]
        while t_vals[-1] < xf:
            x = t_vals[-1]
            y = u_vals[-1]
            if ordem == 1:
                k1 = np.array([
                    eval(funcs_input[0], {"x": x, "y": y, "np": np, "math": math, "sin": math.sin, "cos": math.cos, "exp": math.exp, "log": math.log, "sqrt": math.sqrt, "pi": math.pi, "e": math.e}) if isinstance(funcs_input[0], str) else funcs_input[0](x, y),
                    funcs_input[1](x, y)
                ])
                y_new = y + h * k1
            elif ordem == 2:
                k1 = np.array([
                    eval(funcs_input[0], {"x": x, "y": y, "np": np, "math": math, "sin": math.sin, "cos": math.cos, "exp": math.exp, "log": math.log, "sqrt": math.sqrt, "pi": math.pi, "e": math.e}) if isinstance(funcs_input[0], str) else funcs_input[0](x, y),
                    funcs_input[1](x, y)
                ])
                k2 = np.array([
                    eval(funcs_input[0], {"x": x+h, "y": y+h*k1, "np": np, "math": math, "sin": math.sin, "cos": math.cos, "exp": math.exp, "log": math.log, "sqrt": math.sqrt, "pi": math.pi, "e": math.e}) if isinstance(funcs_input[0], str) else funcs_input[0](x+h, y+h*k1),
                    funcs_input[1](x+h, y+h*k1)
                ])
                y_new = y + 0.5 * h * (k1 + k2)
            elif ordem == 3:
                k1 = np.array([
                    eval(funcs_input[0], {"x": x, "y": y, "np": np, "math": math, "sin": math.sin, "cos": math.cos, "exp": math.exp, "log": math.log, "sqrt": math.sqrt, "pi": math.pi, "e": math.e}) if isinstance(funcs_input[0], str) else funcs_input[0](x, y),
                    funcs_input[1](x, y)
                ])
                k2 = np.array([
                    eval(funcs_input[0], {"x": x+h/2, "y": y+h*k1/2, "np": np, "math": math, "sin": math.sin, "cos": math.cos, "exp": math.exp, "log": math.log, "sqrt": math.sqrt, "pi": math.pi, "e": math.e}) if isinstance(funcs_input[0], str) else funcs_input[0](x+h/2, y+h*k1/2),
                    funcs_input[1](x+h/2, y+h*k1/2)
                ])
                k3 = np.array([
                    eval(funcs_input[0], {"x": x+h, "y": y-h*k1+2*h*k2, "np": np, "math": math, "sin": math.sin, "cos": math.cos, "exp": math.exp, "log": math.log, "sqrt": math.sqrt, "pi": math.pi, "e": math.e}) if isinstance(funcs_input[0], str) else funcs_input[0](x+h, y-h*k1+2*h*k2),
                    funcs_input[1](x+h, y-h*k1+2*h*k2)
                ])
                y_new = y + (h/6) * (k1 + 4*k2 + k3)
            elif ordem == 4:
                k1 = np.array([
                    eval(funcs_input[0], {"x": x, "y": y, "np": np, "math": math, "sin": math.sin, "cos": math.cos, "exp": math.exp, "log": math.log, "sqrt": math.sqrt, "pi": math.pi, "e": math.e}) if isinstance(funcs_input[0], str) else funcs_input[0](x, y),
                    funcs_input[1](x, y)
                ])
                k2 = np.array([
                    eval(funcs_input[0], {"x": x+h/2, "y": y+h*k1/2, "np": np, "math": math, "sin": math.sin, "cos": math.cos, "exp": math.exp, "log": math.log, "sqrt": math.sqrt, "pi": math.pi, "e": math.e}) if isinstance(funcs_input[0], str) else funcs_input[0](x+h/2, y+h*k1/2),
                    funcs_input[1](x+h/2, y+h*k1/2)
                ])
                k3 = np.array([
                    eval(funcs_input[0], {"x": x+h/2, "y": y+h*k2/2, "np": np, "math": math, "sin": math.sin, "cos": math.cos, "exp": math.exp, "log": math.log, "sqrt": math.sqrt, "pi": math.pi, "e": math.e}) if isinstance(funcs_input[0], str) else funcs_input[0](x+h/2, y+h*k2/2),
                    funcs_input[1](x+h/2, y+h*k2/2)
                ])
                k4 = np.array([
                    eval(funcs_input[0], {"x": x+h, "y": y+h*k3, "np": np, "math": math, "sin": math.sin, "cos": math.cos, "exp": math.exp, "log": math.log, "sqrt": math.sqrt, "pi": math.pi, "e": math.e}) if isinstance(funcs_input[0], str) else funcs_input[0](x+h, y+h*k3),
                    funcs_input[1](x+h, y+h*k3)
                ])
                y_new = y + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
            x_next = x + h
            if x_next > xf + 1e-12:
                break
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
    # Gráfico
    plt.figure(figsize=(10, 5))
    plt.plot(t_vals, u_vals[:, 0], label="y(x)", marker='o')
    plt.plot(t_vals, u_vals[:, 1], label="y'(x)", marker='s')
    plt.xlabel('x')
    plt.ylabel('Soluções')
    plt.title('Solução da EDO de 2ª ordem')
    plt.legend()
    plt.grid(True)
    plt.show()

def menu():
    print("\n===== MENU DE EQUAÇÕES DIFERENCIAIS =====")
    print("1 - Método de Euler (Runge-Kutta 1ª ordem)")
    print("2 - Método de Runge-Kutta (2ª, 3ª ou 4ª ordem)")
    print("3 - Sistemas de EDOs")
    print("4 - Equações Diferenciais de 2ª Ordem")
    print("0 - Sair")   
    return input("Escolha uma opção: ")

def runge_kutta(func_input, x0, y0, h, xn, ordem):
    func_input = func_input.replace(' ', '')  # Remove espaços
    import re
    func_input = re.sub(r'(\d)([xy])', r'\1*\2', func_input)
    
    f = lambda x, y: eval(func_input)
    
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
        4: "Runge-Kutta 4ª ordem"
    }
    print(f"\n--- {nomes[ordem]} ---")
    try:
        # Entrada facilitada da função
        print("Digite a função f(x,y) em notação matemática simples:")
        print("Exemplo: y - x  (será interpretado como y - x)")
        func_input = input("f(x,y) = ").strip()
        
        # Condições iniciais separadas
        print("\nCondições iniciais:")
        x0 = float(input("x inicial: "))
        y0 = float(input("y inicial: "))
        
        # Solução exata opcional
        print("\nSolução exata (opcional, pressione Enter se não houver):")
        sol_exata_input = input("y(x) = ").strip()
        if sol_exata_input:
            sol_exata_expr = sol_exata_input.replace(' ', '').replace('^', '**')
            def solucao_exata(x):
                return eval(sol_exata_expr, {"x": x, "exp": math.exp, "sin": math.sin, "cos": math.cos, "log": math.log, "sqrt": math.sqrt, "pi": math.pi, "e": math.e})
        else:
            sol_exata_expr = ""
            solucao_exata = None
        
        # Configuração específica para Euler
        if ordem == 1:
            # Para Euler, entrada simples como outros métodos
            h = float(input("Passo h: "))
            xn = float(input("Valor final de x (xn): "))
            pontos_calculo = []  # não usado
        else:
            # Para outros métodos, escolha como especificar h
            print("\nComo deseja especificar o passo h?")
            print("1 - Inserir h diretamente")
            print("2 - Inserir intervalo [a,b] e número de subintervalos m")
            choice = input("Escolha (1 ou 2): ").strip()
            
            if choice == '1':
                h = float(input("Passo h: "))
                xn = float(input("Valor final de x (xn): "))
            elif choice == '2':
                b = float(input("x final (b): "))
                m = int(input("Número de subintervalos m: "))
                h = (b - x0) / m
                xn = b
                print(f"Calculado h = {h}")
            else:
                print("Opção inválida, usando h=0.1 e xn=1.0")
                h = 0.1
                xn = 1.0
            
            pontos_calculo = []  # não usado
        
        # Função exata para comparação
        if solucao_exata is not None:
            print(f"\nUsando solução exata: y(x) = {sol_exata_expr}")
        else:
            print("\nSem solução exata fornecida.")
        
        # Lógica específica por método
        x_vals, y_vals = runge_kutta(func_input, x0, y0, h, xn, ordem)
        
        # Exibir resultados
        if False:  # Unificar display para todos os métodos
            # Tabela comparativa para Euler
            print(f"{'='*80}")
            print(f"Tabela Comparativa - {nomes[ordem]}")
            print(f"Função: f(x,y) = {func_input}")
            print(f"Condições iniciais: x={x0}, y={y0}")
            if sol_exata_expr:
                print(f"Solução exata: y(x) = {sol_exata_expr}")
            else:
                print("Sem solução exata fornecida.")
            print(f"{'='*80}")
            
            # Cabeçalho da tabela
            header = f"{'x':>8}"
            for h in h_vals:
                header += f"{'y(h='+str(h)+')':>15}"
            if solucao_exata is not None:
                header += f"{'y_exato':>15} {'Erro(h=0.1)':>15} {'Erro(h=0.01)':>15}"
            print(header)
            print("-" * len(header))
            
            # Linhas da tabela para cada ponto
            for x_busca in pontos_calculo:
                linha = f"{x_busca:>8}"
                
                y_aprox_vals = []
                for h in h_vals:
                    x_vals, y_vals = resultados[h]
                    # Encontrar o valor mais próximo
                    idx = np.argmin(np.abs(np.array(x_vals) - x_busca))
                    y_aprox = y_vals[idx]
                    y_aprox_vals.append(y_aprox)
                    linha += f"{y_aprox:>15}"
                
                if solucao_exata is not None:
                    # Valor exato
                    y_real = solucao_exata(x_busca)
                    linha += f"{y_real:>15}"
                    
                    # Erros
                    for y_aprox in y_aprox_vals:
                        erro = abs(y_real - y_aprox)
                        linha += f"{erro:>15}"
                
                print(linha)
            
            print(f"{'='*80}")
            
            # Gráfico simples
            plt.figure(figsize=(10, 6))
            for h in h_vals:
                x_vals, y_vals = resultados[h]
                plt.plot(x_vals, y_vals, marker='o', markersize=3, label=f'Aproximado (h={h})')
            if solucao_exata is not None:
                x_plot = np.linspace(x0, max(pontos_calculo), 100)
                y_exato_plot = [solucao_exata(x) for x in x_plot]
                plt.plot(x_plot, y_exato_plot, color='green', linestyle='--', linewidth=2, label='Solução Exata')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title(f'Comparação - {nomes[ordem]}')
            plt.legend()
            plt.grid(True)
            plt.show()
            
        else:
            # Para outros métodos: exibir tabela simples
            if solucao_exata is not None:
                print("\n--- Tabela de Comparação ---")
                print(f"{'x':>5} {'y_aprox':>18} {'y_exato':>18}")
                print("-" * 43)
                for xi, yi in zip(x_vals, y_vals):
                    y_real = solucao_exata(xi)
                    print(f"{xi:.1f} {yi} {y_real}")
            else:
                print("\nValores calculados:")
                for xi, yi in zip(x_vals, y_vals):
                    print(f"x = {xi:.1f}, y = {yi}")
            
            # Gráfico simples
            plt.plot(x_vals, y_vals, marker='o', label='Aproximado')
            if solucao_exata is not None:
                plt.plot(x_vals, [solucao_exata(xi) for xi in x_vals], linestyle='--', label='Exato')
            plt.xlabel("x")
            plt.ylabel("y")
            plt.title(nomes[ordem])
            plt.legend()
            plt.grid(True)
            plt.show()
        
    except Exception as e:
        print(f"Erro: {e}")

# === NOVAS FUNÇÕES PARA SISTEMAS DE EDOS ===

def runge_kutta_sistema(funcs_input, u0, t0, tf, h, ordem):
    """
    Versão vetorial do método de Runge-Kutta para sistemas de EDOs.
    Mantém a mesma lógica dos métodos escalares, mas opera com vetores.
    """
    # Preprocessar cada função do sistema para aceitar y[1], y[2], ... (1-based)
    import re
    funcs = []
    n = len(u0)
    for func_input in funcs_input:
        expr = func_input.strip().replace('^', '**').replace(' ', '')
        # Substituir y[1] por y[0], y[2] por y[1], etc.
        def repl_idx(m):
            idx = int(m.group(1))
            return f'y[{idx-1}]'
        expr = re.sub(r'y\[(\d+)\]', repl_idx, expr)
        def make_func(e):
            def f(x, y):
                local = {
                    'x': x,
                    'y': y,
                    'np': np,
                    'math': math,
                    'sin': math.sin,
                    'cos': math.cos,
                    'exp': math.exp,
                    'log': math.log,
                    'sqrt': math.sqrt,
                    'pi': math.pi,
                    'e': math.e
                }
                return eval(e, {"__builtins__": None}, local)
            return f
        funcs.append(make_func(expr))
    
    t_vals = [t0]
    u_vals = [u0.copy()]
    n = len(u0)  # número de equações
    
    while t0 < tf:
        if ordem == 1:
            # Euler
            k1 = np.array([f(t0, u_vals[-1]) for f in funcs])
            u_new = u_vals[-1] + h * k1
        elif ordem == 2:
            # RK2
            k1 = np.array([f(t0, u_vals[-1]) for f in funcs])
            k2 = np.array([f(t0 + h, u_vals[-1] + h * k1) for f in funcs])
            u_new = u_vals[-1] + 0.5 * h * (k1 + k2)
        elif ordem == 3:
            # RK3
            k1 = np.array([f(t0, u_vals[-1]) for f in funcs])
            k2 = np.array([f(t0 + h/2, u_vals[-1] + h*k1/2) for f in funcs])
            k3 = np.array([f(t0 + h, u_vals[-1] - h*k1 + 2*h*k2) for f in funcs])
            u_new = u_vals[-1] + (h/6) * (k1 + 4*k2 + k3)
        elif ordem == 4:
            # RK4
            k1 = np.array([f(t0, u_vals[-1]) for f in funcs])
            k2 = np.array([f(t0 + h/2, u_vals[-1] + h*k1/2) for f in funcs])
            k3 = np.array([f(t0 + h/2, u_vals[-1] + h*k2/2) for f in funcs])
            k4 = np.array([f(t0 + h, u_vals[-1] + h*k3) for f in funcs])
            u_new = u_vals[-1] + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
        
        t0 += h
        if t0 > tf:
            break
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
        elif escolha_h == '2':
            m = int(input("Digite o número de subintervalos m: "))
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
        
        
        # Gráfico corrigido para sistemas: cada y[j] ao longo de x
        plt.figure(figsize=(10, 6))
        for j in range(n):
            plt.plot(t_vals, u_vals[:, j], label=f'y[{j+1}](x)', marker='o', markersize=2)
        plt.xlabel('x')
        plt.ylabel('y[j]')
        plt.title(f'Solução do Sistema de EDOs - RK{ordem}')
        plt.legend()
        plt.grid(True)
        plt.show()
        
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
        
        # Converter para sistema
        funcs_input = ['u[1]', f_input]  # dy1/dx = y2, dy2/dx = f
        u0 = [y0, yp0]
        
        # Resolver usando o método de sistemas
        t_vals, u_vals = runge_kutta_sistema(funcs_input, u0, x0, xf, h, ordem)
        
        # Exibir resultados
        print(f"\nSolução da EDO de 2ª ordem:")
        print(f"{'x':>10} {'y':>15} {'y\'':>15}")
        print("-" * 40)
        
        for i, (x, u) in enumerate(zip(t_vals, u_vals)):
            print(f"{x:10.4f} {u[0]:15.8f} {u[1]:15.8f}")
        
        # Gráfico
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
        plt.ylabel('y\'')
        plt.title('Derivada y\'(x)')
        plt.grid(True)
        plt.legend()
        
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"Erro: {e}")

def menu_principal():
    while True:
        opcao = menu()
        if opcao == '1':
            # Método de Euler (ordem 1)
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
        elif opcao == '0':
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu_principal()