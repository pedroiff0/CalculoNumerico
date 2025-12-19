"""
Constantes compartilhadas entre módulos.

Este módulo centraliza constantes e configurações comuns usadas
em múltiplos módulos do projeto de Cálculo Numérico.

Author: Pedro Henrique Rocha de Andrade
Date: Dezembro 2025
"""

from sympy import sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, exp, sqrt, log, Abs, pi, E
import math

# Mapeamento padrão para uso com sympify (padroniza nomes de funções/constantes)
SYMPY_LOCALS = {
    'sin': sin, 'cos': cos, 'tan': tan,
    'asin': asin, 'acos': acos, 'atan': atan,
    'sinh': sinh, 'cosh': cosh, 'tanh': tanh,
    'exp': exp, 'sqrt': sqrt, 'log': log, 'abs': Abs,
    'pi': pi, 'e': E, 'E': E
}

# mapa seguro com funções do math (para uso em fallbacks com eval)
SAFE_MATH = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}

# Configurações padrão para plotagem
PLOT_CONFIG = {
    'figsize': (10, 6),
    'dpi': 100,
    'linewidth': 2,
    'markersize': 4,
    'fontsize': 12
}

# Tolerâncias numéricas padrão
TOLERANCIAS = {
    'zero': 1e-12,
    'igualdade': 1e-10,
    'convergencia': 1e-6,
    'integral': 1e-4
}

# Configurações de métodos numéricos
METODOS_CONFIG = {
    'max_iter': 1000,
    'max_subintervals': 10000,
    'default_h': 0.01,
    'min_h': 1e-12,
    'max_h': 1.0
}