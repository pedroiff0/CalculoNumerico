# Makefile para compilação do guia de cálculo numérico

# Compilador LaTeX
LATEX = pdflatex
BIBTEX = bibtex
MAKEINDEX = makeindex

# Arquivos principais
MAIN = latex/main.tex
SLIDES = latex/slides.tex
BIB = biblio.bib

# Diretórios
LATEX_DIR = latex
CAPITULOS_DIR = capitulos
FRONTMATTER_DIR = frontmatter
BACKMATTER_DIR = backmatter

# Alvos principais
.PHONY: all book slides clean clean-all help

# Compilar tudo
all: book slides

# Compilar o livro
book: $(MAIN) $(BIB)
	cd $(LATEX_DIR) && \
	$(LATEX) main && \
	$(BIBTEX) main && \
	$(MAKEINDEX) main && \
	$(LATEX) main && \
	$(LATEX) main
	mv $(LATEX_DIR)/main.pdf guia_calculo_numerico.pdf

# Compilar os slides
slides: $(SLIDES)
	cd $(LATEX_DIR) && \
	$(LATEX) slides && \
	$(LATEX) slides
	mv $(LATEX_DIR)/slides.pdf guia_slides.pdf

# Limpar arquivos auxiliares
clean:
	cd $(LATEX_DIR) && rm -f *.aux *.log *.out *.toc *.lof *.lot *.bbl *.blg *.idx *.ind *.ilg

# Limpar tudo, incluindo PDFs
clean-all: clean
	rm -f guia_calculo_numerico.pdf guia_slides.pdf

# Verificar dependências
check-deps:
	@echo "Verificando dependências..."
	@which $(LATEX) || echo "pdflatex não encontrado"
	@which $(BIBTEX) || echo "bibtex não encontrado"
	@which $(MAKEINDEX) || echo "makeindex não encontrado"
	@kpsewhich minted.sty || echo "pacote minted não encontrado (instale python-pygments)"
	@kpsewhich abnt.bst || echo "estilo ABNT não encontrado"

# Ajuda
help:
	@echo "Comandos disponíveis:"
	@echo "  make all        - Compila livro e slides"
	@echo "  make book       - Compila apenas o livro"
	@echo "  make slides     - Compila apenas os slides"
	@echo "  make clean      - Remove arquivos auxiliares"
	@echo "  make clean-all  - Remove arquivos auxiliares e PDFs"
	@echo "  make check-deps - Verifica dependências"
	@echo "  make help       - Mostra esta ajuda"

# Regra padrão
.DEFAULT_GOAL := help