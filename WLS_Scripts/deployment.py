print "************************************************************************"
print "*** Successfully Deployment Started   **********************************"
print "************************************************************************"

print 'Trying to connect to AdminServer'
connect(adminUsername, adminPassword, adminUrl)
print 'Connected...'

edit()
startEdit()

deploymentsArray=deploymentNames.split(',')
deploymentFilesArray=deploymentFiles.split(',')
deploymentTargetNamesArray=deploymentTargetNames.split(',')
deploymentTargetTypesArray=deploymentTargetTypes.split(',')
deploymentIsDeployArray=deploymentIsDeploy.split(',')


for i in range(0,len(deploymentsArray)):

    print i
    deploy(deploymentsArray[i],deploymentFilesArray[i],upload='true')
    try:
        cd('/AppDeployments/'+deploymentsArray[i])
        #set('Targets',jarray.array([ObjectName('com.bea:Name=DefaultServer,Type=Server')], ObjectName))

        targetArray=[]
        print targetArray 
        
        print 'TEST'
        j=0

        for x in range(0,len(deploymentTargetNamesArray)):
            print i
            print x
            print 'TEST1'
            target_name=deploymentTargetNamesArray[x]
            print target_name
            target_type=deploymentTargetTypesArray[x]
            print target_type
            deploymentIsTargetArray=deploymentIsDeployArray[x].split(';')
            if deploymentIsTargetArray[i]=='y':
                if j==0:
                    targetArray.insert(x,ObjectName('com.bea:Name=' + str(target_name) + ',Type=' + str(target_type)))
                else:
                    targetArray.append(ObjectName('com.bea:Name=' + str(target_name)+ ',Type=' + str(target_type)))	
                print target_name
                j = j +1
        print 'TEST2'
        set('Targets',jarray.array(targetArray,ObjectName))

    except BeanAlreadyExistsException:
		print('\n\n'+ str(ds_name) + ' Bean Already Exists.\n')
		pass

activate()

print "************************************************************************"
print "*** Successfully Deployed **********************************************"
print "************************************************************************"

disconnect()
exit()

