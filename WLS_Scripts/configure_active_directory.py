#!/usr/bin/python

import time
import getopt
import os.path
import sys
import re

# Get location of the properties file.
#properties = ''
#try:
#   opts, args = getopt.getopt(sys.argv[1:],"p:h::",["properies="])
#except getopt.GetoptError:
#   print 'create_cluster.py -p '
#   sys.exit(2)
#for opt, arg in opts:
#   if opt == '-h':
#      print 'create_cluster.py -p '
#      sys.exit()
#   elif opt in ("-p", "--properties"):
#      properties = arg
#print 'properties=', properties

# Load the properties from the properties file.
from java.io import FileInputStream
 
envproperty=""
if (len(sys.argv) > 1):
	envproperty=sys.argv[1]
else:
	print "Environment Property file not specified"
	sys.exit(2)
propInputStream=FileInputStream(envproperty)
configProps = Properties()
configProps.load(propInputStream)

# Set all variables from values in properties file.
adminUsername=configProps.get("admin.username")
adminPassword=configProps.get("admin.password")
adminURL=configProps.get("admin.url")
domainName=configProps.get("domain.name")
providerName=configProps.get("provider.name")
adUsername=configProps.get("ad.username")
adPassword=configProps.get("ad.password")
adPrincipal=configProps.get("ad.principal")
adHost=configProps.get("ad.host")
ldport=configProps.get("ad.port")
ldapSSL=configProps.get("ad.ssl")
adUserObjectClass=configProps.get("ad.user.object.class")
adGroupBaseDN=configProps.get("ad.group.base.dn")
adUserBaseDN=configProps.get("ad.user.base.dn")

# Display the variable values.
print 'adminUsername=', adminUsername
print 'adminPassword=', adminPassword
print 'adminURL=', adminURL
print 'domainName=', domainName
print 'providerName=', providerName
print 'adUsername=', adUsername
print 'adPassword=', adPassword
print 'adPrincipal=', adPrincipal
print 'adHost=', adHost
print 'adUserObjectClass=', adUserObjectClass
print 'adGroupBaseDN=', adGroupBaseDN
print 'adUserBaseDN=', adUserBaseDN

# Connect to the AdminServer.
connect(adminUsername, adminPassword, adminURL)

edit()
# make the default authenticator sufficient
startEdit()
cd('/SecurityConfiguration/' + domainName + '/Realms/myrealm/AuthenticationProviders/DefaultAuthenticator')
cmo.setControlFlag('SUFFICIENT')

activate()

startEdit()

# Configure Active Directory.
cd('/SecurityConfiguration/' + domainName + '/Realms/myrealm')
cmo.setSecurityDDModel('Advanced')
cmo.setDeployRoleIgnored(false)
cmo.setDeployPolicyIgnored(false)
cmo.createAuthenticationProvider(providerName, 'weblogic.security.providers.authentication.ActiveDirectoryAuthenticator')

cd('/SecurityConfiguration/' + domainName + '/Realms/myrealm/AuthenticationProviders/' + providerName)
cmo.setControlFlag('OPTIONAL')

cd('/SecurityConfiguration/' + domainName + '/Realms/myrealm')
set('AuthenticationProviders',jarray.array([ObjectName('Security:Name=myrealm' + providerName), ObjectName('Security:Name=myrealmDefaultAuthenticator'), ObjectName('Security:Name=myrealmDefaultIdentityAsserter')], ObjectName))

cd('/SecurityConfiguration/' + domainName + '/Realms/myrealm/AuthenticationProviders/' + providerName)
cmo.setControlFlag('SUFFICIENT')
cmo.setUserNameAttribute(adUsername)
cmo.setPrincipal(adPrincipal)
cmo.setHost(adHost)
cmo.setPort(int(ldport))
cmo.setSSLEnabled(bool(ldapSSL))
cmo.setUserObjectClass(adUserObjectClass)
cmo.setCredential(adPassword)
cmo.setGroupBaseDN(adGroupBaseDN)
cmo.setUserBaseDN(adUserBaseDN)
#cmo.setAllUsersFilter('(&(uid=*)(objectclass=user))')
#cmo.setAllGroupsFilter('(&(cn=*)(objectclass=group))')
cmo.setGroupFromNameFilter('(&(cn=%g)(objectclass=group))')
cmo.setUserFromNameFilter('(&(uid=%u)(objectclass=person))')
cmo.setStaticGroupNameAttribute('cn')

# prevents cyclically nested AD groups from causing the JVM to seg fault (kinda bad)
print "*** Limiting nested group membership searching to 10 levels..."
cmo.setGroupMembershipSearching('limited')
cmo.setMaxGroupMembershipSearchLevel(10)
cmo.setEnableGroupMembershipLookupHierarchyCaching(true) 
cmo.setPropagateCauseForLoginException(true)
cmo.setUseTokenGroupsForGroupMembershipLookup(true)
cmo.setResultsTimeLimit(15000)
cmo.setConnectionRetryLimit(2)
cmo.setConnectTimeout(30)
cmo.setCacheTTL(28800)
cmo.setIgnoreDuplicateMembership(true)
cmo.setConnectionPoolSize(50)
cmo.setCacheSize(3200)
cmo.setParallelConnectDelay(7)
cmo.setKeepAliveEnabled(true)
cmo.setGroupHierarchyCacheTTL(14400)
cmo.setMaxGroupHierarchiesInCache(1024)
cmo.setEnableSIDtoGroupLookupCaching(true)
cmo.setMaxSIDToGroupLookupsInCache(5000)


activate()

#startEdit()

#cd('/SecurityConfiguration/' + domainName + '/Realms/myrealm')
#set('AuthenticationProviders',jarray.array([ObjectName('Security:Name=myrealm' + providerName), ObjectName('Security:Name=myrealmDefaultAuthenticator'), ObjectName('Security:Name=myrealmDefaultIdentityAsserter')], ObjectName))

#save()
#activate()

print "************************************************************************"
print "*** Successfully created authentication provider. Please restart your server(s)."
print "************************************************************************"

disconnect()
exit()