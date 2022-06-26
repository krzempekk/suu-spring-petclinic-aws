import requests
import json
import os

BASE_FOLDER = 'test-2'
TRACES_PER_REQUEST = 100

if not os.path.exists(BASE_FOLDER):
    os.makedirs(BASE_FOLDER)

base_url = 'http://localhost:9411/api/v2'
services = requests.get(url=f'{base_url}/services').json()
print(services)

for service in services:

    service_traces = []
    params = {
        'serviceName': service,
        'limit': TRACES_PER_REQUEST
    }
    trace_batch = requests.get(url=f'{base_url}/traces', params=params).json()
    service_traces.extend(trace_batch)

    while len(trace_batch) > 0:
        # transform list of traces to a list of spans
        spans = [span for spans in trace_batch for span in spans]
        # get earliest span timestamp
        min_timestamp = min(spans, key=lambda span: int(span['timestamp']))['timestamp']
        params['endTs'] = min_timestamp
        trace_batch = requests.get(url=f'{base_url}/traces', params=params).json()
        service_traces.extend(trace_batch)

    with open(f'{BASE_FOLDER}/{service}.json', 'w') as f:
        json.dump(service_traces, f)
