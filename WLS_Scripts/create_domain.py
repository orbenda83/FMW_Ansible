#############################################################################
# Create a SOA/BPM/OSB domain
#
# @author Martien van den Akker, Darwin-IT Professionals
# @version 1.0, 2016-04-09
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

# Print script usage
def usage():
  print 'Call script as: '
  print 'Windows: wlst.cmd '+scriptName+' -loadProperties localhost.properties'
  print 'Linux: wlst.sh '+scriptName+' -loadProperties environment.properties'
  print 'Property file should contain the following properties: '
  print "adminUrl='localhost:7101'"
  print "adminUser='weblogic'"
  print "adminPwd='welcome1'"
#
# Create a boot properties file.
def createBootPropertiesFile(directoryPath,fileName, username, password):
  print ('Create Boot Properties File for folder: '+directoryPath)
  print (lineSeperator)
  serverDir = File(directoryPath)
  bool = serverDir.mkdirs()
  fileNew=open(directoryPath + '/'+fileName, 'w')
  fileNew.write('username=%s\n' % username)
  fileNew.write('password=%s\n' % password)
  fileNew.flush()
  fileNew.close()
#
# Create Startup Properties File
def createAdminStartupPropertiesFile(directoryPath, args):
  print 'Create AdminServer Boot Properties File for folder: '+directoryPath
  print (lineSeperator)
  adminserverDir = File(directoryPath)
  bool = adminserverDir.mkdirs()
  fileNew=open(directoryPath + '/startup.properties', 'w')
  args=args.replace(':','\\:')
  args=args.replace('=','\\=')
  fileNew.write('Arguments=%s\n' % args)
  fileNew.flush()
  fileNew.close()
 #
# Set Log properties
def setLogProperties(logMBeanPath, logFile, fileCount, fileMinSize, rotationType, fileTimeSpan):
  print '\nSet Log Properties for: '+logMBeanPath
  print (lineSeperator)
  cd(logMBeanPath)
  print ('Server log path: '+pwd())
  print '. set FileName to '+logFile
  set('FileName'    ,logFile)
  print '. set FileCount to '+str(fileCount)
  set('FileCount'   ,int(fileCount))
  print '. set FileMinSize to '+str(fileMinSize)
  set('FileMinSize' ,int(fileMinSize))
  print '. set RotationType to '+rotationType
  set('RotationType',rotationType)
  print '. set FileTimeSpan to '+str(fileTimeSpan)
  set('FileTimeSpan',int(fileTimeSpan))
#

# Create Server Log
def createServerLog(serverName, logFile, fileCount, fileMinSize, rotationType, fileTimeSpan):
  print ('\nCreate Log for '+serverName)
  print (lineSeperator)
  cd('/Server/'+serverName)
  create(serverName,'Log')
  setLogProperties('/Server/'+serverName+'/Log/'+serverName, logFile, fileCount, fileMinSize, rotationType, fileTimeSpan)
#
# Change DataSource to XA
def changeDatasourceToXA(datasource):
  print 'Change datasource '+datasource
  print (lineSeperator)
  cd('/')
  cd('/JDBCSystemResource/'+datasource+'/JdbcResource/'+datasource+'/JDBCDriverParams/NO_NAME_0')
  set('DriverName','oracle.jdbc.xa.client.OracleXADataSource')
  print '. Set UseXADataSourceInterface='+'True'
  set('UseXADataSourceInterface','True') 
  cd('/JDBCSystemResource/'+datasource+'/JdbcResource/'+datasource+'/JDBCDataSourceParams/NO_NAME_0')
  print '. Set GlobalTransactionsProtocol='+'TwoPhaseCommit'
  set('GlobalTransactionsProtocol','TwoPhaseCommit')
  cd('/')
#

# Create cluster
def createCluster(cluster):
  print ('\nCreate '+cluster)
  print (lineSeperator)
  cd('/')
  create(cluster, 'Cluster')
#
# Create a Unix Machine
def createUnixMachine(serverMachine,serverAddress):
  print('\nCreate machine '+serverMachine+' with type UnixMachine')
  print (lineSeperator)
  cd('/')
  create(serverMachine,'UnixMachine')
  cd('UnixMachine/'+serverMachine)
  create(serverMachine,'NodeManager')
  cd('NodeManager/'+serverMachine)
  set('ListenAddress',serverAddress)
#
# Add server to  Unix Machine
def addServerToMachine(serverName, serverMachine):
  print('\nAdd server '+serverName+' to '+serverMachine)
  print (lineSeperator)
  cd('/Servers/'+serverName)
  set('Machine',serverMachine)
#
# Determine the Server Java Args
def getServerJavaArgs(serverName,javaArgsBase,logsHome):
  javaArgs = javaArgsBase+' -Dweblogic.Stdout='+logsHome+'/'+serverName+'.out -Dweblogic.Stderr='+logsHome+'/'+serverName+'_err.out'
  return javaArgs
#
# Change Managed Server
def changeManagedServer(server,listenAddress,listenPort,javaArgs):
  print '\nChange ManagedServer '+server
  print (lineSeperator)
  cd('/Servers/'+server)
  print '. Set listen address and port to: '+listenAddress+':'+str(listenPort)
  set('ListenAddress',listenAddress)
  set('ListenPort'   ,int(listenPort))
  # ServerStart
  print ('. Create ServerStart')
  create(server,'ServerStart')
  cd('ServerStart/'+server)
  print ('. Set Arguments to: '+javaArgs)
  set('Arguments' , javaArgs)
  # SSL
  cd('/Server/'+server)
  print ('. Create server SSL')
  create(server,'SSL')
  cd('SSL/'+server)
  print ('. Set SSL Enabled to: '+'False')
  set('Enabled'                    , 'False')
  print ('. Set SSL HostNameVerificationIgnored to: '+'True')
  set('HostNameVerificationIgnored', 'True')
  #
  if jsseEnabled == 'true':
    print ('. Set JSSEEnabled to: '+ 'True')
    set('JSSEEnabled','True')
  else:
    print ('. Set JSSEEnabled to: '+ 'False')
    set('JSSEEnabled','False')
#
# Create a Managed Server
def createManagedServer(server,listenAddress,listenPort,cluster,machine,
                        javaArgsBase,fileCount,fileMinSize,rotationType,fileTimeSpan):
  print('\nCreate '+server)
  print (lineSeperator)
  cd('/')
  create(server, 'Server')
  cd('/Servers/'+server)
  javaArgs=getServerJavaArgs(server,javaArgsBase,logsHome)
  changeManagedServer(server,listenAddress,listenPort,javaArgs)
  createServerLog(server, logsHome+'/'+server+'.log', fileCount, fileMinSize, rotationType, fileTimeSpan)
  print('Add '+server+' to cluster '+cluster)
  cd('/')
  assign('Server',server,'Cluster',cluster)
  addServerToMachine(server, machine)
#
# Adapt a Managed Server
def adaptManagedServer(server,newSrvName,listenAddress,listenPort,cluster,machine,
                       javaArgsBase,fileCount,fileMinSize,rotationType,fileTimeSpan):
  print('\nAdapt '+server)
  print (lineSeperator)
  cd('/')
  cd('/Servers/'+server)
  # name of adminserver
  print '. Rename '+server+' to '+ newSrvName
  set('Name',newSrvName )
  cd('/Servers/'+newSrvName)
  javaArgs=getServerJavaArgs(newSrvName,javaArgsBase,logsHome)
  changeManagedServer(newSrvName,listenAddress,listenPort,javaArgs)
  createServerLog(newSrvName, logsHome+'/'+newSrvName+'.log', fileCount, fileMinSize, rotationType, fileTimeSpan)
  print('Add '+newSrvName+' to cluster '+cluster)
  cd('/')
  assign('Server',newSrvName,'Cluster',cluster)
  addServerToMachine(newSrvName, machine)
#
# Change Admin Server
def changeAdminServer(adminServerName,listenAddress,listenPort,javaArguments):
  print '\nChange AdminServer'
  print (lineSeperator)
  cd('/Servers/AdminServer')
  # name of adminserver
  print '. Set Name to '+ adminServerName
  set('Name',adminServerName )
  cd('/Servers/'+adminServerName)
  # address and port
  print '. Set ListenAddress to '+ adminListenAddress
  set('ListenAddress',adminListenAddress)
  print '. Set ListenPort to '+ str(adminListenPort)
  set('ListenPort'   ,int(adminListenPort))
  #
  # ServerStart
  print 'Create ServerStart'
  create(adminServerName,'ServerStart')
  cd('ServerStart/'+adminServerName)
  print '. Set Arguments to: '+javaArguments
  set('Arguments' , javaArguments)
  # SSL
  cd('/Server/'+adminServerName)
  print 'Create SSL'
  create(adminServerName,'SSL')
  cd('SSL/'+adminServerName)
  set('Enabled'                    , 'False')
  set('HostNameVerificationIgnored', 'True')
  #
  if jsseEnabled == 'true':
    print ('. Set JSSEEnabled to: '+ 'True')
    set('JSSEEnabled','True')
  else:
    print ('. Set JSSEEnabled to: '+ 'False')
    set('JSSEEnabled','False')
#
#
def main():
  try:
    #
    # Section 1: Base Domain + Admin Server
    print (lineSeperator)
    print ('1. Create Base domain '+soaDomainName)
    print('\nCreate base wls domain with template '+wlsjar)
    print (lineSeperator)
    readTemplate(wlsjar)
    #
    cd('/')
    # Domain Log
    print('Set base_domain log')
    create('base_domain','Log')
    setLogProperties('/Log/base_domain', logsHome+soaDomainName+'.log', fileCount, fileMinSize, rotationType, fileTimeSpan)    
    #
    # Admin Server
    adminJavaArgs = getServerJavaArgs(adminServerName,adminJavaArgsBase,logsHome)
    changeAdminServer(adminServerName,adminListenAddress,adminListenPort,adminJavaArgs)
    createServerLog(adminServerName, logsHome+'/'+adminServerName+'.log', fileCount, fileMinSize, rotationType, fileTimeSpan)   
    
    # Set Admin password
    print('\nSet password in '+'/Security/base_domain/User/weblogic')
    cd('/')
    cd('Security/base_domain/User/weblogic')
    # weblogic user name + password
    print('. Set Name to: ' +adminUser)
    set('Name',adminUser)
    cmo.setPassword(adminPwd)
    
    # Set production mode
    if productionMode == 'true':
      print('. Set ServerStartMode to: ' +'prod')
      setOption('ServerStartMode', 'prod')
    else:
      print('. Set ServerStartMode to: ' +'dev')
      setOption('ServerStartMode', 'dev')
    
    # Writing the domain
    print('write Domain...')
    # write path + domain name
    writeDomain(soaDomainHome)
    closeTemplate()
    
    # Set startup and boot properties for admin
    createAdminStartupPropertiesFile(soaDomainHome+'/servers/'+adminServerName+'/data/nodemanager',adminJavaArgs)
    createBootPropertiesFile(soaDomainHome+'/servers/'+adminServerName+'/security','boot.properties',adminUser,adminPwd)
    createBootPropertiesFile(soaDomainHome+'/config/nodemanager','nm_password.properties',adminUser,adminPwd)
    
    # Encrypt admin password
    es = encrypt(adminPwd,soaDomainHome)
    
    # Get SOA domain
    readDomain(soaDomainHome)
    
    # Setting encrypted password for domain
    print('set Domain password for '+soaDomainName) 
    cd('/SecurityConfiguration/'+soaDomainName)
    set('CredentialEncrypted',es)
    
    # Set NM password
    print('Set nodemanager password')
    set('NodeManagerUsername' ,adminUser )
    set('NodeManagerPasswordEncrypted' ,es )
    
    # Set base application folder
    cd('/')
    setOption( "AppDir", soaApplicationsHome )
    #
    print('Finished base domain.')
    #
    # Section 2: Templates
    print('\n2. Extend Base domain with templates.')
    print (lineSeperator)
    print ('Adding Webservice template '+wlservicetpl)
    addTemplate(wlservicetpl)
    # SOA Suite
    if soaEnabled == 'true':
      print ('Adding SOA Template '+soatpl)    
      addTemplate(soatpl)
    else:
      print('SOA is disabled')
    # BPM
    if bpmEnabled == 'true':
      print ('Adding BPM Template '+bpmtpl)
      addTemplate(bpmtpl)
    else:
      print('BPM is disabled')
    # OSB
    if osbEnabled == 'true':
      print ('Adding OSB template '+osbtpl)
      addTemplate(osbtpl)
    else:
      print('OSB is disabled')
    
    # Application Core
    print ('Adding ApplCore Template '+applCoreTpl)
    addTemplate(applCoreTpl)
    
    # BAM
    if bamEnabled == 'true':
      print ('Adding BAM Template '+bamtpl)
      addTemplate(bamtpl)
    else:
      print ('BAM is disabled')
    
    # OHS Web-Tier
    if webtierEnabled == 'true' == true:
      print ('Adding OHS Template '+ohsTpl)
      addTemplate(ohsTpl)
    else:
      print('OHS is disabled') 
    
    # B2B     
    if b2bEnabled == 'true':
      print 'Adding B2B Template '+b2bTpl
      addTemplate(b2bTpl)
    else:
      print('B2B is disabled')
    
    # ESS
    if essEnabled == 'true':
      print ('Adding ESS Template'+essBasicTpl)
      addTemplate(essBasicTpl)
      print ('Adding ESS Em Template'+essEmTpl)
      addTemplate(essEmTpl)
    else:
      print('ESS is disabled')
    # 
    dumpStack()
    print ('Finished templates')
    #
    # Section 3: Change Datasources
    print ('\n3. Change datasources')
    print 'Change datasource LocalScvTblDataSource'
    cd('/JDBCSystemResource/LocalSvcTblDataSource/JdbcResource/LocalSvcTblDataSource/JDBCDriverParams/NO_NAME_0')
    set('URL',soaRepositoryDbUrl)
    set('PasswordEncrypted',soaRepositoryStbPwd)
    cd('Properties/NO_NAME_0/Property/user')
    set('Value',soaRepositoryDbUserPrefix+'_STB')
    #
    print ('Call getDatabaseDefaults which reads the service table')
    getDatabaseDefaults()    
    #
    if soaEnabled == 'true':
      changeDatasourceToXA('EDNDataSource')
    if osbEnabled == 'true':
      changeDatasourceToXA('wlsbjmsrpDataSource')
    changeDatasourceToXA('OraSDPMDataSource')
    changeDatasourceToXA('SOADataSource')
    #
    if bamEnabled == 'true':
      changeDatasourceToXA('BamDataSource')
    #
    print '\nFinshed DataSources'
    #
    # Section 4: Create UnixMachines, Clusters and Managed Servers
    print ('\n4. Create UnixMachines, Clusters and Managed Servers')
    print (lineSeperator)
    cd('/')
    #
    print ("\nConfiguring " + serversNumber + " Unix Machines")
    serverAddressArray=serverAddresses.split(',')
    serverMachineArray=serverMachines.split(',')
    
    for i in range(0,int(serversNumber)):
      server_address=serverAddressArray[i]
      server_machine=serverMachineArray[i]
      createUnixMachine(server_machine,server_address)
      if i == 0:
        addServerToMachine(adminServerName,server_machine)
        
    #
    cd('/')
   # SOA Suite
    if soaEnabled == 'true':
      createCluster(soaClr)
      soaSvrNameArray=soaSvrNames.split(',')
      soaSvrAddressArray=soaSvrAddresses.split(',')
      soaSvrMachineArray=soaSvrMachines.split(',')

      for i in range(0,int(soaNumber)):
        if i == 0:
          adaptManagedServer('soa_server1',soaSvrNameArray[i],soaSvrAddressArray[i], soaSvrPort,soaClr,soaSvrMachineArray[i],soaJavaArgsBase,fileCount,fileMinSize,rotationType,fileTimeSpan)
        else:
          createManagedServer(soaSvrNameArray[i],soaSvrAddressArray[i], soaSvrPort,soaClr,soaSvrMachineArray[i],soaJavaArgsBase,fileCount,fileMinSize,rotationType,fileTimeSpan)
    
    #
   # OSB
    if osbEnabled == 'true':
      createCluster(osbClr)
      osbSvrNameArray=osbSvrNames.split(',')
      osbSvrAddressArray=osbSvrAddresses.split(',')
      osbSvrMachineArray=osbSvrMachines.split(',')

      for i in range(0,int(osbNumber)):
        if i == 0:
          adaptManagedServer('osb_server1',osbSvrNameArray[i],osbSvrAddressArray[i], osbSvrPort,osbClr,osbSvrMachineArray[i],osbJavaArgsBase,fileCount,fileMinSize,rotationType,fileTimeSpan)
        else:
          createManagedServer(osbSvrNameArray[i],osbSvrAddressArray[i], osbSvrPort,osbClr,osbSvrMachineArray[i],osbJavaArgsBase,fileCount,fileMinSize,rotationType,fileTimeSpan)
    #
   # BAM
    if bamEnabled == 'true':
      createCluster(bamClr)
      bamSvrNameArray=bamSvrNames.split(',')
      bamSvrAddressArray=bamSvrAddresses.split(',')
      bamSvrMachineArray=bamSvrMachines.split(',')

      for i in range(0,int(bamNumber)):
        if i == 0:
          adaptManagedServer('bam_server1',bamSvrNameArray[i],bamSvrAddressArray[i], bamSvrPort,bamClr,bamSvrMachineArray[i],bamJavaArgsBase,fileCount,fileMinSize,rotationType,fileTimeSpan)
        else:
          createManagedServer(bamSvrNameArray[i],bamSvrAddressArray[i], bamSvrPort,bamClr,bamSvrMachineArray[i],bamJavaArgsBase,fileCount,fileMinSize,rotationType,fileTimeSpan)
      
   #
    # ESS
    if essEnabled == 'true':
      createCluster(essClr)
      essSvrNameArray=essSvrNames.split(',')
      essSvrAddressArray=essSvrAddresses.split(',')
      essSvrMachineArray=essSvrMachines.split(',')

      for i in range(0,int(essNumber)):
        if i == 0:
          adaptManagedServer('ess_server1',essSvrNameArray[i],essSvrAddressArray[i], essSvrPort,essClr,essSvrMachineArray[i],essJavaArgsBase,fileCount,fileMinSize,rotationType,fileTimeSpan)
        else:
          createManagedServer(essSvrNameArray[i],essSvrAddressArray[i], essSvrPort,essClr,essSvrMachineArray[i],essJavaArgsBase,fileCount,fileMinSize,rotationType,fileTimeSpan)
      
 
    #
    print ('Finshed creating Machines, Clusters and ManagedServers')
    #
    # Section 5: Add Servers to ServerGroups.
    print ('\n5. Add Servers to ServerGroups')
    print (lineSeperator)
    cd('/')
    print 'Add server groups '+adminSvrGrpDesc+ ' to '+adminServerName
    setServerGroups(adminServerName, adminSvrGrp)                      
    # SOA
    if soaEnabled == 'true':
      for i in range(0,int(soaNumber)):
        print 'Add server group '+soaSvrGrpDesc+' to '+soaSvrNameArray[i]
        setServerGroups(soaSvrNameArray[i], soaSvrGrp)
      
    #      
    # OSB
    if osbEnabled == 'true':
      for i in range(0,int(osbNumber)):
        print 'Add server group '+osbSvrGrpDesc+' to '+osbSvrNameArray[i]
        setServerGroups(osbSvrNameArray[i], osbSvrGrp)
    #
    if bamEnabled == 'true':
      for i in range(0,int(bamNumber)):
        print 'Add server group '+bamSvrGrpDesc+' to '+bamSvrNameArray[i]
        setServerGroups(bamSvrNameArray[i], bamSvrGrp)   
    #
    if essEnabled == 'true':
      for i in range(0,int(essNumber)):
        print 'Add server group '+essSvrGrpDesc+' to '+essSvrNameArray[i]
        setServerGroups(essSvrNameArray[i], essSvrGrp)
    #
    print ('Finshed ServerGroups.')
    #
    updateDomain()
    closeDomain();
    #
    # Section 6: Create boot properties files.
    print ('\n6. Create boot properties files')
    print (lineSeperator)
    # SOA
    if soaEnabled == 'true':
      for i in range(0,int(soaNumber)):
        createBootPropertiesFile(soaDomainHome+'/servers/'+soaSvrNameArray[i]+'/security','boot.properties',adminUser,adminPwd)
    #
    # OSB
    if osbEnabled == 'true':
      for i in range(0,int(osbNumber)):
        createBootPropertiesFile(soaDomainHome+'/servers/'+osbSvrNameArray[i]+'/security','boot.properties',adminUser,adminPwd)
    #
    if bamEnabled == 'true':
      for i in range(0,int(bamNumber)):
        createBootPropertiesFile(soaDomainHome+'/servers/'+bamSvrNameArray[i]+'/security','boot.properties',adminUser,adminPwd)
    #
    if essEnabled == 'true':
      for i in range(0,int(essNumber)):
        createBootPropertiesFile(soaDomainHome+'/servers/'+essSvrNameArray[i]+'/security','boot.properties',adminUser,adminPwd)
    #
    print ('\nFinished')
    print ('\nSuccessfully configured wls domain')
    #
    print('\nExiting...')
    exit()
  except NameError, e:
    print 'Apparently properties not set.'
    print "Please check the property: ", sys.exc_info()[0], sys.exc_info()[1]
    usage()
  except:
    apply(traceback.print_exception, sys.exc_info())
    stopEdit('y')
    exit(exitcode=1)
#call main()
main()
exit()