# Makefile para construir a documentação via Sphinx

SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

.PHONY: help clean html

help:
	@echo "Makefile mínimo para construir docs"

html:
	$(SPHINXBUILD) -b html $(SOURCEDIR) $(BUILDDIR)/html
	@echo "Docs geradas em $(BUILDDIR)/html"

clean:
	rm -rf $(BUILDDIR)