import requests

endpoint = 'http://localhost:8000/api/'

response = requests.post(
    endpoint, json={'title': 'Hello, World!', 'price': 123.50}, params={'q': 123})

print(response.text)
print(response.status_code)
