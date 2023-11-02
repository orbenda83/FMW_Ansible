#! /bin/bash

JAVA_HOME={{ java_home }}
export JAVA_HOME

CONNSTR='{{ db_server }}:{{ db_port }}:{{ db_service }}'
PASS_INPUT="{{ working_directory }}/rcu_password.txt"

if [ $# -eq 0 ]
  then
      echo "No arguments supplied"
fi

PRODUCT=$1

echo "Running RCU for "$PRODUCT

{{ oracle_common_home }}/bin/rcu -silent -createRepository -useSamePasswordForAllSchemaUsers true -databaseType ORACLE \
-connectString $CONNSTR \
-dbUser sys -dbRole SYSDBA \
 -schemaPrefix {{ soa_repo_prefix }} \
 {{ schema_components_args }} \
-tablespace {{ soa_tablespace }} \
 -f < $PASS_INPUT
