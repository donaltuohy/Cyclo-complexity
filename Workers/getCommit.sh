#!/bin/bash

##First Arg =   workerID
##Second Arg =  repo_name
##Third Arg =   SHA
echo $2
echo  '/home/donal-tuohy/Documents/SS_year/Cyclo-complexity/Workers/worker'$1'/'$2

cd '/home/donal-tuohy/Documents/SS_year/Cyclo-complexity/Workers/worker'$1'/'$2

git checkout $3
