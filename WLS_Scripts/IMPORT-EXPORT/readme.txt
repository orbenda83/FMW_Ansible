This sample demonstrates the import and export capabilities in OSB 10gR3 using WLST


It shows the use of WLST to write powerful scripts controlling import and export of OSB configurations. It also illustrates the use of Customization Files. 

############# before starting  ##############
The properties files - export.properties and import.properties - control the behavior of the scripts

export.properties:
set the OSB domain config properly: adminUrl, exportUser, exportPassword
-if a project is specified, will export all the resources contained in the project
-if no project is specified the whole config is exported
exportJar is the name of the configuration file created by export
customizationFile is the optional name of a created customization file with a findAndReplace action

import.properties:
set the OSB domain config properly: adminUrl, exportUser, exportPassword
-if a project is specified, the project will be overlaid by the new config (resources updated, created or deleted)
-if no project is specified an additive deployment will be performed (resources updated or created)

exportJar is the name of the config file to import
customizationFile is the optional name of a customization file. If a project is specified the customization will only be applied to created resources.

############# running the samples ############
To run the sample make sure your path and classpath are setup correctly with java, ant, weblogic/osb libraries and python
Easiest way is to run setDomainEnv from your favorite shell

edit the import and export properties file as described above

run "ant export" to export a config
It will launch WLST, execute export.py and create a file with the exported config (optionally a customization file)

run "ant import" to import a config
It will launch WLST, execute import.py and import the configuration on your target server

Feel free to edit the scripts to personalize them to your needs


