import flask, requests, git
from flask import Flask

###Config###
REPO_LINK = "https://api.github.com/repos/donaltuohy/CS4400---Internet-Applications"
COMMITS_LINK = REPO_LINK + "/commits"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisShouldBeSecret'


def getCommitFilenames(sha):
    response = requests.get(COMMITS_LINK + "/" + str(sha))
    commitDict = response.json()
    return commitDict['files']


if __name__ == "__main__":

    #First, get repository name
    response = requests.get(REPO_LINK)
    response = response.json()
    repoName = response['name']
    print(repoName)

    #Second, get json of commit details
    response = requests.get(COMMITS_LINK)
    jsonResponse = response.json()
    listOfCommits = []
    dictOfCommits = {} 

    #Create a list of all the sha's
    for commit in jsonResponse:
        listOfCommits.append(commit["sha"])

    #Create a dict of all the sha's, whether they've been analysed and their average complexity 
    for count in range(len(listOfCommits)):
        dictOfCommits[count] = [listOfCommits[count], False, 0] 

    # filenames = []
    # files = getCommitFilenames(dictOfCommits[25])
    # for name in files:
    #     filenames.append(name["filename"])

    print("\n\nList of commit sha's in", repoName)
    print("__________________________________")
    for commit in dictOfCommits.values():
        print(commit[0], ",  ", commit[1], ",   ", commit[2])
