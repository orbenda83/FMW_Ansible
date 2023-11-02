#! /bin/bash
# set -x
#
# @Created By Or Ben-David - Oracle ACS
# @Modified on 2020-04-01
#
# Variable Selection
#==========================================
# List process monitor in the variable below.
PROGRAM1="{{ admin_server_name }}"
PROGRAM2="weblogic.NodeManager"

# Weblogic home definition
WLS_HOME={{ wl_server_home }}

# Check if Node Manager Is running
NMCHK=$({{ wls_domain_home }}/bin/manageNM.sh status | grep pid | wc -l)

if [ $NMCHK = '0' ];
then
  sudo systemctl restart nodemanager_{{ wls_domain_name }}.service
fi

sleep 30

# wait for NM to start
x=5
while [ \($NMCHK = '0'\) -a \(x > 0\) ];
do
  sleep 5;
  x=$x-1
  NMCHK=$(/opt/oracle/middleware/user_projects/domains/bpm_domain/bin/manageNM.sh status | grep pid | wc -l);
done

# Variable checks to see if $PROGRAM1 is running.
APPCHK=$(ps aux | grep -i 'java' | grep -i $PROGRAM1 | grep -i '{{ wls_domain_home }}' | grep -v grep | wc -l)

#======================================================================================
# The 'if' statement below checks to see if the process is running with the 'ps' command.
# If the value returned as a '0' then the process will start.
if [ $APPCHK != '0' ];
then
  echo "AdminServer of {{ wls_domain_name }} is already running."
else
  echo "AdminServer of {{ wls_domain_name }} is not running. Starting AdminServer instance."
  {{ wlst_command }} {{ wls_domain_home }}/bin/nmStartAdmin.py
fi

exit
