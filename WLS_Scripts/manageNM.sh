#!/bin/sh
#
### BEGIN INIT INFO
# Provides:        nodemanager
# Required-Start:
# Required-Stop:
# Default-Start:    2 3 4 5
# Default-Stop:        0 1 6
# Short-Description:    WebLogic Nodemanager
### END INIT INFO

# nodemgr Oracle Weblogic NodeManager service
#
# chkconfig:   345 99 15
# description: Oracle Weblogic NodeManager service
# 

### BEGIN INIT INFO
# Provides: nodemgr
# Required-Start: $network $local_fs
# Required-Stop:
# Should-Start:
# Should-Stop:
# Default-Start: 3 4 5
# Default-Stop: 0 1 2 6
# Short-Description: Oracle Weblogic NodeManager service.
# Description: Starts and stops Oracle Weblogic NodeManager.
### END INIT INFO

# Source function library.
if test -f /lib/lsb/init-functions; then
    . /lib/lsb/init-functions
fi

. /etc/init.d/functions

# set NodeManager environment
NodeManagerLockFile=/opt/oracle/middleware/user_projects/domains/bpm_domain/nodemanager/nodemanager.process.lck
exec=/opt/oracle/middleware/user_projects/domains/bpm_domain/bin/startNodeManager.sh
prog='nodemanager'
user=oracle

is_nodemgr_running() {
    local nodemgr_cnt=`ps -ef        | \
        grep -i 'java'                  | \
        grep -i 'weblogic.NodeManager'  | \
        grep -i '/opt/oracle/middleware/user_projects/domains/bpm_domain'  | \
        grep -v grep                  | \
        wc -l`
    echo $nodemgr_cnt
}

get_nodemgr_pid() {
    nodemgr_pid=0
    if [ `is_nodemgr_running` -eq 1 ]; then
        nodemgr_pid=`ps -ef             | \
            grep -i 'java'                 | \
            grep -i 'weblogic.NodeManager' | \
            grep -i '/opt/oracle/middleware/user_projects/domains/bpm_domain'  | \
            grep -v grep                 | \
            tr -s ' '                    | \
            cut -d' ' -f2`
    fi
    echo $nodemgr_pid
}

check_nodemgr_status () {
    local retval=0
    local nodemgr_cnt=`is_nodemgr_running`
    if [ $nodemgr_cnt -eq 0 ]; then
        if [ -f $NodeManagerLockFile ]; then
            retval=2
        else
            retval=3
        fi
    elif [ $nodemgr_cnt -gt 1 ]; then
        retval=4
    else
        retval=0
    fi

    echo $retval
}

start() {
    ulimit -n 65535
    [ -x $exec ] || exit 5
    echo -n $"Starting $prog: "
    sleep 10
    if [ "$USER" == "$user" ]
    then
       export JAVA_OPTIONS=-Djava.security.egd=file:/dev/./urandom;$exec &>/dev/null &
    else
       su $user -c "export JAVA_OPTIONS=-Djava.security.egd=file:/dev/./urandom;$exec &>/dev/null &"
    fi
    retval=$?
    echo
    return $retval
}

stop() {
    echo -n $"Stopping $prog: "
    kill -s 9 `get_nodemgr_pid` &> /dev/null
    retval=$?
    echo
    [ $retval -eq 0 ] && rm -f $NodeManagerLockFile
    return $retval
}

restart() {
    stop
    start
}

reload() {
    restart
}

force_reload() {
    restart
}

rh_status() {
    local retval=`check_nodemgr_status`
    if [ $retval -eq 0 ]; then
        echo "$prog (pid:`get_nodemgr_pid`) is running..."
    elif [ $retval -eq 4 ]; then
        echo "Multiple instances of $prog are running..."
    else
        echo "$prog is stopped"
    fi
    return $retval
}

rh_status_q() {
    rh_status >/dev/null  2>&1
}

case "$1" in
    start)
        rh_status_q && exit 0
        $1
        ;;
    stop)
        rh_status_q || exit 0
        $1
        ;;
    restart)
        $1
        ;;
    reload)
        rh_status_q || exit 7
        $1
        ;;
    force-reload)
        force_reload
        ;;
    status)
        rh_status
        ;;
    condrestart|try-restart)
        rh_status_q || exit 0
        restart
        ;;
    *)
        echo -n "Usage: $0 {"
        echo -n "start|"
        echo -n "stop|"
        echo -n "status|"
        echo -n "restart|"
        echo -n "condrestart|"
        echo -n "try-restart|"
        echo -n "reload|"
        echo -n "force-reload"
        echo "}"

        exit 2
esac
exit $?
