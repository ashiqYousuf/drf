import requests

product_id = int(input("Enter product id: "))

endpoint = f'http://localhost:8000/api/products/{product_id}'

response = requests.get(endpoint)
print(response.json())
print(response.status_code)
