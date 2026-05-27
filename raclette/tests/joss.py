import requests
import bs4
from bs4 import XMLParsedAsHTMLWarning
import warnings
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


with open('Joss_all_published_github.txt', 'w') as save:

    for page in range(179):
        print(page+1)
        url = f'https://joss.theoj.org/papers/published?page={str(page+1)}'
        response = requests.get(url)

        for i in response.text.split('\n'):
            if 'href' in i and 'published' not in i and 'papers' in i:
                paperurl = i.split(' ')[-1].strip('"/>').strip("href=")[1:]


                response_paper = requests.get(paperurl)

                for j in response_paper.text.split('\n'):
                    if 'github' in j and 'btn paper-btn' in j and 'review' not in j:
                        githuburl = j.split(' ')[-1].strip("href=").strip('>').strip('"')
                        save.write(githuburl+'\n')
                        print(paperurl, githuburl)
