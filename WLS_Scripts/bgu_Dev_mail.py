connect('weblogic','<WLS_PASSWORD>','t3://<ADMIN_HOST>:<ADMIN_PORT>') 
# 4. wls:/base_domain/domainRuntime/>
#edit()
connect('weblogic','<WLS_PASSWORD>','t3://<ADMIN_HOST>:<ADMIN_PORT>') 
 driverProperties=EmailDriverProperties()
 driverProperties.OutgoingMailServer='<EXCHANGE_HOST>'
 driverProperties.RetryLimit='3'
 driverProperties.IncomingMailServer='<EXCHANGE_HOST>'
 driverProperties.IncomingMailIDs = '<MAIL_ID>'
 driverProperties.IncomingUserIDs = '<MAIL_ID>'
 driverProperties.OutgoingMailServerPort='25'
 driverProperties.OutgoingDefaultFromAddr='<MAIL_ID>'
 driverProperties.OutgoingPassword = '<MAIL_PASS>'
 driverProperties.IncomingMailServerPort = '993'
 driverProperties.ProcessingChunkSize = '100'
 driverProperties.IncomingUserPasswords = '<MAIL_PASS>'
 configUserMessagingDriver(baseDriver='email',appName='Xmail',driverProperties=driverProperties,clusterName='bpm_cluster')


# print EmailDriverProperties().__dict__
# {'AutoDelete': None, 'IncomingUserIDs': None, 'OutgoingMailServerPort': None, #'OutgoingPassword': None, 'MailAccessProtocol': None, 'OutgoingUsername': #None, 'Debug': None, 'OutgoingMailServer': None, 'OutgoingDefaultFromAddr': #None, 'OutgoingMailServerSecurity': None, 'IncomingMailServerPort': None, #'ProcessingChunkSize': None, 'CheckMailFreq': None, 'IncomingMailServerSSL': #None, 'ImapAuthPlainDisable': None, 'IncomingUserPasswords': None, #'ReceiveFolder': None, 'IncomingMailServer': None, 'IncomingMailIDs': None}

# print ServerProperties().__dict__
# {'WhiteListEnabled': None, 'WhiteList': None, 'EnginePendingReceiveQueueInfo': None, 'DuplicateMessageRetryDelay': None, 'ReceivedmessageStatusEnabled': None, 'ResendMax': None, 'EngineSendingQueuesInfo': None, 'SupportedDeliveryTypes': None, 'JpsContext': None, 'SecurityPrincipal': None, 'EngineReceivingQueuesInfo': None, 'ResendDelay': None, 'SessionTimeout': None, 'AppReceivingQueuesInfo': None, 'ResendDefault': None}