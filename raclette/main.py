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
from .utils import cli
from .queries import pypi, github

def main():
    '''
    This is the main function
    '''

    ##1st we use the command line interface to look at potential
    ##arguments
    args = cli.command_line_interface(sys.argv[1:])

    ##Analyse what was given    
    language = args['pl']

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
        info =pypi.get_package_info(package)
        print(info)
        github.get_citation(info['owner'], info['repo'], args['token'])
