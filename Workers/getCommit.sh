#!/bin/bash

##First Arg =   workerID
##Second Arg =  repo_name
##Third Arg =   SHA
 
cd '/home/donal-tuohy/Documents/SS_year/Cyclo-complexity/Workers/worker'$1'/'$2

git checkout $3
