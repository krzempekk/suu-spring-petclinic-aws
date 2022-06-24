import csv
import requests
import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def get_metrics_names(url):
    response = requests.get('{0}/api/v1/label/__name__/values'.format(url))
    names = response.json()['data']
    #Return metrix names
    return names
"""
Prometheus hourly data as csv.
"""
writer = csv.writer(sys.stdout)
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-t", "--time", help="what time of data to get", default="1h")
parser.add_argument("host", help="Prometheus host")
args = vars(parser.parse_args())

url = args["host"]
time = args["time"]

metrixNames=get_metrics_names(url)
writeHeader=True
for metrixName in metrixNames:
     #now its hardcoded for hourly
     response = requests.get('{0}/api/v1/query'.format(url),
      params={'query': metrixName+'['+time+']'})
     results = response.json()['data']['result']
     # Build a list of all labelnames used.
     #gets all keys and discard __name__
     labelnames = set()
     for result in results:
        labelnames.update(result['metric'].keys())
     # Canonicalize
     labelnames.discard('__name__')
     labelnames = sorted(labelnames)
     # Write the samples.
     if writeHeader:
        writer.writerow(['name', 'timestamp', 'value'] + labelnames)
        writeHeader=False
     for result in results:
        l = [result['metric'].get('__name__', '')] + result['values']
        for label in labelnames:
            l.append(result['metric'].get(label, ''))
            writer.writerow(l)
