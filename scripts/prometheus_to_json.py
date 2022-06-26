import csv
import requests
import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import json
import time

prefixes = ["application_", "container_", "disk_", "envoy_", "executor_", "hikaricp_", "http_", "istio_", "jdbc_",
            "jvm_", "tomcat_"]

app_names = ["customers-service", "vets-service", "visits-service", "api-gateway"]


def get_metrics_names(url):
    response = requests.get('{0}/api/v1/label/__name__/values'.format(url))
    names = response.json()['data']
    filtered = list(filter(lambda name: name.lower().startswith(tuple(prefixes)), names))
    # Return filtered metric names
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
parser.add_argument("-t", "--time", help="what time of data to get", default="5s")
parser.add_argument("-om", "--output_metadata", help="metrics metadata file name", default=time
                    .strftime("%Y%m%d-%H%M%S-metrics-metadata.json"))
parser.add_argument("-ov", "--output_values", help="metrics values file name", default=time
                    .strftime("%Y%m%d-%H%M%S-metrics-values.json"))
parser.add_argument("host", help="Prometheus host")
args = vars(parser.parse_args())

url = args["host"]
time = args["time"]
output_metadata = args["output_metadata"]
output_values = args["output_values"]

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
