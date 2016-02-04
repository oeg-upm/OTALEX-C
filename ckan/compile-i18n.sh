#!/bin/bash
#
# Este script genera unos ficheros de idiomas con todas las traducciones de ckan y los módulos
#
#

# Directorio de las extensiónes
EXTENSIONS_DIR=/vagrant
# Directorio donde se encuentra CKAN
CKAN_DIR=/usr/lib/ckan/default/src/ckan
# Directorio donde se pondran los ficheros finales con las traducciones
DESTINATION_DIR=/etc/ckan

for LANGUAGE in "es" "en" "pt_BR"
do
	
	EXTENSIONS=""
	
	for EXTENSION_NAME in "ckanext-geoslab_spatial" "ckanext-geoslab_harvest" "ckanext-otalexc_template"
	do
		CURRENT_LANGUAGE_FILE="$EXTENSIONS_DIR/$EXTENSION_NAME/i18n/$LANGUAGE/LC_MESSAGES/$EXTENSION_NAME.po"
		if [ -f "$CURRENT_LANGUAGE_FILE" ]
		then
			EXTENSIONS="$EXTENSIONS $CURRENT_LANGUAGE_FILE"
		fi
		
	done

	# Si CKAN tiene este idioma añadimos la traducción
	CURRENT_LANGUAGE_FILE="$CKAN_DIR/ckan/i18n/$LANGUAGE/LC_MESSAGES/ckan.po"
	if [ -f "$CURRENT_LANGUAGE_FILE"  ] 
	then
		EXTENSIONS="$EXTENSIONS $CURRENT_LANGUAGE_FILE"
	fi
	
	# Creamos la carpeta del idioma si aun no está creada
	LANGUAGE_DIR="$DESTINATION_DIR/i18n/$LANGUAGE/LC_MESSAGES"
	mkdir -p $LANGUAGE_DIR

	# Unimos todos los ficheros de este idioma en uno solo
	LANGUAGE_FILE="$LANGUAGE_DIR/ckan.mo"
	msgcat --use-first $EXTENSIONS | msgfmt - -o "$LANGUAGE_FILE"

done
