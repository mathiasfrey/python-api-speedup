# py-speedup

## Installation

```
virtualenv --python=python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run


### Start the server in one terminal
```
source venv/bin/activate
uvicorn main:app --reload
```

### Make the client's calls from another
```
source venv/bin/activate
python client.py
```