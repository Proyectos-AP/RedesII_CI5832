'''
    servidor-descarga.py

    Descripción: Provee los métodos de la interfaz por cónsola de un
    servidor de descarga del servicio de descarga de videos.

    Autores:
        - Alejandra Cordero / 12-10645
        - Pablo Maldonado / 12-10561

    Última modificación: 

'''

#------------------------------------------------------------------------------#
#                           DEFINICIÓN DE FUNCIONES                            #
#------------------------------------------------------------------------------#

def iniciar_servidor():
	'''
        Descripción:
    '''
	
	# Se comunica con el servidor centralds

	# Se sincronizan los videos 

	print("iniciar_servidor")

#------------------------------------------------------------------------------#

def videos_descargando():
	'''
        Descripción:
    '''
	print("videos_descargando")

#------------------------------------------------------------------------------#

def videos_descargados():
	'''
        Descripción:
    '''

#------------------------------------------------------------------------------#
#                        INICIO DEL CÓDIGO PRINCIPAL                           #
#------------------------------------------------------------------------------#

print("---- SERVIDOR DESCARGA -----")

# Primero, inicializa el servidor
iniciar_servidor()

# Luego de esto, se presenta el menu de opciones
while True:

	opcion = input("SD ---> ")

	if opcion == "VIDEOS_DESCARGANDO":
		videos_descargando()

	elif opcion == "VIDEOS_DESCARGADOS":
		videos_descargados
	else:
		print("ERROR : La opción no es válida. Intente de nuevo")

#------------------------------------------------------------------------------#