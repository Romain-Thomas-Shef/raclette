"""
This file is part of the raclette project
it read pyproject.toml and get the list of packages 


Author: R. Thomas
Place: U. of Sheffield, RSE Team
Year: 2025-
"""

###Python standard library
import tomllib


##Third party

##Local imports

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
    final_dep_versions = {}
    for dep in all_dep:
        #print(dep)
        if '==' in dep:
            final_dep_versions[dep.split('==')[0]] = dep.split('==')[1]
        if '~=' in dep:
            final_dep_versions[dep.split('~=')[0]] = dep.split('~=')[1]


    print(final_dep_versions)
            
