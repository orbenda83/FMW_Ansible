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

envproperty=""

if (len(sys.argv) > 1):
	envproperty=sys.argv[1]
else:
	print "Environment Property file not specified"
	sys.exit(2)

propInputStream=FileInputStream(envproperty)
configProps=Properties()
configProps.load(propInputStream)

wls_user=configProps.get("wls_user")
wls_pass=configProps.get("wls_pass")
wls_admin=configProps.get("wls_admin")

connect(wls_user,wls_pass,wls_admin)

edit()
startEdit()

total_servers=configProps.get("total_servers")
print ("\nConfiguring " + total_servers + " JMS Servers")

for i in range(0,int(total_servers)):
	print 'yossi'
	server_name=configProps.get('jms.server.' + str(i) + '.name')
	server_target=configProps.get('jms.server.' + str(i) + '.target')
	print 'yossi2'
	try:
		print 'yossi3'
		cd('/')
		print 'yossi4'
		cmo.createJMSServer(server_name)
		print server_name
		#systime.sleep(30.0)
		#cd(jmsModulePath+'/Queues/'+jmsQueueName)
		cd('/JMSServers/'+str(server_name.strip()))
		set('Targets',jarray.array([ObjectName('com.bea:Name='+ str(server_target) + ',Type=Server')], ObjectName))
		print('\n\nCreated ' + str(server_name) + '.\n')
	except BeanAlreadyExistsException:
		print('\n\n'+ str(server_name) + ' Bean Already Exists.\n')
		pass

activate()

edit()
startEdit()

total_modules=configProps.get("total_modules")
print ("\nConfiguring " + total_modules + " JMS Modules")

for i in range(0,int(total_modules)):
	module_name=configProps.get('jms.module.' + str(i) + '.name')
	print('\nCreating ' + str(module_name) + '.')
	module_target_num=configProps.get('jms.module.' + str(i) + '.target.number')
	print('\nmodule_target_num: ' + str(module_target_num) + '.')
	
	try:
		cd('/')
		cmo.createJMSSystemResource(module_name)
		print('\n\nCreated ' + str(module_name) + '.\n')
		
		cd('/JMSSystemResources/' + str(module_name))
		
		targetArray=[]
		print targetArray

		for x in range(0,int(module_target_num)):
			module_target=configProps.get('jms.module.' + str(i) + '.target.' + str(x) + '.name')
			print module_target
			module_target_type=configProps.get('jms.module.' + str(i) + '.target.' + str(x) + '.type')
			print module_target_type

			if x ==0:
			  targetArray.insert(x,ObjectName('com.bea:Name=' + str(module_target) + ',Type=' + str(module_target_type)))
			  print targetArray
			else:
			  targetArray.append(ObjectName('com.bea:Name=' + str(module_target) + ',Type=' + str(module_target_type)))
			  print targetArray

		print 'Targeting to cluster'
		#set('Targets',jarray.array([ObjectName('com.bea:Name=' + str(configProps.get('jms.module.' + str(i) + '.target.0')) + ',Type=Cluster')], ObjectName))
		
		#print targetArray
		set('Targets',jarray.array(targetArray, ObjectName))
		total_subDeployment=configProps.get('jms.module.' + str(i) + '.subDeployment.number')
		
		for j in range(0,int(total_subDeployment)):
			cd('/JMSSystemResources/' + str(module_name))
			module_subDeployment=configProps.get('jms.module.' + str(i) + '.subDeployment.' + str(j) + '.name')
			print module_subDeployment
			# module_server=configProps.get('jms.module.' + str(i) + '.subDeployment.' + str(j) + '.server')
			# print module_server
			module_subDeployment_num=configProps.get('jms.module.' + str(i) + '.subDeployment.' + str(j) + '.targets')
			print module_subDeployment_num
			
			cmo.createSubDeployment(module_subDeployment)
			print('\n\nCreated ' + str(module_subDeployment) + '.\n')
			
			cd('/JMSSystemResources/' + str(module_name) + '/SubDeployments/' + str(module_subDeployment))

			targetArray=[]
			print targetArray

			for x in range(0,int(module_subDeployment_num)):
				target_name=configProps.get('jms.module.' + str(i) + '.subDeployment.' + str(j) + '.target.' + str(x) + '.name')
				print target_name
				target_type=configProps.get('jms.module.' + str(i) + '.subDeployment.' + str(j) + '.target.' + str(x) + '.type')
				print target_type

				if x ==0:
				  	targetArray.insert(x,ObjectName('com.bea:Name=' + str(target_name) + ',Type=' + str(target_type)))
				# print targetArray
				else:
					targetArray.append(ObjectName('com.bea:Name=' + str(target_name) + ',Type=' + str(target_type)))
				# print targetArray

			print 'Targeting the SubDeployment'
			#set('Targets',jarray.array([ObjectName('com.bea:Name=' + str(configProps.get('jms.module.' + str(i) + '.target.0')) + ',Type=Cluster')], ObjectName))
			
			print targetArray
			set('Targets',jarray.array(targetArray, ObjectName))
			print 'YOSSI10###'
			#set('Targets',jarray.array([ObjectName('com.bea:Name=' + str(module_server) + ',Type=JMSServer')], ObjectName))
	except BeanAlreadyExistsException:
		print('\n\n' + str(module_name) + ' Bean Already Exists.\n')
		pass
	
	total_cf=configProps.get('jms.module.' + str(i) + '.cf.number')
	
	for j in range(0,int(total_cf)):
		cf_name=configProps.get('jms.module.' + str(i) + '.cf.' + str(j) + '.name')
		cf_xa=configProps.get('jms.module.' + str(i) + '.cf.' + str(j) + '.xa')
		try:
			cd('/JMSSystemResources/' + str(module_name) + '/JMSResource/' + str(module_name))
			print 'yossi_CF'
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
	
	total_queues=configProps.get('jms.module.' + str(i) + '.queues.number')
	
	for j in range(0,int(total_queues)):
		queue_name=configProps.get('jms.module.' + str(i) + '.queues.' + str(j) + '.name')
		#print queue_name
		queue_sub=configProps.get('jms.module.' + str(i) + '.queues.' + str(j) + '.sub')
		#print queue_sub
		queue_target=configProps.get('jms.module.' + str(i) + '.queues.' + str(j) + '.target')
		#print queue_target
		queue_type=configProps.get('jms.module.' + str(i) + '.queues.' + str(j) + '.type')
		#print queue_type
	
		try:
			cd('/JMSSystemResources/' + str(module_name) + '/JMSResource/' + str(module_name))
			
			if queue_type == 'queue':
				cmo.createQueue(queue_name)
				
				cd('/JMSSystemResources/' + str(module_name) + '/JMSResource/' + str(module_name) + '/Queues/' + str(queue_name))
				cmo.setJNDIName(queue_name)
				cmo.setSubDeploymentName(queue_sub)
				
				cd('/JMSSystemResources/' + str(module_name) + '/SubDeployments/' + str(queue_sub))
				set('Targets',jarray.array([ObjectName('com.bea:Name=' + str(queue_target) + ',Type=JMSServer')], ObjectName))
				print '######################   '
			
			else:
				cmo.createUniformDistributedQueue('Dist_' + str(queue_name))
				
				cd('/JMSSystemResources/' + str(module_name) + '/JMSResource/' + str(module_name) + '/UniformDistributedQueues/Dist_' + str(queue_name))
				cmo.setJNDIName(queue_name)
				# cmo.setDefaultTargetingEnabled(true)
				cmo.setSubDeploymentName(str(queue_sub))
				print 'queue_sub = ' + queue_sub
				print '######################   2222222'
			print('\n\nCreated ' + str(queue_name) + '.\n')
		except BeanAlreadyExistsException:
			print('\n\n' + str(queue_name) + ' Bean Already Exists.\n')
			pass
	
	activate()
	
	edit()
	startEdit()

activate()

disconnect()
