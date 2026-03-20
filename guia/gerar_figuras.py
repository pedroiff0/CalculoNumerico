#!/usr/bin/env python3
"""
Script para gerar gráficos de exemplo para o livro de Cálculo Numérico.
Estes gráficos serão incluídos como figuras no documento LaTeX.
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# Criar diretório para as figuras se não existir
output_dir = "guia/figs"
os.makedirs(output_dir, exist_ok=True)

# Configurações de plot
plt.rcParams.update({
    'font.size': 10,
    'axes.linewidth': 1.0,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.figsize': (6, 4),
    'figure.dpi': 150
})

def gerar_grafico_interpolacao():
    """Gera gráfico de exemplo de interpolação polinomial."""
    # Pontos de dados
    x_data = np.array([0, 1, 2, 3, 4])
    y_data = np.array([0, 1, 4, 9, 16])  # x^2

    # Pontos para interpolação
    x_interp = np.linspace(0, 4, 100)
    y_interp = x_interp**2  # Função exata x^2

    plt.figure(figsize=(6, 4))
    plt.plot(x_data, y_data, 'ro', markersize=8, label='Pontos dados')
    plt.plot(x_interp, y_interp, 'b-', linewidth=2, label='Interpolação polinomial')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Exemplo de Interpolação Polinomial')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/interpolacao_exemplo.pdf", bbox_inches='tight')
    plt.close()

def gerar_grafico_ajuste_linear():
    """Gera gráfico de exemplo de ajuste linear."""
    # Dados com ruído
    np.random.seed(42)
    x = np.linspace(0, 10, 20)
    y_true = 2*x + 1
    y = y_true + np.random.normal(0, 1, len(x))

    # Ajuste linear
    coeffs = np.polyfit(x, y, 1)
    y_fit = np.polyval(coeffs, x)

    plt.figure(figsize=(6, 4))
    plt.scatter(x, y, alpha=0.7, label='Dados')
    plt.plot(x, y_true, 'g--', linewidth=2, label='Relação verdadeira')
    plt.plot(x, y_fit, 'r-', linewidth=2, label=f'Ajuste: y = {coeffs[0]:.2f}x + {coeffs[1]:.2f}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Exemplo de Ajuste Linear')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/ajuste_linear_exemplo.pdf", bbox_inches='tight')
    plt.close()

def gerar_grafico_raizes():
    """Gera gráfico mostrando método da bissecção."""
    def f(x):
        return x**3 - x - 2

    x = np.linspace(1, 2, 100)
    y = f(x)

    plt.figure(figsize=(6, 4))
    plt.plot(x, y, 'b-', linewidth=2, label='f(x) = x³ - x - 2')
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    plt.axvline(x=1.769, color='r', linestyle='--', alpha=0.7, label='Raiz ≈ 1.769')
    plt.scatter([1.769], [0], color='r', s=50, zorder=5)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Exemplo: Método da Bissecção')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/bissecção_exemplo.pdf", bbox_inches='tight')
    plt.close()

def gerar_grafico_edo():
    """Gera gráfico de solução de EDO."""
    def euler_method(f, y0, t0, tf, h):
        t_values = [t0]
        y_values = [y0]
        t = t0
        y = y0
        while t < tf:
            y = y + h * f(t, y)
            t = t + h
            t_values.append(t)
            y_values.append(y)
        return np.array(t_values), np.array(y_values)

    # EDO: dy/dt = -2y, solução exata: y = y0 * exp(-2t)
    def f(t, y):
        return -2 * y

    t0, tf, y0, h = 0, 2, 1, 0.1
    t_euler, y_euler = euler_method(f, y0, t0, tf, h)

    # Solução exata
    t_exact = np.linspace(t0, tf, 100)
    y_exact = y0 * np.exp(-2 * t_exact)

    plt.figure(figsize=(6, 4))
    plt.plot(t_exact, y_exact, 'b-', linewidth=2, label='Solução exata')
    plt.plot(t_euler, y_euler, 'ro-', markersize=4, linewidth=1, label='Método de Euler')
    plt.xlabel('t')
    plt.ylabel('y')
    plt.title('Exemplo: Solução de EDO pelo Método de Euler')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/edo_euler_exemplo.pdf", bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    print("Gerando gráficos de exemplo para o livro...")

    gerar_grafico_interpolacao()
    print("✓ Gráfico de interpolação gerado")

    gerar_grafico_ajuste_linear()
    print("✓ Gráfico de ajuste linear gerado")

    gerar_grafico_raizes()
    print("✓ Gráfico de raízes (bissecção) gerado")

    gerar_grafico_edo()
    print("✓ Gráfico de EDO gerado")

    print(f"\nGráficos salvos em: {output_dir}/")
    print("Arquivos gerados:")
    print("- interpolacao_exemplo.pdf")
    print("- ajuste_linear_exemplo.pdf")
    print("- bissecção_exemplo.pdf")
    print("- edo_euler_exemplo.pdf")