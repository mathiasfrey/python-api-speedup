import json, orjson

from typing import Optional, Any
from fastapi import FastAPI, Request
from fastavro import reader
from io import BytesIO

app = FastAPI()

@app.post("/model")
async def read_avro(request: Request):
    #print(">>>", Request)
    #import pdb; pdb.set_trace()
    #print(Request.body)

    content_type = request.headers['content-type']

    if content_type == 'text/json':
        b = await request.body()
        x = json.loads(b)
        print(len(x), "JSON records received")
        return True

    elif content_type == 'text/orjson':
        b = await request.body()
        x = orjson.loads(b)
        print(len(x), "orJSON records received")
        return True

    elif content_type == 'avro/binary':
        bytes = await request.body()

        fo = BytesIO(bytes)

        cnt = 0
        for record in reader(fo):
            #print(record.get('station'))
            cnt += 1
        print(cnt, "Avro records received")
        return True

    else:
        print('Unknown Content-Type header received')


@app.get("/")
def read_root():
    return {"Hello": "World"}