"""
Requirements do projeto:

matplotlib==3.10.7
numpy==2.3.4
sympy==1.14.0
pandas==2.3.3
mpmath==1.3.0

"""
import numpy as np
from sympy import symbols, integrate, sympify
from sympy import sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, exp, sqrt, log, Abs, pi, E

# Mapeamento padrão para uso com sympify (padroniza nomes de funções/constantes)
SYMPY_LOCALS = {
    'sin': sin, 'cos': cos, 'tan': tan,
    'asin': asin, 'acos': acos, 'atan': atan,
    'sinh': sinh, 'cosh': cosh, 'tanh': tanh,
    'exp': exp, 'sqrt': sqrt, 'log': log, 'abs': Abs,
    'pi': pi, 'e': E, 'E': E
}


"""

Projeto de Cálculo Numérico:
Autor: Pedro Henrique Rocha de Andrade
Orientador: Rodrigo Lacerda da Silva
Ano Início: 2025.2

Ideia: Reunir os códigos em um pacote, tornar público para o instituto e auxiliar os alunos a melhor compreender a lógica de programação resolvendo problemas de cálculo, álgebra e computação.
Apresentar ao instituto futuramente. 

Github: https://github.com/pedroiff0/CalculoNumerico
Paper: 
Documentação:
Tutoriais:

% pip3 install calculonumiff

"""

"""
Sistema de Conversão de Bases - Parte 0 (Teórica)

    Funções:
    - binario_para_decimal(s)
    - decimal_para_binario(n)
    - decimal_para_hexadecimal(n)
    - hexadecimal_para_decimal(s)
    - binario_para_hexadecimal(s)
    - hexadecimal_para_binario(s)
"""

from codigos.bases import (
    dados as dados_bases,
    binario_para_decimal,
    decimal_para_binario,
    decimal_para_hexadecimal,
    hexadecimal_para_decimal,
    binario_para_hexadecimal,
    hexadecimal_para_binario,
)

def menu_bases():
    while True:
        opcao = dados_bases()
        if opcao == '0':
            return
        if opcao == '1':
            s = input("Digite o número binário (ex: 1011): ").strip()
            print(f"Decimal: {binario_para_decimal(s)}")
        elif opcao == '2':
            try:
                n = int(input("Digite o número decimal (inteiro): "))
                print(f"Binário: {decimal_para_binario(n)}")
            except ValueError:
                print("Entrada inválida. Digite um inteiro.")
        elif opcao == '3':
            s = input("Digite o número binário (ex: 1111): ").strip()
            print(f"Hexadecimal: {binario_para_hexadecimal(s)}")
        elif opcao == '4':
            s = input("Digite o número hexadecimal (ex: FE): ").strip()
            print(f"Binário: {hexadecimal_para_binario(s)}")
        elif opcao == '5':
            try:
                n = int(input("Digite o número decimal (inteiro): "))
                print(f"Hexadecimal: {decimal_para_hexadecimal(n)}")
            except ValueError:
                print("Entrada inválida. Digite um inteiro.")
        elif opcao == '6':
            s = input("Digite o número hexadecimal (ex: 1A3): ").strip()
            print(f"Decimal: {hexadecimal_para_decimal(s)}")
        else:
            print("Opção inválida. Tente novamente.")


"""

Sistemas Lineares - Parte 1

    Funções:
    - eliminacao_gauss_sem_pivotamento(A, b)
    - eliminacao_gauss_com_pivotamento(A, b)
    - lu_sem_pivot(A,b)
    - lu_com_pivot(A,b)
    - forward_solve(L, b)
    - backward_solve(U, y)
    - calcular_residuo(A, x, b)
    
    Funções Auxiliares:
    - imprimir_sistema_linear()
    - montar_sistema_valores() # (pedir dados ao usuario)
    - exibir_residuo_detalhado(A, x, b)
    - matriz_zeros_manual(n) # opcional
    - multiplicar_matrizes(A, B) # opcional
    - matriz_identidade(n) # opcional
"""

from codigos.sistemaslineares import (
    eliminacao_gauss_sem_pivotamento,
    eliminacao_gauss_com_pivotamento,
    lu_sem_pivot,
    lu_com_pivot,
    montar_sistema_valores,
    forward_solve,
    backward_solve,
    calcular_residuo,
    exibir_residuo_detalhado,
)


def menu_sistemas():
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
                x, Atri, bmod, _ = eliminacao_gauss_sem_pivotamento(A, b) # variavel, a trinangular, b _ era uma opcao para trocar q removi
                if x is None:
                    print("Sistema impossível pelo método sem pivotamento.") # se der algum 0 diagonal, ou encontrar pivo 0.
                    continue
                print("\nSolução pelo método de Gauss sem pivotamento:")
                for var, val in zip(vars, x):
                    print(f"{var} = {val}") # exibir a solução
                exibir_residuo_detalhado(A, x, b) # resíduo mostrando Ax - b = r
            elif opcao == '2':
                x, Atri, bmod = eliminacao_gauss_com_pivotamento(A, b) # variavel, a tringualar, b
                if x is None:
                    print("Sistema impossível pelo método com pivotamento.") # se o pivotamento ainda assim der 0 na diagonal.
                    continue
                print("\nSolução pelo método de Gauss com pivotamento:")
                for var, val in zip(vars, x):
                    print(f"{var} = {val}") # exibir solução
                exibir_residuo_detalhado(A, x, b) # resíduo mostrando Ax - b = r 
            elif opcao == '3':
                L, U = lu_sem_pivot(A,b)
                y = forward_solve(L, b) # resolve em baixo Ly = b
                x = backward_solve(U, y) # resolve em cima = Ux = y
                print("\nSolução pela decomposição LU sem pivotamento:")
                for var, val in zip(vars, x):
                    print(f"{var} = {val}") # exibir solução
                exibir_residuo_detalhado(A, x, b) # resíduo mostrando Ax - b = r
            elif opcao == '4':
                result = lu_com_pivot(A,b)
                if result is None:
                    print("Sistema impossível pela decomposição LU com pivotamento.")
                    continue
                P, L, U = result # P (matriz Identidade), L = Lower, U = Upper
                b_mod = P @ b # operação para multiplicar as duas matrizes 
                y = forward_solve(L, b_mod) # resolve em baixo Ly = b
                x = backward_solve(U, y) # resolve em cima = Ux = y
                print("\nSolução pela decomposição LU com pivotamento:")
                for var, val in zip(vars, x):
                    print(f"{var} = {val}") # exibir solução
                exibir_residuo_detalhado(A, x, b) # resíduo mostrando Ax - b = r
            else:
                print("Opção inválida. Tente novamente.")
        except Exception as e:
            print(f"Erro: {e}")


"""
Interpolações - Parte 2

    Funções:
    - newton_dif_divididas(x, tabela, xp, max_grau=None)
    - gregory_newton_progressivo(x, y, xp, max_grau=None)
    - lagrange_interpol(x, y, xp, max_grau=None)
    - dispositivo_pratico_lagrange(x, y, xp, max_grau=None)
    - calcular_erro(func_str, x_vals, x_interp, grau, valor_interpolado)
    
    Funções Auxiliares:
    - dados_interpolacao()
    - obter_max_grau(n):
    - verifica_espaçamento_uniforme(x, tol=1e-15)
    - tabela_diferencas_divididas(x, y)
    - imprimir_tabela_diferencas_divididas(tabela)
    - tabela_diferencas_finitas(y)
    - imprimir_tabela_diferencas_finitas(tabela)
    - perguntar_erro(x_vals, x_interp, grau, valor_interpolado)
    
"""

from codigos.interpolacoes import (
    newton_dif_divididas,
    gregory_newton_progressivo,
    lagrange_interpol,
    dispositivo_pratico_lagrange,
    dados_interpolacao,
    obter_max_grau,
    verifica_espaçamento_uniforme,
    tabela_diferencas_divididas,
)

def menu_interpolacao():
    while True:
        print("\n=== Interpolações ===")
        print("1 - Newton (diferenças divididas)")
        print("2 - Gregory-Newton progressivo")
        print("3 - Lagrange")
        print("4 - Dispositivo prático Lagrange")
        print("0 - Voltar")
        op = input("Escolha uma opção: ").strip()
        if op == '0':
            return
        try:
            x_vals, y_vals, xp = dados_interpolacao()
        except Exception as e:
            print(f"Erro na leitura dos pontos: {e}")
            continue

        max_grau = obter_max_grau(len(x_vals))

        if op == '1':
            tabela = tabela_diferencas_divididas(x_vals, y_vals)
            resultado = newton_dif_divididas(x_vals, tabela, xp, max_grau)
            print(f"Resultado (Newton): {resultado}")
        elif op == '2':
            uniforme, h = verifica_espaçamento_uniforme(x_vals)
            if not uniforme:
                print("Atenção: pontos não têm espaçamento uniforme. Gregory-Newton pode ser impreciso.")
            resultado = gregory_newton_progressivo(np.array(x_vals), np.array(y_vals), xp, max_grau)
            print(f"Resultado (Gregory-Newton): {resultado}")
        elif op == '3':
            resultado = lagrange_interpol(np.array(x_vals), np.array(y_vals), xp, max_grau)
            print(f"Resultado (Lagrange): {resultado}")
        elif op == '4':
            resultado = dispositivo_pratico_lagrange(np.array(x_vals), np.array(y_vals), xp, max_grau)
            print(f"Resultado (Dispositivo de Lagrange): {resultado}")
        else:
            print("Opção inválida.")

"""
Ajustes de Curvas - Parte 3

    Funções:
    - regressaolinear(x, y) # opcional!
    - regressaolinear_intervalo(x, y) # opcional!
    - minquadrados(x, y)
    - minquadrados_ordem_n_manual(x, y, ordem=1, tabela=True, grafico=True)
    - calcula_chi_e_r2(x, y, b0, b1, n_params=2)
    
    Funções Auxiliares:
    - log_output(message, logfile='log_resultados.txt') # opcional
    - dados() # especificamente  (pode ser para Interpolações e Ajustes de Curvas)
    - tabela_interpolador(x, y, p1x) # opcional
    - tabela_minimos_quadrados(x, y) # opcional

"""

from codigos.ajustecurvasv2 import (
    regressaolinear,
    regressaolinear_intervalo,
    minquadrados,
    dados as dados_ajustes,
)

from codigos.ajustecurvasOrdemn import minquadrados_ordem_n_manual

def menu_ajustes():
    while True:
        print("\n=== Ajustes de Curvas ===")
        print("1 - Regressão linear (método 1)")
        print("2 - Regressão linear por intervalo (método 2)")
        print("3 - Mínimos quadrados (linear)")
        print("4 - Mínimos quadrados (ordem n)")
        print("0 - Voltar")
        op = input("Escolha uma opção: ").strip()
        if op == '0':
            return
        x, y = dados_ajustes()
        if x.size == 0:
            print("Nenhum dado fornecido.")
            continue

        if op == '1':
            regressaolinear(x, y)
        elif op == '2':
            regressaolinear_intervalo(x, y)
        elif op == '3':
            minquadrados(x, y)
        elif op == '4':
            try:
                ordem = int(input("Digite a ordem do polinômio (inteiro >=0): "))
            except ValueError:
                print("Ordem inválida. Usando ordem 1.")
                ordem = 1
            minquadrados_ordem_n_manual(x, y, ordem=ordem)
        else:
            print("Opção inválida.")


"""
Ajustes de Curvas - Parte 3

    Funções:
    - regressaolinear(x, y) # opcional!
    - regressaolinear_intervalo(x, y) # opcional!
    - minquadrados(x, y)
    - minquadrados_ordem_n_manual(x, y, ordem=1, tabela=True, grafico=True)
    - calcula_chi_e_r2(x, y, b0, b1, n_params=2)
    
    Funções Auxiliares:
    - log_output(message, logfile='log_resultados.txt') # opcional
    - dados() # especificamente  (pode ser para Interpolações e Ajustes de Curvas)
    - tabela_interpolador(x, y, p1x) # opcional
    - tabela_minimos_quadrados(x, y) # opcional

"""

from codigos.integracoes import (
    pedir_dados_integral,
    trapezio_composta,
    simpson_1_3_composta,
    simpson_3_8_composta,
    trapezio_tabela,
    simpson_1_3_tabela,
    simpson_3_8_tabela,
    newton_cotes,
)


def menu_integracoes():
    while True:
        print("\n--- MÉTODOS DE INTEGRAÇÃO NUMÉRICA ---")
        print("1 - Regra do Trapézio")
        print("2 - Regra de Simpson 1/3")
        print("3 - Regra de Simpson 3/8")
        print("0 - Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")
        if opcao == '0':
            break

        tabela = input("Deseja inserir dados em tabela (x, y)? (s/n): ").strip().lower() == 's'
        if tabela:
            if opcao == '1':
                trapezio_tabela()
            elif opcao == '2':
                simpson_1_3_tabela()
            elif opcao == '3':
                simpson_3_8_tabela()
            else:
                print("Opção inválida.")
            continue
        
        func, a, b, composta = pedir_dados_integral()
        if func is None:
            continue

        resultado = None
        if opcao == '1':
            if composta:
                resultado = trapezio_composta(func, a, b)
            else:
                resultado = newton_cotes(func, a, b, 1)
        elif opcao == '2':
            if composta:
                resultado = simpson_1_3_composta(func, a, b)
            else:
                resultado = newton_cotes(func, a, b, 2)
        elif opcao == '3':
            if composta:
                resultado = simpson_3_8_composta(func, a, b)
            else:
                resultado = newton_cotes(func, a, b, 3)
        else:
            print("Opção inválida. Tente novamente.")
            continue

        if resultado is not None:
            valor_exato = None
            calc_exata = input("Deseja calcular a integral exata (simbólica)? (s/n): ").strip().lower() == 's'
            if calc_exata:
                x = symbols('x')
                func_sympy = func.replace('math.', '')
                try:
                    funcao = sympify(func_sympy, locals=SYMPY_LOCALS)
                    integral_exata = integrate(funcao, (x, a, b))
                    try:
                        valor_exato = float(integral_exata.evalf())
                    except Exception:
                        valor_exato = float(integral_exata)
                    print(f"\nResultado exato da integral de {func_sympy} de {a} a {b}: {valor_exato}\n")
                    # Se foi pedido o exato e estamos em caso composto, mostra erro relativo (módulo)
                    if composta and valor_exato is not None:
                        try:
                            erro_rel = abs(float(resultado) - float(valor_exato)) / abs(float(valor_exato)) if float(valor_exato) != 0 else float('inf')
                            print(f"Erro relativo (módulo) entre o valor numérico composto e o exato: {erro_rel}\n")
                        except Exception as _:
                            print("Não foi possível calcular o erro relativo.")
                except Exception as e:
                    print("\nErro ao calcular a integral simbolicamente:", e)
            if not composta:
                calc_erro = input("Deseja calcular o erro de truncamento? (s/n): ").strip().lower() == 's'
                if calc_erro:
                    if valor_exato is None:
                        v_str = input("Digite o valor EXATO da integral (analítico): ")
                        try:
                            valor_exato = float(sympify(v_str, locals=SYMPY_LOCALS))
                        except Exception:
                            try:
                                valor_exato = float(v_str)
                            except Exception:
                                print("Valor exato inválido.")
                                valor_exato = None
                    erro = abs(float(valor_exato) - float(resultado))
                    print(f"\nValor exato informado: {valor_exato}")
                    print(f"Resultado numérico: {resultado}")
                    print(f"Erro de truncamento: {erro}\n")

"""
Ajustes de Curvas - Parte 3

    Funções:
    - regressaolinear(x, y) # opcional!
    - regressaolinear_intervalo(x, y) # opcional!
    - minquadrados(x, y)
    - minquadrados_ordem_n_manual(x, y, ordem=1, tabela=True, grafico=True)
    - calcula_chi_e_r2(x, y, b0, b1, n_params=2)
    
    Funções Auxiliares:
    - log_output(message, logfile='log_resultados.txt') # opcional
    - dados() # especificamente  (pode ser para Interpolações e Ajustes de Curvas)
    - tabela_interpolador(x, y, p1x) # opcional
    - tabela_minimos_quadrados(x, y) # opcional

"""

from codigos.EDOs import (
    pedir_dados_edo,
    passos_edo,
    plotar_grafico_edo,
    mostrar_tabela_e_grafico_edo,
    resolver_edo_2ordem,
    runge_kutta,
    executar_runge_kutta,
    runge_kutta_sistema,
    executar_sistema_edos,
)

def menu_edos():
    """
    Submenu interativo para resolver Equações Diferenciais Ordinárias (EDOs).
    Oferece métodos RK1..RK4, sistemas e EDOs de segunda ordem.
    """
    while True:
        print("\n===== MENU DE EQUAÇÕES DIFERENCIAIS =====")
        print("1 - Método de Euler (Runge-Kutta 1ª ordem)")
        print("2 - Método de Runge-Kutta (2ª, 3ª ou 4ª ordem)")
        print("3 - Sistemas de EDOs")
        print("4 - Equações Diferenciais de 2ª Ordem")
        print("0 - Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")
        if opcao == '0':
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


"""
Ajustes de Curvas - Parte 3

    Funções:
    - regressaolinear(x, y) # opcional!
    - regressaolinear_intervalo(x, y) # opcional!
    - minquadrados(x, y)
    - minquadrados_ordem_n_manual(x, y, ordem=1, tabela=True, grafico=True)
    - calcula_chi_e_r2(x, y, b0, b1, n_params=2)
    
    Funções Auxiliares:
    - log_output(message, logfile='log_resultados.txt') # opcional
    - dados() # especificamente  (pode ser para Interpolações e Ajustes de Curvas)
    - tabela_interpolador(x, y, p1x) # opcional
    - tabela_minimos_quadrados(x, y) # opcional

"""

from codigos.raizes import (
    plotar_funcao,
    bissecao,
    newton,
    secante,
    pedir_dados_raizes,
)

def menu_raizes():
    """
    Menu interativo para os métodos de cálculo de raízes (Bisseção, Newton, Secante).
    """
    while True:
        print("\n--- MÉTODOS PARA CÁLCULO DE RAÍZES ---")
        print("1 - Bisseção")
        print("2 - Newton-Raphson (Tangente)")
        print("3 - Secante")
        print("0 - Voltar ao menu principal")

        escolha = input("Escolha o método: ").strip()
        if escolha == '0':
            break
        if escolha == '1':
            func_str, tol, max_iter, params = pedir_dados_raizes('bissecao')
            if func_str is None:
                continue
            a, b = params
            raiz, iters = bissecao(func_str, a, b, tol, max_iter)
            if raiz is not None:
                print(f"\nA raiz encontrada é: {raiz:.6f}")
                print(f"Número total de iterações: {iters}")
                plotar_funcao(func_str, a, b, raiz)
        elif escolha == '2':
            func_str, tol, max_iter, params = pedir_dados_raizes('newton')
            if func_str is None:
                continue
            x0 = params[0]
            raiz, iters = newton(func_str, x0, tol, max_iter)
            if raiz is not None:
                print(f"\nA raiz encontrada é: {raiz:.6f}")
                print(f"Número total de iterações: {iters}")
                plotar_funcao(func_str, x0 - 5, x0 + 5, raiz)
        elif escolha == '3':
            func_str, tol, max_iter, params = pedir_dados_raizes('secante')
            if func_str is None:
                continue
            x0, x1 = params
            raiz, iters = secante(func_str, x0, x1, tol, max_iter)
            if raiz is not None:
                print(f"\nA raiz encontrada é: {raiz:.6f}")
                print(f"Número total de iterações: {iters}")
                plotar_funcao(func_str, min(x0, x1) - 5, max(x0, x1) + 5, raiz)
        else:
            print("Opção inválida.")

def menu_principal():
    """
    Menu principal do pacote de Cálculo Numérico.

    Apresenta as opções principais (Bases, Sistemas, Interpolações, Ajustes  de EDOs, Integração Numérica e Métodos de Raízes). 
    """
    while True:
        print("\n=== Cálculo Numérico - Menu Principal ===")
        print("1 - Conversão de Bases")
        print("2 - Sistemas Lineares")
        print("3 - Interpolações")
        print("4 - Ajustes de Curvas")
        print("5 - Equações Diferenciais (EDOs)")
        print("6 - Integração Numérica")
        print("7 - Métodos de Raízes")
        print("0 - Sair")
        escolha = input("Escolha uma opção: ").strip()
        if escolha == '0':
            print("Saindo...")
            break
        elif escolha == '1':
            menu_bases()
        elif escolha == '2':
            menu_sistemas()
        elif escolha == '3':
            menu_interpolacao()
        elif escolha == '4':
            menu_ajustes()
        elif escolha == '5':
            menu_edos()
        elif escolha == '6':
            menu_integracoes()
        elif escolha == '7':
            menu_raizes()
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    menu_principal()