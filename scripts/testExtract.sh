#!/bin/bash

(istioctl dashboard zipkin & istioctl dashboard prometheus & sleep 20) && (python3 ./scripts/data-extraction/extract-traces.py & python3 ./scripts/data-extraction/extract-metrics.py)
