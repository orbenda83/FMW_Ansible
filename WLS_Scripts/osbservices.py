# Script to List All the OSB projects, Business Services and Proxy Services deployed in sbconsole
import sys
import os
import socket

connect('weblogic', '<WLS_PASSWORD>', 't3://<ADMIN_HOST>:<ADMIN_PORT>')

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

domainRuntime()

alsbCore = findService(ALSBConfigurationMBean.NAME, ALSBConfigurationMBean.TYPE)
refs = alsbCore.getRefs(Ref.DOMAIN)
it = refs.iterator()
print "List of Project in OSB"
while it.hasNext():
    r = it.next()
    if r.getTypeId() == Ref.PROJECT_REF:      
        print "Project Name : " + (r.getProjectName())

allRefs= alsbCore.getRefs(Ref.DOMAIN)
print "List of Proxy Service"
for ref in allRefs:  
  typeId = ref.getTypeId()
  if typeId == "ProxyService":    
     print "Proxy Service: " + ref.getFullName()
allRefs= alsbCore.getRefs(Ref.DOMAIN)
print "List of Business Service"
for ref in allRefs:
  typeId = ref.getTypeId()
  if typeId == "BusinessService":         
     print "Business Service: " + ref.getFullName()
disconnect()
exit()
