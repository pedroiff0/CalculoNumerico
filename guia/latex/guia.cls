% guia.cls - Classe personalizada para o livro guia de Cálculo Numérico
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{guia}[2025/12/19 Classe para livro guia de Cálculo Numérico]

% Carrega a classe base 'book' com opções padrão
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{book}}
\ProcessOptions\relax
\LoadClass[12pt,a4paper,oneside]{book}

% Pacotes essenciais
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage[brazilian]{babel}  % Português brasileiro
\RequirePackage{geometry}
\geometry{
  left=3cm,
  right=2cm,
  top=3cm,
  bottom=2cm,
  headheight=1cm,
  footskip=1cm
}
\RequirePackage{titlesec}
\titlespacing*{\chapter}{0pt}{12pt}{14pt}
\titlespacing*{\section}{0pt}{12pt}{12pt}
\titlespacing*{\subsection}{0pt}{12pt}{12pt}
\titleformat{\chapter}[display]{\normalfont\Large\bfseries}{\chaptertitlename\ \thechapter}{14pt}{\Large}
\titleformat{\section}{\normalfont\large\bfseries}{\thesection}{1em}{}
\titleformat{\subsection}{\normalfont\normalsize\bfseries}{\thesubsection}{1em}{}
\RequirePackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\leftmark}  % Capítulo à esquerda
\fancyhead[R]{\thepage}   % Página à direita
\renewcommand{\headrulewidth}{0.5pt}

% Make chapter opening pages use the same style as normal pages
% (LaTeX's \chapter uses \thispagestyle{plain} by default)
\makeatletter
\let\ps@plain\ps@fancy
% Ensure \cleardoublepage does not insert blank pages for openany layout
\let\cleardoublepage\clearpage
\makeatother

% Configurações ABNT-like
\RequirePackage{natbib}  % Para citações
\bibliographystyle{abntex2-alf}  % Estilo ABNT
\RequirePackage{setspace}
%\onehalfspacing  % Espaçamento 1.5 - removido para reduzir espaçamento extra
\singlespacing   % Espaçamento simples para reduzir espaçamento extra

% Suporte a cores e hyperlinks
\RequirePackage{xcolor}
\RequirePackage{hyperref}
\hypersetup{
  colorlinks=true,
  linkcolor=blue,
  citecolor=green,
  urlcolor=purple
}

% Comando para título personalizado
\newcommand{\tituloLivro}[1]{\title{#1}}
\newcommand{\autorLivro}[1]{\author{#1}}
\newcommand{\dataLivro}[1]{\date{#1}}

% Ambiente para códigos Python
% \RequirePackage{minted}
% \newminted{python}{fontsize=\footnotesize, linenos, frame=single, bgcolor=gray!10}

\RequirePackage{listings}
\lstset{
  language=Python,
  basicstyle=\footnotesize\ttfamily,
  numbers=left,
  numberstyle=\tiny,
  frame=single,
  backgroundcolor=\color{gray!10},
  breaklines=true,
  captionpos=b,
  inputencoding=utf8,
  extendedchars=true,
  showstringspaces=false,
  keywordstyle=\color{blue},
  commentstyle=\color{green!60!black},
  stringstyle=\color{red},
}

\endinput