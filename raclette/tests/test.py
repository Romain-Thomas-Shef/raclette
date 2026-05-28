from raclette import extract_bibtex_data

with open('citation_double.bib') as F:
    A=F.read()

A = extract_bibtex_data(A, 'doi')
