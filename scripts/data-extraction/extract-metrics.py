import csv
import requests
import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import json
import time
import os

prefixes = ["application_", "container_", "disk_", "envoy_", "executor_", "hikaricp_", "http_", "istio_", "jdbc_",
            "jvm_", "tomcat_", "mysql_"]

app_names = ["customers-service", "vets-service", "visits-service", "api-gateway", "mysql-exporter-customers",
             "mysql-exporter-vets", "mysql-exporter-visits"]
test_num = os.getenv('TEST_NUMBER')
if test_num is None:
    test_num = '1'
BASE_FOLDER = f'test-data/test-{test_num}/metrics'

if not os.path.exists(BASE_FOLDER):
    os.makedirs(BASE_FOLDER)

def get_metrics_names(url):
    response = requests.get('{0}/api/v1/label/__name__/values'.format(url))
    names = response.json()['data']
    filtered = list(filter(lambda name: name.lower().startswith(tuple(prefixes)), names))
    # Return filter ed metric names
    return filtered


def app_name_is_substring_of_label(label):
    for name in app_names:
        if name in label:
            return True
    return False


def get_app_name(metric):
    app_name = metric.get('app', '')
    if app_name != '':
        return app_name
    else:
        return metric.get('pod', '')


"""
Prometheus hourly data as csv.
"""
writer = csv.writer(sys.stdout)
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-t", "--time", help="what time of data to get", default="10m")
parser.add_argument("-om", "--output_metadata", help="metrics metadata file name", default=time
                    .strftime("%Y%m%d-%H%M%S-metrics-metadata.json"))
parser.add_argument("-ov", "--output_values", help="metrics values file name", default=time
                    .strftime("%Y%m%d-%H%M%S-metrics-values.json"))
parser.add_argument("-ho", "--host", help="Prometheus host", default="http://localhost:9090")
args = vars(parser.parse_args())

url = args["host"]
time = args["time"]
output_metadata = f'{BASE_FOLDER}/{args["output_metadata"]}'
output_values = f'{BASE_FOLDER}/{args["output_values"]}'

metricNames = get_metrics_names(url)
writeHeader = True
isFirst = True
with open(output_metadata, 'a', encoding='utf-8') as f:
    f.write("[\n")
with open(output_values, 'a', encoding='utf-8') as f:
    f.write("[\n")
for metricName in metricNames:
    response = requests.get('{0}/api/v1/query'.format(url),
                            params={'query': metricName + '[' + time + ']'})
    results = response.json()['data']['result']
    for result in results:
        if result['metric'].get('app', '') in app_names \
                or app_name_is_substring_of_label(result['metric'].get('pod', '')):
            with open(output_values, 'a', encoding='utf-8') as f:
                if not isFirst:
                    f.write(",\n")
                values_for_metric = {'metric_name': result['metric']['__name__'],
                                     'app': get_app_name(result['metric']),
                                     'values': result['values']}
                json.dump(values_for_metric, f, ensure_ascii=False, indent=4)
            with open(output_metadata, 'a', encoding='utf-8') as f:
                if not isFirst:
                    f.write(",\n")
                else:
                    isFirst = False
                json.dump(result['metric'], f, ensure_ascii=False, indent=4)
with open(output_metadata, 'a', encoding='utf-8') as f:
    f.write("\n]")
with open(output_values, 'a', encoding='utf-8') as f:
    f.write("\n]")
