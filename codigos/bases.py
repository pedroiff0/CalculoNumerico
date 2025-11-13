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
    """
    Cálculo: Soma dos dígitos binários multiplicados pelas potências de 2 conforme posição.
    Para cada dígito (d) na posição i (contando da direita para esquerda), soma-se d * 2^i.
    
    Exemplo: bin_str = '1011'
    1*2^0 + 1*2^1 + 0*2^2 + 1*2^3 = 1 + 2 + 0 + 8 = 11 decimal
    """
    decimal = 0
    for i, digito in enumerate(reversed(bin_str)):
        decimal += int(digito) * (2 ** i)
    return decimal

def decimal_para_binario(numDecimal):
    """
    Cálculo: Divisões sucessivas por 2, coletando os restos.
    O número decimal é dividido por 2 repetidamente, e os restos (0 ou 1) formam o número binário do último para o primeiro.
    
    Exemplo: numDecimal = 11
    11/2 = 5 resto 1
    5/2 = 2 resto 1
    2/2 = 1 resto 0
    1/2 = 0 resto 1
    Lendo os restos de baixo para cima: 1011 binário
    """
    if numDecimal == 0:
        return "0"
    binario = ""
    while numDecimal > 0:
        binario = str(numDecimal % 2) + binario
        numDecimal = numDecimal // 2
    return binario

def decimal_para_hexadecimal(numDecimal):
    """
    Cálculo: Divisões sucessivas por 16, coletando restos que representam dígitos hexadecimais.
    Usa tabela '0123456789ABCDEF' para representar restos >= 10.
    
    Exemplo: numDecimal = 254
    254/16 = 15 resto 14 (E)
    15/16 = 0 resto 15 (F)
    Resultado: FE hexadecimal
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
    """
    Cálculo: Soma dos dígitos hexadecimais multiplicados por potências de 16 conforme posição.
    Cada caracter é convertido para seu valor decimal e multiplicado por 16^i (contando da direita para esquerda).
    
    Exemplo: hex_str = '1A3'
    3*16^0 + 10*16^1 + 1*16^2 = 3 + 160 + 256 = 419 decimal
    """
    hex_str = hex_str.upper()
    digitos = "0123456789ABCDEF"
    decimal = 0
    for i, digito in enumerate(reversed(hex_str)):
        valor = digitos.index(digito)
        decimal += valor * (16 ** i)
    return decimal

def binario_para_hexadecimal(bin_str):
    """
    Cálculo: Primeiro converte binário para decimal;
    Depois converte o decimal para hexadecimal usando o método das divisões sucessivas.
    
    Exemplo: bin_str = '1111'
    Binário para decimal: 15
    Decimal para hexadecimal: F
    """
    decimal = binario_para_decimal(bin_str)
    return decimal_para_hexadecimal(decimal)

def hexadecimal_para_binario(hex_str):
    """
    Cálculo: Primeiro converte hexadecimal para decimal;
    Depois converte o decimal para binário usando divisões sucessivas por 2.
    
    Exemplo: hex_str = 'F'
    Hexadecimal para decimal: 15
    Decimal para binário: 1111
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