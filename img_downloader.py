import json
from typing import List, Dict

import requests

offerings: List[Dict] = []

with open('../krosmoz.json', 'r') as f:
    offerings = json.load(f)

for offering in offerings:
    url = offering.get('img')
    if url is None:
        continue
    filename = url.split('/')[-1]
    r = requests.get(url, allow_redirects=True)
    with open(filename, 'wb') as f:
        f.write(r.content)
