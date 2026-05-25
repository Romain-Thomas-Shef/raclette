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
from . import open_files
from .. import python_analysis

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
    parser.add_argument('package', help='Dependency file to analyse'+
                                         '\nCan be a setup.py, pyproject.toml')
    parser.add_argument('--source', help="source", choices = ['pypi', 'R', 'github'])
    parser.add_argument('--token')
    parser.add_argument('--version', action='version', version='1.0')

    ###analyse the arguments
    parsed = vars(parser.parse_args(args))

    return parsed


def analyse_arguments(parsed):
    '''
    This function analyses the argument used by the user and return
    the configuration to be used

    Parameter
    ---------
    parsed: dict
            arguments of the interface with values

    Returns
    -------
    config: dict
            configuration to be used by raclette
    '''
    ##initialise outpout
    config = {'packages': {}, 'source': None}

    ###source where we will fetch info
    config['source'] = parsed['source']
 


    ##if multiple packages where given we split them and then look for version
    packages = parsed['package'].split(';')
    for p in packages:
        if '.toml' in p:
            if config['source'] == 'pypi':
                ##analyse the toml file
                for package_info in python_analysis.read_toml(p):
                    config['packages'].append(package_info)
                

        elif config['source'] == 'pypi': ##we got packages
            name, version_info = python_analysis.extract_version_python(p)
            config['packages'][name] = version_info

        elif config['source'] == 'github':
            print('ok')
    return config
    

