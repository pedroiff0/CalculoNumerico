"""Testes para o módulo `codigos.bases`.

Valida conversões entre representações numéricas: binário, decimal e hexadecimal.
"""

from codigos import bases


def test_binario_decimal_roundtrip():
    """Valida a conversão binário -> decimal e decimal -> binário."""
    assert bases.binario_para_decimal('1011') == 11
    assert bases.decimal_para_binario(11) == '1011'


def test_hexadecimal_roundtrip():
    """Valida a conversão decimal -> hexadecimal e hexadecimal -> decimal."""
    assert bases.decimal_para_hexadecimal(254) == 'FE'
    assert bases.hexadecimal_para_decimal('FE') == 254


def test_binario_hexadecimal():
    """Valida a conversão direta binário <-> hexadecimal."""
    assert bases.binario_para_hexadecimal('1111') == 'F'
    assert bases.hexadecimal_para_binario('F') == '1111'
