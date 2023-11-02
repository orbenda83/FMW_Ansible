#############################################################################
# Fix a SOA/BPM/OSB domain
#
# @author Or Ben-David, FMW ACS IL, Oracle
# @version 2.0, 2020-03-30
#
#############################################################################
# Modify these values as necessary
import sys, traceback
scriptName = 'createSoaBpmDomain.py'
#
#Home Folders
wlsHome    = fmwHome+'/wlserver'
soaDomainHome       = domainsHome+'/'+soaDomainName
soaApplicationsHome = applicationsHome+'/'+soaDomainName
#
# Templates for 12.1.3
#wlsjar =fmwHome+'/wlserver/common/templates/wls/wls.jar'
#oracleCommonTplHome=fmwHome+'/oracle_common/common/templates'
#wlservicetpl=oracleCommonTplHome+'/oracle.wls-webservice-template_12.1.3.jar'
#osbtpl=fmwHome+'/osb/common/templates/wls/oracle.osb_template_12.1.3.jar'
#applCoreTpl=oracleCommonTplHome+'/wls/oracle.applcore.model.stub.1.0.0_template.jar'
#soatpl=fmwHome+'/soa/common/templates/wls/oracle.soa_template_12.1.3.jar'
#bamtpl=fmwHome+'/soa/common/templates/wls/oracle.bam.server_template_12.1.3.jar'
#bpmtpl=fmwHome+'/soa/common/templates/wls/oracle.bpm_template_12.1.3.jar'
#essBasicTpl=oracleCommonTplHome+'/wls/oracle.ess.basic_template_12.1.3.jar'
#essEmTpl=fmwHome+'/em/common/templates/wls/oracle.em_ess_template_12.1.3.jar'
#ohsTpl=fmwHome+'/ohs/common/templates/wls/ohs_managed_template_12.1.3.jar'
#b2bTpl=fmwHome+'/soa/common/templates/wls/oracle.soa.b2b_template_12.1.3.jar'
#
# Templates for 12.2.1
wlsjar =fmwHome+'/wlserver/common/templates/wls/wls.jar'
oracleCommonTplHome=fmwHome+'/oracle_common/common/templates'
wlservicetpl=oracleCommonTplHome+'/wls/oracle.wls-webservice-template.jar'
osbtpl=fmwHome+'/osb/common/templates/wls/oracle.osb_template.jar'
applCoreTpl=oracleCommonTplHome+'/wls/oracle.applcore.model.stub_template.jar'
soatpl=fmwHome+'/soa/common/templates/wls/oracle.soa_template.jar'
bamtpl=fmwHome+'/soa/common/templates/wls/oracle.bam.server_template.jar'
bpmtpl=fmwHome+'/soa/common/templates/wls/oracle.bpm_template.jar'
essBasicTpl=oracleCommonTplHome+'/wls/oracle.ess.basic_template.jar'
essEmTpl=fmwHome+'/em/common/templates/wls/oracle.em_ess_template.jar'
ohsTpl=fmwHome+'/ohs/common/templates/wls/ohs_managed_template.jar' # need to be validated!
b2bTpl=fmwHome+'/soa/common/templates/wls/oracle.soa.b2b_template.jar' # need to be validated!
#
# ServerGroup definitions
adminSvrGrpDesc='WSM-CACHE-SVR WSMPM-MAN-SVR JRF-MAN-SVR'
adminSvrGrp=["WSM-CACHE-SVR" , "WSMPM-MAN-SVR" , "JRF-MAN-SVR"]
essSvrGrpDesc="ESS-MGD-SVRS"
essSvrGrp=["ESS-MGD-SVRS"]
soaSvrGrpDesc="SOA-MGD-SVRS"
soaSvrGrp=["SOA-MGD-SVRS"]
bamSvrGrpDesc="BAM12-MGD-SVRS"
bamSvrGrp=["BAM12-MGD-SVRS"]
osbSvrGrpDesc="OSB-MGD-SVRS-COMBINED"
osbSvrGrp=["OSB-MGD-SVRS-COMBINED"]
#
#
lineSeperator='__________________________________________________________________________________'
#
#


# Target FileStore/JDBCStores
def targetMesageStore(storeName, storeType, targetName, targetType):
  try:
    print 'cd("/"'+storeType+'/'+storeName+')'
    cd('/'+ storeType +'/' + storeName)
    set('Targets',jarray.array([ObjectName('com.bea:Name=' + targetName + ',Type=' + targetType)], ObjectName))
    print '\n Targeting ' + storeType + ': ' + storeName + ' To ' + targetName + ';' + targetType + '.'
  except BeanAlreadyExistsException:
    print('\n\n'+ str(storeName) + ' Bean Already Exists.\n')
    pass
#

# Create FileStore
def createFileStore(fsName, targetName, targetType):
  try:
    cd('/')
    cmo.createFileStore(fsName)
    #create(fsName,'FileStore')
    print '\n Created FileStore: ' + fsName + '.'
  
    cd('/FileStores/' + fsName)
    cmo.setDirectory(fsName)
    # set('Directory', fsName)
    set('Targets',jarray.array([ObjectName('com.bea:Name=' + targetName + ',Type=' + targetType)], ObjectName))
    print '. Targeting FileStore: ' + fsName + ' To ' + targetName + ';' + targetType + '.'
  except BeanAlreadyExistsException:
    print('\n\n'+ str(fsName) + ' Bean Already Exists.\n')
    pass
#

# Target JMSServer
def targetJMSServer(serverName, targetName, targetType):
  try:
    print 'Server name: '+serverName
    cd('/JMSServers/' + serverName)
    set('Targets',jarray.array([ObjectName('com.bea:Name=' + targetName + ',Type=' + targetType)], ObjectName))
    print '\n Targeting JMSServer: ' + serverName + ' To ' + targetName + ';' + targetType + '.'
  except BeanAlreadyExistsException:
    print('\n\n'+ str(serverName) + ' Bean Already Exists.\n')
    pass
#

# Create JMSServer
def createJMSServer(serverName, storeName, targetName, targetType, additionalSettings):
  try:
    cd('/')
    cmo.createJMSServer(serverName)
    # create(serverName,'JMSServer')
    print '\n Created JMSServer: ' + serverName + '.'
  
    cd('/JMSServers/' + serverName)
    cmo.setPersistentStore(getMBean('/FileStores/'+storeName))
    # set('PersistentStore', '/FileStores/'+storeName)
    set('Targets',jarray.array([ObjectName('com.bea:Name=' + targetName + ',Type=' + targetType)], ObjectName))
    cmo.setPersistentStore(getMBean('/FileStores/'+storeName))
    print '. Targeting JMSServer: ' + serverName + ' To ' + targetName + ';' + targetType + '.'
  
    if additionalSettings:
      print '. Applying Settings To: ' + serverName + '.'
      print '... Set TemporaryTemplateResource To: None.'
      cmo.setTemporaryTemplateResource(None)
      # set('TemporaryTemplateResource',None)
      print '... Set TemporaryTemplateName To: None.'
      cmo.setTemporaryTemplateName(None)
      # set('TemporaryTemplateName',None)
      print '... Set HostingTemporaryDestinations To: true.'
      cmo.setHostingTemporaryDestinations(true)
      # set('HostingTemporaryDestinations',true)
      print '... Set AllowsPersistentDowngrade To: false.'
      cmo.setAllowsPersistentDowngrade(false)
      # set('AllowsPersistentDowngrade',false)
      print '... Set StoreMessageCompressionEnabled To: false.'
      cmo.setStoreMessageCompressionEnabled(false)
      # set('StoreMessageCompressionEnabled',false)
      print '... Set PagingMessageCompressionEnabled To: false.'
      cmo.setPagingMessageCompressionEnabled(false)
      # set('PagingMessageCompressionEnabled',false)
      print '... Set MessageBufferSize To: 100000.'
      cmo.setMessageBufferSize(100000)
      # set('MessageBufferSize',100000)
      print '... Set ExpirationScanInterval To: 30.'
      cmo.setExpirationScanInterval(30)
      # set('ExpirationScanInterval',30)
      print '... Set InsertionPausedAtStartup To: false.'
      cmo.setInsertionPausedAtStartup('false')
      # set('InsertionPausedAtStartup','false')
      print '... Set PagingBlockSize To: -1.'
      cmo.setPagingBlockSize(-1)
      # set('PagingBlockSize',-1)
      print '... Set PagingMaxWindowBufferSize To: -1.'
      cmo.setPagingMaxWindowBufferSize(-1)
      # set('PagingMaxWindowBufferSize',-1)
      print '... Set PagingMaxFileSize To: 1342177280.'
      cmo.setPagingMaxFileSize(1342177280)
      # set('PagingMaxFileSize',1342177280)
      print '... Set ProductionPausedAtStartup To: false.'
      cmo.setProductionPausedAtStartup('false')
      # set('ProductionPausedAtStartup','false')
      print '... Set PagingFileLockingEnabled To: true.'
      cmo.setPagingFileLockingEnabled(true)
      # set('PagingFileLockingEnabled',true)
      print '... Set MessageCompressionOptions To: GZIP_DEFAULT_COMPRESSION.'
      cmo.setMessageCompressionOptions('GZIP_DEFAULT_COMPRESSION')
      # set('MessageCompressionOptions','GZIP_DEFAULT_COMPRESSION')
      print '... Set PagingMinWindowBufferSize To: -1.'
      cmo.setPagingMinWindowBufferSize(-1)
      # set('PagingMinWindowBufferSize',-1)
      print '... Set PagingIoBufferSize To: -1.'
      cmo.setPagingIoBufferSize(-1)
      # set('PagingIoBufferSize',-1)
      print '... Set ConsumptionPausedAtStartup To: false.'
      cmo.setConsumptionPausedAtStartup('false')
      # set('ConsumptionPausedAtStartup','false')
      print '... Set StoreEnabled To: true.'
      cmo.setStoreEnabled(true)
      # set('StoreEnabled',true)
  except BeanAlreadyExistsException:
    print('\n\n'+ str(serverName) + ' Bean Already Exists.\n')
    pass
#

# Target SubDeployment
def targetSubDeployment(subName, moduleName, soaNumber):
  try:
    print '. Targeting SubDeployment: '+subName+'SubDeployment_auto_1.'

    if subName == 'UMS':
      cd('/JMSSystemResources/'+subName+moduleName+'/SubDeployments/'+subName+'JMSSubDeployment_auto_1')
    else:
      cd('/JMSSystemResources/'+subName+moduleName+'/SubDeployments/'+subName+'SubDeployment_auto_1')
    
    targetArray=[]
    print targetArray
    for x in range(0,int(soaNumber)):
      if x ==0:
        targetArray.insert(x,ObjectName('com.bea:Name=' + str(subName) + 'JMSServer_auto_' + str(x+1) + ',Type=JMSServer'))
      else:
        targetArray.append(ObjectName('com.bea:Name=' + str(subName) + 'JMSServer_auto_' + str(x+1) + ',Type=JMSServer'))
      print targetArray
    set('Targets',jarray.array(targetArray, ObjectName))
    print '. Targeted to '+str(targetArray)
  except BeanAlreadyExistsException:
    print('\n\n'+ str(subName) + ' Bean Already Exists.\n')
    pass
#

# Fix Topics - Set Parameters
def fixTopics():
  topics = ["PeopleQuery", "Measurement"]

  try:
    for x in range(0,len(topics)):
      print '\n. Setting Parameters for dist_'+topics[x]+'Topic_auto_1:'
      cd('/JMSSystemResources/BPMJMSModule/JMSResource/BPMJMSModule/UniformDistributedTopics/dist_'+topics[x]+'Topic_auto_1/DeliveryParamsOverrides/dist_'+topics[x]+'Topic_auto_1')
      print '... Set TimeToLive To: -1.'
      cmo.setTimeToLive(-1)
      # set('TimeToLive',-1)
      if topics[x] == "PeopleQuery":
        print '... Set DeliveryMode To: Non-Persistent.'
        cmo.setDeliveryMode('Non-Persistent')
        # set('DeliveryMode','Non-Persistent')
      else:
        print '... Set DeliveryMode To: Persistent.'
        cmo.setDeliveryMode('Persistent')
        # set('DeliveryMode','Persistent')
      print '... Set Priority To: -1.'
      cmo.setPriority(-1)
      # set('Priority',-1)
      print '... Set TimeToDeliver To: -1.'
      cmo.setTimeToDeliver('-1')
      # set('TimeToDeliver','-1')
  
      cd('/JMSSystemResources/BPMJMSModule/JMSResource/BPMJMSModule/UniformDistributedTopics/dist_'+topics[x]+'Topic_auto_1/DeliveryFailureParams/dist_'+topics[x]+'Topic_auto_1')
      print '... Set ExpirationPolicy To: Discard.'
      cmo.setExpirationPolicy('Discard')
      # set('ExpirationPolicy','Discard')
      if topics[x] == "PeopleQuery":
        print '... Set RedeliveryLimit To: 1.'
        cmo.setRedeliveryLimit(1)
        # set('RedeliveryLimit',1)
      else:
        print '... Set RedeliveryLimit To: 3.'
        cmo.setRedeliveryLimit(3)
        # set('RedeliveryLimit',3)
  
      cd('/JMSSystemResources/BPMJMSModule/JMSResource/BPMJMSModule/UniformDistributedTopics/dist_'+topics[x]+'Topic_auto_1/DeliveryParamsOverrides/dist_'+topics[x]+'Topic_auto_1')
      print '... Set RedeliveryDelay To: -1.'
      cmo.setRedeliveryDelay(-1)
      # set('RedeliveryDelay',-1)
  
      cd('/JMSSystemResources/BPMJMSModule/JMSResource/BPMJMSModule/UniformDistributedTopics/dist_'+topics[x]+'Topic_auto_1/DeliveryFailureParams/dist_'+topics[x]+'Topic_auto_1')
      print '... Set ErrorDestination To: None.'
      cmo.unSet('ErrorDestination')
      # set('ErrorDestination',None)
  
      cd('/JMSSystemResources/BPMJMSModule/JMSResource/BPMJMSModule/UniformDistributedTopics/dist_'+topics[x]+'Topic_auto_1')
      print '... Set Template To: None.'
      cmo.unSet('Template')
      # set('Template',None)
      print '... Set JMSCreateDestinationIdentifier To: jms/bpm/'+topics[x]+'Topic.'
      cmo.setJMSCreateDestinationIdentifier('jms/bpm/'+topics[x]+'Topic')
      # set('JMSCreateDestinationIdentifier','jms/bpm/'+topics[x]+'Topic')
      print '... Set UnitOfOrderRouting To: Hash.'
      cmo.setUnitOfOrderRouting('Hash')
      # set('UnitOfOrderRouting','Hash')
      print '... Set DefaultTargetingEnabled To: false.'
      cmo.setDefaultTargetingEnabled(false)
      # set('DefaultTargetingEnabled',false)
      print '... Set IncompleteWorkExpirationTime To: -1.'
      cmo.setIncompleteWorkExpirationTime(-1)
      # set('IncompleteWorkExpirationTime',-1)
      print '... Set InsertionPausedAtStartup To: false.'
      cmo.setInsertionPausedAtStartup(false)
      # set('InsertionPausedAtStartup',false)
      print '... Set UnitOfWorkHandlingPolicy To: PassThrough.'
      cmo.setUnitOfWorkHandlingPolicy('PassThrough')
      # set('UnitOfWorkHandlingPolicy','PassThrough')
      print '... Set MessagingPerformancePreference To: 25.'
      cmo.setMessagingPerformancePreference(25)
      # set('MessagingPerformancePreference',25)
      print '... Set SAFExportPolicy To: All.'
      cmo.setSAFExportPolicy('All')
      # set('SAFExportPolicy','All')
      print '... Set ProductionPausedAtStartup To: false.'
      cmo.setProductionPausedAtStartup(false)
      # set('ProductionPausedAtStartup',false)
      print '... Set DefaultUnitOfOrder To: false.'
      cmo.setDefaultUnitOfOrder(false)
      # set('DefaultUnitOfOrder',false)
      print '... Set ConsumptionPausedAtStartup To: false.'
      cmo.setConsumptionPausedAtStartup(false)
      # set('ConsumptionPausedAtStartup',false)
      print '... Set LoadBalancingPolicy To: Round-Robin.'
      cmo.setLoadBalancingPolicy('Round-Robin')
      # set('LoadBalancingPolicy','Round-Robin')
      print '... Set AttachSender To: supports.'
      cmo.setAttachSender('supports')
      # set('AttachSender','supports')
  except BeanAlreadyExistsException:
    print('\n\nTopic Bean Already Exists.\n')
    pass
#

# Main function to run
def main():
  try:
    #
    connect(adminUser,adminPwd,'t3://'+adminListenAddress+':'+adminListenPort)

    edit()
    startEdit()

    # Section 5: Set Message Stores.
    print ('\5. Set Message Stores Targets')
    print (lineSeperator)

    cd('/')
    # SOA Suite
    if soaEnabled == 'true':
      print ('\nSet File Stores Targets')
      print (lineSeperator)
      
      soaSvrNameArray=soaSvrNames.split(',')
      soaSvrAddressArray=soaSvrAddresses.split(',')
      soaSvrMachineArray=soaSvrMachines.split(',')
      soaPrefixArray=soaObjectsPrefixes.split(',')
            
      if soaIsMigratable == 'true':
        targetType='MigratableTarget'
        targetSuffix=' (migratable)'
      else:
        targetType='Server'
        targetSuffix=''

      for j in range(0,len(soaPrefixArray)):
        for i in range(0,int(soaNumber)):
          if i == 0:
            targetMesageStore(soaPrefixArray[j]+'JMSFileStore_auto_'+str(i+1), 'FileStores', soaSvrNameArray[i]+targetSuffix, targetType)
          else:
            createFileStore(soaPrefixArray[j]+'JMSFileStore_auto_'+str(i+1), soaSvrNameArray[i]+targetSuffix, targetType)

      print ('\nSet JDBC Stores Targets')
      print (lineSeperator)
      
      for j in range(0,len(soaPrefixArray)):
        targetMesageStore(soaPrefixArray[j]+'JMSJDBCStore', 'JDBCStores', soaClr, 'Cluster')
    #

    # OSB
    # TODO: check and create for OSB deployment also
    #

    # ESS
    # TODO: check and create for ESS deployment also
    #

    # BAM
    # TODO: check and create for BAM deployment also
    #

    #
    print ('Finshed Targeting Message Stores.')
    #

    activate()

    startEdit()

    # Section 6: Set Message Servers.
    print ('\6. Set Message Servers')
    print (lineSeperator)

    cd('/')
    # SOA Suite
    if soaEnabled == 'true':
      print ('\nSet JMS Servers')
      print (lineSeperator)

      if soaIsMigratable == 'true':
        targetType='MigratableTarget'
        targetSuffix=' (migratable)'
      else:
        targetType='Server'
        targetSuffix=''

      for j in range(0,len(soaPrefixArray)):
        for i in range(0,int(soaNumber)):
          if i == 0:
            targetJMSServer(soaPrefixArray[j]+'JMSServer_auto_'+str(i+1), soaSvrNameArray[i]+targetSuffix, targetType)
          else:
            if soaPrefixArray[j] == 'BPM':
              createJMSServer(soaPrefixArray[j]+'JMSServer_auto_'+str(i+1), soaPrefixArray[j]+'JMSFileStore_auto_'+str(i+1), soaSvrNameArray[i]+targetSuffix, targetType, true)
            else:
              createJMSServer(soaPrefixArray[j]+'JMSServer_auto_'+str(i+1), soaPrefixArray[j]+'JMSFileStore_auto_'+str(i+1), soaSvrNameArray[i]+targetSuffix, targetType, false)
    #

    # OSB
    # TODO: check and create for OSB deployment also
    #

    # ESS
    # TODO: check and create for ESS deployment also
    #

    # BAM
    # TODO: check and create for BAM deployment also
    #

    #
    print ('Finshed Targeting Message Stores.')
    #

    activate()

    startEdit()

    # Section 7: Update SubDeployments.
    print ('\7. Update SubDeployments')
    print (lineSeperator)

    cd('/')
    # SOA Suite
    if soaEnabled == 'true':
      print ('\nUpdating SubDeployment')
      print (lineSeperator)

      for j in range(0,len(soaPrefixArray)):
        if soaPrefixArray[j] == 'UMS':
          targetSubDeployment(soaPrefixArray[j], 'JMSSystemResource', soaNumber)
        else:
          targetSubDeployment(soaPrefixArray[j], 'JMSModule', soaNumber)
    #

    # OSB
    # TODO: check and create for OSB deployment also
    #

    # ESS
    # TODO: check and create for ESS deployment also
    #

    # BAM
    # TODO: check and create for BAM deployment also
    #

    #
    print ('Finshed Targeting SubDeployments.')
    #

    # Section 8: Fix Topics - Set Parameters
    print ('\8. Fix Topics - Set Parameters')
    print (lineSeperator)

    cd('/')
    # SOA Suite
    if soaEnabled == 'true':
      print ('\nFixing Topics')
      print (lineSeperator)

      fixTopics()
    #

    # OSB
    # TODO: check and create for OSB deployment also
    #

    # ESS
    # TODO: check and create for ESS deployment also
    #

    # BAM
    # TODO: check and create for BAM deployment also
    #

    #
    print ('Finshed Fixing Topics.')
    #

    activate()

    disconnect()

    # DONE
    print ('\nFinished')
    print ('\nSuccessfully configured wls domain')
    #
    print('\nExiting...')
    exit()
  except NameError, e:
    print 'Apparently properties not set.'
    print "Please check the property: ", sys.exc_info()[0], sys.exc_info()[1]
    # usage()
  except:
    apply(traceback.print_exception, sys.exc_info())
    stopEdit('y')
    exit(exitcode=1)
#call main()
main()
exit()
