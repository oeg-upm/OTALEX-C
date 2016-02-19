'''
Created on 5 de feb. de 2016

@author: prodrig
'''
import sys
import logging

import csv
import urllib, urllib2, httplib
import json

########################################################
#
#                     PERSONALIZACION
#
########################################################

# URL donde tenemos instalado CKAN
URL = "http://localhost:5000"
# API KEY del usuario con el que se van a importar los datasets del CSV
API_KEY = "c3a82849-ddac-45e7-b25e-90f455c48a28"
# Fichero CSV a importar
CSV_FILE = './Datasets_otalex.csv'
# Nivel del log (CRITICAL, ERROR, WARNING, INFO, DEBUG)
LOG_LEVEL = logging.INFO
# Si ya existe el dataset: Borramos o actualizamos (True, False)
DELETE_IF_EXISTS = False

########################################################
#
#                     OBJETOS
#
########################################################

# Definimos la clase Object para poder crear atributos dinamicamente a un objeto de un tipo generico
class Object(object):
    pass

########################################################
#
#                     FUNCIONES
#
########################################################

def ckan_request(url="http://localhost:5000", path="", key="", data={}):
    """ Funcion que realiza una llamada a la api de CKAN
        
        Keyword arguments:
        url    -- La url del CKAN (default http://localhost:5000) (Por ejemplo: http://ckan.com:500)
        path   -- El path de la llamada arealizar (default 0.0) (Por ejemplo: /api/action/package_create) 
        key    -- El token de un usaurio de CKAN para utilizar en las peticiones (Por ejemplo: c3a82869-deac-45e7-b25e-90f765c48a28)
        data   -- Datos de la peticion (default {})
    """

    # Mostramos los datos que vamos a enviar
    logging.debug('REQUEST DATA POST: %s', json.dumps(data))

    # Use the json module to dump the dictionary to a string for posting.
    data_string = urllib.quote(json.dumps(data))
    
    # Inicializamos la peticion
    request = urllib2.Request(url + path)
    
    # Anyadimos el token de nuestro usuario a la peticion
    request.add_header('Authorization', API_KEY)
    # Anyadimos los datos a la peticion
    request.add_data(data_string)
    
    # Hacemos la peticion
    try: 
        response = urllib2.urlopen(request)
    except urllib2.HTTPError, error:
        # logging.exception(str(error.reason))
        return error
    except urllib2.URLError, error:
        logging.exception(str(error.reason))
        return error
    except httplib.HTTPException, error:
        logging.exception(str(error.reason))
        return error
    except Exception:
        import traceback
        logging.error('generic exception: ' + traceback.format_exc())
        exit()
    
    # Use the json module to load CKAN's response into a dictionary.
    response_dict = json.loads(response.read())
    logging.debug('RESPONSE: %s', json.dumps(response_dict))
    return response_dict


########################################################
#
#                        MAIN
#
########################################################

# Configuramos el log
rootLogger = logging.getLogger()
rootLogger.setLevel(LOG_LEVEL)
consoleHandler = logging.StreamHandler(sys.stdout)
#logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

# Leemos el fichero
logging.info('Leemos el fichero CSV: %s', CSV_FILE)
reader = csv.reader(open(CSV_FILE, 'rb'))
datasets = enumerate(reader)
# Quitamos la primera linea que contiene los titulos de las columnas
next(datasets)
for index,row in datasets:
    
    # Cogemos cada columna del CSV
    csv_dataset             = row[0]
    csv_id                  = row[1]
    csv_title               = row[2]
    csv_description         = row[3]
    csv_tags                = row[4]
    csv_license             = row[5]
    csv_organization        = row[6]
    csv_state               = row[7]
    csv_source              = row[8]
    csv_version             = row[9]
    csv_author              = row[10]
    csv_author_email        = row[11]
    csv_maintainer          = row[12]
    csv_maintainer_email    = row[13]
    csv_epsg                = row[14]
    csv_spatial             = row[15]
    
    # Parseamos los tags
    # Tenemos que generar el siguiente formato
    #[
    #    {
    #        "name":"government-spending"
    #    },
    #    {
    #        "name":"climate"
    #    }
    #]
    tags_array_dirty = csv_tags.decode('utf-8').split(";")
    tags_array = list()
    for name in tags_array_dirty:
        
        #if isinstance(name, str):
        #    #print "ordinary string"
        #    print(name.decode('utf-8'))
        #elif isinstance(name, unicode):
        #    print "unicode string"
        #else:
        #    print "not a string"
        
        # Miramos si no es una cadena vacia
        if name:
            tag_object = Object()
            tag_object.name = lambda: None
            setattr(tag_object, 'name', name)
            tags_array.append(tag_object.__dict__)
    
    extras = []
    
    # Extraemos
    if csv_spatial:
        geometry = json.loads(csv_spatial)
        coordinates = geometry['coordinates']
        
        # Inicializamos los valores del bbox a extraer con unos valores para que cualquier nuevo sea mejor
        lat_max = -sys.float_info.max
        lat_min = sys.float_info.max
        long_max = -sys.float_info.max
        long_min = sys.float_info.max
        # Recorremos todos los puntos
        for coordinates2 in coordinates:
            for coordinate in coordinates2:
                if coordinate[0] < long_min :
                    long_min = coordinate[0] 
                    
                if long_max < coordinate[0] :
                    long_max = coordinate[0]
                    
                if coordinate[1] < lat_min :
                    lat_min = coordinate[1]
                    
                if lat_max < coordinate[1] :
                    lat_max = coordinate[1]
        
        # Anyadimos los datos de la geometria
        extras.append({
                        'key': 'bbox-east-long',
                        'value': long_max,
                    })
        extras.append({
                       'key': 'bbox-north-lat',
                        'value': lat_max,
                    })
        extras.append({
                       'key': 'bbox-south-lat',
                        'value': lat_min,
                    })
        extras.append({
                       'key': 'bbox-west-long',
                        'value': long_min,
                    })
        extras.append({
                       'key': 'spatial-reference-system',
                       'value': csv_epsg,
                    })
        extras.append({
                       'key': 'spatial',
                       'value': csv_spatial,
                    })     
    
    dataset_dict = {
        'name': csv_id,
        'title': csv_title,
        'description': csv_description,
        'author': csv_author,
        'author_email': csv_author_email,
        'maintainer': csv_maintainer,
        'maintainer_email': csv_maintainer_email,
    #    'id': 'bc3ee679-fd88-46c4-9559-858cd60d9e4b', READONLY
        'state': csv_state,
        'tags': tags_array,
        'version': csv_version,
    #    'groups': [{"name": "grupo1"}],
        'license_id': csv_license,
        'owner_org': csv_organization,
        'url': csv_source,
    #    'notes': None,
    #    'revision_id': 'fe8c2064-349a-4d97-9878-090a7c07ec20', READONLY
        'extras': extras,
    }
    
    # Miramos si existe
    logging.info('Tratamos el dataset: ' + dataset_dict['name'])
    logging.info('- Comprobamos si existe')
    response_dict = ckan_request(url=URL, path="/api/action/package_show", key=API_KEY, data={'id': dataset_dict['name']})
    if type(response_dict) is urllib2.HTTPError and response_dict.code == 404:
        
        # Creamos el dataset
        logging.info('Lo creamos')
        response_dict = ckan_request(url=URL, path="/api/action/package_create", key=API_KEY, data=dataset_dict)
        
    else:
        
        if DELETE_IF_EXISTS:
            # Borramos el dataset PERO no se borra permanentemente. Hay que purgar desde el usuario admin los borrados
            logging.info('- Lo borramos')
            response_dict = ckan_request(url=URL, path="/api/action/package_delete", key=API_KEY, data={'id': dataset_dict['name']})
        else:
            # Actualizamos el dataset
            logging.info('- Lo actualizamos')
            response_dict = ckan_request(url=URL, path="/api/action/package_update", key=API_KEY, data=dataset_dict)


