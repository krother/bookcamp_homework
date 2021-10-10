
import requests

url = 'http://localhost:8000?contract=two_year&tenure=1&monthlycharges=10'
j = requests.get(url)
print(j)
print(j.json())
