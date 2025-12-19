Testes: test_ajustecurvas
-------------------------

Testes para o módulo `codigos.ajustecurvas`.

Cobre mínimos quadrados (linear e ordem n), cálculo de Chi²/R², validações
básicas e execução silenciosa (verbose=False).

Conteúdo dos testes: 

.. literalinclude:: ../../tests/test_ajustecurvas.py
   :language: python
   :linenos:

Resumo das funções de teste:

- **test_calcula_chi_e_r2_perfect_linear**: Verifica que métricas (Desvio, Chi², R²) indicam ajuste perfeito para reta exata.
- **test_minquadrados_coefficients**: Verifica que o cálculo de coeficientes por fórmula produz R² ≈ 1 em dados perfeitos.
- **test_tabela_minimos_quadrados_runs_without_error**: Garante que a função de impressão de tabela não lança exceções (modo silencioso).
- **test_minquadrados_ordem_n_quadratic**: Ajuste polinomial de ordem 2 recupera coeficientes exatos em dados sintéticos.
- **test_minquadrados_ordem_n_linear**: Ajuste linear recupera coeficientes exatos em dados sintéticos.
- **test_minquadrados_ordem_n_cubic**: Ajuste cúbico recupera coeficientes exatos em dados sintéticos.
- **test_calcula_chi_e_r2_imperfect_fit**: Dados não perfeitos devem resultar em R² < 1 e Chi² > 0.
- **test_minquadrados_silent**: Verifica que minquadrados executa sem imprimir em modo silencioso.
- **test_input_validation_errors**: Valida que validações de entrada levantam erros apropriados.
- **test_minquadrados_height_weight_dataset**: Exemplo prático: ajuste de altura x peso (aceita execução sem exceção).
- **test_minquadrados_linear_dataset_7_points**: Valida execução em conjunto de 7 pontos (no-throw).
- **test_minquadrados_linear_dataset_8_points**: Valida execução em conjunto de 8 pontos (no-throw).
- **test_minquadrados_linear_dataset_10_points**: Valida execução em conjunto de 10 pontos (no-throw).
- **test_minquadrados_negative_slope_dataset**: Valida execução para conjunto com declive negativo (no-throw).
- **test_minquadrados_ordem_n_quadratic_user_example**: Ajuste polinomial de ordem n em exemplo fornecido pelo usuário.
