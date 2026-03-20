# Guia de Cálculo Numérico

Este repositório contém um guia completo de cálculo numérico com implementações em Python, formatado como um livro LaTeX profissional.

## Estrutura do Projeto

```
guia/
├── latex/              # Arquivos LaTeX principais
│   ├── guia.cls       # Classe LaTeX personalizada
│   ├── config.sty     # Configurações gerais
│   ├── estilos.sty    # Estilos específicos
│   ├── main.tex       # Arquivo principal do livro
│   └── slides.tex     # Apresentações Beamer
├── capitulos/         # Capítulos do livro
│   └── intro.tex      # Introdução
├── frontmatter/       # Elementos pré-textuais
│   └── capa.tex       # Capa do livro
├── backmatter/        # Elementos pós-textuais
│   └── apendices.tex  # Apêndices (a criar)
├── biblio.bib         # Referências bibliográficas
├── figs/              # Figuras e imagens
├── Makefile          # Sistema de compilação
└── README_guia.md    # Este arquivo
```

## Pré-requisitos

### LaTeX
- LaTeX completo (TeX Live, MiKTeX ou MacTeX)
- Pacotes necessários:
  - `minted` (para highlighting de código Python)
  - `abnt` (estilo bibliográfico brasileiro)
  - `beamer` (para slides)
  - `geometry`, `hyperref`, `amsmath`, etc.

### Python
- Python 3.6+
- Pygments (para minted): `pip install Pygments`

### Instalação de dependências no macOS

```bash
# Instalar MacTeX (se não tiver)
brew install --cask mactex

# Instalar pygments
pip install Pygments

# Verificar instalação
make check-deps
```

## Compilação

### Compilar o livro completo
```bash
make book
```
Gera `guia_calculo_numerico.pdf`

### Compilar apenas os slides
```bash
make slides
```
Gera `guia_slides.pdf`

### Compilar tudo
```bash
make all
```

### Limpar arquivos auxiliares
```bash
make clean
```

### Limpar tudo (incluindo PDFs)
```bash
make clean-all
```

## Estrutura dos Capítulos

O livro está organizado nos seguintes capítulos:

1. **Introdução** - Conceitos básicos e fundamentos
2. **Fundamentos** - Análise de erros e conceitos matemáticos
3. **Raízes de Equações** - Métodos para encontrar raízes
4. **Sistemas Lineares** - Resolução de sistemas de equações
5. **Interpolação** - Aproximação de funções
6. **Ajuste de Curvas** - Regressão e ajuste de modelos
7. **Integração Numérica** - Cálculo aproximado de integrais
8. **Equações Diferenciais Ordinárias** - Métodos para EDOs

## Adicionando Novo Conteúdo

### Novo Capítulo
1. Criar arquivo `capitulos/nome_capitulo.tex`
2. Adicionar entrada no `main.tex`:
   ```latex
   \input{../capitulos/nome_capitulo}
   ```

### Código Python
Use o ambiente minted para incluir código Python:

```latex
\begin{minted}{python}
def exemplo():
    return "Olá, mundo!"
\end{minted}
```

### Referências
Adicione entradas no arquivo `biblio.bib` seguindo o formato ABNT.

## Integração com Código Python

Os códigos Python estão localizados em `../codigos/`. Para incluir trechos específicos:

```latex
\inputminted[python]{../codigos/raizes.py}
```

## Personalização

### Classe LaTeX (`guia.cls`)
- Baseada em `book.cls`
- Suporte a português brasileiro
- Configurações de geometria otimizadas
- Integração com minted para código Python

### Estilos (`estilos.sty`)
- Definições de teoremas, lemas, etc.
- Configurações de hyperref
- Estilos para algoritmos

### Configurações (`config.sty`)
- Pacotes matemáticos (AMS)
- Suporte a figuras e tabelas
- Índices e glossário

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Contato

Para dúvidas ou sugestões, abra uma issue no GitHub.