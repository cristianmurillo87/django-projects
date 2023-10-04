import requests

endpoint = 'http://127.0.0.1:8000/api/products/'
# get_response = requests.get(endpoint)
response = requests.post(endpoint, json=dict(
    title='Another remotely created product', content='This product was also created remotely', price=5.00))
print(response.json())
