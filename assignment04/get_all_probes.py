import requests
import json

BASE_URL = 'https://atlas.ripe.net/api/v2'
ENDPOINT = '/probes'

if __name__ == '__main__':
    probes = []
    pages = 1

    url = BASE_URL + ENDPOINT
    res = requests.get(url)
    json_res = json.loads(res.text)

    while json_res["next"] is not None:
        url = json_res["next"]
        res = requests.get(url)
        json_res = json.loads(res.text)
        probes.extend(json_res["results"])
        pages += 1

    with open('probes.json', 'w') as f:
        json.dump(probes, f)

    print(f"Found {len(probes)} probes in {pages} pages")