import sys
import requests
from requests.auth import HTTPBasicAuth

print("Running Tester....\n")

address = 'http://localhost:5000'

# TEST 1 TRY TO REGISTER A NEW USER
try:
    url = address + '/users'
    data = dict(username="Best", password="User")
    response = requests.post(url, json=data)
    resp = response.json()
    print(response.json())
    status = response.status_code
    if status != 201 and status != 200:
        raise Exception('Received an unsuccessful status code of %s' % status)
except Exception as err:
    print("Test 1 FAILED: Could not make a new user")
    print(err.args)
    sys.exit()
else:
    print("Test 1 PASS: Succesfully made a new user")

# TEST 2: TRY TO ADD OBJECT TO DB
try:
    url = address + '/resources'
    data = dict(name="laptop", description="ASUS X515", quantity="3", price="$999.99")
    response = requests.post(url, json=data, auth=HTTPBasicAuth(username="Best", password="User"))
    print(response.json())
    status = response.status_code
    if status != 200:
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
except Exception as err:
    print("Test 2 FAILED: Could not add new object to the db")
    print(err.args)
    sys.exit()
else:
    print("Test 2 PASS: Succesfully made new bagels")

# TEST 3: TRY TO GET OBJECT WITH CORRECT CREDENTIALS
try:
    url = address + '/resources'
    response = requests.get(url, auth=HTTPBasicAuth(username="Best", password="User"))
    status = response.status_code
    if status != 200:
        raise Exception("Unable to get resources with valid credentials")
except Exception as err:
    print("Test 3 FAILED")
    print(err.args)
    sys.exit()
else:
    print("Test 3 PASS: App checks against invalid credentials")

# TEST 4 TRY TO ACCESS DB WITH INVALID CREDENTIALS
try:
    url = address + '/resources'
    response = requests.get(url, auth=HTTPBasicAuth(username="Best", password="Thief"))
    status = response.status_code
    if status == 200:
        raise Exception("Failed! Able to log in with invalid credentials")
except Exception as err:
    print("Test 4 FAILED")
    print(err.args)
    sys.exit()
else:
    print("Test 4 PASS: Request rejected against invalid credentials")
    print("ALL TESTS PASSED!")
