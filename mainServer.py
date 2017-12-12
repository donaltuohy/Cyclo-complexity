import flask, requests, git
from flask import Flask

###Config###
REPO_LINK = "https://api.github.com/repos/donaltuohy/CS4400---Internet-Applications"
CLONE_URL = "https://github.com/donaltuohy/CS4400---Internet-Applications.git"
COMMITS_LINK = REPO_LINK + "/commits"
listOfWorkers = ["http://127.0.0.1:5002/"]

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

    #Then tell all the workers to clone that repo
    # repoDetails = {'repoName' : repoName, 'cloneURL' : CLONE_URL}
    # for address in listOfWorkers:
    #     response = requests.post(address + "getrepo", json=repoDetails)
    #     if response.ok:
    #         print("Repo cloned on", address)
    #     else: 
    #         print("Could not clone repo on ", address)

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


    #Send each commit to a worker
    for commit in dictOfCommits.values():
        shaDict = {'sha' : (commit[0])}
        response = requests.post(listOfWorkers[0] + "compute", json=shaDict)
        if response.ok:
            commit[1] = True
            commit[2] = ((response.json())['complexityScore'])
        else:
            print("Commit could not be computed.")
    
    
    #Results
    print("\n\nList of commit sha's in", repoName)
    print("_________________________________________________________________________")
    print("SHA                                      Checked        Avg. Complexity")
    print("_________________________________________________________________________")
    sum = 0
    for commit in dictOfCommits.values():
        sum += commit[2]
        print(commit[0], ",  ", commit[1], ",   ", commit[2])

    print("_________________________________________________________________________\n")
    print("Average complexity for repo:", sum/len(dictOfCommits), "\n\n")
    


