import flask, requests, git, os, sys, subprocess
from flask import Flask, request, jsonify
from radon.complexity import SCORE, cc_visit, cc_rank
from radon.metrics import mi_parameters



#returns the Id of this current node
def getWorkerID():
    if(len(sys.argv) > 0):
        return int(sys.argv[1])
    return 1

reposName = "CS4400---Internet-Applications"
workerID = getWorkerID()

###########General Config###########
Main_FOLDER = "/home/donal-tuohy/Documents/SS_year/Cyclo-complexity/Workers"
Worker_FOLDER = "/home/donal-tuohy/Documents/SS_year/Cyclo-complexity/Workers/worker" + str(workerID)
MAIN_SERVER = "http://127.0.0.1:5000/"

###Flask Config###
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisShouldBeSecret'

###########Local functions###########

    
#returns the Id of this current node
def getWorkerID():
    if(len(sys.argv) > 0):
        return int(sys.argv[1])
    return 1

#Returns a file from the local directory
def getFile(filePath):
    fileRead = open(filePath, 'r+t')
    source = fileRead.read()
    return source     

def setRepoName(repoName):
    reposName = repoName

def cloneRepo(cloneURL):
    print("WorkerID = ", workerID)
    subprocess.call(["bash", Main_FOLDER + "/getRepo.sh",str(workerID), cloneURL])

def checkoutCommit(sha):
    print("Checking out " + sha)
    print("Repo Name:", reposName)
    subprocess.call(["bash", Main_FOLDER + "/getCommit.sh",str(workerID), reposName, sha])

def getListOfFiles():
    listOfFiles =[]
    for path, subdirs, files in os.walk(Worker_FOLDER):
        for filename in files:
            if(filename.endswith('.py')):
                f = os.path.join(path, filename)
                listOfFiles.append(f)
    return listOfFiles    

def getComplexityScore(source):
    try:
        RadonList = mi_parameters(source)
        return RadonList[1]
    except:
        print("Unable to compute complexity for this file.")
        return -1

def getComplexityAverage():
    sum = 0
    listOfFiles = getListOfFiles()
    totalFiles = len(listOfFiles)
    for filename in listOfFiles:
        print("Computing: ", filename)
        source = getFile(filename)
        sum += getComplexityScore(source)
    return sum/totalFiles
    
###########Flask Endpoints###########
@app.route('/getrepo', methods=['POST'])
def getRepo():
    serverJson = request.get_json()
    cloneURL = serverJson['cloneURL']
    repoName = serverJson['repoName']
    setRepoName(repoName)
    cloneRepo(cloneURL)
    return "Repo Downloaded"

@app.route('/compute', methods=['POST'])
def computeComplexity():
    requestJSON = request.get_json()
    sha = requestJSON['sha']
    checkoutCommit(sha)
    ###Call 
    complexity = getComplexityAverage()
    print("Complexity has been computed.")
    return jsonify({'complexityScore' : complexity })


if __name__ == "__main__":

    workerID = getWorkerID()

    directory = 'worker' + str(workerID) 
    if not os.path.exists(directory):
        os.makedirs(directory)

    portNum = 5000 + workerID

    app.run(debug=True, port=portNum)

