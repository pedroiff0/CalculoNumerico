Equações Diferenciais Ordinárias (EDOs)
=======================================

Esta página descreve as funções disponíveis em :mod:`codigos.EDOs` para resolver
EDOs escalares e sistemas por métodos de Runge–Kutta (RK).

Seções
------

Documentação da API
-------------------

.. automodule:: codigos.EDOs
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:

Exemplo de Uso
--------------

.. literalinclude:: ../tests/examples/edo_example.py
    :language: python
    :linenos:

Testes de Integração
--------------------

Coberto pelo caso de integração em::

    pytest tests/test_inputs_calcnum.py::test_calcnum_inputs_basic -q

Teste correspondente: :file:`tests/inputs/inputEDOS.txt`

Testes Unitários (visíveis)
---------------------------

.. literalinclude:: ../tests/test_edos.py
    :language: python
    :linenos:

.. literalinclude:: ../tests/test_edos_extra.py
    :language: python
    :linenos:

Links rápidos
-------------

- Testes relacionados: :file:`tests/test_edos.py`, :file:`tests/test_edos_extra.py`