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


def get_package_info(package_name):

    package_info = {}


    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()['info']
        urls = data['project_urls']
        for i in urls:
            if 'github.com' in urls[i] and 'issues' not in urls[i] and 'releases' not in urls[i]:
                github = urls[i]
                owner = github.split('/')[3]
                repo = github.split('/')[4].split('.git')[0]

        package_info['name'] = data['name']
        package_info['version'] = data['version']
        package_info['github'] = github
        package_info['owner'] = owner
        package_info['repo'] = repo
        
    else:
        print(f"Package {package_name} not found.")

    return package_info
