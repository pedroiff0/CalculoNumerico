Testes: test_sistemaslineares
-----------------------------

_Sem docstring de módulo._

Conteúdo dos testes: 

.. literalinclude:: ../../tests/test_sistemaslineares.py
   :language: python
   :linenos:

Resumo das funções de teste:

- **test_eliminacao_sem_pivotamento_basic**: Verifica solução de um sistema 2x2 pelo método de Gauss sem pivotamento.
- **test_eliminacao_sem_pivotamento_pivo_zero**: Garante que o método sem pivotamento detecta pivô zero e retorna falha.
- **test_eliminacao_com_pivotamento_basic**: Verifica que a eliminação com pivotamento resolve sistemas que
- **test_lu_sem_pivot_reconstructs_A**: Verifica que a decomposição LU sem pivotamento reconstrói A (L@U == A).
- **test_lu_com_pivot_reconstructs_PA**: Verifica que para LU com pivotamento vale P @ A == L @ U.
- **test_calcular_residuo_zero_for_exact_solution**: Garante que o resíduo r = b - A x é zero quando x é solução exata.
- **test_eliminacao_sem_pivotamento_flag_error**: Verifica que a função sinaliza erro (flag True) quando detecta pivô zero.
- **test_eliminacao_com_pivotamento_impossible**: Caso degenerado: matriz nula deve ser marcada como impossível pelo método.
- **test_forward_solve_basic**: Testa substituição progressiva (forward solve) para uma L triangular inferior.
- **test_backward_solve_basic**: Testa substituição regressiva (backward solve) para uma U triangular superior.
- **test_lu_sem_pivot_zero_pivot_raises**: Verifica que LU sem pivotamento lança ZeroDivisionError quando pivô é zero.
- **test_gauss_com_pivotamento_example_1**: Exemplo realista (3x3) testando eliminação com pivotamento.
- **test_gauss_sem_pivotamento_example_2**: Exemplo 3x3 testando eliminação sem pivotamento retorna solução correta.
- **test_lu_sem_pivot_example_3**: Outro exemplo 3x3 verificando LU sem pivotamento e solução resultante.
- **test_gauss_sem_pivotamento_example_4**: Exemplo 3x3 com resultados conhecidos para validação do método sem pivotamento.
- **test_gauss_com_pivotamento_5x5**: Caso 5x5 retirado do conjunto de exemplos interativos, valida convergência.
- **test_input_validation_non_square_A**: Validação: matriz não quadrada deve levantar ValueError.
- **test_input_validation_b_wrong_shape**: Validação: vetor b com tamanho incompatível deve levantar ValueError.
- **test_input_validation_b_not_1d**: Validação: vetor b com dimensões incorretas (2D) deve levantar ValueError.
- **test_montar_sistema_valores_eof**: Se ocorrer EOF durante a leitura interativa, a função retorna None.
