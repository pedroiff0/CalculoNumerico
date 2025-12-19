Conversões de Bases
====================

Documentação das funções do módulo :mod:`codigos.bases` relacionadas à conversão de bases.

Documentação
-------------

As funções listadas abaixo implementam conversões entre bases numéricas (binário/decimal/hexadecimal). Todas seguem a convenção de entradas simples (strings para representações binárias/hexadecimais e inteiros para conversões de decimal) e levantam exceções quando aplicável.

.. automodule:: codigos.bases
    :members: binario_para_decimal, decimal_para_binario, decimal_para_hexadecimal, hexadecimal_para_decimal, binario_para_hexadecimal, hexadecimal_para_binario
    :noindex:

Exemplo de Uso
--------------

.. literalinclude:: ../tests/exemplos/exemplo_bases.py
    :language: python
    :linenos:

Testes de Integração
--------------------

O teste de integração que valida a opção de conversão de bases está em::

    pytest tests/test_inputs_calcnum.py::test_calcnum_inputs_basic -q

Teste correspondente: :file:`tests/inputs/inputBases.txt`

Testes Unitários (visíveis)
---------------------------

Abaixo está o arquivo de testes unitários para a funcionalidade de bases. Ele é incluído para fácil visualização e referência.

.. literalinclude:: ../tests/test_bases.py
    :language: python
    :linenos:

Links rápidos
-------------

- Teste de integração relacionado: :file:`tests/test_inputs_calcnum.py::test_calcnum_inputs_basic`
- Testes unitários (arquivo): :file:`tests/test_bases.py`
- Página de testes (docs): :doc:`tests/test_bases`