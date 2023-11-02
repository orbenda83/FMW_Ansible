from java.util import HashMap
from java.util import HashSet
from java.util import ArrayList
from java.io import FileInputStream

from com.bea.wli.sb.util import Refs
from com.bea.wli.config.customization import Customization
from com.bea.wli.sb.management.importexport import ALSBImportOperation

import sys

#=======================================================================================
# Entry function to deploy project configuration and resources
#        into a ALSB domain
#=======================================================================================

def importToALSBDomain(globalConfigFile, importConfigFile):
    try:
        SessionMBean = None
        print 'Loading Deployment config from :', globalConfigFile
        globalConfigProp = loadProps(globalConfigFile)
        adminUrl = globalConfigProp.get("adminUrl")
        importUser = globalConfigProp.get("importUser")
        importPassword = globalConfigProp.get("importPassword")
        deploymetDir = globalConfigProp.get("deploymetDir")
        customDir = globalConfigProp.get("customDir")
        
        print 'Loading Deployment config from :', importConfigFile
        configProp = loadProps(importConfigFile)
        total_ds=configProp.get("import.arraySize")
        request_id=configProp.get("requestID")

        for i in range(0,int(total_ds)):
            jarToDeploy = configProp.get("import." + str(i) + ".jar")
            customFile = configProp.get("import." + str(i) + ".customFile")
            passphrase = configProp.get("import." + str(i) + ".passphrase")
            project = configProp.get("import." + str(i) + ".project")

            importJar(importUser, importPassword, adminUrl, jarToDeploy, customFile, passphrase, project, request_id, deploymetDir, customDir)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        if SessionMBean != None:
            SessionMBean.discardSession(sessionName)
        raise

#=======================================================================================
# Utility function to print the list of operations
#=======================================================================================
def printOpMap(map):
    set = map.entrySet()
    for entry in set:
        op = entry.getValue()
        print op.getOperation(),
        ref = entry.getKey()
        print ref
    print

#=======================================================================================
# Utility function to print the diagnostics
#=======================================================================================
def printDiagMap(map):
    set = map.entrySet()
    for entry in set:
        diag = entry.getValue().toString()
        print diag
    print

#=======================================================================================
# Utility function to load properties from a config file
#=======================================================================================

def loadProps(configPropFile):
    propInputStream = FileInputStream(configPropFile)
    configProps = Properties()
    configProps.load(propInputStream)
    return configProps

#=======================================================================================
# Connect to the Admin Server
#=======================================================================================

def connectToServer(username, password, url):
    connect(username, password, url)
    domainRuntime()

#=======================================================================================
# Utility function to read a binary file
#=======================================================================================
def readBinaryFile(fileName):
    file = open(fileName, 'rb')
    bytes = file.read()
    return bytes

#=======================================================================================
# Utility function to create an arbitrary session name
#=======================================================================================
def createSessionName():
    sessionName = String("SessionScript"+Long(System.currentTimeMillis()).toString())
    return sessionName

#=======================================================================================
# Utility function to load a session MBeans
#=======================================================================================
def getSessionManagementMBean(sessionName):
    SessionMBean = findService("SessionManagement", "com.bea.wli.sb.management.configuration.SessionManagementMBean")
    SessionMBean.createSession(sessionName)
    return SessionMBean

#=======================================================================================
# Utility function to import the OSB deployment
#=======================================================================================
def importJar(importUser, importPassword, adminUrl, jarToDeploy, customFile, passphrase, project, request_id, deploymetDir, customDir):
    try:
        connectToServer(importUser, importPassword, adminUrl)

        print 'Attempting to import :', jarToDeploy, " from Request Id: ", request_id, "on ALSB Admin Server listening on :", adminUrl

        theBytes = readBinaryFile(deploymetDir + "/" + jarToDeploy)
        print 'Read file', deploymetDir + "/" + jarToDeploy
        sessionName = createSessionName()
        print 'Created session', sessionName
        SessionMBean = getSessionManagementMBean(sessionName)
        print 'SessionMBean started session'
        ALSBConfigurationMBean = findService(String("ALSBConfiguration.").concat(sessionName), "com.bea.wli.sb.management.configuration.ALSBConfigurationMBean")
        print "ALSBConfiguration MBean found", ALSBConfigurationMBean
        ALSBConfigurationMBean.uploadJarFile(theBytes)
        print 'Jar Uploaded'

        if project == None:
            print 'No project specified, additive deployment performed'
            alsbJarInfo = ALSBConfigurationMBean.getImportJarInfo()
            alsbImportPlan = alsbJarInfo.getDefaultImportPlan()
            alsbImportPlan.setPassphrase(passphrase)
            alsbImportPlan.setPreserveExistingEnvValues(true)
            importResult = ALSBConfigurationMBean.importUploaded(alsbImportPlan)
            #SessionMBean.activateSession(sessionName, "Deployment " + jarToDeploy + " from Request Id: " + request_id)
            SessionMBean.activateSession(sessionName, request_id + " -> " + jarToDeploy)
        else:
            print 'ALSB project', project, 'will get overlaid'
            alsbJarInfo = ALSBConfigurationMBean.getImportJarInfo()
            alsbImportPlan = alsbJarInfo.getDefaultImportPlan()
            alsbImportPlan.setPassphrase(passphrase)
            operationMap=HashMap()
            operationMap = alsbImportPlan.getOperations()
            print
            print 'Default importPlan'
            printOpMap(operationMap)
            set = operationMap.entrySet()

            alsbImportPlan.setPreserveExistingEnvValues(true)

            #boolean
            abort = false
            #list of created ref
            createdRef = ArrayList()

            for entry in set:
                ref = entry.getKey()
                op = entry.getValue()
                #set different logic based on the resource type
                type = ref.getTypeId
                if type == Refs.SERVICE_ACCOUNT_TYPE or type == Refs.SERVICE_PROVIDER_TYPE:
                    if op.getOperation() == ALSBImportOperation.Operation.Create:
                        print 'Unable to import a service account or a service provider on a target system', ref
                        abort = true
                elif op.getOperation() == ALSBImportOperation.Operation.Create:
                    #keep the list of created resources
                    createdRef.add(ref)

            if abort == true :
                print 'This jar must be imported manually to resolve the service account and service provider dependencies'
                SessionMBean.discardSession(sessionName)
                raise

            print
            print 'Modified importPlan'
            printOpMap(operationMap)
            importResult = ALSBConfigurationMBean.importUploaded(alsbImportPlan)

            printDiagMap(importResult.getImportDiagnostics())

            if importResult.getFailed().isEmpty() == false:
                print 'One or more resources could not be imported properly'
                raise

            #customize if a customization file is specified
            #affects only the created resources
            if customFile != None :
                print 'Loading customization File', customDir + "/" + customFile
                print 'Customization applied to the created resources only', createdRef
                iStream = FileInputStream(customDir + "/" + customFile)
                customizationList = Customization.fromXML(iStream)
                filteredCustomizationList = ArrayList()
                setRef = HashSet(createdRef)

                # apply a filter to all the customizations to narrow the target to the created resources
                for customization in customizationList:
                    print customization
                    newcustomization = customization.clone(setRef)
                    filteredCustomizationList.add(newcustomization)

                ALSBConfigurationMBean.customize(filteredCustomizationList)

            SessionMBean.activateSession(sessionName, "Complete test import with customization using wlst")

        print "Deployment of : " + jarToDeploy + " successful"
    except:
        print "Unable to deploy " + jarToDeploy + " deployment."
        dumpStack()
        raise

#=======================================================================================
# MAIN
#=======================================================================================
# IMPORT script init
try:
    # import the service bus configuration
    # argv[1] is the export config properties file
    importToALSBDomain(sys.argv[1], sys.argv[2])

except:
    print "Unexpected error: ", sys.exc_info()[0]
    dumpStack()
    raise
