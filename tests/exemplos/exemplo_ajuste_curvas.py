"""Exemplo: ajuste de curva linear simples (ajustecurvas)"""
import numpy as np
from codigos import ajustecurvas as ac

if __name__ == '__main__':
    # Dados de exemplo
    x = np.array([0.0, 1.0, 2.0])
    y = 1.0 + 2.0 * x  # y = 1 + 2x

    print("=== Exemplo de Ajuste de Curvas ===")
    print("Dados: x =", x)
    print("Dados: y =", y)
    print("Função esperada: y = 1 + 2x")
    print()

    # Ajuste com saída controlada
    print("1. Ajuste com tabelas e gráficos desabilitados:")
    ac.minquadrados(x, y, verbose=True, tabela=False, grafico=False)

    print("\n2. Cálculo de estatísticas:")
    stats = ac.calcula_chi_e_r2(x, y, b0=1.0, b1=2.0, n_params=2, verbose=False)
    print(f"R² = {stats['R2']:.6f} (esperado: 1.0 para ajuste perfeito)")
    print(f"Chi² ajustado = {stats['Chi2']:.6f}")
    print(f"Desvio (SQRes) = {stats['Desvio']:.6f}")

    print("\n3. Exemplo com dados reais (altura vs peso):")
    # Exemplo com dados reais
    x_altura = np.array([150, 160, 170, 180, 190])  # cm
    y_peso = np.array([50, 60, 65, 75, 85])  # kg
    ac.minquadrados(x_altura, y_peso, verbose=True, tabela=False, grafico=False)