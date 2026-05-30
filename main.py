from web_scrape import *
import tabulate as tbl

locations = get_alp_locations(longitude=-96.7943025, latitude=32.8333535, distance=250)

headers = ['id', 'name', 'distance']
data = [[location.get('id'), location.get('name'), location.get('distance')] for location in locations]
print(tbl.tabulate(data, headers=headers, tablefmt="simple", showindex=True, floatfmt='.1f'))

