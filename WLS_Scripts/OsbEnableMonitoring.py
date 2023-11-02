##############################################################################################################################
# Scope    : To Enable the monitoring options on the proxy services deployed on the OSB.
# Process  :
#  1. Set the classpath 
#   CLASSPATH=/u01/app/oracle/product/fmw/Oracle_OSB1/lib/sb-kernel-api.jar:/u01/app/oracle/product/fmw/Oracle_OSB1/lib/sb-kernel-impl.jar:/u01/app/oracle/product/fmw/Oracle_OSB1/lib/modules/com.bea.alsb.configfwk-wls.jar:$CLASSPATH 
#  2. export CLASSPATH
#  3. set the domain  eg : . ./bin/setDomain.sh  
#  4. Update the sction below on the Enviroment specificaitons ( host,port,credentials)
#  5. execute the following command  java weblogic.WLST ProxyServiceMonotringOptions.py
################################################################################################################################## 

import javax.management
import java.util
import javax.management.remote
import javax.naming
from com.bea.wli.sb.util import Refs
# import weblogic.management.mbeanservers.domainruntime
# import com.bea.wli.sb.management.configuration
# from java.util import Hashtable
# from java.util import HashSet
# from java.util import ArrayList
# from javax.management.remote import JMXServiceURL
# from weblogic.management.mbeanservers.domainruntime import DomainRuntimeServiceMBean
# from javax.naming import Context
# from javax.management.remote import JMXConnectorFactory
# from javax.management import ObjectName
from com.bea.wli.sb.management.configuration import SessionManagementMBean
from com.bea.wli.sb.management.configuration import ALSBConfigurationMBean
# from com.bea.wli.sb.management.configuration import CommonServiceConfigurationMBean
# import weblogic.management.jmx.MBeanServerInvocationHandler
# from com.bea.wli.config import Ref
# from com.bea.wli.config.env import EnvValueQuery
# from com.bea.wli.config.env import QualifiedEnvValue
# from com.bea.wli.config.resource import DependencyQuery
# from com.bea.wli.sb.management.query import ProxyServiceQuery
# from com.bea.wli.sb.management.query import BusinessServiceQuery
# from com.bea.wli.sb.util import EnvValueTypes
# from java.util import Collection
# from java.util import Collections


def setMonitoringAllProjectsAndServices(isEnabled):
    refs = ALSBConfigurationMBean.getRefs(Ref.DOMAIN)
    # refs = configMBean.getRefs(Ref.DOMAIN)
    refsList = ArrayList()
    refsList.addAll(refs)
    
    for ref in refsList :
        print ref.getTypeId() + " => " + ref.getFullName()
        # if ref.getTypeId() == "ProxyService" :
        #     if ref.getTypeId() == "ProxyService" :
        #         isPS = "1"
        #     else:
        #         isPS =  "0"
        #     if isEnabled:
        #         print "enabling monitoring for ", ref.getFullName()
        #         proxyServiceConfigurationMBean.enableMonitoring(ref)
        #     else:
        #         print "disabling monitoring for ", ref.getFullName()
        #         proxyServiceConfigurationMBean.disableMonitoring(ref)
        #     else: 
        #         print " This is Not a Proxy", ref.getFullName()


sessionName = "MonitorUpdate"
hostname=sys.argv[1]
port=7001
username=sys.argv[2]
password=sys.argv[3]

# serviceURL=JMXServiceURL("t3", hostname, port, "/jndi/" + DomainRuntimeServiceMBean.MBEANSERVER_JNDI_NAME)
# h=Hashtable()
# h.put(Context.SECURITY_PRINCIPAL, username)
# h.put(Context.SECURITY_CREDENTIALS, password)
# h.put(JMXConnectorFactory.PROTOCOL_PROVIDER_PACKAGES, "weblogic.management.remote")

# conn = JMXConnectorFactory.connect(serviceURL, h)

connect(username, password, "t3://" + hostname + ":" + str(port))
domainRuntime()

# mbconn = conn.getMBeanServerConnection()
# sm = JMX.newMBeanProxy(mbconn, ObjectName.getInstance(SessionManagementMBean.OBJECT_NAME), SessionManagementMBean)
# sm.createSession(sessionName)
SessionMBean = findService("SessionManagement", "com.bea.wli.sb.management.configuration.SessionManagementMBean")
SessionMBean.createSession(sessionName)

# configMBean = JMX.newMBeanProxy(mbconn, ObjectName.getInstance("com.bea:Name=" + ALSBConfigurationMBean.NAME + "." + sessionName + ",Type=" + ALSBConfigurationMBean.TYPE), ALSBConfigurationMBean)
# domainService = weblogic.management.jmx.MBeanServerInvocationHandler.newProxyInstance(mbconn, ObjectName(DomainRuntimeServiceMBean.OBJECT_NAME), DomainRuntimeServiceMBean, false)
ALSBConfigurationMBean = findService(String("ALSBConfiguration.").concat(sessionName), "com.bea.wli.sb.management.configuration.ALSBConfigurationMBean")

# proxyServiceConfigurationMBean = domainService.findService(String("ProxyServiceConfiguration.").concat(sessionName),'com.bea.wli.sb.management.configuration.ProxyServiceConfigurationMBean', None)


setMonitoringAllProjectsAndServices(true)

# SessionMBean.activateSession(sessionName, "Complete enable/disable service monitoring")
SessionMBean.discardSession(sessionName)

# conn.close()
disconnect()
exit()
