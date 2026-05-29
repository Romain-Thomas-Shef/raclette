"""
This file is part of the raclette project
it makes operation on bibtex files

Author: R. Thomas
Place: U. of Sheffield, RSE Team
Year: 2025-

"""

###Python standard library

##Third party
import bibtexparser

##Local imports

def extract_bibtex_data(bibtex, selected_field):
    '''
    This function extracts all the data
    of a bibtex field.
    Input has to be given as a list of line

    bibtex lines are:
    doi = {10.21105/joss.01249},
    or
    doi = 10.21105/joss.01249,

    some particular cases that we handle:
    doi ==> can be given with full adress or just doi part

    Parameters
    ----------
    bibtex  :   str
                the bibtex text
    selected_field   :   str
                         bibtex we want the data from 
    Return
    ------
    data    :   str
                line of interest
    '''
    ###we always return data
    data = None 

    ###parse the bibtex entry
    parsed = bibtexparser.parse_string(bibtex)

    saved_data = []
    ##go through entries in bibtex
    for entry in parsed.entries:
        ##for each entry
        for field in entry.fields:
            if selected_field in field.key:
                
                if selected_field == 'doi' and field.key == 'doi':
                    if 'https://doi.org/' in field.value:
                        data = field.value
                    else:
                        data = 'https://doi.org/' + field.value 

                elif selected_field in field.key:
                    data = field.value
                saved_data.append(data)

    return saved_data
