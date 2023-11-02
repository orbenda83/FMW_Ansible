#! /bin/bash
# set -x
#
# Created By Or Ben-David - Oracle ACS
#
# Variable Selection
#==========================================
# List process monitor in the variable below.
PROGRAM1="AdminServer"
PROGRAM2="weblogic.NodeManager"
# Check for the current user.
USER_NAME="osb"
# Weblogic home definition
WLS_HOME=/opt/fmw/Middleware/wlserver_10.3


if [ $USER_NAME != $USER ];
then
  echo "The script is running from the wrong user. Please login as "$USER_NAME"!"
else
  echo "The script is running from the right user. ;)"
  
  # Check if Node Manager Is running
  NMCHK=$(ps aux | grep $PROGRAM2 | grep $USER_NAME | grep -v "grep $PROGRAM2" | wc -l)

  if [ $NMCHK = '0' ];
  then
    $WLS_HOME/server/bin/nmStart.sh
  fi

  # Variable checks to see if $PROGRAM1 is running.
  APPCHK=$(ps aux | grep $PROGRAM1 | grep $USER_NAME | grep -v "grep $PROGRAM1" | wc -l)
  
  #======================================================================================
  # The 'if' statement below checks to see if the process is running with the 'ps' command.
  # If the value returned as a '0' then the process will start.
  
  if [ $APPCHK != '0' ];
  then
    echo "AdminServer of "$USER_NAME" is already running."
  else
    echo "AdminServer of "$USER_NAME" is not running. Starting AdminServer instance."
    nohup $WLS_HOME/common/bin/wlst.sh $WLS_HOME/server/bin/nmStartAdmin.py > admin.out &
  fi

fi
exit
