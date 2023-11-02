from java.util import Properties
from java.io import FileInputStream
from java.io import File
from java.io import FileOutputStream
from java import io
from java.lang import Exception
from java.lang import Throwable
import time as systime
import os.path
import sys

print "************************************************************************"
print "*** Successfully Started Configuring JMS Resources *********************"
print "************************************************************************"

# Create File Store
def createFileStore(fileStore):
	fsname=fileStore['name']
	fsdir=fileStore['dir']
	fstarget=fileStore['target']
	
	print fsname

	try:
		cd('/')
		cmo.createFileStore(fsname)

		cd('/FileStores/' + str(fsname))
		cmo.setDirectory(fsdir)
		set('Targets',jarray.array([ObjectName('com.bea:Name='+ str(fstarget) +',Type=Server')], ObjectName))
		print('\n\nCreated ' + str(fsname) + '.\n')
	except BeanAlreadyExistsException:
		print('\n\n'+ str(fsname) + ' Bean Already Exists.\n')
		pass

# Create File Store
def createJmsServer(jmsServer):	
	server_name=jmsServer['name']
	server_target=jmsServer['target']
	server_persist=jmsServer['persiststore']

	try:
		cd('/')
		cmo.createJMSServer(server_name)
		print server_name
		#systime.sleep(30.0)
		#cd(jmsModulePath+'/Queues/'+jmsQueueName)
		# cd('/JMSServers/'+str(server_name.strip()))
		cd('/JMSServers/'+ server_name)

		if (server_persist):
			cmo.setPersistentStore(getMBean('/FileStores/' + server_persist))

		set('Targets',jarray.array([ObjectName('com.bea:Name='+ str(server_target) + ',Type=Server')], ObjectName))
		print('\n\nCreated ' + str(server_name) + '.\n')
	except BeanAlreadyExistsException:
		print('\n\n'+ str(server_name) + ' Bean Already Exists.\n')
		pass

# Main:
#=====================
if len(sys.argv) != 2:
	print "Invalid Arguments :: Please provide input file."
	exit ()

print "Load properties file"
props=sys.argv[1]
file=open(props, 'r')
print "Read properties file"
exec file
print "Execute properties file"
file.close

#Connect to WLS admin
connect(wls_user,wls_pass,wls_admin)

edit()
startEdit()

print ("\nConfiguring " + str(len(fileStoresArray)) + " JMS File Stores")

for fileStore in fileStoresArray:
	createFileStore(fileStore)

# total_servers=configProps.get("total_servers")
print ("\nConfiguring " + str(len(jmsServersArray)) + " JMS Servers")

# for i in range(0,int(total_servers)):
for jmsServer in jmsServersArray:
	createJmsServer(jmsServer)

activate()

edit()
startEdit()

# total_modules=configProps.get("total_modules")
print ("\nConfiguring " + str(len(jmsModulesArray)) + " JMS Modules")

for jmsModule in jmsModulesArray:
	module_name=jmsModule['name']
	print('\nCreating ' + str(module_name) + '.')
	# module_target_num=configProps.get('jms.module.' + str(i) + '.target.number')
	# print('\nmodule_target_num: ' + str(module_target_num) + '.')
	
	try:
		cd('/')
		cmo.createJMSSystemResource(module_name)
		print('\n\nCreated ' + str(module_name) + '.\n')
		
		cd('/JMSSystemResources/' + str(module_name))
		
		targetArray=[]
		print targetArray

		moduleTargetsArray=jmsModule['targets']

		for moduleTarget in moduleTargetsArray:
			module_target=moduleTarget['name']
			print module_target
			module_target_type=moduleTarget['type']
			print module_target_type

			if len(targetArray) ==0:
				targetArray.insert(0,ObjectName('com.bea:Name=' + str(module_target) + ',Type=' + str(module_target_type)))
				print targetArray
			else:
				targetArray.append(ObjectName('com.bea:Name=' + str(module_target) + ',Type=' + str(module_target_type)))
				print targetArray

		print 'Targeting to cluster'
		#set('Targets',jarray.array([ObjectName('com.bea:Name=' + str(configProps.get('jms.module.' + str(i) + '.target.0')) + ',Type=Cluster')], ObjectName))
		
		#print targetArray
		set('Targets',jarray.array(targetArray, ObjectName))

		# total_subDeployment=configProps.get('jms.module.' + str(i) + '.subDeployment.number')
		moduleSubsArray=jmsModule['subdeployments']

		for moduleSub in moduleSubsArray:
			cd('/JMSSystemResources/' + str(module_name))
			module_subDeployment=moduleSub['name']
			print module_subDeployment
			# module_server=configProps.get('jms.module.' + str(i) + '.subDeployment.' + str(j) + '.server')
			# print module_server
			# module_subDeployment_num=configProps.get('jms.module.' + str(i) + '.subDeployment.' + str(j) + '.targets')
			# print module_subDeployment_num
			
			cmo.createSubDeployment(module_subDeployment)
			print('\n\nCreated ' + str(module_subDeployment) + '.\n')
			
			cd('/JMSSystemResources/' + str(module_name) + '/SubDeployments/' + str(module_subDeployment))

			targetArray=[]
			print targetArray

			moduleSubTargetsArray=jmsModule['targets']

			for moduleSubTarget in moduleSubTargetsArray:
				target_name=moduleSubTarget['name']
				print target_name
				target_type=moduleSubTarget['type']
				print target_type

				if len(targetArray) == 0:
					targetArray.insert(0,ObjectName('com.bea:Name=' + str(target_name) + ',Type=' + str(target_type)))
				# print targetArray
				else:
					targetArray.append(ObjectName('com.bea:Name=' + str(target_name) + ',Type=' + str(target_type)))
				# print targetArray

			print 'Targeting the SubDeployment'
			#set('Targets',jarray.array([ObjectName('com.bea:Name=' + str(configProps.get('jms.module.' + str(i) + '.target.0')) + ',Type=Cluster')], ObjectName))
			
			print targetArray
			set('Targets',jarray.array(targetArray, ObjectName))
			#set('Targets',jarray.array([ObjectName('com.bea:Name=' + str(module_server) + ',Type=JMSServer')], ObjectName))
	except BeanAlreadyExistsException:
		print('\n\n' + str(module_name) + ' Bean Already Exists.\n')
		pass
	
	# total_cf=configProps.get('jms.module.' + str(i) + '.cf.number')
	cfsArray=jmsModule['cfs']
	
	for cf in cfsArray:
		cf_name=cf['name']
		cf_xa=cf['xa']
		try:
			cd('/JMSSystemResources/' + str(module_name) + '/JMSResource/' + str(module_name))
			print cf_name
			cmo.createConnectionFactory(cf_name)
			print '\nCreated ' + str(cf_name) + ' in ' + str(module_name)
			
			cd('/JMSSystemResources/' + str(module_name) + '/JMSResource/' + str(module_name) + '/ConnectionFactories/' + str(cf_name))
			cmo.setJNDIName(cf_name)
			
			cd('/JMSSystemResources/' + str(module_name) + '/JMSResource/' + str(module_name) + '/ConnectionFactories/' + str(cf_name) + '/SecurityParams/' + str(cf_name))
			cmo.setAttachJMSXUserId(false)
			
			cd('/JMSSystemResources/' + str(module_name) + '/JMSResource/' + str(module_name) + '/ConnectionFactories/' + str(cf_name) + '/ClientParams/' + str(cf_name))
			cmo.setClientIdPolicy('Restricted')
			cmo.setSubscriptionSharingPolicy('Exclusive')
			cmo.setMessagesMaximum(10)
			
			cd('/JMSSystemResources/' + str(module_name) + '/JMSResource/' + str(module_name) + '/ConnectionFactories/' + str(cf_name) + '/TransactionParams/' + str(cf_name))
			cmo.setXAConnectionFactoryEnabled(bool(cf_xa))
			
			cd('/JMSSystemResources/' + str(module_name) + '/JMSResource/' + str(module_name) + '/ConnectionFactories/' + str(cf_name))
			cmo.setDefaultTargetingEnabled(true)
			print('\n\nCreated ' + str(cf_name) + '.\n')
		except BeanAlreadyExistsException:
			print('\n\n' + str(cf_name) + ' Bean Already Exists.\n')
			pass
	
	activate()
	
	edit()
	startEdit()
	
	# total_queues=configProps.get('jms.module.' + str(i) + '.queues.number')
	queuesArray=jmsModule['queues']
	print "Queues Array Values are: ", queuesArray
	
	for queue in queuesArray:
		queue_name=queue['name']
		print queue_name
		queue_sub=queue['subdeployment']
		print queue_sub
		queue_target=queue['target']
		print queue_target
		queue_type=queue['type']
		print queue_type
		queue_error=queue['errorqueue']
		print queue_error

		print "\n*******\nCreating queue with Values: ", queue
	
		try:
			cd('/JMSSystemResources/' + str(module_name) + '/JMSResource/' + str(module_name))
			
			if queue_type == 'queue':
				cmo.createQueue(queue_name)
				
				cd('/JMSSystemResources/' + str(module_name) + '/JMSResource/' + str(module_name) + '/Queues/' + str(queue_name))
				cmo.setJNDIName(queue_name)
				cmo.setSubDeploymentName(queue_sub)
				
				cd('/JMSSystemResources/' + str(module_name) + '/SubDeployments/' + str(queue_sub))
				set('Targets',jarray.array([ObjectName('com.bea:Name=' + str(queue_target) + ',Type=JMSServer')], ObjectName))

				if queue_error != "":
					cd('/JMSSystemResources/' + str(module_name) + '/JMSResource/' + str(module_name) + '/Queues/' + str(queue_name) + '/DeliveryFailureParams/' + str(queue_name))
					cmo.setExpirationPolicy('Redirect')
					cmo.setRedeliveryLimit(2)

					cd('/JMSSystemResources/' + str(module_name) + '/JMSResource/' + str(module_name) + '/Queues/' + str(queue_name) + '/DeliveryParamsOverrides/' + str(queue_name))
					cmo.setRedeliveryDelay(30)

					cd('/JMSSystemResources/' + str(module_name) + '/JMSResource/' + str(module_name) + '/Queues/' + str(queue_name) + '/DeliveryFailureParams/' + str(queue_name))
					cmo.setErrorDestination(getMBean('/JMSSystemResources/' + str(module_name) + '/JMSResource/' + str(module_name) + '/Queues/' + str(queue_error)))

				print '######################   '
				# break;

			if queue_type == 'uniform':
				cmo.createUniformDistributedQueue('Dist_' + str(queue_name))
				
				cd('/JMSSystemResources/' + str(module_name) + '/JMSResource/' + str(module_name) + '/UniformDistributedQueues/Dist_' + str(queue_name))
				cmo.setJNDIName(queue_name)
				# cmo.setDefaultTargetingEnabled(true)
				cmo.setSubDeploymentName(str(queue_sub))
				print 'queue_sub = ' + queue_sub
				# break;
			
			if queue_type == 'weighted':
				cmo.createDistributedQueue('Dist_' + str(queue_name))

				cd('/JMSSystemResources/' + str(module_name) + '/JMSResource/' + str(module_name) + '/DistributedQueues/Dist_' + str(queue_name))
				cmo.setJNDIName(queue_name)

				distQueuesArray=queue['subQueues']

				for distQueue in distQueuesArray:
					cmo.createDistributedQueueMember(distQueue['name'])

				# break;
			# else:
			# 	print 'No queue type'

			# activate()

			print('\nCreated ' + str(queue_name) + '.\n')
			
			# edit()
			# startEdit()
		except BeanAlreadyExistsException:
			print('\n\n' + str(queue_name) + ' Bean Already Exists.\n')
			pass
	
activate()

disconnect()

print 'JMS resources creation finished successfully.'