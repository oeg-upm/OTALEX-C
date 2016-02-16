#!/bin/bash
#
# Este script crea las aplicaciones del proyecto Otalex-C en el sistema de CKAN
#

# Token del usuario con el que se crearán las aplicaciones
TOKEN=c3a82869-ddac-45d7-c25e-90f644c48a28
# URL de CKAN
CKAN_URL=http://127.0.0.1:5000

# Creamos las aplicaciones

# Catálogo de Metadatos
TITLE="Catálogo de Metadatos"
URL="http://www.ideotalex.eu/geonetwork"
DESCRIPTION="Este es el catálogo de datos de Otalex-c"
IMAGE="$CKAN_URL/ckanext/otalexc_template/images/apps/catalogo.jpg"
curl $CKAN_URL/api/3/action/related_create \
-H "Authorization: $TOKEN" \
-X POST --data '{"type":"Application", "title":"'"$TITLE"'", "url":"'"$URL"'", "description":"'"$DESCRIPTION"'", "image_url":"'"$IMAGE"'"}' \
-w "\n"

# Visualizador de Mapas
TITLE="Visualizador de mapas"
URL="http://www.ideotalex.eu/OtalexC/PortalOtalex/Visor.html"
DESCRIPTION="Este es el visualizador de mapas"
IMAGE="$CKAN_URL/ckanext/otalexc_template/images/apps/visualizador.jpg"
curl $CKAN_URL/api/3/action/related_create \
-H "Authorization: $TOKEN" \
-X POST --data '{"type":"Application", "title":"'"$TITLE"'", "url":"'"$URL"'", "description":"'"$DESCRIPTION"'", "image_url":"'"$IMAGE"'"}' \
-w "\n"

# Nomenclator
TITLE="Nomenclator (Gazetteer)"
URL="http://www.ideotalex.eu/OtalexC/cargaBuscarToponimias.do?language=es"
DESCRIPTION="Este es el Nomenclator (Gazetteer)"
IMAGE="$CKAN_URL/ckanext/otalexc_template/images/apps/nomenclator.jpg"
curl $CKAN_URL/api/3/action/related_create \
-H "Authorization: $TOKEN" \
-X POST --data '{"type":"Application", "title":"'"$TITLE"'", "url":"'"$URL"'", "description":"'"$DESCRIPTION"'", "image_url":"'"$IMAGE"'"}' \
-w "\n"

# Sistema de indicadores
TITLE="Sistema de indicadores"
URL="http://www.ideotalex.eu/SIOIdeOtalex"
DESCRIPTION="Este es el sistema de indicadores"
IMAGE="$CKAN_URL/ckanext/otalexc_template/images/apps/SIO.jpg"
curl $CKAN_URL/api/3/action/related_create \
-H "Authorization: $TOKEN" \
-X POST --data '{"type":"Application", "title":"'"$TITLE"'", "url":"'"$URL"'", "description":"'"$DESCRIPTION"'", "image_url":"'"$IMAGE"'"}' \
-w "\n"

# Buscador semántico
TITLE="Buscador semántico"
URL="http://www.ideotalex.eu/sparql"
DESCRIPTION="Este es el buscador semántico"
IMAGE="$CKAN_URL/ckanext/otalexc_template/images/apps/virtuoso.jpg"
curl $CKAN_URL/api/3/action/related_create \
-H "Authorization: $TOKEN" \
-X POST --data '{"type":"Application", "title":"'"$TITLE"'", "url":"'"$URL"'", "description":"'"$DESCRIPTION"'", "image_url":"'"$IMAGE"'"}' \
-w "\n"

# Visualizador semántico
TITLE="Visualizador semántico"
URL="http://www.ideotalex.eu/map4rdf"
DESCRIPTION="Este es el visualizador semántico"
IMAGE="$CKAN_URL/ckanext/otalexc_template/images/apps/map4rdf.jpg"
curl $CKAN_URL/api/3/action/related_create \
-H "Authorization: $TOKEN" \
-X POST --data '{"type":"Application", "title":"'"$TITLE"'", "url":"'"$URL"'", "description":"'"$DESCRIPTION"'", "image_url":"'"$IMAGE"'"}' \
-w "\n"
