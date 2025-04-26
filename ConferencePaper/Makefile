# LATEX: pdflatex | xelatex | lualatex
LATEX = lualatex
LATEX_FLAGS = -shell-escape
BIBTEX = bibtex

FILES = $(patsubst %.tex, %.pdf, $(wildcard *.tex))

make:
	pdflatex main.tex
	bibtex main
	pdflatex main.tex
	pdflatex main.tex

clean:
	-rm -f *.{log,toc,tac,aux,dvi,ps,bbl,blg,tmp,nav,out,snm,vrb,rel,cut,abs,xmpi,xmpdata,*~}
	-rm -rf out _minted* auto
	for i in $(ALLSUBDIRS); do \
	    (cd $$i; make clean) || exit 1; \
	done
	-rm $(FILES)

cleanall: clean
	-rm -rf out auto