"""
This file is part of the raclette project
It codes the command line interface


Author: R. Thomas
Place: U. of Sheffield, RSE Team
Year: 2025-
"""

###Python standard library
import argparse

##Third party

##Local imports

def command_line_interface(args):
    '''
    This function defines the command line interface of the program.

    Parameters
    -----------
    args    :   sys.argv
                arguments passed to the interface

    Returns
    -------
    parsed  :   Namespace
                parsed arguments
    '''
    ##create parser object
    parser = argparse.ArgumentParser(description=\
            '------------------------------------------------'+\
            '\n - Raclette: Software citation made easy'+\
            '\n - Authors: R. Thomas'+\
            '\n - Licence: GPLv3 - '+\
            '\n------------------------------------------------', \
            formatter_class=argparse.RawTextHelpFormatter)

    ###add arguments
    parser.add_argument('dep', help='Dependency file to analyse'+
                                         '\nCan be a setup.py, pyproject.toml')
    parser.add_argument('source', help="source", choices = ['pypi', 'R', 'github'])
    parser.add_argument('--package_version', help="if a single package name is given, this gives the version. If nothing is given, that latest findable version will be assumed")
    
    parser.add_argument('--token')
    parser.add_argument('--is_file', action='store_true')
    parser.add_argument('--version', action='version', version='1.0')

    ###analyse the arguments
    parsed = vars(parser.parse_args(args))

    return parsed
