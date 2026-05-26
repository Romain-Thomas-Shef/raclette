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
from .utils import cli, open_files
from .queries import pypi, github
from . import cff_to_bibtex,bibtex,python_analysis

def main():
    '''
    This is the main function
    '''

    ##1st we use the command line interface to look at potential
    ##arguments
    args = cli.command_line_interface(sys.argv[1:])
    config = cli.analyse_arguments(args)
    
    ###get the token
    token = args['token']

    for package in config['packages']:
        bibtex_info = analyse_package(config['packages'][package], config['source'], token=token)

def analyse_package(package, source, token=False):
    '''
    For a given package and a given source
    extract the bibtex

    Parameter
    ---------
    package :   str
                name of the package/repo

    source  :   str
                where we will fetch info
    
    token   :   str
                token for github query
    '''
    all_data = {'name': None,
                'platform': None,
                'version': None,
                'repo_url': None,
                'cran_url': None,
                'repo_owner': None,
                'repo_name': None,
                'julia_url': None,
                'last_commit': None,
                'citation_url': None,
                'doi_url': None,
                'bibtex_source': None,
                'bibtex': None}

    ##start filling the results:
    all_data['name'] = package['name']

    if source == 'pypi':
        ##some info will be useless
        all_data['platform'] = 'pypi'
        all_data['cran_url'] = 'N.A.'
        all_data['julia_url'] = 'N.A.'

        ##scrap pypi
        info = python_analysis.get_pypi_info(package['name'])        

        #add pypi url 
        if info:
            all_data['pypi_url'] = info['pypi_url']
            all_data['repo_owner'] = info['repo_owner']
            all_data['repo_name'] = info['repo_name']


    ##Find citation files
    citation_files = [] 
    if all_data['repo_owner']:
        citation_files, other_info = github.get_citation_url(all_data['repo_owner'], all_data['repo_name'], token)

        ###add repository url to all data
        all_data['repo_url'] = other_info['repo_url']

    ##prioritise
    if citation_files:
        for f in citation_files:

            ###priority is given to .bib files
            if '.bib' in f:
                #Read the file
                all_data['bibtex_source'] = f
                _, bibtex_str = open_files.get_online_file(f)

                ##bibtex
                all_data['bibtex'] = bibtex_str

                ###get doi url
                all_data['doi_url'] = bibtex.extract_line_data(bibtex_str, 'doi')

                ###if we have a bibtex we do not need the latest commit
                all_data['last_commit'] = 'N.A.'

                ###url in bibtex
                all_data['citation_url'] = bibtex.extract_line_data(bibtex_str, 'url')

                ###if it comes from the .bib file it will work for all version
                all_data['version'] = 'all'
                
                break

            ###then to .cff
            elif '.cff' in f:
               bibtex_source = f
                 
        
    else:
        print('not found')


    return all_data

'''
###make the query
for package in packages:
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
'''
