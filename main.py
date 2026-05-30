from web_scrape import *
import tabulate as tbl
import random
import time


for i in range(100):
    lon = random.uniform(-151.05376, -68.40191)
    lat = random.uniform(25.76312, 64.86018)
    locations = get_alp_locations(longitude=lon, latitude=lat, distance=100)
    
    time.sleep(random.uniform(.6, 1))

    if locations == None:
        print(f'{f'({i})':>5} locations not found')
        continue

    print(f'{f'({i})':>5} {len(locations):>3} location{'' if len(locations) == 1 else 's'} found')
    

