#!/bin/bash

#Date    : 2017-05-12
#Author  : Victor Lyu

function usage()
{
	let exitcode=0

    cat <<EOF

	Usage:
	Please attach your config-path and job-path:
	./package_test_cluster.sh CONFIG_PATH JOB_PATH
	
EOF

    exit $exitcode
}
if [[ "$1" != "" ]];then
    arg=$1
    if [ "$arg" = "--help" -o "$arg" = "-h" ]; then
        usage
	fi
fi


echo $*

CONFIG_PATH="$1" 
JOB_PATH="$2"
LOG_PATH="$3"

SCRIPT_DIR="$(readlink -f $(dirname "$0"))"


#get the leader server
LEADER_SERVER=$(python << END
import json, sys
with open("${CONFIG_PATH}/tram_system.config") as f:
	cfg_lines = []
	for l in f.readlines():
		if l.strip().startswith("#") is False:
			cfg_lines.append(l)
		cfg = '\n'.join(cfg_lines)
config = json.loads(cfg)
print(config["TRAM-SERVERS"]["TRAMServer-0"]["hostname"])
END
)


#get the slave server 1
SLAVE_SERVER1=$(python << END
import json, sys
with open("${CONFIG_PATH}/tram_system.config") as f:
	cfg_lines = []
	for l in f.readlines():
		if l.strip().startswith("#") is False:
			cfg_lines.append(l)
		cfg = '\n'.join(cfg_lines)
config = json.loads(cfg)
print(config["TRAM-SERVERS"]["TRAMServer-1"]["hostname"])
END
)

#get the slave server 2
SLAVE_SERVER2=$(python << END
import json, sys
with open("${CONFIG_PATH}/tram_system.config") as f:
	cfg_lines = []
	for l in f.readlines():
		if l.strip().startswith("#") is False:
			cfg_lines.append(l)
		cfg = '\n'.join(cfg_lines)
config = json.loads(cfg)
print(config["TRAM-SERVERS"]["TRAMServer-2"]["hostname"])
END
)

#get the work dir path from tram_params.config file
WORK_DIR=$(python << END
import json, sys
with open("${CONFIG_PATH}/tram_params.config") as f:
	cfg_lines = []
	for l in f.readlines():
		if l.strip().startswith("#") is False:
			cfg_lines.append(l)
		cfg = '\n'.join(cfg_lines)
config = json.loads(cfg)
print(config["TRAM-SERVER-PARAMETERS"]["tram_work_dir"])
END
)

if [[ $SLAVE_SERVER1 = "" ]];then
	testFail "Cannot read slave-server1's name from tram_system.config"
fi
if [[ $SLAVE_SERVER2 = "" ]];then
	testFail "Cannot read slave-server2's name from tram_system.config"
fi
if [[ $WORK_DIR = "" ]];then
	testFail "Cannot read work-dir-path from tram_params.config"
fi

TRAM_MASTER=$(hostname)

#log the package test result in file for daily checking
function log()
{
	if [[ "$LOG_PATH" != "" ]];then 
		result=$1
		if [[ "$result" = "success" ]];then
			echo "Tram-Ngen test was success.No problem." >> $LOG_PATH		
		else
			echo -e "Tram-Ngen test was fail.\nERROR: $result\nPlease check the test manually." >> $LOG_PATH
			echo "tram log path is $WORK_DIR/log/tram-$LEADER_SERVER.log" >> $LOG_PATH
			echo "job log path is $JOB_PATH/h/work/ram" >> $LOG_PATH
		fi
	 #else do not need to log
	fi
}

function testFail()
{
	let exitcode=0
    if [[ "$1" != "" ]]; then
        echo
        echo "ERROR: $1"
		echo "Tram-Ngen testing fail."
		log "$1"
        let exitcode=1
    fi
	
	exit $exitcode
}

function killProcessManually()
{
	echo "Killing related process manually........."
	#kill tram process
	$SCRIPT_DIR/../etc/tram.sh killcluster
	
	#kill db process
	$SCRIPT_DIR/../etc/tramdb.sh stopcluster
}

function stopSystem()
{	
	#stop tram system
	echo "stoping system..................";
	$SCRIPT_DIR/../etc/tram.sh stopsystem
	if [ $? -ne 0 ];then
		killProcessManually
		testFail "Stop system was fail."
	fi
}

#setup tram
echo "setup tram......................";
$SCRIPT_DIR/../setup_tram.sh --input $CONFIG_PATH/../setup_tram.in --yes --user $USER --group PLT --nopasswd <<< "\nyes\n"
if [ $? -ne 0 ];  #setup fail
then
	testFail "setup failed"
fi


#do the initial of tram(mainly database)
echo "init tram system.........................";
$SCRIPT_DIR/../etc/tramdb.sh initcluster yes
if [ $? -ne 0 ]; 
then
	testFail "Init failed"
fi

#start tram system
echo "start tram system......................";
$SCRIPT_DIR/../etc/tram.sh startsystem
if [ $? -ne 0 ] 
then
	echo "start tram system failed";
	stopSystem
	testFail "start failed"
fi

#modify the opc_tram_test.sh
sed -i "16c\JOBDIR=$JOB_PATH" $SCRIPT_DIR/../demo/opc_tram_test.sh 
sed -i '41d' $SCRIPT_DIR/../demo/opc_tram_test.sh 


BJOB_ROOT=/gpfs/software/openlava_dev/3.3.3/bin
num1=$($BJOB_ROOT/bjobs | wc -l)

#upload jobs
echo "Uploading jobs......................................";
$BJOB_ROOT/bsub -J job1 -o $JOB_PATH/ngen.log -e $JOB_PATH/ngen_err.log $SCRIPT_DIR/../demo/opc_tram_test.sh
if [ $? -ne 0 ] 
then
	echo "Upload jobs fail. Tram system will be stopped";
	stopSystem
	testFail "Upload jobs failed"
fi

startTime=$(date +%s)

#check the test
echo "Checking the test.............";
isTimeOut=0
num2=$($BJOB_ROOT/bjobs | wc -l)
#check the job is submitted successfully
until [ $[num2 - num1] -gt 3 -o $num2 -eq 0 ]
do
	echo "Waiting for the jobs submitting..........";
	endTime=$(date +%s)
	timeWaste=$[endTime - startTime]
	if [ $timeWaste -gt 120 ];
	then
		echo "Time out.......................";
		isTimeOut=1
		break
	fi
	num2=$($BJOB_ROOT/bjobs | wc -l)
	sleep 3
done

if [ $isTimeOut -eq 1 -o $num2 -eq 0 ];
then
	stopSystem
	testFail "Job submitting was time-out(120s).";
else
	echo "Job submit successfully........................";
fi

$BJOB_ROOT/bjobs

echo
echo "Killing jobs...................";
#kill all the unfinished jobs
$BJOB_ROOT/bkill 0

until [ $num2 -eq 0 ]
do
	echo "Waiting for all jobs killed...........................";
	sleep 3
	num2=$($BJOB_ROOT/bjobs | wc -l)
done

stopSystem
echo
echo "Tram-Ngen testing success"
log "success"
exit 0
