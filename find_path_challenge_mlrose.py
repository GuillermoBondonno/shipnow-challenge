import json
import six
import sys
sys.modules['sklearn.externals.six'] = six
import mlrose
import numpy as np
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km


# Create list of distances between pairs of cities
dist_list = []
filepath = r'./breweries.geojson'
f = open(filepath, 'r').read()

data = json.loads(f)['features']

c = 0
for feature in data:
    feature['properties']['name_code'] = c #mlrose necesita que los nombres de los puntos sean enteros
    c += 1

for feature in data:
    for _feature in data:
        if _feature['properties']['name_code'] != feature['properties']['name_code']: #creamos la lista de distancias
            dist_list.append((feature['properties']['name_code'] ,_feature['properties']['name_code'] , haversine(feature['geometry']['coordinates'][1],feature['geometry']['coordinates'][0], _feature['geometry']['coordinates'][1],_feature['geometry']['coordinates'][0])))


# Initialize fitness function object using dist_list
#https://mlrose.readthedocs.io/en/stable/source/tutorial2.html#

fitness_dists = mlrose.TravellingSales(distances = dist_list)

problem_fit = mlrose.TSPOpt(length = len(data), fitness_fn = fitness_dists,
                            maximize=False)

best_state, best_fitness = mlrose.genetic_alg( problem_fit, random_state = 10, pop_size=500)
'''parametros para modificar: pop_size, mutation_prob, max_attempts'''
path = []
for point in best_state:
    for feature in data:
        if feature['properties']['name_code'] == point:
            path.append(feature['properties']['name'])

print('El mejor camino es: ', path)

print('La menor distancia es: ', best_fitness)

'''
El mejor camino es:  ['Taberna Odín', 'Cervecería El Textil', 'Baum Palermo', 'Maldita Malta Belgrano', 'La Puerta Roja', 'La Birreria Puerto Madero', 'Estación MaB', 'Cerveza Patagonia', 'Bombar', 'Antares San Telmo', 'On Tap Retiro', 'Temple Craft Recoleta', 'Unplug bar', 'Marea Cervecería Bar', 'Mundo 2150', 'Jerome Palermo Hollywood', 'Cervecería Charlone', 'Francis Platz', 'PARDO Home Brew Beer', 'Samhain Pub']

La menor distancia es:  64.02796506912598
'''
