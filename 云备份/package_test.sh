#!/bin/bash

#Date    : 2017-05-12
#Author  : Victor Lyu

CONFIG_PATH=  
JOB_PATH=
PACKAGE_PATH=
LOG_PATH=
STAG_PATH=
REMOVE_PACKAGE=0


function usage()
{
	let exitcode=0
    if [ "$1" != "" ]; then
        echo
        echo "ERROR: $1"
        let exitcode=1
    fi

    cat <<EOF

Usage: package_test [-c config-path] [-j job-path]
                    [-p package-path] [-r][--help]
where:
	-c config-path
	Specifies a path to an exting TRAM configuration file that will be used
	for gathering setup parameters, and be used to establish the config files
	for this setup instance.

	-j job-path
	Specifies a path where your jobs saved
	
	-s local staging dir path
	Specifies the local staging dir path like this: /home/vlyu/ngenPack
	
	-p remote package dir path
	Specifies the remote(cluster) package dir where you want to copy local package to cluster
	
	-l logFile-path
	Spcifies a path where you want to log test result into file. This is optional which is only used in daily email check.
	
	-r
	remove all existing files and subdirs under staging-path and package-path. Please ensure that you don't have important files in this path.
	
	--help
	Prints this message and exits.
EOF

    exit $exitcode
}

inputConfigPath=0
inputJobPath=0
inputStagPath=0
inputPackagePath=0

while [ "$1" != "" ]; do
    arg=$1
    if [ "$arg" = "--help" ]; then
        usage
	elif [ "$arg" = "-c" ]; then
		inputConfigPath=1
		shift
			if [ "$1" != "" -a -e "$1" ]; then
				CONFIG_PATH="$1"
				if [ ! -d "$CONFIG_PATH" ]; then
					usage "CONFIG_PATH does not exist"
				fi
				
				if [ ! -f $CONFIG_PATH/tram_system.config ]; then
					usage "this CONFIG_PATH does not contain tram_system.config"
				fi
				if [ ! -f $CONFIG_PATH/../setup_tram.in ]; then
					usage "$CONFIG_PATH/../ does not contain setup_tram.in."
				fi
			else
				usage "missing or invalid value for $arg option"
			fi
	
	elif [ "$arg" = "-j" ]; then
		inputJobPath=1
		shift
			if [ "$1" != "" -a -e "$1" ]; then
				JOB_PATH="$1"
				if [ ! -d "$JOB_PATH" ]; then
					usage "JOB_PATH does not exist"
				fi
				
				if [ ! -d $JOB_PATH/DB ]; then
					usage "this JOB_PATH does not contain DB directory. Path should be like this: /gpfs/users/vlyu/testjob/testlmc"
				fi
			else
				usage "missing or invalid value for $arg option"
			fi
	
	elif [ "$arg" = "-p" ]; then
		inputPackagePath=1
		shift
			if [ "$1" != "" ]; then
				PACKAGE_PATH="$1"
				
				#check PackagePath
				if [ ${PACKAGE_PATH:0:6} != "/gpfs/" ];then
					usage "PACKAGE_PATH's format is wrong. It should be like this: /gpfs/DEV/... or /gpfs/users/... .Please check your package path."
				fi

				if [ ! -d "$PACKAGE_PATH" ]; then
					echo "PACKAGE_PATH does not exist.Automatically creating directory.................."
					mkdir -p "$PACKAGE_PATH"
				fi
			else
				usage "missing or invalid value for $arg option"
			fi
			
	elif [ "$arg" = "-s" ]; then
	inputStagPath=1
	shift
		if [ "$1" != "" ]; then
			STAG_PATH="$1"
			if [ ! -d "$STAG_PATH" ]; then
				echo "Local staging path does not exist.Automatically creating directory.................."
				mkdir -p "$STAG_PATH"
			fi
		else
			usage "missing or invalid value for $arg option"
		fi
		
	elif [ "$arg" = "-l" ]; then
		shift
			if [ "$1" != "" ]; then
				LOG_PATH="$1"
				if [ ! -f "$LOG_PATH" ]; then
					echo "Log file does not exist.Automatically creating file.................."
					touch "$LOG_PATH"
				fi
			else
				usage "missing or invalid value for $arg option"
			fi
	elif [ "$arg" = "-r" ]; then
        REMOVE_PACKAGE=1	
	else
		usage "Invalid option......................."
	fi
	shift
done

#check whether the parameters are enough
if [ $inputPackagePath = 0 ]; then
	usage "Please input package path."
fi
if [ $inputConfigPath = 0 ]; then
	usage "Please input config path."
fi
if [ $inputJobPath = 0 ]; then
	usage "Please input job path."
fi
if [ $inputStagPath = 0 ]; then
	usage "Please input local staging path."
fi


function log()
{
	if [ "$LOG_PATH" != "" ];then
		echo -e "Tram-Ngen test was fail.\nERROR: $1\nPlease check the test manually." >> $LOG_PATH
	 #else do not need to log
	fi
}

function testFail()
{
	let exitcode=0
    if [ "$1" != "" ]; then
        echo
        echo "ERROR: $1"
		echo "Tram-Ngen testing fail."
		log "$1"
        let exitcode=1
    fi
	
	exit $exitcode
}

VERSION=`grep VERSION ./../src/python/shared/tram_version.py | awk -F= '{print $2}'| sed -e 's/[ "]//g'`   #get the tramNgen version

#get the master host
TRAM_MASTER=$(python << END
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

if [[ $TRAM_MASTER = "" ]];then
	testFail "Cannot read tram-master's name from ${CONFIG_PATH}/tram_system.config"
else
	echo -e "Master hostname is: $TRAM_MASTER\n"
fi

if [ $REMOVE_PACKAGE = 1 ]; then
	echo "rm -rf $STAG_PATH/*"
	rm -rf $STAG_PATH/*
	if [ $? -ne 0 ];then
		testFail "rm -rf $STAG_PATH/* fail."
	fi
	echo "rm -rf $PACKAGE_PATH/*"
	rm -rf $PACKAGE_PATH/*
	if [ $? -ne 0 ];then
		testFail "rm -rf $PACKAGE_PATH/* fail."
	fi
fi


#make package to local staging path
../build/make_package.sh $STAG_PATH
if [ $? -ne 0 ];
then
	testFail "Make package fail."
fi

#scp the package to cluster's PACKAGE_PATH and then extract it
cp -f $STAG_PATH/$VERSION.tar.gz $PACKAGE_PATH
echo -e "Extract the package...................\n"
tar xvf $PACKAGE_PATH/$VERSION.tar.gz -C $PACKAGE_PATH

#copy the package_test_cluster.sh
cp ./package_test_cluster.sh $PACKAGE_PATH/$VERSION/debug/

echo "Jumping to fnode to run package_test_cluster.sh";
ssh -t ${TRAM_MASTER} "hostname;$PACKAGE_PATH/$VERSION/debug/package_test_cluster.sh ${CONFIG_PATH} ${JOB_PATH} ${LOG_PATH}"

