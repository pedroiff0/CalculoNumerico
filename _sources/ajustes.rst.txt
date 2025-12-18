Ajustes de Curvas
==================

Funções do módulo :mod:`codigos.ajustecurvas` para ajustes de curvas e estatísticas.

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

Coberto pelo caso de integração em::

    pytest tests/test_inputs_calcnum.py::test_calcnum_inputs_basic -q

Teste correspondente: :file:`tests/inputs/inputAjustes.txt`

Testes Unitários (visíveis)
---------------------------

Abaixo estão os testes unitários para Ajustes de Curvas.

.. literalinclude:: ../tests/test_ajustecurvas.py
    :language: python
    :linenos:

Links rápidos
-------------

- Teste de integração relacionado: :file:`tests/test_inputs_calcnum.py::test_calcnum_inputs_basic`
- Testes unitários: :file:`tests/test_ajustecurvas.py`