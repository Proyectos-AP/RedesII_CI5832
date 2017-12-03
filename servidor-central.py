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
#                                   IMPORTES                                   #
#------------------------------------------------------------------------------#

import socket  

#------------------------------------------------------------------------------#
#                            VARIABLES GLOBALES                                #
#------------------------------------------------------------------------------#

clientes = {}
PORT_CLIENTE = 9999   

#------------------------------------------------------------------------------#
#                           DEFINICIÓN DE FUNCIONES                            #
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
def inscribir_cliente(addr):

    global clientes

    clientes[addr[0],addr[1]] = ""

    print("Se ha inscrito el cliente",addr)

#------------------------------------------------------------------------------#

def consola():
    while True:

        opcion = input("SC --> ")

        if opcion == "NUMERO_DESCARGAS_VIDEO":
            numero_descargas_video()

        elif opcion == "VIDEOS_CLIENTE":
            videos_cliente()

        else:
            print("ERROR : La opción no es válida. Intente de nuevo")

#------------------------------------------------------------------------------#

def escuchar_cliente():
    # Se crea el socket
    serversocket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM) 


    # Se obtiene el hostname de la maquina
    host = socket.gethostname()                           
    print("Hostname",host)
                                            

    # bind to the PORT_CLIENTE
    serversocket.bind((host, PORT_CLIENTE))                                  

    # queue up to 5 requests
    serversocket.listen(5) 

    print("---- SERVIDOR CENTRAL -----")
    while True:

        # Se establece la conexion
        clientsocket,addr = serversocket.accept()      
        inscribir_cliente(addr)     
        msg = 'ACK'+ "\r\n"
        clientsocket.send(msg.encode('ascii'))
        clientsocket.close()

#------------------------------------------------------------------------------#
#                        INICIO DEL CÓDIGO PRINCIPAL                           #
#------------------------------------------------------------------------------#

escuchar_cliente()

#------------------------------------------------------------------------------#