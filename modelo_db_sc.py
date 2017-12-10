'''
    Archivo: modelo-db.py

    Descripción: Define las entidades y las relaciones de la Base de Datos
    del sistema.

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
    ubicacion_archivo = Required(str)
    servidor_descargas = Set('ServidorDescarga')
    solicitud_descargas = Set('SolicitudDescarga')
    estado_servidor_descargas = Set('EstadoServidorDescarga')

#------------------------------------------------------------------------------#

class SolicitudDescarga(db.Entity):
    id = PrimaryKey(int, auto=True)
    video = Required(Video)

#------------------------------------------------------------------------------#

class ServidorDescarga(db.Entity):
    id = PrimaryKey(int, auto=True)
    direccion_ip = Optional(str)
    puerto = Optional(str)
    estado = Optional(str)
    videos = Set(Video)

#------------------------------------------------------------------------------#

class Cliente(db.Entity):
    id = PrimaryKey(int, auto=True)
    direccion_ip = Required(str)
    puerto = Required(int)
    descargas = Set('Descarga')
    estado_servidor_descargas = Set('EstadoServidorDescarga')

#------------------------------------------------------------------------------#

class Descarga(db.Entity):
    id = PrimaryKey(int, auto=True)
    cliente = Required(Cliente)

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