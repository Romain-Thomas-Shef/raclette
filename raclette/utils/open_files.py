"""
This file is part of the raclette project
just file handling


Author: R. Thomas
Place: U. of Sheffield, RSE Team
Year: 2025-
"""

###Python standard library
import urllib

##Third party

##Local imports

def get_online_file(url):
    '''
    read the file at the url given in argument

    Parameters
    -----------
    url    :   str
               the url to read

    Returns
    -------
    content  :


    Warning: we do not check if the url exist!
    '''
    ##initialise the list
    content = []

    ##read the file
    file = urllib.request.urlopen(url)
    for line in file:
        content.append(line.decode('utf-8'))

    return content, ''.join(content)
