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

records2 = [
    {
    "header": ["station", "temp", "time"],
    "data": [[u'011990-99999', "0", "1433269388"]]*250
    }
]


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
schema2 = {
  "name": "MyClass",
  "type": "array",
  "namespace": "com.acme.avro",
  "items": {
    "name": "MyClass_record",
    "type": "record",
    "fields": [
      {
        "name": "header",
        "type": {
          "type": "array",
          "items": "string"
        }
      },
      {
        "name": "data",
        "type": {
          "type": "array",
          "items": {
            "type": "array",
            "items": "string"
          }
        }
      }
    ]
  }
}

parsed_schema = parse_schema(schema)
parsed_schema2 = parse_schema(schema2)

# Writing
with open('weather.avro', 'wb') as out:
    writer(out, parsed_schema, records)

# with open('weather2.avro', 'wb') as out2:
# writer(out2, parsed_schema2, records2)

def request_orjson_split():

    content_type = 'text/orjson'

    return('orJSON+split', __request_json(content_type, records2))

def request_orjson():

    content_type = 'text/orjson'

    return('orJSON', __request_json(content_type, records))

def request_json_split():

    content_type = 'text/json'

    return('JSON+split', __request_json(content_type, records2))

def request_json():

    content_type = 'text/json'

    return('JSON', __request_json(content_type, records))

def __request_json(content_type, payload):

    response = requests.post(
        url, 
        data=json.dumps(payload),
        headers={'Content-Type': content_type}
        )
    return response.elapsed.total_seconds()

def request_avro():

    content_type = 'avro/binary'

    with open('./weather.avro', 'rb') as f:
        payload = f.read()

    response = requests.post(
        url, 
        data=payload,
        headers={'Content-Type': content_type}
        )
    return('Avro', response.elapsed.total_seconds())


if __name__ == '__main__':

    stats = {}
    
    calls = [
        request_json, 
        request_orjson, 
        request_avro, 
        request_json_split,
        request_orjson_split,
        ]

    for i in range(2):
        for c in calls:
            x = c()
            stats.setdefault(x[0], []).append(x[1])
    
    print("Method\t\t\tMean response\tSTDEV")
    print('-'*50)
    for k, v in stats.items():
        print(f"{k:20s}\t{statistics.mean(v):.10f}\t{statistics.stdev(v):7f}")