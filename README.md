<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="image.png" alt="Bot logo"></a>
</p>
<h3 align="center">Cálculo Numérico</h3>

<div align="center">

[![CI](https://github.com/pedroiff0/CalculoNumerico/actions/workflows/ci.yml/badge.svg)](https://github.com/pedroiff0/CalculoNumerico/actions)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://pedroiff0.github.io/CalculoNumerico/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> Repostiório de Códigos da Disciplina de Cálculo Numérico - 2025.2
    <br> 
</p>

## 📝 Sumário

- [Sobre](#sobre)
- [Como rodar?](#como_rodar)
- [Requisitos](#requisitos)
- [Autores](#autores)
## 🧐 Sobre <a name = "sobre"></a>

Repositório de códigos da disciplina de Cálculo Numérico - 2025.2

Professor: Rodrigo Lacerda da Silva

Aluno: Pedro Henrique Rocha de Andrade

Curso: Bacharelado em Engenharia de Computação

Instituição: Instituto Federal Fluminense <i>Campus</i> Bom Jesus do Itabapoana.

Setembro/2025 à Março/2026,

Bom Jesus do Itabapoana - RJ.

### Ementa

<ol>
        <li>Números Binários e Análise de Erros
            <ol>
                <li>✅ Representação de números em diversas bases</li>
                <li>✅ Conversão de números nos sistemas decimal e binário</li>
                <li>Aritmética de ponto flutuante</li>
                <li>Erros absolutos e relativos</li>
                <li>Erros de arredondamento e truncamento em um sistema de aritmética de ponto flutuante</li>
            </ol>
        </li>
        <li>Solução de Equações não Lineares
            <ol>
                <li>✅ Isolamento de raízes, refinamento e critérios de parada</li>
                <li>✅ Método da bisseção</li>
                <li>Método do ponto fixo</li>
                <li>✅ Método de Newton-Raphson</li>
                <li>✅ Método da secante</li>
                <li>Comparação entre os métodos</li>
            </ol>
        </li>
        <li>Interpolação
            <ol>
                <li>✅ Interpolação polinomial</li>
                <li>✅ Formas de se obter o polinômio interpolador: resolução do sistema linear, forma de Lagrange e forma de Newton</li>
                <li>Estudo do erro na interpolação</li>
                <li>Fenômeno de Runge</li>
                <li>Funções spline: spline linear interpolante e spline cúbica interpolante</li>
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
                <li>Teorema geral do erro</li>
            </ol>
        </li>
        <li>Soluções Numéricas de Equações Diferenciais Ordinárias
            <ol>
                <li>Problemas de valor inicial</li>
                <li>✅ Método de Euler, métodos de série de Taylor</li>
                <li>✅ Métodos de Runge-Kutta de 2.ª ordem</li>
                <li>✅ Métodos de Runge-Kutta de ordens superiores</li>
                <li>✅ Equações de ordem superior, problemas de valor de contorno</li>
                <li>Método das diferenças finitas</li>
            </ol>
        </li>
    </ol>

## 🏁 Como rodar? <a name = "como_rodar"></a>

### Prerequisitos

```
Python 3.14.0
```

### Instalando

Apenas instale o Python, e as bibliotecas com

```
pip install -r requirements.txt
```

## ⛏️ Requisitos <a name = "requisitos"></a>

- [Python](https://www.python.org/ftp/python/3.13.7/) - Python

## ✍️ Autores <a name = "autores"></a>

- [@pedroiff0](https://github.com/pedroiff0) - Pedro Henrique Rocha de Andrade

## 🧾 Documentação

A documentação do projeto é gerada com **Sphinx** (em Português). Para gerar localmente:

```bash
cd docs
pip install -r requirements.txt
make html
# abrir docs/_build/html/index.html
```

## ✅ Testes

Utilizamos `pytest`. Execute:

```bash
pytest -q
```

para rodar a suíte de testes.

## 🤝 Contribuindo

Leia `CONTRIBUTING.md` para orientações sobre estilo, docstrings (NumPy style) e fluxo de contribuições.

## 📜 Licença

Este repositório inclui um arquivo `LICENSE`.