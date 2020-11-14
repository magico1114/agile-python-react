from flask import Flask, request, Response, json
from flask_api import status
from flask_cors import CORS
from datetime import datetime
from threading import Thread
import queue
import time
import string
import random
from enums.transactionType import transactionType

app = Flask(__name__)
cors = CORS(app)

DBLOCKED = False
TIMEOUT = 10

HISTORY = {}
'''
HISTORY = {
       '1111111111100012': {'id': '1111111111100012', 'type': transactionType.CREDIT, 'amount': 1234, 'effectiveDate': datetime.now()},
       '1111111111100013': {'id': '1111111111100013', 'type': transactionType.DEBIT, 'amount': 1000, 'effectiveDate': datetime.now()},
       '1111111111100014': {'id': '1111111111100014', 'type': transactionType.CREDIT, 'amount': 234, 'effectiveDate': datetime.now()},
       '1111111111100015': {'id': '1111111111100015', 'type': transactionType.DEBIT, 'amount': 1000, 'effectiveDate': datetime.now()},
       '1111111111100016': {'id': '1111111111100016', 'type': transactionType.CREDIT, 'amount': 234, 'effectiveDate': datetime.now()},
       '1111111111100017': {'id': '1111111111100017', 'type': transactionType.CREDIT, 'amount': 1000, 'effectiveDate': datetime.now()},
       '1111111111100018': {'id': '1111111111100018', 'type': transactionType.CREDIT, 'amount': 234, 'effectiveDate': datetime.now()},
       '1111111111100019': {'id': '1111111111100019', 'type': transactionType.DEBIT, 'amount': 1000, 'effectiveDate': datetime.now()},
       '1111111111100020': {'id': '1111111111100020', 'type': transactionType.CREDIT, 'amount': 234, 'effectiveDate': datetime.now()},
       '1111111111100021': {'id': '1111111111100021', 'type': transactionType.DEBIT, 'amount': 1000, 'effectiveDate': datetime.now()},
       '1111111111100022': {'id': '1111111111100022', 'type': transactionType.CREDIT, 'amount': 234, 'effectiveDate': datetime.now()}
}
'''

PROCESSING = {}
BALANCE = 0

@app.route('/', methods = ['GET'])
def default():
    if request.method == 'GET':
        response = app.response_class(
            response=json.dumps({'BALANCE': BALANCE}),
            status=status.HTTP_200_OK,
            mimetype='application/json'
        )
        return response
    
    else:
        # Error 405 Method Not Allowed // NOT Necesary, validation at decorator level.
        response = app.response_class(
            response=json.dumps({}),
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
            mimetype='application/json'
        )
        return response   

@app.route('/transactions/', methods = ['GET', 'PUT'])
def transactions():

    if request.method == 'GET':
        if not DBLOCKED:
            response = app.response_class(
                response=json.dumps(list(HISTORY.values())),
                status=status.HTTP_200_OK,
                mimetype='application/json'
            )
        else:
            tReference = time.time()
            while True:
                if not DBLOCKED:
                    response = app.response_class(
                        response=json.dumps(list(HISTORY.values())),
                        status=status.HTTP_200_OK,
                        mimetype='application/json'
                    )
                    break
                elif time.time() >= tReference + TIMEOUT:
                    response = app.response_class(
                        response=json.dumps({"error": "timeout"}),
                        status=status.HTTP_503_SERVICE_UNAVAILABLE,
                        mimetype='application/json'
                    )
                    break
                time.sleep(0.01) # sleep for 10 milliseconds // Avoid CPU high load.

        return response

    elif request.method == 'PUT':
        processKey = genKey()

        # Quick validation
        try:
            jsonData = request.json # If fail return BAD REQUEST
            transType = jsonData['type']
            transAmount = float(jsonData['amount'])
            # negative transactions not allowed
            if transAmount < 0:
                raise
            elif transType == transactionType.DEBIT:
                print("Debit Ok!")
            elif transType == transactionType.CREDIT:
                print("Credit Ok!")
            else:
                raise
        except:
            # return BAD REQUEST 
            response = app.response_class(
                response=json.dumps({}),
                status=status.HTTP_400_BAD_REQUEST,
                mimetype='application/json'
            )
            return response

        transaction = {'id': processKey, 'type': transType, 'amount': transAmount, 'effectiveDate': datetime.now()}

        PROCESSING[processKey] = { 'PROCESSING': True, 'status': 'pending', 'transaction' : transaction }

        processData(processKey)

        if PROCESSING[processKey]['status'] == 'acepted':
            response = app.response_class(
                response=json.dumps({'status': "Transaction accepted"}),
                status=status.HTTP_201_CREATED,
                mimetype='application/json'
            )
        elif PROCESSING[processKey]['status'] == 'rejected':
            response = app.response_class(
                response=json.dumps({'status': "Transaction rejected. Insuficient founds"}),
                status=status.HTTP_409_CONFLICT,
                mimetype='application/json'
            )
        elif PROCESSING[processKey]['status'] == 'timeout':
            response = app.response_class(
                response=json.dumps({'status': "Service not available. Timeout"}),
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
                mimetype='application/json'
            )
        else:
            response = app.response_class(
                response=json.dumps({'status': "Transaction rejected. Unknow error"}),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                mimetype='application/json'
            )

        return response

    else:
        # Error 405 Method Not Allowed // NOT Necesary, validation at decorator level.
        response = app.response_class(
            response=json.dumps({}),
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
            mimetype='application/json'
        )
        return response


def genKey():
    now = datetime.now().strftime('%Y%m%d%H%M%S%f')
    rand = ''.join(random.choice(string.digits) for _ in range(2))
    return "%s.%s"%(now, rand)


def processData(processKey):
    global DBLOCKED, BALANCE, PROCESSING, HISTORY

    status = "error" # Default status if raised.
    try:
        #locked status verification
        tReference = time.time()
        while DBLOCKED:
            # If while reach timeout, return an error
            if time.time() >= tReference + TIMEOUT:
                status = 'timeout'
                raise
            time.sleep(0.01) # sleep for 10 milliseconds // Avoid CPU high load.

        # Lock and try to write
        try:
            DBLOCKED = True
            # get transaction amount, if it's fine add transaction to HISTORY.
            tmp_amount = PROCESSING[processKey]['transaction']['amount']
            transaction_amount = tmp_amount if PROCESSING[processKey]['transaction']['type'] == transactionType.CREDIT else -(tmp_amount)
            if BALANCE + transaction_amount >= 0:
                BALANCE += transaction_amount
                HISTORY[processKey] = PROCESSING[processKey]['transaction']
                status = 'acepted'

            else:
                status = 'rejected'
        except:
            # Log error....
            pass

        # unlock write
        DBLOCKED = False

    except:
        # Log error....
        pass        
    
    PROCESSING[processKey]['status'] = status
    PROCESSING[processKey]['PROCESSING'] = False
    

if __name__ == "__main__":
    app.run(threaded=True)
