print "************************************************************************"
print "*** Successfully Started authentication provider ***********************"
print "************************************************************************"

# Connect to the AdminServer.
print 'Trying to connect to AdminServer'
connect(adminUsername, adminPassword, adminUrl)
print 'Connected...'

edit()
startEdit()


cd('/SecurityConfiguration/DefaultDomain/Realms/myrealm')
cmo.createAuthenticationProvider(asserterName, 'examples.security.providers.identityassertion.simple.SimpleSampleIdentityAsserter')
print 'Enter Directory'+ asserterName
activate()

startEdit()

cd('/SecurityConfiguration/DefaultDomain/Realms/myrealm/AuthenticationProviders/'+asserterName)
set('ActiveTypes',jarray.array([], String))

activate()

startEdit()
cmo.setDbPassword(adPassword)
cmo.setDbTokenSql(dbTokenSql)
cmo.setDbURL(prefix+hostName+':'+port+':'+sid)
cmo.setDbUser(dbUser)

activate()

print "************************************************************************"
print "*** Successfully created authentication provider. Please restart your server(s)."
print "************************************************************************"

disconnect()
exit()

# wlst.sh xxx.py xxxx.props
# wlst.sh xxx.py -loadProperties xxx.props