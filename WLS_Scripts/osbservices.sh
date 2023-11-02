#!/bin/sh
# set up WL_HOME and OSBHOME the root directory of your WebLogic installation
WL_HOME="/opt/oracle/middleware"
OSBHOME="OSB_HOME Directory"
rm output.txt
umask 027

# set up common environment
WLS_NOT_BRIEF_ENV=true
. "${WL_HOME}/server/bin/setWLSEnv.sh"


CLASSPATH="${CLASSPATH}${CLASSPATHSEP}${FMWLAUNCH_CLASSPATH}${CLASSPATHSEP}${DERBY_CLASSPATH}${CLASSPATHSEP}${DERBY_TOOLS}${CLASSPATHSEP}${POINTBASE_CLASSPATH}${CLASSPATHSEP}${POINTBASE_TOOLS}"

CLASSPATH=$CLASSPATH:$WL_HOME/osb/lib/modules/oracle.servicebus.configfwk.jar:$WL_HOME/server/lib/weblogic.jar;
#CLASSPATH=$CLASSPATH:$OSBHOME/modules/com.bea.common.configfwk_1.6.0.0.jar:$OSBHOME/lib/sb-kernel-api.jar:$OSBHOME/lib/sb-kernel-impl.jar:$WL_HOME/server/lib/weblogic.jar:$OSBHOME/lib/alsb.jar;
export CLASSPATH

if [ "${WLST_HOME}" != "" ] ; then
        WLST_PROPERTIES="-Dweblogic.wlstHome='${WLST_HOME}'${WLST_PROPERTIES}"
        export WLST_PROPERTIES
fi
JVM_ARGS="-Dprod.props.file='${WL_HOME}'/.product.properties ${WLST_PROPERTIES} ${JVM_D64} ${MEM_ARGS} ${CONFIG_JVM_ARGS}"

ORACLE_HOME/common/bin/wlst.sh osbservices.py  >> output.txt
date >> output.txt