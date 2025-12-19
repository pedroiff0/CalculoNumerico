Ajustes de Curvas
==================

Funções do módulo :mod:`codigos.ajustecurvas` para ajustes de curvas e estatísticas.

Características Implementadas
-----------------------------

O módulo ``codigos/ajustecurvas.py`` implementa métodos robustos para ajuste de curvas com as seguintes características:

- **Validação de Entrada**: Todas as funções validam entradas usando ``_validate_curve_fitting_inputs()``
- **Parâmetros Consistentes**: Todas as funções principais seguem a assinatura ``(x, y, ..., verbose=True, tabela=None, grafico=None)``
- **Controle de Saída**:
  - ``verbose=True`` controla impressão de resultados
  - ``tabela=None`` usa variável global ou padrão ``True`` para exibir tabelas
  - ``grafico=None`` usa variável global ou padrão ``True`` para exibir gráficos
- **Tratamento de Erros**: Validação robusta com mensagens de erro informativas
- **Métodos Implementados**:
  - Regressão linear por pontos selecionados
  - Regressão linear por intervalo
  - Mínimos quadrados (linear)
  - Mínimos quadrados polinomial (ordem n)
- **Métricas Estatísticas**: Cálculo de R², Chi² ajustado, desvios e resíduos
- **Interface Interativa**: Função ``dados()`` para entrada de dados com validação
- **Testes Abrangentes**: 15+ testes cobrindo casos normais e de erro

Documentação
------------

As funções abaixo implementam métodos de ajuste (regressão linear, mínimos quadrados
ordem n, estatísticas de ajuste e utilitários de tabela). Todas aceitam ``numpy.ndarray``
como entrada e retornam estruturas numpy para integração simples com outras rotinas.

.. automodule:: codigos.ajustecurvas
    :members: minquadrados, calcula_chi_e_r2, tabela_minimos_quadrados, regressaolinear, regressaolinear_intervalo, dados
    :noindex:

Exemplo de Uso
--------------

.. literalinclude:: ../tests/exemplos/exemplo_ajuste_curvas.py
    :language: python
    :linenos:

Testes de Integração
--------------------

Coberto pelos seguintes testes:

- **Teste global**: ``pytest -q`` (roda todos os testes do projeto)
- **Teste de calcnum**: ``pytest tests/test_inputs_calcnum.py::test_calcnum_inputs_basic -q`` (valida integração via menu principal)
- **Teste individual**: ``pytest tests/test_ajustecurvas.py -v`` (testes específicos do módulo)

Teste correspondente: :file:`tests/inputs/inputAjustes.txt`

Testes Unitários (visíveis)
---------------------------

:doc:`tests/test_ajustecurvas`

Links rápidos
-------------

- Teste de integração relacionado: :file:`tests/test_inputs_calcnum.py::test_calcnum_inputs_basic`
- Testes unitários (arquivo): :file:`tests/test_ajustecurvas.py`
- Página de testes (docs): :doc:`tests/test_ajustecurvas`