"""Exemplo simples de uso: encontrar raiz com bisseção"""

from codigos import raizes

if __name__ == "__main__":
    raiz, iters = raizes.bissecao("x**2 - 4", 0, 3, 1e-8, 100)
    print(f"Raiz encontrada: {raiz} (iteração {iters})")
