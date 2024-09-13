import requests

endpoint = 'http://localhost:8000/api/'

response = requests.get(
    endpoint, json={'username': 'ashiqYousuf'}, params={'q': 123})

print(response.text)
print(response.status_code)
