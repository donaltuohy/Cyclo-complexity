import flask, requests, git
from flask import Flask

###Config###
REPO_LINK = "https://api.github.com/repos/donaltuohy/CS4400---Internet-Applications/"
COMMITS_LINK = REPO_LINK + "commits"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisShouldBeSecret'


def getCommitFilenames(sha):
    response = requests.get(COMMITS_LINK + "/" + sha)
    commitDict = response.json()
    return commitDict['files']

if __name__ == "__main__":

    response = requests.get(COMMITS_LINK)
    jsonResponse = response.json()
    listOfCommits = []
    dictOfCommits = {}
    
    for commit in jsonResponse:
        listOfCommits.append(commit['sha'])

    for count in range(len(listOfCommits)):
        dictOfCommits[count] = listOfCommits[count] 

    filenames = []
    files = getCommitFilenames(dictOfCommits[25])
    for name in files:
        filenames.append(name["filename"])

    print(filenames)