import requests
import json

# from source:
#
# "max_results": 100
# 
# "radius_options": [
#       10,
#       25,
#       50,
#       100,
#       250
#     ]


def get_alp_locations(longitude: float, latitude: float, distance: int) -> list[dict]:
    """Finds 100 closest alp locations within the specified radius"""
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'if-modified-since': 'Wed, 11 Mar 2026 19:11:31 GMT',
        'origin': 'https://alppouch.com',
        'priority': 'u=1, i',
        'referer': 'https://alppouch.com/',
        'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
    }

    params = {
        'tag': 'map_pqkj57y3',
        'latitude': str(latitude),
        'longitude': str(longitude),
        'filter_operator': 'and',
        'distance': str(distance),
    }

    response = requests.get('https://stockist.co/api/v1/map_pqkj57y3/locations/search', params=params, headers=headers)
    return json.loads(response.text).get('locations')