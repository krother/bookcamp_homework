
# docker build -t churnpred .
# docker run -d -p 8000:8000 churnpred mypredserver
# docker run -it -p 8000:8000 --rm --entrypoint=bash churnpred
# pipenv run gunicorn --bind 0.0.0.0:8000 app:app

import requests

url = 'http://0.0.0.0:8000?contract=two_year&tenure=12&monthlycharges=10'
j = requests.get(url)
print(j)
print(j.json())
