#!/bin/bash

#Latest modify Date: 2017-05-12
#Author  : Victor Lyu

PASSWORD=
TEST=false

function usage()
{
	let exitcode=0
    if [ "$1" != "" ]; then
        echo
        echo "ERROR: $1"
        let exitcode=1
    fi
	
    cat <<EOF

This file will check whether the Tram-Ngen project's code was changed :
If yes, then package test will be triggered, otherwise will not.
And the package test result will be throwed by email(Victor + Yao-bin + Liang Zhao).

Usage:
-p password
input your p4 password
-t 
means for personal test,ignore p4 sync and send email to Victor only
EOF

    exit $exitcode
}

while [ "$1" != "" ]; do
    arg=$1
    if [ "$arg" = "--help" -o "$arg" = "-h" ]; then
        usage
	elif [ "$arg" = "-p" ]; then
		shift
		if [ "$1" != "" ]; then
			PASSWORD="$1"
		else
			usage "missing or invalid value for $arg option"
		fi
	elif [ "$arg" = "-t" ]; then
		TEST=true
	else
		usage "Invalid option......................."
	fi	
	shift
done

if [ "$PASSWORD" = "" ]; then
	usage "Please input your password."
fi

homePath=/n/filer3b/home/dev/vlyu

#crontab doesn't import environment path, so we need to import it manually
. /etc/profile
source $homePath/.bash_profile
source $homePath/.bashrc

cd $homePath/vlyu_ngen_fdev1/
echo "$PASSWORD" | /usr/local/bin/p4 login 
if [ "$TEST" = true ];then
	syncResult="This is for testing"
else
	syncResult="$(/usr/local/bin/p4 sync)"
fi

resultFile=/gpfs/DEV/PLT/vlyu/packageTestResult.txt
logFile=/gpfs/DEV/PLT/vlyu/packageTest.log
syncResultFile=/gpfs/DEV/PLT/vlyu/syncResult.txt
configPath=/gpfs/DEV/PLT/vlyu/NgenPack/TFlex_RAM_NGen_2.0qa3/etc
jobPath=/gpfs/DEV/PLT/vlyu/testjob/testlmc
packagePath=/gpfs/DEV/PLT/vlyu/tramNgen
stagingPath=$homePath/staging

function checkFile()
{
	file=$1
	if [ ! -f "$file" ]; then
		echo "$file does not exist.Automatically creating file.................."
		touch "$file"
	fi
}

function clearFile()
{
	> $1
	> $2
	> $3
}

function sendEmail()
{
	if [ "$TEST" = true ];then
		emailAddress="victor.lyu@asml.com"
	else
		emailAddress="victor.lyu@asml.com liang.zhao@asml.com yao-bin.tang@asml.com"
	fi
	cat "$syncResultFile" | mutt -s "Tram-Ngen package test" $emailAddress -a $logFile
	#cat "$syncResultFile" | mutt -s "Tram-Ngen package test" victor.lyu@asml.com liang.zhao@asml.com yao-bin.tang@asml.com dl-brion-tram-ngen-dev@asml.com -a $logFile
}

#dynamically change the port of db server
function modifyConfigPort()
{

ServerPort=$(python << END
import json, sys
with open("${configPath}/tram_system.config") as f:
	cfg_lines = []
	for l in f.readlines():
		if l.strip().startswith("#") is False:
			cfg_lines.append(l)
		cfg = '\n'.join(cfg_lines)
config = json.loads(cfg)
print(config["TRAM-SERVERS"]["TRAMServer-0"]["port"])
END
)
	
	if [[ $ServerPort = "" ]];then
		echo "Cannot read ServerPort from tram_system.config"
		exit 1
	fi
	

DBPort=$(python << END
import json, sys
with open("${configPath}/tram_system.config") as f:
	cfg_lines = []
	for l in f.readlines():
		if l.strip().startswith("#") is False:
			cfg_lines.append(l)
		cfg = '\n'.join(cfg_lines)
config = json.loads(cfg)
print(config["TRAM-DB-SERVER"]["db_driver_mongo"]["port_number"])
END
)

	if [[ $DBPort = "" ]];then
		echo "Cannot read DBPort from tram_system.config"
		exit 1
	fi	
	
	
	#May need to change the line numbers if tram_system.config was modified
	line_num_of_first_serverport=32
	num2=$[line_num_of_first_serverport + 5]
	num3=$[num2 + 4]
	line_num_of_DBPort=62
	
	if [ $ServerPort -ge 11260 ];then
		ServerPort=11160
	else
		ServerPort=$[ServerPort + 1]
	fi
	sed -i "${line_num_of_first_serverport}c\      \"port\"     : $ServerPort," $configPath/tram_system.config
	sed -i "${num2}c\      \"port\"     : $ServerPort" $configPath/tram_system.config
	sed -i "${num3}c\      \"port\"     : $ServerPort" $configPath/tram_system.config
	
	if [ $DBPort -ge 11270 ];then
		DBPort=11171
	else
		DBPort=$[DBPort + 1]
	fi
	sed -i "${line_num_of_DBPort}c\        \"port_number\" : $DBPort" $configPath/tram_system.config
}

if [ "$syncResult" = "" ];then
	echo "No update of Tram-Ngen project's code."
else
	#check the file whether exists
	checkFile "$resultFile"
	checkFile "$logFile"
	checkFile "$syncResultFile"
	
	modifyConfigPort
	
	#clear the file
	clearFile "$logFile" "$resultFile" "$syncResultFile"
	
	echo "This email is automatically sent by system." >> $syncResultFile
	echo -e "\nTram code has been changed:\n$syncResult \n\nPackage test was triggered. Here is the package test result:" >> $syncResultFile
	
	
	cd $homePath/vlyu_ngen_fdev1/debug/
	./package_test.sh -c $configPath -j $jobPath -s $stagingPath -p $packagePath -l $resultFile -r | tee $logFile
	
	count=1
	loopTimes=3
	#continually run test until test is success or number of test times = 3
	while [ "$(cat "$resultFile")" != "Tram-Ngen test was success.No problem." ];do
		> $resultFile
		./package_test.sh -c $configPath -j $jobPath -s $stagingPath -p $packagePath -l $resultFile -r | tee $logFile
		count=$[count + 1]
		if [ $count -ge $loopTimes ];then
			break
		fi
	done
	
	result=$(cat "$resultFile")
	echo -e "\n$result\n" >> $syncResultFile
	sendEmail "$result"	
fi

