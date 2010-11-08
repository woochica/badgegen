all: output.pdf

output.pdf : output.tex
	pdflatex output.tex
	pdflatex output.tex

output.tex : template.tex gentex.py cleaned_resztvevok.csv
	python gentex.py cleaned_resztvevok.csv output.tex template.tex

clean :
	rm output.tex output.pdf
