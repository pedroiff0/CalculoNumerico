Sistemas Lineares
==================

Documentação das funções do módulo :mod:`codigos.sistemaslineares` para montagem e
resolução de sistemas lineares (Eliminação de Gauss, Pivotamento, Decomposição LU,
forward/backward solves e cálculo de residuo).

Documentação
------------

As funções listadas abaixo implementam métodos clássicos para resolver sistemas
lineares e utilitários de inspeção/depuração. Estão escritas para aceitar e
retornar objetos do tipo ``numpy.ndarray``.

.. automodule:: codigos.sistemaslineares
    :members: eliminacao_gauss_sem_pivotamento, eliminacao_gauss_com_pivotamento, lu_sem_pivot, lu_com_pivot, forward_solve, backward_solve, calcular_residuo, exibir_residuo_detalhado, montar_sistema_valores
    :noindex:

Exemplo de Uso
--------------

.. literalinclude:: ../tests/exemplos/exemplo_resolver_sistema.py
    :language: python
    :linenos:

Testes de Integração
--------------------

O teste de integração que valida a opção de sistemas no menu principal é::

    pytest tests/test_inputs_calcnum.py::test_calcnum_inputs_basic -q

Teste correspondente: :file:`tests/inputs/inputSistemas.txt`

Testes Unitários (visíveis)
---------------------------

Abaixo estão os testes unitários para as funções de sistemas. Eles são incluídos
para referência e para facilitar revisão rápida do comportamento implementado.

.. literalinclude:: ../tests/test_sistemaslineares.py
    :language: python
    :linenos:

Links rápidos
-------------

- Teste de integração relacionado: :file:`tests/test_inputs_calcnum.py::test_calcnum_inputs_basic`
- Testes unitários: :file:`tests/test_sistemaslineares.py`, :file:`tests/test_calcnum_linear_solve.py`
