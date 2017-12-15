# Cyclo-complexity

Student Name:   Donal Tuohy

Student Number: 14313774

## Overview
For this assignment I decided to use the request and flask libraries in python as I had gained a strong understanding of them after building the distributed file system.

 This system consists of two python files and two bash scripts:

 ### mainServer.py
 This file is run once and is the manager of all the workers running. It is the script which communicates with the github API and parses all the information about the repo we are interested in.

 When run, this script connects to githubs API and gets all the details about the repository and a list of all its commits. It also sends out a link to each worker which they use to clone the repository into their local directory.

 When each worker has cloned the repo, this script begins to start individual threads for each worker. Each thread will then take a commit for which the cyclometic complexity has not been computed yet and return its average complexity. 

 Each thread will keep grabbing and computing commits until every commit has been complete.

 This script then outputs the results and the time taken with various nodes.

 To run this script in terminal, set up all your workers and then set the path to the file's directory and call:

 >python3.6 mainServer.py

 ### worker.py
This file is run for every worker you want on the system. It is passed in a worker ID which distinguishes it form other workers.

When it is started, it creates a local directory eg.worker2 where it stores the repository that the server tells it to clone. 

The workers make good use of the python module *subprocess* which allows bash scripts to be called within a python program. Using this I was able to use two bash scripts, one to clone a given repository and one to rollback to a certain commit given it's sha.

The Radon libary was used to calculate the complexity of python files.
When a commit has been rolled back, the worker steps through each python file in that commit and calculates the average complexity of the whole commit. It then returns this value to the server and begins working on the next commit until there are none left. 

To run this script in terminal, set the path to the file's directory and call:

> python3.6 worker.py workerID(int)

## Evaluation

I evaluated my program on two different repositories, one being quite small and the other being quite large:

* [My Chat Server](https://github.com/donaltuohy/CS4400---Internet-Applications)
* [Python Repository](https://github.com/python/pythondotorg)

The program begins computing the complexity with just one node and then begins to scale up until ten nodes are used to calulate the complexity.

As you can see from both figure 1 and figure 2, the general shape of the graph is similiar. It is clear that parrellelisation of the workload has a much greater effect when there is less nodes. This is expected. Also the program was run locally so a lack of computing power is also a reason for the time taken begining to plateau as more nodes are added.

One problem I could see with my program is if there there is only a small number of commits, parrallelisation will only work up until the number of nodes is qula to the number of commits. 
This is because I am passing a commit to each worker rather than an indivdual file. If there was more workers than commits, some workers would not be passed a commit to compute and would just sit there idle.

If I had the time to change this problem I would instead pass a file name to each worker so that there would be plenty of work to be distributed between workers.   

![myrepo](https://user-images.githubusercontent.com/20796292/34058730-10f8f70a-e1d4-11e7-9fa8-28e1d7cccd0f.png)
*Figure 1: Complexity of small repo computed with various amount of nodes*

![pythonrepo](https://user-images.githubusercontent.com/20796292/34058733-15093d78-e1d4-11e7-9587-ef87457feb68.png)
*Figure 2: Complexity of large repo computed with various amount of nodes* 


