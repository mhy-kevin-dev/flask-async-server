# Async Server with Flask API


## workflow

1. [client] posts a JSON query to server `search` as a request.
2. [server] receives client's request, sends a JSON back to the client: `{'message': 'Processing...', 'id':"UUID"}`, stores this JSON to `UUID.json`, and calls the main part function through thread.
3. [client] posts a JSON query to `get_report` based on the ID from step2: `{"id":"UUID"}`,  to check if all tasks have been completed. (use polling to check)
4. [server] writes result JSON back to `UUID.json` if the job is finished.

## requirements

- python 3.6+
- flask


## how to use

running this command in your server:
```sh
python flask_async.py
```


running these commands in client:

- (1) search
```sh
curl -x POST  -H "Content-Type: application/json" -d '{"parameters.user-define.session-id":"7892239","start-time":{"$gte":"2022-09-20 09:50","$lte":"2022-09-20 10:25"}}'  http://localhost:7733/search
```


- (2) get_report
```sh
curl  -X POST  -H "Content-Type: application/json" -d '{"id":"78036b6a-d0bd-4464-b91e-909cf0489135"}'  http://localhost:7733/get_report
```





