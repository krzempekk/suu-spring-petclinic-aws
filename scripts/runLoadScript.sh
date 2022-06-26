#!/bin/bash

export RESULTS_FILE=results.jtl
export TEST_PLAN=./test-plans/petclinic_test_plan_2.jmx

while : ; do
  EXTERNAL_IP=$(kubectl get svc -n spring-petclinic api-gateway | sed -n '2p' | awk '{ print $4 }')
  curl $EXTERNAL_IP > /dev/null
  if (( $? == 0 )); then
    jmeter -Jhost=$EXTERNAL_IP -Jport=80 -n -t $TEST_PLAN -f -l $RESULTS_FILE
    break
  else
    echo "External IP unreachable, retrying..."
  fi
done

