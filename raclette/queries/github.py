'''
This file is part of the raclette project
this deals with github information retrieving

Author: R. Thomas
Place: U of Sheffield, RSE Team
Year: 2025-
'''

##Python standard library
import datetime

##Third party
import requests

##Local imports

def slash_repo_url(url):
    '''
    This function cuts the github url and
    extract owner and repo name
    Parameters
    ----------
    url :   str
            address of a github repo. Ex: https://github.com/Romain-Thomas-Shef/raclette

    return:
    ------
    info    :   dict
                with owner and repo as keys
    '''
    info = {}
    info['owner'] = url.split('/')[3]
    info['repo'] = url.split('/')[4].split('.git')[0]
        
    return info

def get_citation_url(owner, repo, token):
    '''
    This function goes to github and tries to find
    a citation file. It can be a *.cff or *.bib
    It returns a dictionary with all the citation files
    found.
    
    Parameters
    ----------
    owner   :   str
                owner of the repository
    repo    :   str
                name of the repository
    
    Return:
    -------
    citation_files_urls  :   list of str
                        with url to citation files
                        it can be empty
    '''
    #initialise the files
    citation_files_urls = []
    other_info = {}

    ##
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    repo_url = f"https://api.github.com/repos/{owner}/{repo}"
    repo_data = requests.get(repo_url).json()

    branch = repo_data["default_branch"]
    '''
    for i in repo_data:
        print(i, repo_data[i])
    '''

    ##other info
    other_info['creation_date'] = repo_data['created_at']
    other_info['repo_url'] = repo_data['html_url']
    other_info['name'] = repo_data['name']
    other_info['access_date'] = datetime.datetime.now().isoformat()

    ''' --> get name
    user_github_url = f"https://api.github.com/users/{repo_data['owner']['login']}"  
    user_json = requests.get(user_github_url, headers=headers)
    print(user_json.json().get('name'))
    '''

    tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    tree_data = requests.get(tree_url, headers=headers).json()

    found_files = [item["path"] for item in tree_data.get("tree", []) if 'CITATION' in item["path"]]

    ##try to find CITATION files
    citationfiles = []
    for pattern in ["CITATION.bib", ".github/CITATION.cff", "CITATION.cff", "CITATION.txt", "CITATION"]:
        if pattern in found_files:
            citationfiles.append(pattern)

    ###get the urls
    for file in citationfiles:
        file_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file}"
        file_data = requests.get(file_url, headers=headers).json()
        citation_files_urls.append(file_data['download_url'])

    return citation_files_urls, other_info
