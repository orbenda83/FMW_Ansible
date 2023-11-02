[WLST by Example](https://wlstbyexamples.blogspot.com/)  
http://itbuzzpress.com/weblogic-tutorials/oracle-weblogic-wlst.html  
http://www.learn-it-with-examples.com/middleware/weblogic/weblogic-scripting-tool/create-weblogic-data-source-wlst.html  
https://www.oracle.com/webfolder/technetwork/tutorials/obe/fmw/wls/12c/09-DeployPlan--4464/deployplan.htm  
  
  
  
#### Running wlst: 

```bash
${ORACLE_HOME}/wlserver_10.3/common/bin/wlst.sh   

offline:\> help()  
offline:\> help('connect')  
BPMDomain:\>   
```  
  
#### 1st way to invoke:  
```bash
${ORACLE_HOME}/wlserver_10.3/common/bin/wlst.sh/cmd/bat <script>.py [<extra args/properties file/etc>]  
```
  
##### example:  
```bash
${ORACLE_HOME}/wlserver_10.3/common/bin/wlst.sh JMS.py JMS_dev.properties  
```
  
#### 2nd way to invoke:  
```bash
${ORACLE_HOME}/wlserver/server/bin/setWLSEnv.sh  
${JAVA_HOME}/bin/java weblogic.WLST <script>.py [<extra args/properties file/etc>]  
```
  
##### example:  
```bash
${ORACLE_HOME}/wlserver_10.3/common/bin/wlst.sh JMS.py JMS_dev.properties
```

**Note:** The DB Adapter scripts needs to run on the AdminServer Machine due to a bug in WLST (not loading remote resources).

TODO: Add running explanations on all the resource types.  
TODO: Standardize the running mechanism for Ansible implementation.  

${ORACLE_HOME}/wlserver_10.3/common/bin/wlst.sh/cmd/bat decrypt.py <decoded> <full domain path>