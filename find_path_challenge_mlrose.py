import json
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

def path(data, current, visited, total_distance):
    if not current['properties']['name'] in visited: #En la primera iteracion, current no va a estar en visited, y si no
        #lo agregamos vamos a volver al primer punto
        visited.append(current['properties']['name'])
    
    for val in visited: #sacamos de las distancias desde el punto en el que estamos todos los puntos a los que ya fuimos
        current['distances'].pop(val, None)
    
    try: #En la ultima iteracion min() va a dar error porque es un dicionario vacio, si no lo agarramos crashea
        nearest = min(current['distances'], key=current['distances'].get)
        visited.append(nearest)
        total_distance.append(current['distances'][nearest])
        
        for feature in data: #agarramos el nombre del nearest bar, que es el proximo al que vamos a ir
            if feature['properties']['name'] == nearest:
                next_bar = feature
    
    except:
        pass
        
    if len(current['distances']) > 0: #si no sacamos todas las distancias con la logica de arriba, significa que nos quedan 
        # puntos a donde ir
        path(data, next_bar, visited, total_distance)
        
    return visited, sum(total_distance)

def find_path(filepath):

    f = open(filepath, 'r').read()

    data = json.loads(f)['features']

    for feature in data:
            feature['distances'] = {}

    for feature in data:
        for _feature in data:
            if _feature['properties']['name'] != feature['properties']['name']:
                feature['distances'][_feature['properties']['name']] = haversine(feature['geometry']['coordinates'][1],feature['geometry']['coordinates'][0], _feature['geometry']['coordinates'][1],_feature['geometry']['coordinates'][0])
                
    return path(data, data[0], [], [])

optimal_path, distance = find_path('./breweries.geojson')

print('Camino: ', optimal_path)
print('Distancia: ', distance)


