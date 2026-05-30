from geopy.distance import geodesic
import json
import math
import random
import requests
import time

class Location:
    def __init__(self, data: dict):
        self.id: str = data.get('id','').replace(',','').replace('\n','')
        self.name: str = data.get('name','').replace(',','').replace('\n','')
        self.lat: float = data.get('latitude')
        self.lon: float = data.get('longitude')
        self.address: str = data.get('address_line_1','').replace(',','').replace('\n','')
        self.city: str = data.get('city','').replace(',','').replace('\n','')
        self.state: str = data.get('state','').replace(',','').replace('\n','')
        self.zip: str = data.get('postal_code','').replace(',','').replace('\n','')

    def __eq__(self, other):
        if not isinstance(other, Location): return NotImplemented
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f'({self.id}) {self.name}'
    
    def csv(self):
        return f'{self.id},{self.name.replace(',','')},{self.lat},{self.lon},{self.address},{self.city},{self.state},{self.zip}\n'

call_ct = 0
def get_alp_locations(lon: float, lat: float, distance: int = 50000) -> set[Location]:
    """Finds 100 closest alp locations within the specified radius"""

    global call_ct
    call_ct += 1

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
        'latitude': str(lat),
        'longitude': str(lon),
        'filter_operator': 'and',
        'distance': str(distance),
    }

    response = requests.get('https://stockist.co/api/v1/map_pqkj57y3/locations/search', params=params, headers=headers)
    locations_json = json.loads(response.text).get('locations')
    while locations_json == None:
        print("Request failed. Waiting 60 seconds")
        time.sleep(60)
        response = requests.get('https://stockist.co/api/v1/map_pqkj57y3/locations/search', params=params, headers=headers)
        locations_json = json.loads(response.text).get('locations')
    
    time.sleep(random.uniform(.5,1.5))

    locations = {Location(l) for l in locations_json}
    return locations

# from source:
#
# "bounds": {
#       "west": -151.05376,
#       "south": 25.76312,
#       "east": -68.40191,
#       "north": 64.86018
#     }

# roughly 42 by 84

def search_tile(lon, lat, side_length, depth=0):
    """ Recursively search for locations in tile """
    distance = int(geodesic((lat, lon),(lat + side_length*math.sqrt(2)/2, lon + side_length*math.sqrt(2)/2)).miles)
    print(f'{depth*'  '}({call_ct}) searching {distance} mile radius at ({lon:.2f}, {lat:.2f})... ', end='', flush=True)
    locations = get_alp_locations(lon, lat, distance)
    print(f'found {len(locations)} locations')
    
    if len(locations) == 100:
        # location cap is hit - subdivide tile into four subtiles
        for dx, dy in [[1,1], [-1,1], [-1,-1], [1,-1]]:
            locations |= search_tile(lon + dx*side_length/4, lat + dy*side_length/4, side_length/2, depth+1)
    return locations



def main():
    start_time = time.time()

    locations = search_tile(-89,46,42)
    locations |= search_tile(-131,46,42)

    print(f'\nfound {len(locations)} locations')
    with open('locations.csv', 'w') as f:
        for l in locations:
            f.write(l.csv())
    print(f'completed {call_ct} requests in {(time.time()-start_time)/60:.2f} minutes')

if __name__ == '__main__': main()