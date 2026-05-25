"""
This file is part of the raclette project
This file look at the packages and extract version
if given

Author: R. Thomas
Place: U. of Sheffield, RSE Team
Year: 2025-
"""

###Python standard library
import tomllib

##Third party
import requests

##Local imports
from .queries import github


def read_toml(file, include_optional=False):
    '''
    Read the yaml file give as argument

    Parameters
    -----------
    file    :  str
               path to the file to read

    Returns
    -------
    packages    : dictionary
                  keys = packages
                  values = version number (if any), or url, or None

    Warning: We do not check that the file exist
    '''
    #initialise list of packages
    all_packages = {}

    ##open file
    with open(file, 'rb') as tomlfile:
        file = tomllib.load(tomlfile)

    ##read the project section and find dependencies sub-section
    dependencies_section = []
    for subsection in file['project']:
        if subsection == 'dependencies':
            dependencies_section.append(subsection)
        elif include_optional is True and subsection == 'optional-dependencies':
            dependencies_section.append(subsection)

    ##extract dependencies
    all_dep = []
    for ss in dependencies_section:
        for dep in file['project'][ss]:
            if ss == 'optional-dependencies':
                for subdep in file['project'][ss][dep]:
                    all_dep.append(subdep)
            else:
                all_dep.append(dep)


    ##Cut all dep to find version
    for dep in all_dep:
        name_pac, version = extract_version_python(dep)
        all_packages[name_pac] = version 

    return all_packages

def extract_version_python(package):
    '''
    This function extract the version number
    of the package.
    if no version unmber is given, the package
    name is returned
    
    Parameter
    ---------
    package:    str
                string to analyse

    Return
    ------
    name:   str
            name of the package
    version: dict
             sign/version
    '''
    if '==' in package:
        sign = '=='
        name, version = package.split('==')

    elif '~=' in package:
        sign = '~='
        name, version = package.split('~=')

    elif '<=' in package:
        sign = '<='
        name, version = package.split('<=')

    elif '>=' in package:
        sign = '>='
        name, version = package.split('>=')

    elif '>' in package:
        sign = '>'
        name, version = package.split('>')

    elif '<' in package:
        sign = '<'
        name, version = package.split('<')

    else:
        name = package
        sign = None
        version = None

    return f"{name.strip()}_{version}", {'name': name.strip(), 'sign': sign, 
                          'version': version.strip() if version is not None else version} 

def get_pypi_info(package_name):
    '''
    This function fetches the information
    from pypi. It simply scraps the page

    Parameter
    ---------
    package_name    :   str
                        name of the package to look for

    Return
    ------
    package_info    :   dict
                        Information of the package
    '''    

    package_info = {}
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        urls = data['info']['project_urls']
        for i in urls:
            if 'github.com' in urls[i] and 'issues' not in urls[i] and 'releases' not in urls[i]:
                github_url = urls[i]
                github_info = github.slash_repo_url(github_url)
                owner = github_info['owner']
                repo = github_info['repo']

        package_info['name'] = data['info']['name']
        package_info['version'] = data['info']['version']
        package_info['repo_owner'] = owner
        package_info['repo_name'] = repo
        package_info['repo_url'] = github_url
        package_info['pypi_url'] = data['info']['package_url']
        package_info['releases_list'] = data['releases'].keys()

    else:
        print(f"Package {package_name} not found.")

    return package_info

