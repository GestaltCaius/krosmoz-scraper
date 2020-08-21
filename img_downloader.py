import json
from typing import List, Dict
import os

import requests

offerings: List[Dict] = []

with open('../krosmoz.json', 'r') as f:
    offerings = json.load(f)

for offering in offerings:
    url = offering.get('img')
    if url is None:
        continue
    filename = url.split('/')[-1]
    try:
        file_size = os.path.getsize(filename)
        if file_size > 42:
            continue
    except OSError:
        pass
    r = requests.get(url, allow_redirects=True)
    with open(filename, 'wb') as f:
        f.write(r.content)
