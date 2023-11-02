import sys
#read properties file
 
if len(sys.argv) != 2:
    print "Invalid Arguments :: Please provide input file"
    exit()
    try:
        print "Load properties file"
        properties=sys.argv[1]
        file=open(properties,'r')
        print "Read properties file"
        exec file
        print "Execute properties file"
        file.close
    except:
        exit()
    
    print 'userName Array Values are : ',userNameArray
    print 'Admin server user name : ',USER
    print 'ADMIN Server URL : ',ADMIN_URL

    connect(USER,PASSWORD,ADMIN_URL)
    edit()
    serverConfig()
    successCount=0

    for userName in userNameArray:
        usrName=userName['name']
        # print 'The Name of the user will be created : ',usrName
        cd('/SecurityConfiguration/APICS01_domain/Realms/myrealm/AuthenticationProviders/DefaultAuthenticator')
        cmo.removeUser(usrName)
        print usrName,'- has been Deleted' 
        successCount=successCount+1
        print str(successCount)+" users successfully deleted"
