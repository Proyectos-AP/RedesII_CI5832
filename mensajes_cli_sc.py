'''
    Archivo: mensajes_cli_sc.py

    Descripción: Provee los métodos de la interfaz por cónsola del servidor
    central del servicio de descarga de videos.

    Autores:
        - Alejandra Cordero / 12-10645
        - Pablo Maldonado / 12-10561

    Última modificación: 
'''

#------------------------------------------------------------------------------#
#                           DEFINICIÓN DE FUNCIONES                            #
#------------------------------------------------------------------------------#

class Mensaje_inscripcion:

	def __init__(self,ip,port):
		self.id = 1
		self.ip = ip
		self.port = port
		self.type = "cliente-sevidor"

#------------------------------------------------------------------------------#

class Mensaje_mostrar_videos:

	def __init__(self,ip,port):
		self.id = 2
		self.type = "cliente-sevidor"

#------------------------------------------------------------------------------#

class Mensaje_descarga_videos:
	def __init__(self,ip,port):
		self.id = 3
		self.type = "cliente-sevidor"

#------------------------------------------------------------------------------#

class Mensaje_ack:

	def __init__(self,id):
		self.id = id
		self.type = "ack"

#------------------------------------------------------------------------------#

class Mensaje_lista_videos:

	def __init__(self,videos):
		self.id = 4
		self.videos = videos
		self.type = "sevidor-cliente"

#------------------------------------------------------------------------------#