from java.util import Properties
from java.io import FileInputStream
from java.io import File
from java.io import FileOutputStream
from java import io
from java.lang import Exception
from java.lang import Throwable
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

total_ds=configProps.get("total_ds")
print ("\nConfiguring " + total_ds + " JDBC Data Sources")

for i in range(0,int(total_ds)):
	print i
	ds_name=configProps.get('jdbc.' + str(i) + '.name')
	print ds_name
	ds_jndi=configProps.get('jdbc.' + str(i) + '.jndi')
	print ds_jndi
	ds_driver=configProps.get('jdbc.' + str(i) + '.driver')
	print ds_driver
	ds_driver_type=configProps.get('jdbc.' + str(i) + '.driver_type')
	print ds_driver_type
	ds_driver_url=configProps.get('jdbc.' + str(i) + '.driver_url')
	print ds_driver_url
	ds_user=configProps.get('jdbc.' + str(i) + '.user')
	print ds_user
	ds_password=configProps.get('jdbc.' + str(i) + '.password')
	print ds_password
	ds_initial=configProps.get('jdbc.' + str(i) + '.initial')
	print ds_initial
	ds_max=configProps.get('jdbc.' + str(i) + '.max')
	print ds_max
	ds_min=configProps.get('jdbc.' + str(i) + '.min')
	print ds_min
	ds_target_number=configProps.get('jdbc.' + str(i) + '.target.number')
	print ds_target_number
	
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
		
		cd('/JDBCSystemResources/' + str(ds_name))
		print(ds_name)

		targetArray=[]
		print targetArray 
		target_num = configProps.get('jdbc.' + str(i) + '.target.number')
		print 'TEST0'
		print target_num
		for x in range(0,int(target_num)):
			print str(i)
			print str(x)
			print 'TEST1'
			target_name=configProps.get('jdbc.'+ str(i)+'.target.' + str(x) + '.name')
			print target_name
			target_type=configProps.get('jdbc.'+ str(i)+'.target.' + str(x) + '.type')
			print target_type
			if x==0:
				targetArray.insert(x,ObjectName('com.bea:Name=' + str(target_name) + ',Type=' + str(target_type)))
			else:
				targetArray.append(ObjectName('com.bea:Name=' + str(target_name)+ ',Type=' + str(target_type)))	
			print target_name
		print 'TEST2'
		set('Targets',jarray.array(targetArray,ObjectName))	


	except BeanAlreadyExistsException:
		print('\n\n'+ str(ds_name) + ' Bean Already Exists.\n')
		pass

activate()

disconnect()
