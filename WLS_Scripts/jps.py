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
si=configProps.get("si")

connect(wls_user,wls_pass,wls_admin)
domainRuntime()

total_params=configProps.get("total_params")

for i in range(0,int(total_params)):
	key=configProps.get('param.' + str(i) + '.key')
	val=configProps.get('param.' + str(i) + '.val')
	
	on = ObjectName("com.oracle.jps:type=JpsConfig")
	sign = ["java.lang.String","java.lang.String","java.lang.String"]
	params = [si,key,val]
	mbs.invoke(on, "updateServiceInstanceProperty", params, sign)
	mbs.invoke(on, "persist", None, None)
