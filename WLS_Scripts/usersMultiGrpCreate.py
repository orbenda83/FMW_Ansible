import sys

# Read properties file
if len(sys.argv) != 2:
    print "Invalid Arguments :: Please provide input file."
    exit ()

    try:
        print "Load properties file"
        props=sys.argv[1]
        file=open(props, 'r')
        print "Read properties file"
        exec file
        print "Execute properties file"
        file.close
    except:
        exit()
    
    print "Username Array Values are: ", userNameArray
    print "Admin server user name: ", USER
    print "Admin Server URL: ", ADMIN_URL

    connect(USER, PASSWORD, ADMIN_URL)
    edit()
    serverConfig()
    successCount=0

    for userName in userNameArray:
        usrName=userName['name']
        # print 'The Name of the user will be created : ',usrName
        pwd=userName['userPwd']
        #print 'The password for this user : ',pwd
        #print 'The password for this user : ',pwd
        desc=userName['description']
        # print 'Description for this user : ',desc
        grps=userName['groups']
        # print 'Group Names for this user : ',grps

        # grpName1=userName['groupName1']
        # print 'First Group Name for this user : ',grpName1
        # grpName2=userName['groupName2']
        # print 'Second Group Name for this user : ',grpName2
        # grpName3=userName['groupName3']
        # print 'Third Group Name for this user : ',grpName3
        cd('/SecurityConfiguration/APICS01_domain/Realms/myrealm/AuthenticationProviders/DefaultAuthenticator')
        cmo.createUser(usrName,pwd,desc)
        print usrName,'- been created' 

        groupsArray=grps.split(',')
        print ("\nConfiguring " + len(groupsArray) + " Groups to user")
        
        for i in range(0,len(groupsArray)):
            group=groupsArray[i]
            cmo.addMemberToGroup(group,usrName)
            print group,' - been assigend to ',usrName

        # cmo.addMemberToGroup(grpName1,usrName)
        # cmo.addMemberToGroup(grpName2,usrName)
        # cmo.addMemberToGroup(grpName3,usrName)
        # print grpName1, grpName2, grpName3,'- been assigend to ',usrName
        successCount=successCount+1
        print str(successCount)+" users successfully created"
