## Extracting traces
Once the app is running in AWS, you can extract traces from all instrumented services.

#### Steps
1. Run `istioctl dashboard zipkin`. This will forward Zipkin to your local port.
2. Run `python extract-traces.py`. The script will save all traces that Zipkin collected in JSON files named by the services that produced the traces.

#### Trace data format
The trace format is compliant with the OpenTelemetry standard.
A trace is a collection of spans. A span represents a unit of work done by a particular service. 

A span contains:
* traceId, id
* timestamp
* duration
* annotations
* tags

A full description is availabe [here](https://zipkin.io/zipkin-api/#/).
