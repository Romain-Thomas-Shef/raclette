"""
This file is part of the raclette project
It is where the application starts.

Author: R. Thomas
Place: U. of Sheffield
Year: 2025-
version: 0.1

changelog:
----------
0.1 : RTh - Creation of the file
"""

####Standard Library
import os
import sys

####Local imports
from .utils import cli, read_online_file
from .queries import pypi, github
from . import cff_to_bibtex

def main():
    '''
    This is the main function
    '''

    ##1st we use the command line interface to look at potential
    ##arguments
    args = cli.command_line_interface(sys.argv[1:])

    ##Analyse what was given    
    source = args['source']

    packages = {}
    if args['is_file']:
        ##A file is given, e must read it and extract packages name and versions
        package = {}

    else:
        ##a simple package was given  
        if args['package_version']:        
            packages[args['dep']] = args['package_version']
        else:
            packages[args['dep']] = None

    ###make the query
    for package in packages:
        if source == 'pypi':
            info =pypi.get_package_info(package)
        elif source == 'github':
            info = github.slash_repo_url(package)
        citation_files, other_info = github.get_citation_url(info['owner'], info['repo'], args['token'])

        if not citation_files:
            print('No citation files found')
            nofile_citation_info = github.get_owners_name(other_info, token)
            print(nofile_citation_info) 
        else:
            for file in citation_files:
                content,asstring = read_online_file.get_file(file)
                if 'bib' in file:
                    bibtex = asstring
                    print('BIB:\n' + bibtex)
                if 'cff' in file:
                    bibtex = cff_to_bibtex.cff_to_bibtex(content, initial_only=False, author_number=-99)
                    print('CFF:\n' + bibtex)

            
