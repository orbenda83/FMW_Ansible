wls_user="weblogic"
wls_pass="<WLS_PASSWORD>"
wls_admin="t3://<ADMIN_HOST>:<ADMIN_PORT>"

connect(wls_user,wls_pass,wls_admin)

edit()
startEdit()

cd('/')
cmo.createStartupClass('GlobalParamsStartup')

cd('/StartupClasses/GlobalParamsStartup')
cmo.setClassName('corp.evo.ims.GlobalParamsStartup')
set('Targets',jarray.array([ObjectName('com.bea:Name=AdminServer,Type=Server'), ObjectName('com.bea:Name=bpm_cluster,Type=Cluster'), ObjectName('com.bea:Name=osb_cluster,Type=Cluster')], ObjectName))

activate()

disconnect()

exit()