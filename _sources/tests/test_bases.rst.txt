Testes: test_bases
------------------

Testes para o módulo `codigos.bases`.

Valida conversões entre representações numéricas: binário, decimal e hexadecimal.

Conteúdo dos testes: 

.. literalinclude:: ../../tests/test_bases.py
   :language: python
   :linenos:

Resumo das funções de teste:

- **test_binario_decimal_roundtrip**: Valida a conversão binário -> decimal e decimal -> binário.
- **test_hexadecimal_roundtrip**: Valida a conversão decimal -> hexadecimal e hexadecimal -> decimal.
- **test_binario_hexadecimal**: Valida a conversão direta binário <-> hexadecimal.
