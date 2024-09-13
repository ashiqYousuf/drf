import requests

pid = int(input("Enter id: "))
title = input("Enter title: ")
content = input("Enter content: ")

data = {
    "title": title,
    "content": content
}

endpoint = f'http://localhost:8000/api/products/{pid}/'

response = requests.put(endpoint, json=data)
print(response.json())
print(response.status_code)
