#! /bin/bash

JAVA_HOME=/opt//jdk//jdk1.8.0_221/
export JAVA_HOME

CONNSTR='<DB_HOST>:<DB_PORT>:<DB_SID>'
PASS_INPUT="/home/oracle/build/rcu_password.txt"

if [ $# -eq 0 ]
  then
      echo "No arguments supplied"
fi

PRODUCT=$1

echo "Running RCU for "$PRODUCT

/opt/oracle/middleware/oracle_common/bin/rcu -silent -createRepository -useSamePasswordForAllSchemaUsers true -databaseType ORACLE \
-connectString $CONNSTR \
-dbUser sys -dbRole SYSDBA \
 -schemaPrefix DEV \
 -component MDS -component IAU -component IAU_APPEND -component IAU_VIEWER -component OPSS -component UCSUMS -component WLS -component STB -component SOAINFRA \
 -f < $PASS_INPUT
