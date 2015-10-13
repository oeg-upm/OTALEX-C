#!/bin/bash
#
# Este script genera unos ficheros de idiomas con todas las traducciones de ckan y los módulos
#
#

# Nombre de la extensión 
EXTENSION_NAME=ckanext-geoslab_spatial
# Directorio donde se encuentra CKAN
CKAN_DIR=/home/vagrant/ckan.git
# Directorio donde se pondran los fichero con las traducciones
DESTINATION_DIR=/tmp/ckan
# Idiomas usados
#LANGUAGES=("es" "en" "pt_BR")

for LANGUAGE in "es" "en" "pt_BR"
#for LANGUAGE in "${LANGUAGES[@]}"
do
	LANGUAGE_DIR="$DESTINATION_DIR/i18n/$LANGUAGE/LC_MESSAGES"
	LANGUAGE_FILE="$DESTINATION_DIR/i18n/$LANGUAGE/LC_MESSAGES/ckan.mo"
	
	# Creamos la carpeta del idioma si aun no está creada
	mkdir -p $LANGUAGE_DIR

	# Si es inglés no añadimos la traducción de ckan porque ya la trae de serie
	if [ "$LANGUAGE" = "en" ] 
	then
		msgcat --use-first "./i18n/$LANGUAGE/LC_MESSAGES/$EXTENSION_NAME.po" | msgfmt - -o "$LANGUAGE_FILE"
	else
		msgcat --use-first "./i18n/$LANGUAGE/LC_MESSAGES/$EXTENSION_NAME.po" "$CKAN_DIR/ckan/i18n/$LANGUAGE/LC_MESSAGES/ckan.po" | msgfmt - -o "$LANGUAGE_FILE"
	fi
done
