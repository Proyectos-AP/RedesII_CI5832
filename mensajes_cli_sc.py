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
		self.id = 21
		self.ip = ip
		self.port = port
		self.type = "cliente-sevidor"

#------------------------------------------------------------------------------#

class Mensaje_mostrar_videos:

	def __init__(self):
		self.id = 22
		self.type = "cliente-sevidor"

#------------------------------------------------------------------------------#

class Mensaje_descarga_videos:
	def __init__(self,ip,port,video):
		self.id    = 23
		self.ip    = ip
		self.port  = port
		self.video = video
		self.type  = "cliente-sevidor"

#------------------------------------------------------------------------------#

class Mensaje_ack:

	def __init__(self,id,type,message=""):
		self.id     = id
		self.type   = type
		self.message = message

#------------------------------------------------------------------------------#

class Mensaje_lista_videos:

	def __init__(self,videos):
		self.id = 34
		self.videos = videos
		self.type = "sevidor-cliente"

#------------------------------------------------------------------------------#
#                           DEFINICIÓN DE FUNCIONES                            #
#------------------------------------------------------------------------------#

class Mensaje_inscripcion_SD:

	def __init__(self,ip,port,videos):
		self.id      = 11
		self.ip      = ip
		self.port    = port
		self.videos  = videos
		self.type    = "sevidorD-sevidorC"

#------------------------------------------------------------------------------#

class Mensaje_atender_video:

	def __init__(self,ip,port,video,parte):
		self.id             = 32
		self.ip_cliente     = ip
		self.port_cliente   = port
		self.video          = video
		self.parte          = parte
		self.type           = "sevidorC-sevidorD"

#------------------------------------------------------------------------------#
#                           DEFINICIÓN DE FUNCIONES                            #
#------------------------------------------------------------------------------#

class Mensaje_enviar_video:

	def __init__(self,ip,port,video,parte):
		self.id             = 12
		self.ip             = ip
		self.port           = port
		self.video          = video
		self.parte          = parte
		self.type           = "sevidorD-cliente"

#------------------------------------------------------------------------------#