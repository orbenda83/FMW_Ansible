print "************************************************************************"
print "*** Successfully Started Configuring Adapters **************************"
print "************************************************************************"

import time
import traceback
import sys

def makeDeploymentPlanVariable(moduleOverrideName, wlstPlan, name, value, xpath, origin='planbased', moduleDescriptorName='META-INF/weblogic-ra.xml'):

    try:
        if wlstPlan.getVariableAssignment(name, moduleOverrideName, moduleDescriptorName):
            print 'Variable Assignment exists.'
            wlstPlan.destroyVariableAssignment(name, moduleOverrideName, moduleDescriptorName)
            print 'Variable Assignment destroyed.'
            if wlstPlan.getVariable(name):
                print 'Variable '+name+' exists.'
                wlstPlan.destroyVariable(name)
                print 'Variable '+name+' destroyed.'
                variableAssignment = wlstPlan.createVariableAssignment( name, moduleOverrideName, moduleDescriptorName )
                variableAssignment.setXpath( xpath )
                variableAssignment.setOrigin( origin )
                wlstPlan.createVariable( name, value )
        else:
            print 'Variable Assignment Doesn\'t exists.'
            variableAssignment = wlstPlan.createVariableAssignment(name, moduleOverrideName, moduleDescriptorName)  
            variableAssignment.setXpath(xpath)
            variableAssignment.setOrigin(origin)
            wlstPlan.createVariable(name, value)

    except:
        print('–> was not able to create deployment plan variables successfully')

def setEntries(adapterDepName,plan,cf,value,planType,subType):
    if planType == 'DB':
        if subType == 'xa':
            dbType='xADataSourceName'
        else:
            dbType='dataSourceName'

    
        makeDeploymentPlanVariable(adapterDepName, plan, 'ConnectionInstance_'+ cf +'_JNDIName', cf, '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="javax.resource.cci.ConnectionFactory"]/connection-instance/[jndi-name="'+ cf + '"]/jndi-name')

        makeDeploymentPlanVariable(adapterDepName, plan, 'ConfigProperty_' + dbType + '_'+ value ,value, '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="javax.resource.cci.ConnectionFactory"]/connection-instance/[jndi-name="'+ cf + '"]/connection-properties/properties/property/[name="' + dbType +'"]/value')

    if planType == 'JMS':
        makeDeploymentPlanVariable(adapterDepName, plan, 'ConnectionInstance_'+ cf +'_JNDIName', cf, '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="oracle.tip.adapter.jms.IJmsConnectionFactory"]/connection-instance/[jndi-name="'+ cf + '"]/jndi-name')

        makeDeploymentPlanVariable(jmsAadapterDepNamedapterDepName, plan, 'ConfigProperty_ConnectionFactoryLocation_'+ cf ,value, '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="oracle.tip.adapter.jms.IJmsConnectionFactory"]/connection-instance/[jndi-name="'+ cf + '"]/connection-properties/properties/property/[name="ConnectionFactoryLocation"]/value')


def configurePlan(depName,appPath,planPath,planType,CFArray):
    print '__ Using plan ' + str(planPath)
    myPlan=loadApplication(appPath, planPath)
    print '___ BEGIN change plan'

    for cf in CFArray:
        CFName=cf['name']
        CfDs=cf['ds']

        print '___ .. Configuring ' + CFName + ' --> ' + CfDs
        print '___ .. Plan Type ' + planType
        
        if planType == 'DB':
            cfType=cf['dsType']

            setEntries(depName,myPlan,CFName, CfDs, planType, cfType)
        
        if planType == 'JMS':
            setEntries(depName,myPlan,CFName, CfDs, planType, None)

    print '___ DONE change plan'
    myPlan.save();
    save();
    activate(block='true');
    print 'Activated...'

def main():
    #Connect to WLS admin
    print "Connecting to WLS Admin"
    connect(wls_user,wls_pass,wls_admin)
    edit()
    
    # dbAdapterEnabled=db['enabled']
    # jmsAdapterEnabled=jms['enabled']

    try:
        if dbAdapterEnabled:
            dbAdapterDepName=db['name']
            depName=dbAdapterDepName.split('.')[0]
            startEdit()
            # planPath = get('/AppDeployments/DbAdapter/PlanPath')
            planPath = domainConfigPath + db['planName']
            print "planPath => " + planPath
            depPath = appPath + dbAdapterDepName
            dbCFArray=db['cfs']
            
            # if planPath == None:
            #     print 'Got None planPath, defaulting to ' + domainConfigPath + db['planName']
            #     planPath = domainConfigPath + db['planName']
                
            configurePlan(dbAdapterDepName,depPath,planPath,'DB',dbCFArray)
            
            cd('/AppDeployments/DbAdapter/Targets');
            redeploy(depName, planPath,targets=cmo.getTargets());
            print 'EIS Connection factory for ' + depName + ' configured';

        if jmsAdapterEnabled:
            jmsAdapterDepName=jms['name']
            depName=jmsAdapterDepName.split('.')[0]
            startEdit()
            # startApplication(appNameJms)
            # planPath = get('/AppDeployments/JmsAdapter/PlanPath')
            planPath = domainConfigPath + db['planName']
            print "planPath => " + planPath
            depPath = appPath + jmsAdapterDepName
            jmsCFArray=jms['cfs']
            configurePlan(jmsAdapterDepName,depPath,planPath,'JMS',jmsCFArray)   

            cd('/AppDeployments/JmsAdapter/Targets');
            redeploy(depName, planPath,targets=cmo.getTargets());
            print 'EIS Connection factory ' + depName + ' configured';
    except Exception:
        print 'EXCEPTION'
    #     stopEdit('y')
    #     pass
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
    #     # stopEdit('y')

    print "Adapter modification finished successfully."

# Main function
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

main()