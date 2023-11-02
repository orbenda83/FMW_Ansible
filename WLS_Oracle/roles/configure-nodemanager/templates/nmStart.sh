#! /bin/bash
# set -x
#
# @Created By Or Ben-David - Oracle ACS
# @Modified on 2020-04-01
#
# Variable Selection
#==========================================


# Check if Node Manager Is running
NMCHK=$({{ wls_domain_home }}/bin/manageNM.sh status | grep pid | wc -l)

if [ $NMCHK = '0' ];
then
  sudo systemctl restart nodemanager_{{ wls_domain_name }}.service
fi

sleep 10

