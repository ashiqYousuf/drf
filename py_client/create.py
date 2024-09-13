import requests

title = input("Enter title: ")
price = float(input("Enter price: "))

endpoint = 'http://localhost:8000/api/products/'

response = requests.post(endpoint, json={"title": title, "price": price})
print(response.json())
print(response.status_code)
