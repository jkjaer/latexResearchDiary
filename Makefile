##################################################################
# Makefile for LaTeX
##################################################################
# Use:
# make
# make clean
# options for ps2pdf: http://pages.cs.wisc.edu/~ghost/doc/AFPL/6.50/Ps2pdf.htm

TEX:=$(shell ls *.tex)
OTHER = *~ *.aux *.dvi *.toc *.bbl *.blg *.out *.thm *.ps *.idx *.ilg *.ind *.tdo *.auxlock *.maf *.mtc* *-blx.bib *.run.xml

pdflatex: master.tex
	pdflatex -shell-escape -file-line-error -synctex=1 master.tex
	bibtex master.aux
	splitindex master.idx
	pdflatex -shell-escape -file-line-error -synctex=1 master.tex
	pdflatex -shell-escape -file-line-error -synctex=1 master.tex
	rm -f $(OTHER) $(PS)
clean:
	rm -f $(OTHER) $(PS)
