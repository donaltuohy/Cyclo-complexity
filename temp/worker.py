import flask, requests, git, os, sys, subprocess
from flask import Flask, request, jsonify
from radon.complexity import SCORE, cc_visit, cc_rank
from radon.metrics import mi_parameters

###########General Config###########
REPO_FOLDER = "/home/donal-tuohy/Documents/CRC_Repo/CS4400---Internet-Applications/"
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

def getRepoURL():
    if(len(sys.argv) > 1):
        return sys.argv[2]
    return "Error"

#Returns a file from the local directory
def getFile(filePath):
    fileRead = open(REPO_FOLDER + filePath, 'r+t')
    source = fileRead.read()
    return source     

def resetRepo():
    workerID = getWorkerID()
    repoURL = getRepoURL()
    print("WorkerID = ", workerID)
    subprocess.call(getRepo, workerID, repoURL, repoName)

    

def getComplexityScore(source):
    RadonList = mi_parameters(source)
    return RadonList[1]

###########Flask Endpoints###########
@app.route('/compute', methods=['POST'])
def computeComplexity():
    requestJSON = request.get_json()
    filePath = requestJSON['sha']

    ###Call 
    complexity = getComplexityScore(fileCode)
    print("Complexity has been computed.")
    return jsonify({'complexityScore' : complexity })



if __name__ == "__main__":

    workerID = getWorkerID()
    repoCloneURL = getRepoURL()

    directory = 'worker' + str(workerID) 
    if not os.path.exists(directory):
        os.makedirs(directory)
    app.run(debug=True)

