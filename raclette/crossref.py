"""
This file is part of the raclette project
It retrieve, for a give DOI, the citation count
from the crossref database

Author: R. Thomas
Place: U. of Sheffield, RSE Team
Year: 2025-

"""

###Python standard library

##Third party
import requests

##Local imports

def get_citations(doi):
    '''
    This function uses the crossref API
    to retrieve the DOI citation count.

    Parameters
    ----------
    doi  :   str
             full doi.org url

    Return
    ------
    citation    :  str
                   number of citation
    '''

    ##split the doi url
    url_nohttp = doi[16:] ##this remove https://doi.org/

    ###build the crossref url]
    crossref = 'http://api.crossref.org/works/' + url_nohttp

    ##response url
    response = requests.get(crossref)

    if response.status_code == 200:

        ##get the data
        data = response.json()

        citations = data['message']['is-referenced-by-count'] 
    
    else:
        citations = 'N.A'

    return citations
