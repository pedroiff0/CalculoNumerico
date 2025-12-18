"""Exemplo: integrações numéricas simples"""
from codigos import integracoes as ig

if __name__ == '__main__':
    # Evita prompts interativos; usa newton_cotes simples (não composta) para exemplos não interativos
    res_trap = ig.newton_cotes('x', 0.0, 1.0, 1)
    print('Trapézio (x) [0,1] ->', res_trap)
    res_simp = ig.newton_cotes('x**2', 0.0, 1.0, 2)
    print('Simpson 1/3 (x**2) [0,1] ->', res_simp)
