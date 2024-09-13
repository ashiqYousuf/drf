from getpass import getpass

import requests

username = input("Enter username: ")
password = getpass("Enter password: ")


auth_endpoint = 'http://localhost:8000/api/auth/'

auth_response = requests.post(auth_endpoint, json={
    'username': username,
    'password': password
})
print(auth_response.json())

token = auth_response.json(
)['token'] if auth_response.status_code == 200 else None

if token:
    endpoint = 'http://localhost:8000/api/products/'
    response = requests.get(endpoint, headers={
        'Authorization': f'Bearer {token}'
    })
    print(response.json())
