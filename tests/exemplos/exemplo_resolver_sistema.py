"""Exemplo: resolver sistema linear via LU e verificações."""

import numpy as np
from codigos import sistemaslineares as sl


if __name__ == '__main__':
    A = np.array([[4.0, 3.0], [6.0, 3.0]])
    b = np.array([10.0, 12.0])
    P, L, U = sl.lu_com_pivot(A, np.zeros(2))
    b_mod = P @ b
    y = sl.forward_solve(L, b_mod)
    x = sl.backward_solve(U, y)
    print("Solução encontrada:", x)
    print("Resíduo:", sl.calcular_residuo(A, x, b))
