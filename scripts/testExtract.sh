#!/bin/bash

sh ./scripts/runLoadScript.sh &&
istioctl dashboard zipkin &
sleep 20 && python3 ./scripts/data-extraction/extract-traces.py $TEST_NUMBER
