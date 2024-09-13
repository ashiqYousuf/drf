import requests

pid = int(input("Enter id: "))

endpoint = f'http://localhost:8000/api/products/{pid}/'

response = requests.delete(endpoint)
print(response.json())
print(response.status_code)
