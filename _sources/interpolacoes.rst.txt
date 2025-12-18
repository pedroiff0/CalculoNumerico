Interpolações
==============

Funções do módulo :mod:`codigos.interpolacoes` para interpolação (Newton, Lagrange, Gregory-Newton).

Documentação da API
--------------------

.. automodule:: codigos.interpolacoes
    :members:
    :noindex:

Exemplo de Uso
--------------

.. literalinclude:: ../tests/exemplos/exemplo_interpolacoes.py
    :language: python
    :linenos:

Testes de Integração
--------------------

Coberto pelo caso de integração em::

    pytest tests/test_inputs_calcnum.py::test_calcnum_inputs_basic -q

Teste correspondente: :file:`tests/inputs/inputInterpolacoes.txt`

Testes Unitários (visíveis)
---------------------------

Abaixo estão os testes unitários para as funções de interpolação, incluídos para referência rápida.

.. literalinclude:: ../tests/test_interpolacoes.py
    :language: python
    :linenos:

Links rápidos
-------------

- Teste de integração relacionado: :file:`tests/test_inputs_calcnum.py::test_calcnum_inputs_basic`
- Testes unitários: :file:`tests/test_interpolacoes.py`