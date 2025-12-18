# Pacote para permitir importações de `codigos.*`
__all__ = ['bases', 'sistemaslineares', 'interpolacoes', 'ajustecurvas', 'integracoes', 'edos', 'raizes', 'calcnum']

# Não importe submódulos aqui para evitar execução desnecessária e problemas de importação
# circulares em ambientes de CI. Submódulos podem ser importados normalmente com
# `from codigos import <modulo>` ou `import codigos.<modulo>` quando necessário.

# O pacote é composto por módulos individuais; mantenha este arquivo simples para tornar a pasta importável.