'''
Created on 28/9/2015

@author: prodrig
'''

import logging
import pprint

import ckan.plugins as p
from ckanext.spatial.interfaces import ISpatialHarvester
from ckanext.spatial.harvesters.base import guess_resource_format
from ckanext.spatial.harvesters import CSWHarvester

#class CswHarvesterGeoslab(p.SingletonPlugin):
class CswHarvesterGeoslab(CSWHarvester):

    #p.implements(ISpatialHarvester, inherit=True)

    def info(self):
        return {
            'name': 'csw_geoslab',
            'title': 'CSW Server (Geoslab)',
            'description': 'Estension del harvest espacial de CSW por parte de Geoslab'
            }

    def get_package_dict(self, iso_values, harvest_object):

        # Configuramos el log
        log = logging.getLogger(__name__ + '.geoslab')
        log.debug('CswHarvesterGeoslab: get_package_dict.')
        log.debug('CswHarvesterGeoslab: iso_values = \n' + pprint.pformat(iso_values, indent=4) + '\n')
        
        # Ejecutamos el proceso padre
        data_dict = super(CSWHarvester, self).get_package_dict(iso_values, harvest_object)
    
        log.debug('CswHarvesterGeoslab: data_dict = \n' + pprint.pformat(data_dict, indent=4) + '\n')
    
        # TAGS - Cortamos los tags con puntos
        
        # Cogemos los tags del metadato
        tags = []
        if 'tags' in iso_values:
            for tag in iso_values['tags']:
                
                tagsSplit = tag.split('.')
                for tagSplit in tagsSplit:
                    tagSplit = tagSplit[:50] if len(tagSplit) > 50 else tagSplit
                    tags.append({'name': tagSplit})
        # Añadimos los tags por defecto
        default_tags = self.source_config.get('default_tags',[])
        if default_tags:
            for tag in default_tags:
                tags.append({'name': tag})
        # Machacamos los que había
        data_dict['tags'] = tags
        
        # RECURSOS
        
        # Creamos el recurso al metadato en el csw
        resource = {}
        # Ejemplo: http://www.ideotalex.eu/geonetwork/srv/csw?request=GetRecordById&service=CSW&version=2.0.2&outputSchema=http://www.isotc211.org/2005/gmd&id=908b40e5-588b-4d70-aa61-63c98aed7d88
        resource['url'] = harvest_object.source.url + '?request=GetRecordById&service=CSW&version=2.0.2&outputSchema=http://www.isotc211.org/2005/gmd&id=' + harvest_object.guid
        resource['format'] = guess_resource_format(resource.get('url'))
        resource['protocol'] = ''
        resource['name'] = 'Metadato ISO19115'
        resource['description'] = 'Enlace al metadato en el csw'
        resource['resource_locator_protocol]'] = resource.get('protocol')
        resource['resource_locator_function'] = ''
        # Lo añadimos al recurso
        data_dict['resources'].append(resource)
        
        return data_dict