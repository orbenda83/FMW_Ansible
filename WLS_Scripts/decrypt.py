import os.path
import sys

print "************************************************************************"
print "*** Successfully Started Configuring JMS Resources *********************"
print "************************************************************************"

dec_value=""
domain=""

if (len(sys.argv) > 2):
	dec_value=sys.argv[1]
	domain=sys.argv[2]
else:
	print "Environment Property file not specified"
	sys.exit(2)
 
service = weblogic.security.internal.SerializedSystemIni.getEncryptionService(domain)  
encryption = weblogic.security.internal.encryption.ClearOrEncryptedService(service)  

print "The value is: %s" %encryption.decrypt(dec_value)