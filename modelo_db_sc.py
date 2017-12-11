'''
    Archivo: modelo_db_sc.py

    Descripción: Define las entidades y las relaciones de la Base de Datos
    del Servidor Central.

    Autores:
        - Alejandra Cordero / 12-10645
        - Pablo Maldonado / 12-10561

    Última modificación: 11/12/2017
'''

#------------------------------------------------------------------------------#
#                                   IMPORTES                                   #
#------------------------------------------------------------------------------#

from pony.orm import *

db = Database()

#------------------------------------------------------------------------------#
#                            DEFINICIÓN DEL MODELO                             #
#------------------------------------------------------------------------------#

class Video(db.Entity):
    id = PrimaryKey(int, auto=True)
    nombre = Required(str)
    servidor_descargas = Set('ServidorDescarga')
    solicitud_descargas = Set('SolicitudDescarga')
    estado_servidor_descargas = Set('EstadoServidorDescarga')
    descargas = Set('Descarga')

#------------------------------------------------------------------------------#

class SolicitudDescarga(db.Entity):
    id = PrimaryKey(int, auto=True)
    video = Required(Video)

#------------------------------------------------------------------------------#

class ServidorDescarga(db.Entity):
    id = PrimaryKey(int, auto=True)
    direccion_ip = Required(str)
    puerto = Required(int)
    estado = Required(str)
    videos = Set(Video)

#------------------------------------------------------------------------------#

class Cliente(db.Entity):
    id = PrimaryKey(int, auto=True)
    direccion_ip = Required(str)
    puerto = Required(str)
    descargas = Set('Descarga')
    estado_servidor_descargas = Set('EstadoServidorDescarga')

#------------------------------------------------------------------------------#

class Descarga(db.Entity):
    id = PrimaryKey(int, auto=True)
    cliente = Required(Cliente)
    video = Required(Video)
    parte_actual = Required(int)

#------------------------------------------------------------------------------#

class EstadoServidorDescarga(db.Entity):
    id = PrimaryKey(int, auto=True)
    parte_descargada = Optional(int)
    clientes = Set(Cliente)
    videos = Set(Video)

#------------------------------------------------------------------------------#
#                        INICIO DEL CÓDIGO PRINCIPAL                           #
#------------------------------------------------------------------------------#

db.bind(provider='postgres', 
        user='sistemavideo', 
        password='123123', 
        host='localhost', 
        database='servidorcentral')

db.generate_mapping(create_tables=True)
db.drop_all_tables(with_all_data=True)
db.create_tables()

# Para actualizar el modelo se debe eliminar lo que se tiene en el modelo actual
#  - Quitar el atributo de generate_mapping, comentar db.create_tables() y 
#    ejecutar
# Luego, se agregan los cambios en el modelo, se descomenta todo y se agrega
# de nuevo el atributo create_tables=True a db.generate_mapping()



