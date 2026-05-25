"""
This file is part of the raclette project
it makes operation on bibtex files

Author: R. Thomas
Place: U. of Sheffield, RSE Team
Year: 2025-

"""

###Python standard library

##Third party

##Local imports

def extract_line_data(bibtex, field):
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
    bibtex  :   list
                of bibtex lines
    field   :   str
                bibtex we want the data from 
    Return
    ------
    data    :   str
                line of interest
    '''
    ###we always return data
    data = None 
    no_bracket = None

    for line in bibtex: 
        if field in line:
            no_bracket = line.replace(' ', '').split('=')[1].replace(',', '').replace('}', '').replace('{', '').strip('\n')

    if field == 'doi' and no_bracket is not None:
        if 'https://doi.org/' in no_bracket:
            data = no_bracket
        else:
            data = 'https://doi.org/' + no_bracket
    elif no_bracket is not None:
        data = no_bracket

    return data
