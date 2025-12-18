def dados():
    print("\n=== Conversor de Bases ===")
    print("1 - Binário para Decimal")
    print("2 - Decimal para Binário")
    print("3 - Binário para Hexadecimal")
    print("4 - Hexadecimal para Binário")
    print("5 - Decimal para Hexadecimal")
    print("6 - Hexadecimal para Decimal")
    print("0 - Sair")
    opcao = input("Escolha a conversão desejada: ")
    return opcao

def binario_para_decimal(bin_str):
    """Converte uma string binária para inteiro decimal.

    Parameters
    ----------
    bin_str : str
        Representação binária (ex.: ``'1011'``).

    Returns
    -------
    int
        Valor decimal correspondente.

    Examples
    --------
    >>> binario_para_decimal('1011')
    11
    """
    decimal = 0
    for i, digito in enumerate(reversed(bin_str)):
        decimal += int(digito) * (2 ** i)
    return decimal

def decimal_para_binario(numDecimal):
    """Converte um inteiro decimal para sua representação binária em string.

    Parameters
    ----------
    numDecimal : int
        Número decimal não-negativo.

    Returns
    -------
    str
        Representação binária (ex.: ``'1011'``).

    Examples
    --------
    >>> decimal_para_binario(11)
    '1011'
    """
    if numDecimal == 0:
        return "0"
    binario = ""
    while numDecimal > 0:
        binario = str(numDecimal % 2) + binario
        numDecimal = numDecimal // 2
    return binario

def decimal_para_hexadecimal(numDecimal):
    """Converte um inteiro decimal para representação hexadecimal (maiúscula).

    Parameters
    ----------
    numDecimal : int
        Número decimal não-negativo.

    Returns
    -------
    str
        Representação hexadecimal (ex.: ``'FE'``).

    Examples
    --------
    >>> decimal_para_hexadecimal(254)
    'FE'
    """
    if numDecimal == 0:
        return "0"
    digitos = "0123456789ABCDEF"
    hexa = ""
    while numDecimal > 0:
        hexa = digitos[numDecimal % 16] + hexa
        numDecimal = numDecimal // 16
    return hexa

def hexadecimal_para_decimal(hex_str):
    """Converte uma string hexadecimal (base 16) para inteiro decimal.

    Parameters
    ----------
    hex_str : str
        Representação hexadecimal (ex.: ``'FE'``).

    Returns
    -------
    int
        Valor decimal correspondente.

    Examples
    --------
    >>> hexadecimal_para_decimal('FE')
    254
    """
    hex_str = hex_str.upper()
    digitos = "0123456789ABCDEF"
    decimal = 0
    for i, digito in enumerate(reversed(hex_str)):
        valor = digitos.index(digito)
        decimal += valor * (16 ** i)
    return decimal

def binario_para_hexadecimal(bin_str):
    """Converte uma string binária para representação hexadecimal.

    Parameters
    ----------
    bin_str : str
        Representação binária.

    Returns
    -------
    str
        Representação hexadecimal em maiúsculas.

    Examples
    --------
    >>> binario_para_hexadecimal('1111')
    'F'
    """
    decimal = binario_para_decimal(bin_str)
    return decimal_para_hexadecimal(decimal)

def hexadecimal_para_binario(hex_str):
    """Converte uma string hexadecimal para representação binária.

    Parameters
    ----------
    hex_str : str
        Representação hexadecimal (ex.: ``'F'``).

    Returns
    -------
    str
        Representação binária (ex.: ``'1111'``).

    Examples
    --------
    >>> hexadecimal_para_binario('F')
    '1111'
    """
    decimal = hexadecimal_para_decimal(hex_str)
    return decimal_para_binario(decimal)

def main():
    while True:
        escolha = dados()
        if escolha == '0':
            print("Encerrando...")
            break
        elif escolha in ['1', '3']:
            valor = input("Digite o valor binário: ").strip()
            if escolha == '1':
                resultado = binario_para_decimal(valor)
                print(f"Binário para Decimal: {resultado}")
            else:
                resultado = binario_para_hexadecimal(valor)
                print(f"Binário para Hexadecimal: {resultado}")
        elif escolha in ['2', '5']:
            valor = int(input("Digite o valor decimal: ").strip())
            if escolha == '2':
                resultado = decimal_para_binario(valor)
                print(f"Decimal para Binário: {resultado}")
            else:
                resultado = decimal_para_hexadecimal(valor)
                print(f"Decimal para Hexadecimal: {resultado}")
        elif escolha in ['4', '6']:
            valor = input("Digite o valor hexadecimal: ").strip()
            if escolha == '4':
                resultado = hexadecimal_para_binario(valor)
                print(f"Hexadecimal para Binário: {resultado}")
            else:
                resultado = hexadecimal_para_decimal(valor)
                print(f"Hexadecimal para Decimal: {resultado}")
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()