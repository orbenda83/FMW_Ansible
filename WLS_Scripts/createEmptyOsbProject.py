# Script to List All the OSB projects, Business Services and Proxy Services deployed in sbconsole
# Single Project Example: 
# /opt/oracle/middleware/oracle_common/common/bin/wlst.sh createEmptyOsbProject.py <admin server hostname> <Username> <password> <project_name> <Y - multi projects split by ','/N- single project>
#
# Multiple services Example (read from file):
# cat .servicesToCreate | while read line; do /opt/oracle/middleware/oracle_common/common/bin/wlst.sh createEmptyOsbProject.py  <admin server hostname> <Username> <password> $line Y; done
# .servicesToCreate file consosts of comma seperated lines os services
# For example:
# project1,project2,project3
# project4,project5

import sys
import os
import socket

from com.bea.wli.sb.management.configuration import ALSBConfigurationMBean
from com.bea.wli.config import Ref
from java.lang import String
from com.bea.wli.sb.util import Refs
from com.bea.wli.sb.management.configuration import CommonServiceConfigurationMBean
from com.bea.wli.sb.management.configuration import SessionManagementMBean
from com.bea.wli.sb.management.configuration import ProxyServiceConfigurationMBean
from com.bea.wli.monitoring import StatisticType
from com.bea.wli.monitoring import ServiceDomainMBean
from com.bea.wli.monitoring import ServiceResourceStatistic
from com.bea.wli.monitoring import StatisticValue
from com.bea.wli.monitoring import ServiceDomainMBean
from com.bea.wli.monitoring import ServiceResourceStatistic
from com.bea.wli.monitoring import StatisticValue
from com.bea.wli.monitoring import ResourceType

hostname=sys.argv[1]
port=7001
username=sys.argv[2]
password=sys.argv[3]
project=sys.argv[4]
if_multi=sys.argv[5]

connect(username, password, "t3://" + hostname + ":" + str(port))

domainRuntime()

sessionName = String("SessionScript"+Long(System.currentTimeMillis()).toString())
SessionMBean = findService("SessionManagement", "com.bea.wli.sb.management.configuration.SessionManagementMBean")
SessionMBean.createSession(sessionName)
print SessionMBean

# alsbCore = findService(ALSBConfigurationMBean.NAME, ALSBConfigurationMBean.TYPE)
ALSBConfigurationMBean = findService(String("ALSBConfiguration.").concat(sessionName), "com.bea.wli.sb.management.configuration.ALSBConfigurationMBean")
print ALSBConfigurationMBean
refs = ALSBConfigurationMBean.getRefs(Ref.DOMAIN)
# print refs

dummyRef=Ref(Ref.PROJECT_REF,Ref.DOMAIN,"Dummy")
if if_multi == 'N':
  # alsbCore.clone()
  projectRef=Ref(Ref.PROJECT_REF,Ref.DOMAIN,project)
  print projectRef
  # folderRef=Ref(Ref.FOLDER_REF,Ref.DOMAIN,project+"Proxy_Services")
  # print folderRef
  # ALSBConfigurationMBean.createProject(projectRef, String("Project named.").concat(project))
  # ALSBConfigurationMBean.createFolder(folderRef, String("Folder named.").concat(project))
  
  ALSBConfigurationMBean.clone(dummyRef,projectRef)
else:
  projectArray=project.split(',')
  for proj in projectArray:
    projectRef=Ref(Ref.PROJECT_REF,Ref.DOMAIN,proj)
    print projectRef 
    ALSBConfigurationMBean.clone(dummyRef,projectRef)
    
SessionMBean.activateSession(sessionName, "Complete create of " + project+".")
# SessionMBean.discardSession(sessionName)

# conn.close()
disconnect()
exit()
