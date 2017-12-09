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
#                                   IMPORTES                                   #
#------------------------------------------------------------------------------#

import socket
import pickle 
import _thread

#------------------------------------------------------------------------------#
#                            VARIABLES GLOBALES                                #
#------------------------------------------------------------------------------#

PORT = 9998

videos_disponibles = [
    "La_Divaza_En_Mexico",
    "How_To_Flirt",
    "Frozen_iPhone",
    "Tove_Lo_Habits",
]   

#------------------------------------------------------------------------------#
#                       DEFINICIÓN DE FUNCIONES DEL MENÚ                       #
#------------------------------------------------------------------------------#

def iniciar_servidor():
    '''
        Descripción:
    '''
    
    # Se comunica con el servidor central.
    inscribir_servidor_descarga()

    # Se sincronizan los videos 



#------------------------------------------------------------------------------#

def get_ip():

    '''
        Descripción:
    '''

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()

    return ip 


#------------------------------------------------------------------------------#

def inscribir_servidor_descarga():
    '''
        Descripción:
    '''

    # Se crea el socket
    sd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Se obtiene el hostname de la maquina
    ip = get_ip()
    
    # Conectamos el socket
    sd_socket.connect((ip, PORT))

    data_string = pickle.dumps(videos_disponibles)
    sd_socket.send(data_string)

    # Se espera el ACK
    msg = sd_socket.recv(1024)                                     

    # Se cierra el socket
    sd_socket.close()
    print (msg.decode('ascii'))

    # Se obtiene el resultado de la operacion

    inscrito = True
    print("El servidor se ha inscrito de forma satisfactoria.")

    pass
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

def consola():

    print("---- SERVIDOR DESCARGA -----")

    # Primero, inicializa el servidor
    #iniciar_servidor()

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
#                        INICIO DEL CÓDIGO PRINCIPAL                           #
#------------------------------------------------------------------------------#

# Se abre hilo para el inicio de sesión del servidor de descarga
_thread.start_new_thread(iniciar_servidor,())

# Se abre la consola
consola()


#------------------------------------------------------------------------------#