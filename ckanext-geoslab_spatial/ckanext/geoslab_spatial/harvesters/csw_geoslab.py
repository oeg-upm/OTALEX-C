'''
Created on 28/9/2015

@author: prodrig
'''

import logging
import pprint

import ckan.plugins as p
from ckanext.spatial.interfaces import ISpatialHarvester

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
        
        # Mostramos los datos que tenemos
        log.trace('CswHarvesterGeoslab: iso_values = \n' + pprint.pformat(iso_values, indent=4) + '\n')

        # Ejecutamos el proceso padre
        data_dict = super(CSWHarvester, self).get_package_dict(iso_values, harvest_object)
    
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
        
        return data_dict