"""
This file is part of the raclette project
it codes some useful function for the software citation library

Author: R. Thomas
Place: U. of Sheffield, RSE Team
Year: 2025-
"""

def cross_match_database(package, db_query):
    '''
    This function crossmatches the package name
    and the database query. The database query was made
    on source(pypi/cran/github/julia) and name of the package 
    '''
    if len(db_query) == 0:
        package['in_db'] = False
        package['V_db'] = '-'
        package['N_db'] = '-'
        package['Source_db'] = '-'

    else:
        package['in_db'] = True
        package['N_db'] = len(db_query)

        if len(db_query) == 1:
            ##version
            package['V_db'] = db_query[0].version
            
            if '.bib' in db_query[0].bibtex_source:
                package['Source_db'] = '.bib file'
            elif '.cff' in db_query[0].bibtex_source:
                package['Source_db'] = '.cff file'
            elif '#' in db_query[0].bibtex_source:
                package['Source_db'] = 'Git commit'
            else:
                package['Source_db'] = 'Unknown'

            package['platform'] = db_query[0].platform
            package['version'] = db_query[0].version
            package['repo_url'] = db_query[0].repo_url
            package['pypi_url'] = db_query[0].pypi_url
            package['cran_url'] = db_query[0].cran_url
            package['julia_url'] = db_query[0].julia_url
            package['commit'] = db_query[0].commit
            package['citation_url'] = db_query[0].citation_url
            package['doi_url'] = db_query[0].doi_url
            package['bibtex_source'] = db_query[0].bibtex_source
            package['bibtex'] = db_query[0].bibtex
            

        if len(db_query) > 1:
            highest_version = None
            for v in db_query:
                print(v)
                         
    return package
