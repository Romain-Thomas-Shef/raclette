'''
This file is part of the raclette project
it codes query to pypi

Author: R. Thomas
Place: U of Sheffield, RSE Team
Year: 2025-
'''

##Python standard library

##Third party
import requests

##Local imports
from . import github


def get_package_info(package_name):

    package_info = {}


    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()['info']
        urls = data['project_urls']
        for i in urls:
            if 'github.com' in urls[i] and 'issues' not in urls[i] and 'releases' not in urls[i]:
                github_url = urls[i]
                github_info = github.slash_repo_url(github_url)
                owner = github_info['owner']
                repo = github_info['repo']

        package_info['name'] = data['name']
        package_info['version'] = data['version']
        package_info['github'] = github
        package_info['owner'] = owner
        package_info['repo'] = repo
        
    else:
        print(f"Package {package_name} not found.")

    return package_info
