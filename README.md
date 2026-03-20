<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://img.shields.io/badge/🔢-Cálculo%20Numérico-blue?style=for-the-badge&logo=python&logoColor=white" alt="Cálculo Numérico"></a>
</p>
<h3 align="center">Cálculo Numérico</h3>

<div align="center">

[![CI](https://github.com/pedroiff0/CalculoNumerico/actions/workflows/ci.yml/badge.svg)](https://github.com/pedroiff0/CalculoNumerico/actions/workflows/ci.yml)
[![Documentation](https://github.com/pedroiff0/CalculoNumerico/actions/workflows/docs.yml/badge.svg)](https://github.com/pedroiff0/CalculoNumerico/actions/workflows/docs.yml)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](/LICENSE)

</div>

---

<p align="center"> Repostiório de Códigos da Disciplina de Cálculo Numérico - 2025.2
    <br> 
</p>

## 📝 Sumário

- [Sobre](#sobre)
- [Como rodar?](#como_rodar)
- [Requisitos](#requisitos)
- [📚 Documentação](#-documentação)
- [📖 Guia LaTeX](#-guia-de-cálculo-numérico-latex)
- [✅ Testes](#-testes)
- [🚀 CI/CD](#-cicd)
- [📊 Cobertura](#-cobertura)
- [🤝 Contribuição](#-contribuição)
- [📄 Licença](#-licença)
- [Autores](#autores)
## 🧐 Sobre <a name = "sobre"></a>

Este repositório contém a implementação completa dos algoritmos estudados na disciplina de **Cálculo Numérico** do semestre 2025.2, desenvolvida como projeto acadêmico.

### 📋 Informações Acadêmicas

- **Disciplina**: Cálculo Numérico
- **Semestre**: 2025.2
- **Professor**: Rodrigo Lacerda da Silva
- **Aluno**: Pedro Henrique Rocha de Andrade
- **Curso**: Bacharelado em Engenharia de Computação
- **Instituição**: Instituto Federal Fluminense - Campus Bom Jesus do Itabapoana
- **Período**: Setembro/2025 à Março/2026
- **Local**: Bom Jesus do Itabapoana - RJ

### 🎯 Objetivos do Projeto

- Implementar algoritmos numéricos fundamentais em Python
- Desenvolver uma biblioteca robusta e bem testada
- Criar documentação técnica completa e acessível
- Aplicar boas práticas de desenvolvimento de software
- Demonstrar aplicações práticas dos métodos numéricos

### 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.8+
- **Bibliotecas**: NumPy, SymPy, Matplotlib, SciPy
- **Testes**: pytest com 96 testes unitários
- **Documentação**: Sphinx com reStructuredText
- **CI/CD**: GitHub Actions
- **Controle de Versão**: Git

### 📊 Cobertura da Disciplina

A implementação cobre todos os tópicos principais da ementa, incluindo:

### 📚 Conteúdo Programático

<ol>
        <li>Números Binários e Análise de Erros
            <ol>
                <li>✅ Representação de números em diversas bases</li>
                <li>✅ Conversão de números nos sistemas decimal e binário</li>
                <li>✅ Aritmética de ponto flutuante</li>
                <li>✅ Erros absolutos e relativos</li>
                <li>✅ Erros de arredondamento e truncamento em um sistema de aritmética de ponto flutuante</li>
            </ol>
        </li>
        <li>Solução de Equações não Lineares
            <ol>
                <li>✅ Isolamento de raízes, refinamento e critérios de parada</li>
                <li>✅ Método da bisseção</li>
                <li>✅ Método do ponto fixo</li>
                <li>✅ Método de Newton-Raphson</li>
                <li>✅ Método da secante</li>
                <li>✅ Comparação entre os métodos</li>
            </ol>
        </li>
        <li>Interpolação
            <ol>
                <li>✅ Interpolação polinomial</li>
                <li>✅ Formas de se obter o polinômio interpolador: resolução do sistema linear, forma de Lagrange e forma de Newton</li>
                <li>✅ Estudo do erro na interpolação</li>
                <li>✅ Fenômeno de Runge</li>
                <li>✅ Funções spline: spline linear interpolante e spline cúbica interpolante</li>
            </ol>
        </li>
        <li>Ajuste de Curvas
            <ol>
                <li>✅ Caso discreto</li>
                <li>✅ Caso contínuo</li>
                <li>✅ Método dos quadrados mínimos</li>
                <li>✅ Caso não linear</li>
            </ol>
        </li>
        <li>Integração Numérica
            <ol>
                <li>✅ Regra dos trapézios</li>
                <li>✅ Regra dos trapézios repetida</li>
                <li>✅ Regra 1/3 de Simpson</li>
                <li>✅ Regra 1/3 de Simpson repetida</li>
                <li>✅ Teorema geral do erro</li>
            </ol>
        </li>
        <li>Soluções Numéricas de Equações Diferenciais Ordinárias
            <ol>
                <li>✅ Problemas de valor inicial</li>
                <li>✅ Método de Euler, métodos de série de Taylor</li>
                <li>✅ Métodos de Runge-Kutta de 2.ª ordem</li>
                <li>✅ Métodos de Runge-Kutta de ordens superiores</li>
                <li>✅ Equações de ordem superior, problemas de valor de contorno</li>
                <li>✅ Método das diferenças finitas</li>
            </ol>
        </li>
## 📁 Estrutura do Projeto

```
calculoNumerico/
├── codigos/                    # Módulos principais
│   ├── bases.py               # Conversões de bases numéricas
│   ├── sistemaslineares.py    # Resolução de sistemas lineares
│   ├── interpolacoes.py       # Interpolação polinomial
│   ├── ajustecurvas.py        # Ajuste de curvas (mínimos quadrados)
│   ├── integracoes.py         # Integração numérica
│   ├── edos.py                # Equações diferenciais ordinárias
│   ├── raizes.py              # Métodos de busca de raízes
│   ├── calcnum.py             # Menu principal interativo
│   └── ...
├── tests/                     # Testes unitários
│   ├── test_*.py             # Testes por módulo
│   ├── exemplos/             # Exemplos de uso
│   └── inputs/               # Arquivos de entrada para testes
├── docs/                      # Documentação Sphinx
│   ├── _build/               # Documentação compilada
│   ├── scripts/              # Scripts para geração de docs
│   ├── tests/                # Páginas de testes individuais
│   └── *.rst                 # Arquivos reStructuredText
├── guia/          # Livro Guia em LaTeX
│   ├── tarefas/               # Tarefas da disciplina
│   ├── solucoes/               # Soluções das tarefas
└── README.md                 # Este arquivo
```

### Prerequisitos

```
Python 3.8+
```

### Instalando

Instale o pacote diretamente do repositório:

```bash
pip install git+https://github.com/pedroiff0/CalculoNumerico.git
```

Ou clone e instale localmente:

```bash
git clone https://github.com/pedroiff0/CalculoNumerico.git
cd CalculoNumerico
pip install -e .
```

Após a instalação, execute o menu interativo:

```bash
calcnum
```

Ou importe os módulos em Python:

```python
from codigos import bases, sistemaslineares, edos
```

## ⛏️ Requisitos <a name = "requisitos"></a>

- [Python](https://www.python.org/ftp/python/3.13.7/) - Python

## ✍️ Autores <a name = "autores"></a>

- [@pedroiff0](https://github.com/pedroiff0) - Pedro Henrique Rocha de Andrade

## 📚 Documentação

A documentação completa está disponível em [GitHub Pages](https://pedroiff0.github.io/CalculoNumerico/) e é gerada automaticamente usando Sphinx.

### Funcionalidades da Documentação

- **Documentação de API**: Documentação completa de todas as funções com exemplos de uso
- **Testes Interativos**: Cada teste unitário tem sua própria página com comandos para execução
- **Matriz de Funcionalidades**: Visão geral das implementações por módulo
- **Exemplos Práticos**: Casos de uso reais com gráficos e saídas

### Como Usar a Documentação Localmente

```bash
# Instalar dependências
pip install -r codigos/requirements.txt

# Construir documentação
cd docs
make html

# Abrir no navegador
open _build/html/index.html
```

### Documentação dos Testes

- Geramos um resumo com as *docstrings* dos testes unitários em `docs/tests_unitarios.md`
- Esse arquivo é atualizado automaticamente por `scripts/generate_tests_docs.py` e contém todas as descrições dos testes por módulo

Para regenerar a documentação dos testes localmente:

```bash
python scripts/generate_tests_docs.py
```

## 📖 Guia de Cálculo Numérico (LaTeX)

Além da documentação técnica em Sphinx, o projeto inclui um **livro guia completo em LaTeX** com implementações detalhadas e explicações teóricas de todos os métodos numéricos.

### 📋 Conteúdo do Guia

O guia abrange todos os tópicos da disciplina:

- **Introdução ao Cálculo Numérico**
- **Fundamentos**: Análise de erros e representação numérica
- **Raízes de Equações**: Métodos da bissecção, Newton-Raphson, secante
- **Sistemas Lineares**: Eliminação de Gauss, LU, Jacobi
- **Interpolação**: Lagrange, Newton, diferenças divididas
- **Ajuste de Curvas**: Mínimos quadrados, regressão linear e polinomial
- **Integração Numérica**: Trapézio, Simpson, Gauss-Legendre
- **Equações Diferenciais**: Euler, Runge-Kutta, sistemas

### 🛠️ Compilação do Guia

```bash
# Compilar o livro completo
cd guia
make book

# Compilar apenas os slides
make slides

# Compilar tudo
make all

# Limpar arquivos auxiliares
make clean
```

### 📁 Estrutura do Sistema LaTeX

```
guia/
├── latex/              # Arquivos LaTeX principais
│   ├── guia.cls       # Classe LaTeX personalizada
│   ├── main.tex       # Arquivo principal do livro
│   └── slides.tex     # Apresentações Beamer
├── capitulos/         # Capítulos do livro
├── frontmatter/       # Capa e elementos pré-textuais
├── backmatter/        # Apêndices e referências
├── biblio.bib         # Referências bibliográficas
├── Makefile          # Sistema de compilação
└── README_guia.md    # Documentação detalhada
```

### 🎨 Características Técnicas

- **Classe Personalizada**: `guia.cls` baseada em `book.cls` com configurações brasileiras
- **Highlighting de Código**: Integração com `minted` para syntax highlighting de Python
- **Bibliografia ABNT**: Formatação de referências no padrão brasileiro
- **Slides Beamer**: Apresentações automáticas geradas a partir do conteúdo
- **Makefile Automatizado**: Compilação simplificada com um comando

### 📖 Arquivos Gerados

Após a compilação, são gerados:

- `guia_calculo_numerico.pdf`: Livro completo (44 páginas)
- `guia_slides.pdf`: Apresentações em Beamer (10 slides)

### 🔧 Dependências LaTeX

```bash
# macOS com MacTeX
brew install --cask mactex

# Instalar pygments para minted
pip install Pygments

# Verificar instalação
cd guia && make check-deps
```

## ✅ Testes

O projeto inclui 96 testes unitários abrangentes:

```bash
# Rodar todos os testes
pytest tests/ -v

# Rodar testes de um módulo específico
pytest tests/test_edos.py -v

# Com saída detalhada
pytest tests/ -v --tb=short
```

### 🧪 Como Escrever Testes Unitários

Para contribuir com novos testes, siga estas diretrizes:

#### 1. **Estrutura Básica de um Teste**

```python
"""Testes para o módulo `codigos.modulo`.

Descrição breve do que o teste cobre."""

import numpy as np
import pytest
from codigos import modulo

def test_nome_descritivo():
    """Descrição do que o teste verifica."""
    # Arrange (preparar dados)
    entrada = valor_esperado
    
    # Act (executar função)
    resultado = modulo.funcao(entrada)
    
    # Assert (verificar resultado)
    assert resultado == valor_esperado
```

#### 2. **Exemplo Prático - Teste de Função**

```python
def test_conversao_base10_para_base2():
    """Testa conversão de decimal para binário."""
    from codigos.bases import base10_para_base2
    
    # Teste básico
    assert base10_para_base2(10) == "1010"
    
    # Teste com zero
    assert base10_para_base2(0) == "0"
    
    # Teste com potência de 2
    assert base10_para_base2(16) == "10000"
```

#### 3. **Testes com Tolerância Numérica**

```python
def test_integracao_numerica_trapezio():
    """Testa regra do trapézio com função conhecida."""
    from codigos.integracoes import trapezio
    
    # ∫[0,1] x² dx = 1/3 ≈ 0.3333
    resultado = trapezio('x**2', 0, 1, 1000)
    
    # Tolerância relativa para cálculos numéricos
    assert abs(resultado - 1/3) < 1e-6
```

#### 4. **Testes de Exceções**

```python
def test_entrada_invalida_levanta_excecao():
    """Testa se entradas inválidas levantam exceções apropriadas."""
    from codigos.raizes import bisseccao
    
    # Deve levantar ValueError para intervalo inválido
    with pytest.raises(ValueError):
        bisseccao('x**2 - 1', 2, 1, 1e-6, 100)  # a > b
```

#### 5. **Convenções do Projeto**

- **Nomenclatura**: `test_nome_descritivo_da_funcao()`
- **Docstrings**: Em português, descrevendo o que é testado
- **Imports**: Use imports absolutos (`from codigos import modulo`)
- **Asserções**: Use `pytest.approx()` para comparações numéricas
- **Cobertura**: Teste casos normais, bordas e erros

#### 6. **Executando Testes Durante Desenvolvimento**

```bash
# Testes do módulo específico
pytest tests/test_modulo.py -v

# Testes com cobertura
pytest tests/ --cov=codigos --cov-report=html

# Testes em modo watch (re-executa automaticamente)
pytest-watch tests/
```

#### 7. **Estrutura de Arquivos de Teste**

```
tests/
├── test_bases.py          # Testes para bases.py
├── test_sistemaslineares.py  # Testes para sistemaslineares.py
├── test_interpolacoes.py  # Testes para interpolacoes.py
├── test_integracoes.py    # Testes para integracoes.py
├── test_edos.py          # Testes para edos.py
├── test_raizes.py        # Testes para raizes.py
└── test_ajustecurvas.py  # Testes para ajustecurvas.py
```

## 🔄 CI/CD

O projeto utiliza GitHub Actions para integração contínua:

- **Testes Automáticos**: Todos os testes são executados em cada push/pull request
- **Build da Documentação**: Documentação Sphinx é gerada e implantada automaticamente
- **Verificação de Qualidade**: Linting e validação de código
- **Deploy**: Documentação atualizada é publicada em GitHub Pages

### Status do CI

<div align="center">

[![CI](https://github.com/pedroiff0/CalculoNumerico/actions/workflows/ci.yml/badge.svg)](https://github.com/pedroiff0/CalculoNumerico/actions/workflows/ci.yml)
[![Documentation](https://github.com/pedroiff0/CalculoNumerico/actions/workflows/docs.yml/badge.svg)](https://github.com/pedroiff0/CalculoNumerico/actions/workflows/docs.yml)
[![Coverage](https://img.shields.io/badge/coverage-96%25-brightgreen.svg)](https://github.com/pedroiff0/CalculoNumerico/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](/LICENSE)

</div>

#### 📊 Métricas de Qualidade

- **✅ Cobertura de Testes**: 96% (96 testes unitários passando)
- **✅ Build Status**: Todas as verificações automatizadas passando
- **✅ Documentação**: Gerada e implantada automaticamente
- **✅ Linting**: Código seguindo padrões de qualidade

#### 🔄 Workflows Ativos

| Workflow | Status | Descrição |
|----------|--------|-----------|
| **CI Pipeline** | ![CI](https://github.com/pedroiff0/CalculoNumerico/actions/workflows/ci.yml/badge.svg) | Testes, linting e validação |
| **Docs Deploy** | ![Docs](https://github.com/pedroiff0/CalculoNumerico/actions/workflows/docs.yml/badge.svg) | Build e deploy da documentação |

#### 🚀 Funcionalidades do CI

- **Testes Automáticos**: Executados em push e pull requests
- **Verificação Multi-Plataforma**: Compatibilidade com Python 3.8+
- **Build da Documentação**: Sphinx gerado automaticamente
- **Deploy Automático**: Documentação atualizada em GitHub Pages
- **Relatórios de Cobertura**: Análise detalhada da cobertura de testes
- **Validação de Código**: Linting e formatação automática

#### 📈 Histórico de Builds

Para visualizar o histórico completo de builds e detalhes dos testes:

- [📊 CI Pipeline](https://github.com/pedroiff0/CalculoNumerico/actions/workflows/ci.yml)
- [📚 Documentação](https://github.com/pedroiff0/CalculoNumerico/actions/workflows/docs.yml)
- [📖 Documentação Online](https://pedroiff0.github.io/CalculoNumerico/)

## 📜 Licença

Este repositório inclui um arquivo `LICENSE`.