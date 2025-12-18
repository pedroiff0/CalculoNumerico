Métodos de Raízes
=================

Funções do módulo :mod:`codigos.raizes` para cálculo de raízes (Bisseção, Newton, Secante).

Documentação
------------

.. automodule:: codigos.raizes
    :members: bissecao, newton, secante, pedir_dados_raizes
    :noindex:

Exemplo de Uso
--------------

.. literalinclude:: ../tests/examples/simple_root_find.py
    :language: python
    :linenos:

Testes de Integração
--------------------

Coberto pelo caso de integração em::

    pytest tests/test_inputs_calcnum.py::test_calcnum_inputs_basic -q

Teste correspondente: :file:`tests/inputs/inputRaizes.txt`

Testes Unitários (visíveis)
---------------------------

.. literalinclude:: ../tests/test_raizes.py
    :language: python
    :linenos:

Links rápidos
-------------

- Testes unitários: :file:`tests/test_raizes.py`