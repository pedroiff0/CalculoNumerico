Testes: test_interpolacoes
--------------------------

Testes para `codigos.interpolacoes`.

Cobre:
- Cálculo de diferenças divididas e avaliação de Newton
- Interpolação de Lagrange e dispositivo prático
- Método de diferenças finitas de Gregory-Newton
- Estimativa de erro e verificação de espaçamento
- Comportamentos de verbose/tabela/gráfico e validação de entradas

Conteúdo dos testes: 

.. literalinclude:: ../../tests/test_interpolacoes.py
   :language: python
   :linenos:

Resumo das funções de teste:

- **test_tabela_diferencas_divididas_and_newton**: Verifica a tabela de diferenças divididas e avaliação de Newton.
- **test_lagrange_interpol**: Verifica a interpolação por Lagrange em um ponto simples.
- **test_tabela_diferencas_finitas_and_gregory**: Verifica diferenças finitas e interpolação Gregory-Newton progressiva.
- **test_dispositivo_pratico_lagrange**: Valida o 'dispositivo prático' de Lagrange com dados sintéticos.
- **test_verifica_espaçamento_uniforme_and_calcular_erro**: Testa verificação de espaçamento uniforme e estimativa de erro.
- **test_lagrange_real_data_1**: Testa interpolação de Lagrange com dados reais do exemplo do menu
- **test_newton_real_data_1**: Testa interpolação de Newton com dados reais do exemplo do menu
- **test_dispositivo_pratico_lagrange_real_data**: Testa dispositivo prático de Lagrange com dados de temperatura
- **test_newton_real_data_2**: Testa Newton com 4 pontos
- **test_lagrange_real_data_2**: Testa Lagrange com dados de pressão
- **test_lagrange_real_data_3**: Testa Lagrange com outro conjunto de dados de pressão
- **test_newton_real_data_3**: Testa Newton com valores de x decrescentes
- **test_max_grau_limitation**: Garante que o parâmetro max_grau limita o grau do polinômio
- **test_gregory_newton_real_data**: Testa Gregory-Newton com dados igualmente espaçados
- **test_input_validation_errors**: Verifica que validação de entradas levanta erros apropriados
- **test_verbose_output**: Verifica que verbose=False não produz saída e verbose=True produz saída
- **test_lagrange_verbose_detailed_output**: Verifica saída detalhada em verbose para interpolação de Lagrange
- **test_newton_verbose_detailed_output**: Verifica saída detalhada em verbose para interpolação de Newton
- **test_numpy_array_inputs**: Verifica que as funções aceitam arrays numpy como entrada
- **test_verbose_enables_tables_and_details**: Quando verbose=True, a função imprime passos e tabelas detalhadas.
- **test_invalid_xp_raises**: xp deve ser um número finito.
- **test_max_grau_limits_degree**: Garante que max_grau é limitado a [1, n-1]
