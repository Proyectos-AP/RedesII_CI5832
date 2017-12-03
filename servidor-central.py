'''
    Archivo: servidor-central.py

    Descripción: Provee los métodos de la interfaz por cónsola del servidor
    central del servicio de descarga de videos.

    Autores:
        - Alejandra Cordero / 12-10645
        - Pablo Maldonado / 12-10561

    Última modificación: 
'''

#------------------------------------------------------------------------------#
#                       DEFINICIÓN DE FUNCIONES DEL MENÚ                       #
#------------------------------------------------------------------------------#

def iniciar_servidor():
	'''
        Descripción:
    '''
	print("iniciar_servidor")

#------------------------------------------------------------------------------#

def numero_descargas_video():
	'''
        Descripción:
    '''
    print("numero_descargas_video")

#------------------------------------------------------------------------------#

def videos_cliente():
	'''
        Descripción:
    '''
	print("videos_cliente")

#------------------------------------------------------------------------------#
#                        INICIO DEL CÓDIGO PRINCIPAL                           #
#------------------------------------------------------------------------------#

print("---- SERVIDOR CENTRAL -----")

while True:

	opcion = input("SC --> ")

	if opcion == "NUMERO_DESCARGAS_VIDEO":
		numero_descargas_video()

	elif opcion == "VIDEOS_CLIENTE":
		videos_cliente()

	else:
		print("ERROR : La opción no es válida. Intente de nuevo")

#------------------------------------------------------------------------------#