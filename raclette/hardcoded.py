'''
This file is part of raclette
It stores the hardcoded data

Author = R. Thomas
year = 2025 - 
Place = U. of Sheffield
'''


##lots of good material here: https://cran.r-project.org/web/packages/cffr/vignettes/bibtex-cff.html

###BIBTEX | source = https://www.bibtex.com/g/bibtex-format/
bibtex_type = ['article', 'book', 'booklet', 'conference', 'inbook', 
               'incollection', 'inproceedoings', 'manual', 'masterthesis',
               'phdthesis', 'proceedings', 'techreport', 'unpublised', 'misc']

bibtex_fields = ['type', 'author', 'authors', 'year', 'month', 'title', 'booktitle', 'journal',
                 'series', 'volume', 'number', 'issue', 'chapter', 'start', 'end', 'pages', 
                 'editor', 'publisher', 'annote', 'editor', 'instituion',
                 'note',  'edition', 'organization', 'address', 'doi', 'url', ] 

##CFF | source = https://cran.r-project.org/web/packages/cffr/vignettes/bibtex-cff.html
cff_fields = ['abbreviation', 'abstract', 'authors', 'collection-doi', 'collection-title', 
              'collection-type', 'commit', 'conference', 'contact', 'copyright', 'data-type',
              'database-provider', 'database', 'date-accesseddat', 'e-downloaded', 'date-published', 
              'date-released', 'department', 'doi', 'edition', 'editors', 'editors-series', 'end', 'entry',
              'filename', 'format', 'identifiers', 'institution', 'isbn', 'issn', 'issue', 'issue-date',
              'issue-title', 'journal', 'keywords', 'languages', 'license', 'license-url', 'loc-end',
              'loc-start', 'locationmedium', 'month', 'nihmsid', 'notes', 'number', 'number-volumes',
              'pages', 'patent-states', 'pmcid', 'publisher', 'ntsrepos', 'itory', 'repository-artifact',
              'repository-code', 'scope', 'section', 'senders', 'start', 'status', 'term', 'thesis-type',
              'title', 'translators', 'type', 'url', 'version', 'volume', 'volume-title', 'year-original']

cff_type_to_bibtex_type = {'article':'article', 
                           'book':'book', 
                           'booklet': 'booklet',
                           'conference': 'conference',
                           'conference-paper':'inproceedings',
                           'inbook':'inbook',
                           'chapter': 'inbook', 
                           'incollection': 'incollection',
                           'inproceedoings': 'inproceedings',
                           'manual': 'manual',
                           'masterthesis': 'masterthesis',
                           'phdthesis': 'phdthesis',
                           'proceedings': 'proceedings',
                           'techreport': 'techreport',
                           'unpublised': 'unpublished',
                           'generic': 'misc',
                           'thesis': 'pddthesis',
                           'software': 'software', ##note that software is not in the official list but I found that it can be accepted
                           'report': 'techreport',
                           'dataset': 'misc',
                           'website': 'misc',
                           } 

cff_keywords_to_bibtex = {'type': 'type', 
                           'author': 'authors',
                           'year': ['date-released', 'date-published'], ##date-release will be used in priority
                           'month': ['date-released', 'date-published'], ##date-release will be used in priority
                           'title': 'title',
                           'version': 'version',
                           'license': 'license',
                           'doi': 'doi',
                           'url': ['url', 'repository-code']} 
