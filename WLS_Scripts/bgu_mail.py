connect('weblogic','bpmdev4all','t3://localhost:7101') 
# 4. wls:/base_domain/domainRuntime/>
#edit()
connect('weblogic','bpmdev4all','t3://localhost:7101') 
 driverProperties=EmailDriverProperties()
 driverProperties.OutgoingMailServer='xmail.bgu.ac.il'
 driverProperties.RetryLimit='3'
 driverProperties.IncomingMailServer='xmail.bgu.ac.il'
 driverProperties.IncomingMailIDs = 'devbpm@bgu.ac.il'
 driverProperties.IncomingUserIDs = 'devbpm@bgu.ac.il'
 driverProperties.OutgoingMailServerPort='25'
 driverProperties.OutgoingDefaultFromAddr='devbpm@bgu.ac.il'
 driverProperties.OutgoingPassword = 'kgvePi8p'
 driverProperties.IncomingMailServerPort = '993'
 driverProperties.ProcessingChunkSize = '100'
 driverProperties.IncomingUserPasswords = 'kgvePi8p'
 configUserMessagingDriver(baseDriver='email',appName='Xmail2',driverProperties=driverProperties,serverName='DefaultServer')


# print EmailDriverProperties().__dict__
# {'AutoDelete': None, 'IncomingUserIDs': None, 'OutgoingMailServerPort': None, #'OutgoingPassword': None, 'MailAccessProtocol': None, 'OutgoingUsername': #None, 'Debug': None, 'OutgoingMailServer': None, 'OutgoingDefaultFromAddr': #None, 'OutgoingMailServerSecurity': None, 'IncomingMailServerPort': None, #'ProcessingChunkSize': None, 'CheckMailFreq': None, 'IncomingMailServerSSL': #None, 'ImapAuthPlainDisable': None, 'IncomingUserPasswords': None, #'ReceiveFolder': None, 'IncomingMailServer': None, 'IncomingMailIDs': None}

# print ServerProperties().__dict__
# {'WhiteListEnabled': None, 'WhiteList': None, 'EnginePendingReceiveQueueInfo': None, 'DuplicateMessageRetryDelay': None, 'ReceivedmessageStatusEnabled': None, 'ResendMax': None, 'EngineSendingQueuesInfo': None, 'SupportedDeliveryTypes': None, 'JpsContext': None, 'SecurityPrincipal': None, 'EngineReceivingQueuesInfo': None, 'ResendDelay': None, 'SessionTimeout': None, 'AppReceivingQueuesInfo': None, 'ResendDefault': None}