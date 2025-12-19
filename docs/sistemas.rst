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

Coberto pelos seguintes testes:

- **Teste global**: ``pytest -q`` (roda todos os testes do projeto)
- **Teste de calcnum**: ``pytest tests/test_inputs_calcnum.py::test_calcnum_inputs_basic -q`` (valida integração via menu principal)
- **Teste individual**: ``pytest tests/test_sistemaslineares.py -v`` (testes específicos do módulo)

Teste correspondente: :file:`tests/inputs/inputSistemas.txt`

Testes Unitários (visíveis)
---------------------------

:doc:`tests/test_sistemaslineares`

Links rápidos
-------------

- Teste de integração relacionado: :file:`tests/test_inputs_calcnum.py::test_calcnum_inputs_basic`
- Testes unitários (arquivo): :file:`tests/test_sistemaslineares.py`
- Página de testes (docs): :doc:`tests/test_sistemaslineares`
