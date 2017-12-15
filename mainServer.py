import flask, requests, git, threading, time
import matplotlib.pyplot as plt
from flask import Flask
import time
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


listOfCommits = []
dictOfCommits = {}
#threads = {}
times = []

###Config###
REPO_LINK = "https://api.github.com/repos/donaltuohy/CS4400---Internet-Applications"
CLONE_URL = "https://github.com/donaltuohy/CS4400---Internet-Applications.git"
COMMITS_LINK = REPO_LINK + "/commits"
listOfWorkers = ["http://127.0.0.1:5008/", "http://127.0.0.1:5002/", "http://127.0.0.1:5003/", "http://127.0.0.1:5004/", "http://127.0.0.1:5005/", "http://127.0.0.1:5006/", "http://127.0.0.1:5007/","http://127.0.0.1:5009/", "http://127.0.0.1:5010/", "http://127.0.0.1:5011/"]

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

def resetCommmits():
    for count in range(len(listOfCommits)):
        dictOfCommits[count] = [listOfCommits[count], False, False, 0] 


def computePerNode(maxNodes):
    count = 0
    threads = {}
    for address in listOfWorkers:
        if count <= maxNodes:
            threads[address] = threading.Thread(target = workerThreadFunction, args = (address,))
            ((threads[address]).start())
            print("Thread started on:", address)
            count += 1
        else:
            return threads 
    return threads

    




if __name__ == "__main__":

    #First, get repository name
    response = requests.get(REPO_LINK)
    response = response.json()
    repoName = response['name']
    print(repoName)

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
    
    for i in range(10):
        resetCommmits()
        print("Running with", i + 1, "worker(s)")
        start_time = time.time()
        threads = computePerNode(i)

        #Wait for all the threads to finish
        for thread in threads.values():
            thread.join()   
        timeTaken =  (time.time() - start_time)
        times.append(timeTaken)
        print("Time taken:", times[i], "seconds")

    

    #time.sleep(5)
    
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
    
#    print("\n--- %s seconds ---" % (time.time() - start_time))

    for i in range(len(times)):
        print(i+1, "Node(s) takes", times[i], "seconds.")


objects = ('1 Node', '2 Nodes', '3 Nodes', '4 Nodes', '5 Nodes', '6 Nodes', "7 nodes", "8 Nodes", "9 Nodes", "10 Nodes")
y_pos = np.arange(len(objects))
performance = times
 
plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Time Taken (s)')
plt.title('Time taken with various number of nodes.')
 
plt.show()