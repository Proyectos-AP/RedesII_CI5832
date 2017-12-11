'''
    Archivo: mensajes_cli_sc.py

    Descripción: Define los mensajes que son intercambiados durante
    la comunicación entre los distintos actores.

    Autores:
        - Alejandra Cordero / 12-10645
        - Pablo Maldonado / 12-10561

    Última modificación: 11/12/2017
'''

#------------------------------------------------------------------------------#
#                           DEFINICIÓN DE FUNCIONES                            #
#------------------------------------------------------------------------------#

class Mensaje_inscripcion:
	'''
		Descripción:
	'''
	def __init__(self,ip,port):
		self.id = 21
		self.ip = ip
		self.port = port
		self.type = "cliente-sevidor"

#------------------------------------------------------------------------------#

class Mensaje_mostrar_videos:
	'''
		Descripción:
	'''
	def __init__(self):
		self.id = 22
		self.type = "cliente-sevidor"

#------------------------------------------------------------------------------#

class Mensaje_descarga_videos:
	'''
		Descripción:
	'''
	def __init__(self,ip,port,video):
		self.id    = 23
		self.ip    = ip
		self.port  = port
		self.video = video
		self.type  = "cliente-sevidor"

#------------------------------------------------------------------------------#

class Mensaje_ack:
	'''
		Descripción:
	'''
	def __init__(self,id,type,message=""):
		self.id     = id
		self.type   = type
		self.message = message

#------------------------------------------------------------------------------#

class Mensaje_lista_videos:
	'''
		Descripción:
	'''
	def __init__(self,videos):
		self.id = 34
		self.videos = videos
		self.type = "sevidor-cliente"

#------------------------------------------------------------------------------#
#                           DEFINICIÓN DE FUNCIONES                            #
#------------------------------------------------------------------------------#

class Mensaje_inscripcion_SD:
	'''
		Descripción:
	'''
	def __init__(self,ip,port,videos):
		self.id      = 11
		self.ip      = ip
		self.port    = port
		self.videos  = videos
		self.type    = "sevidorD-sevidorC"

#------------------------------------------------------------------------------#

class Mensaje_video_atendido:

	def __init__(self,ip,port,video,parte):
		self.id             = 13
		self.ip_cliente     = ip
		self.port_cliente   = port
		self.video          = video
		self.parte          = parte
		self.type           = "sevidorD-sevidorC"

#------------------------------------------------------------------------------#

class Mensaje_atender_video:
	'''
		Descripción:
	'''
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
	'''
		Descripción:
	'''
	def __init__(self,ip,port,video,parte,nombre_video):
		self.id             = 12
		self.ip             = ip
		self.port           = port
		self.video          = video
		self.parte          = parte
		self.nombre_video   = nombre_video
		self.type           = "sevidorD-cliente"

#------------------------------------------------------------------------------#