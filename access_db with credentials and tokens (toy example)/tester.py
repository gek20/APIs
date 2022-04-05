import sys
import requests
import time

print("Running Tester....\n")

address = 'http://localhost:5000'
token=""
# TEST 1 TRY TO REGISTER A NEW USER
try:
    url = address + '/users/new'
    data = dict(username="Best", password="User")
    response = requests.post(url, json=data)
    resp = response.json()
    print(response.json())
    status = response.status_code
    if status != 201 and status != 200:
        raise Exception('Received an unsuccessful status code of %s' % status)
    try:
        token=resp["token"]
        print("received token {}".format(token))
    except Exception as err:
        print("Test 1 FAILED: Failed to load the token")
        print(err.args)
        sys.exit()
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
    headers = {"Authorization": "Bearer {}".format(token)}
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    status = response.status_code
    if status != 200:
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
except Exception as err:
    print("Test 2 FAILED: Could not add new object to the db")
    print(err.args)
    sys.exit()
else:
    print("Test 2 PASS: Succesfully made new object")

# TEST 3: TRY TO GET OBJECT WITH CORRECT CREDENTIALS
try:
    url = address + '/resources'
    headers = {"Authorization": "Bearer {}".format(token)}
    response = requests.post(url, json=data, headers=headers)
    response = requests.get(url, headers=headers)
    status = response.status_code
    if status != 200:
        raise Exception("Unable to get resources with valid credentials")
except Exception as err:
    print("Test 3 FAILED")
    print(err.args)
    sys.exit()
else:
    print("Test 3 PASS: App checks against invalid credentials")

# TEST 4 TRY TO ACCESS DB WITH INVALID TOKEN
try:
    url = address + '/resources'
    headers = {"Authorization": "Bearer {}".format("FAKE TOKEN")}
    response = requests.get(url, headers=headers)
    status = response.status_code
    print(status)
    if status == 200:
        raise Exception("Failed! Able to log in with invalid credentials")
except Exception as err:
    print("Test 4 FAILED")
    print(err.args)
    sys.exit()
else:
    print("Test 4 PASS: Request rejected against invalid credentials")


# TEST 4 TRY TO ACCESS DB WITH EXPIRED TOKEN

time.sleep(60)
try:
    url = address + '/resources'
    headers = {"Authorization": "Bearer {}".format(token)}
    response = requests.get(url, headers=headers)
    status = response.status_code
    print(status)
    if status == 200:
        raise Exception("Failed! Able to log in with expired tokens")
except Exception as err:
    print("Test 5 FAILED")
    print(err.args)
    sys.exit()
else:
    print("Test 5 PASS: Request rejected against expired tokens")
    print("ALL TESTS PASSED!")