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
print "*** Successfully Started Configuring DB Data Sources *******************"
print "************************************************************************"

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
print "Connecting to WLS Admin"
connect(wls_user,wls_pass,wls_admin)

edit()
startEdit()

print ("\nConfiguring " + str(len(dataSourcesArray)) + " JDBC Data Sources")

for ds in dataSourcesArray:
	ds_name=ds['name']
	print ds_name
	ds_jndi=ds['jndi']
	print ds_jndi
	ds_type=ds['type']
	print ds_type
	ds_driver=ds['driver']
	print ds_driver
	ds_driver_type=ds['driver_type']
	print ds_driver_type
	ds_driver_url=ds['driver_url']
	print ds_driver_url
	ds_user=ds['user']
	print ds_user
	ds_password=ds['password']
	print ds_password
	ds_initial=ds['initial']
	print ds_initial
	ds_max=ds['max']
	print ds_max
	ds_min=ds['min']
	print ds_min
	ds_targets=ds['targets']
	print ds_targets
	
	try:
		cd('/')
		cmo.createJDBCSystemResource(ds_name)
		
		cd('/JDBCSystemResources/' + str(ds_name) + '/JDBCResource/' + str(ds_name))
		cmo.setName(ds_name)
		
		cd('/JDBCSystemResources/' + str(ds_name) + '/JDBCResource/' + str(ds_name) + '/JDBCDataSourceParams/' + str(ds_name))
		set('JNDINames',jarray.array([String(ds_jndi)], String))
		
		if ds_driver_type == 'xa':
			cmo.setKeepConnAfterLocalTx(true)
			cmo.setKeepConnAfterGlobalTx(false)
		
		cd('/JDBCSystemResources/' + str(ds_name) + '/JDBCResource/' + str(ds_name))
		cmo.setDatasourceType('GENERIC')
		
		cd('/JDBCSystemResources/' + str(ds_name) + '/JDBCResource/' + str(ds_name) + '/JDBCDriverParams/' + str(ds_name))
		cmo.setUrl(ds_driver_url)
		cmo.setDriverName(ds_driver)
		cmo.setPassword(ds_password)
		
		if ds_driver_type == 'xa':
			cmo.setUseXaDataSourceInterface(true)
		
		cd('/JDBCSystemResources/' + str(ds_name) + '/JDBCResource/' + str(ds_name) + '/JDBCConnectionPoolParams/' + str(ds_name))
		if ds_type == "MS":
			cmo.setTestTableName('SQL SELECT 1\r\n')
		if ds_type == "Oracle":
			cmo.setTestTableName('SQL PINGDATABASE')

		cmo.setTestConnectionsOnReserve(true)
		cmo.setRemoveInfectedConnections(true)
		cmo.setTestFrequencySeconds(120)
		cmo.setSecondsToTrustAnIdlePoolConnection(10)
		cmo.setShrinkFrequencySeconds(900)
		cmo.setInactiveConnectionTimeoutSeconds(300)
		cmo.setStatementTimeout(180)
		cmo.setStatementCacheSize(25)
		cmo.setPinnedToThread(false)
		cmo.setConnectionReserveTimeoutSeconds(25)
		cmo.setInitialCapacity(int(ds_initial))
		cmo.setMaxCapacity(int(ds_max))
		cmo.setMinCapacity(int(ds_min))
		
		if ds_driver_type == 'xa':
			cmo.setJDBCXADebugLevel(10)
		
		cd('/JDBCSystemResources/' + str(ds_name) + '/JDBCResource/' + str(ds_name) + '/JDBCDriverParams/' + str(ds_name) + '/Properties/' + str(ds_name))
		cmo.createProperty('user')
		
		cd('/JDBCSystemResources/' + str(ds_name) + '/JDBCResource/' + str(ds_name) + '/JDBCDriverParams/' + str(ds_name) + '/Properties/' + str(ds_name) + '/Properties/user')
		cmo.setValue(ds_user)

		if ds_type == "MS":
			propsArray=ds['properties']
			print propsArray

			for prop in propsArray:
				print prop
				propKey=prop['key']
				print propKey
				propVal=prop['value']
				print propVal

				cd('/JDBCSystemResources/' + str(ds_name) + '/JDBCResource/' + str(ds_name) + '/JDBCDriverParams/' + str(ds_name) + '/Properties/' + str(ds_name))
				cmo.createProperty(propKey)
				
				cd('/JDBCSystemResources/' + str(ds_name) + '/JDBCResource/' + str(ds_name) + '/JDBCDriverParams/' + str(ds_name) + '/Properties/' + str(ds_name) + '/Properties/' + str(propKey))
				cmo.setValue(propVal)
		
		cd('/JDBCSystemResources/' + str(ds_name) + '/JDBCResource/' + str(ds_name) + '/JDBCDataSourceParams/' + str(ds_name))
		if ds_driver_type == 'xa':
			cmo.setGlobalTransactionsProtocol('TwoPhaseCommit')
			cmo.setKeepConnAfterLocalTx(true)
			cmo.setKeepConnAfterGlobalTx(false)
			
			cd('/JDBCSystemResources/' + str(ds_name) + '/JDBCResource/' + str(ds_name) + '/JDBCXAParams/' + str(ds_name))
			cmo.setResourceHealthMonitoring(true)
			cmo.setXaTransactionTimeout(120)
			cmo.setXaRetryIntervalSeconds(60)
			cmo.setXaRetryDurationSeconds(0)
			cmo.setXaSetTransactionTimeout(true)
			cmo.setRollbackLocalTxUponConnClose(false)
			cmo.setKeepLogicalConnOpenOnRelease(false)
			cmo.setXaEndOnlyOnce(true)
			cmo.setKeepXaConnTillTxComplete(true)
			cmo.setRecoverOnlyOnce(false)
			cmo.setNeedTxCtxOnClose(false)
		else:
			cmo.setGlobalTransactionsProtocol('OnePhaseCommit')
		
		targetArray=[]
		print targetArray

		cd('/JDBCSystemResources/' + str(ds_name))
		for dsTarget in ds_targets:
			ds_target=dsTarget['name']
			print ds_target
			ds_target_type=dsTarget['type']
			print ds_target_type

			if len(targetArray) ==0:
				targetArray.insert(0,ObjectName('com.bea:Name=' + str(ds_target) + ',Type=' + str(ds_target_type)))
				print targetArray
			else:
				targetArray.append(ObjectName('com.bea:Name=' + str(ds_target) + ',Type=' + str(ds_target_type)))
				print targetArray

		print 'Targeting to cluster'
				
		#print targetArray
		set('Targets',jarray.array(targetArray, ObjectName))

		print('\n\nCreated ' + str(ds_name) + '.\n')
	except BeanAlreadyExistsException:
		print('\n\n'+ str(ds_name) + ' Bean Already Exists.\n')
		pass

activate()

disconnect()

print "DS resources creation finished successfully."