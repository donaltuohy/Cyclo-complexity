import flask, requests, git, threading, time
from flask import Flask

listOfCommits = []
dictOfCommits = {}
threads = []

###Config###
REPO_LINK = "https://api.github.com/repos/donaltuohy/CS4400---Internet-Applications"
CLONE_URL = "https://github.com/donaltuohy/CS4400---Internet-Applications.git"
COMMITS_LINK = REPO_LINK + "/commits"
listOfWorkers = ["http://127.0.0.1:5001/","http://127.0.0.1:5002/"]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisShouldBeSecret'


def getCommitFilenames(sha):
    response = requests.get(COMMITS_LINK + "/" + str(sha))
    commitDict = response.json()
    return commitDict['files']

#commit[1] is whether it has been complete, commit[2] is if it is currently been analysed
def getNextKey():
    for key in dictOfCommits.keys():
        if((dictOfCommits[key])[1] == False and (dictOfCommits[key])[2] == False):
            (dictOfCommits[key])[2] = True
            return key
    #If every commit has been addressed
    return "NONE"

def workerThreadFunction(workerAddress):
    while True:
        key = getNextKey()
        if key == "NONE":
            #Everything has been computed
            print("Worker finished at:", workerAddress)
            return
        shaDict = {'sha' : (dictOfCommits[key])[0]}
        response = requests.post(workerAddress + "compute", json=shaDict)
        if response.ok:
            (dictOfCommits[key])[1] = True
            (dictOfCommits[key])[3] = ((response.json())['complexityScore'])
        else:
            (dictOfCommits[key])[2] = False
            print("Commit could not be computed.")


if __name__ == "__main__":

    #First, get repository name
    response = requests.get(REPO_LINK)
    response = response.json()
    repoName = response['name']

    #Then tell all the workers to clone that repo
    repoDetails = {'repoName' : repoName, 'cloneURL' : CLONE_URL}
    for address in listOfWorkers:
        response = requests.post(address + "getrepo", json=repoDetails)
        if response.ok:
            print("Repo cloned on", address)
        else: 
            print("Could not clone repo on ", address)

    #Second, get json of commit details
    response = requests.get(COMMITS_LINK)
    jsonResponse = response.json()

    #Create a list of all the sha's
    for commit in jsonResponse:
        listOfCommits.append(commit["sha"])

    #Create a dict of all the sha's, whether they've been analysed and their average complexity 
    for count in range(len(listOfCommits)):
        dictOfCommits[count] = [listOfCommits[count], False, False, 0] 


    #Send each commit to a worker
    for address in listOfWorkers:
        print(address)
        thread = threading.Thread(target = workerThreadFunction, args = (address,)).start()
        threads.append(thread)
        print("Thread started on:", address)
    

    #Wait for all the threads to finish
    for thread in threads:
        if thread:
            thread.join()

    time.sleep(5)
    
    #Results
    print("\n\nList of commit sha's in", repoName)
    print("_________________________________________________________________________")
    print("SHA                                      Checked        Avg. Complexity")
    print("_________________________________________________________________________")
    sum = 0
    for commit in dictOfCommits.values():
        sum += commit[3]
        print(commit[0], ",  ", commit[1], ",   ", commit[3])

    print("_________________________________________________________________________\n")
    print("Average complexity for repo:", sum/len(dictOfCommits), "\n\n")
    


