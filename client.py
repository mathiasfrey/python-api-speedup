import requests
import json
import statistics
from fastavro import writer, reader, parse_schema

url = 'http://127.0.0.1:8000/model'


records = [
    {u'station': u'011990-99999', u'temp': 0, u'time': 1433269388},
    {u'station': u'011990-99999', u'temp': 22, u'time': 1433270389},
    {u'station': u'011990-99999', u'temp': -11, u'time': 1433273379},
    {u'station': u'012650-99999', u'temp': 111, u'time': 1433275478},
]*250

schema = {
    'doc': 'A weather reading.',
    'name': 'Weather',
    'namespace': 'test',
    'type': 'record',
    'fields': [
        {'name': 'station', 'type': 'string'},
        {'name': 'time', 'type': 'long'},
        {'name': 'temp', 'type': 'int'},
    ],
}
parsed_schema = parse_schema(schema)

# Writing
with open('weather.avro', 'wb') as out:
    writer(out, parsed_schema, records)


def request_orjson():

    content_type = 'text/orjson'

    return __request_json(content_type)

def request_json():

    content_type = 'text/json'

    return __request_json(content_type)

def __request_json(content_type):

    response = requests.post(
        url, 
        data=json.dumps(records),
        headers={'Content-Type': content_type}
        )
    return(content_type, response.elapsed.total_seconds())

def request_avro():

    content_type = 'avro/binary'

    with open('./weather.avro', 'rb') as f:
        payload = f.read()

    response = requests.post(
        url, 
        data=payload,
        headers={'Content-Type': content_type}
        )
    return(content_type, response.elapsed.total_seconds())


if __name__ == '__main__':

    stats = {}
    
    calls = [request_json, request_orjson, request_avro]

    for i in range(5):
        for c in calls:
            x = c()
            stats.setdefault(x[0], []).append(x[1])
    
    print("Content-Type\tMean response\tSTDEV")
    for k, v in stats.items():
        print(f"{k}\t{statistics.mean(v):.10f}\t{statistics.stdev(v):7f}")