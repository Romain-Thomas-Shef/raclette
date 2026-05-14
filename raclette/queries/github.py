'''
This file is part of the raclette project
this deals with github information retrieving

Author: R. Thomas
Place: U of Sheffield, RSE Team
Year: 2025-
'''

##Python standard library

##Third party
import requests

##Local imports


def get_citation(owner, repo, token=None):
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    repo_url = f"https://api.github.com/repos/{owner}/{repo}"
    repo_data = requests.get(repo_url).json()
    print(repo_data['default_branch'])

    branch = repo_data["default_branch"]

    tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    tree_data = requests.get(tree_url, headers=headers).json()

    found_files = [item["path"] for item in tree_data.get("tree", []) if 'CITATION' in item["path"]]
    print(found_files)

    citationfiles = []
    for pattern in ["CITATION.bib", ".github/CITATION.cff", "CITATION.cff", "CITATION.txt", "CITATION"]:
        if pattern in found_files:
            citationfiles.append(pattern)

    for file in citationfiles:
        file_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file}"
        file_data = requests.get(file_url, headers=headers).json()
        print(file, file_data['download_url'])
