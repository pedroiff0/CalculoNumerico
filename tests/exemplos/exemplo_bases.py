"""Exemplo: uso das conversões de bases em codigos.bases"""
from codigos import bases

if __name__ == '__main__':
    print('1011 ->', bases.binario_para_decimal('1011'))
    print('11 ->', bases.decimal_para_binario(11))
    print('254 ->', bases.decimal_para_hexadecimal(254))
    print('FE ->', bases.hexadecimal_para_decimal('FE'))
