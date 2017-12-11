'''
    Archivo: modelo_db_sd.py

    Descripción: Define las entidades y las relaciones de la Base de Datos
    de los Servidores de Descarga

    Autores:
        - Alejandra Cordero / 12-10645
        - Pablo Maldonado / 12-10561

    Última modificación: 11/12/2017
'''

#------------------------------------------------------------------------------#
#                                   IMPORTES                                   #
#------------------------------------------------------------------------------#

from pony.orm import *
import sys

db = Database()

#------------------------------------------------------------------------------#
#                            DEFINICIÓN DEL MODELO                             #
#------------------------------------------------------------------------------#

class Video(db.Entity):
    id = PrimaryKey(int, auto=True)
    nombre = Required(str)
    ubicacion_archivo = Required(str)
    numero_descargas = Required(int)

#------------------------------------------------------------------------------#
#								CREANDO LOS MODELOS 						   #
#------------------------------------------------------------------------------#

servidor_seleccionado = sys.argv[1]
numero_servidor = int(servidor_seleccionado)

db.bind(provider='postgres', 
        user='sistemavideo', 
        password='123123', 
        host='localhost', 
        database='servidordescarga' + servidor_seleccionado)

db.generate_mapping(create_tables=True)

inicio = 10 * numero_servidor

with db_session:
	for i in range(inicio,inicio + 10):
		nuevo_video = Video(nombre="Video_"+str(i), 
							ubicacion_archivo="./Video_1.mp4",
							numero_descargas=0)
		commit()

