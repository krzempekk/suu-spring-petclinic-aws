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


## Extracting metrics
Once the app is running in AWS, you can extract metrics from all services and containers.

#### Steps
1. Run `istioctl dashboard prometheus`. This will forward Prometheus to your local port.
2. Run `python extract-metrics.py -t [time] -om [metrics metadata file name] -ov [metrics values file name]`. 
   The script will save all metrics that Prometheus collected in two JSON files: one with metadata metrics, 
   one with metadata values. Metrics for all services will be collected in those two files.

#### Collected metrics
The metrics collected from Prometheus are limited to application metrics, database metrics and some container metrics.
In particular, we gather metrics with the following prefix:
* `application_` - apps runtime metrics
* `container_` - container metrics (only related to apps' containers)
* `disk_` - disk in containers metrics ((only related to apps' containers))
* `envoy_` - Envoy metrics (only related to apps' containers)
* `executor_` - task execution metrics
* `hikaricp_` - Hikari-specific data source metrics
* `http_` - HTTP client metrics
* `istio_` - Istio metrics (only related to apps' containers)
* `jdbc_` - data source metrics
* `jvm_` - JVM metrics
* `tomcat_` - Tomcat metrics
* `mysql_` - MYSQL metrics
