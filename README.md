# cc-money-accounting

## Server

### Requirements
```console
Python 3+
Flask (pip install flask)
flask_cors
flask_api
```
###  Run server
```console
cd server
python server.py
```

###  Run with Docker
BUILD
```console
docker-compose build
```
RUN
```console
docker-compose up
```


### Usage

GET /transactions

   Response example:
   ```
   [
       {
            "id": "20201114184233379339.34",
            "effectiveDate": "Sat, 14 Nov 2020 17:42:33 GMT",
            "amount": 100,
            "type": "credit"
        },
        {
            "id": "20201114184242812237.86",
            "type": "debit"
            "amount": 30,
            "effectiveDate": "Sat, 14 Nov 2020 17:42:42 GMT",
        }
   ]
   ```
 
POST  /transaction

  Request format:
  ```
  {
    "type": String [credit, debit],
    "amount": Number
  }
  ```

GET  /

  Response example:
  ```
    {
        "balance": 70
    }
  ```





## Client

### Installation

*Go to client directory (ie: "cd client")

```console
npm i
```
###  Run client
```console
npm start
```


