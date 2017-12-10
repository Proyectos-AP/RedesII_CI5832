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

import _thread
from mensajes_cli_sc import *
import socket
import pickle 

#------------------------------------------------------------------------------#
#                            VARIABLES GLOBALES                                #
#------------------------------------------------------------------------------#

clientes                = {}
videos_disponibles      = []
servidores_descarga     = {}
PORT_CLIENTE            = 9999
PORT_SERVIDOR_DESCARGA  = 9998 
MENSAJE_INSCRIPCION     = 21
MENSAJE_MOSTRAR_VIDEO   = 22
MENSAJE_DESCARGA_VIDEO  = 23
MENSAJE_INSCRIPCION_SD  = 11

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

def asignar_video_cliente(ip,port,video):

    '''
        Descripción:
    '''
    print("videos_cliente",ip,port,video)

#------------------------------------------------------------------------------#
def inscribir_cliente(addr):

    '''
        Descripción:
    '''

    global clientes

    clientes[addr[0],addr[1]] = ""

    print("Se ha inscrito el cliente",addr)


#------------------------------------------------------------------------------#

def inscribir_sd(addr,videos):

    '''
        Descripción:
    '''

    global servidores_descarga
    global videos_disponibles

    servidores_descarga[addr[0],addr[1]] = videos
    videos_disponibles = videos_disponibles + videos

    print("Se ha inscrito el Servidor de descarga",servidores_descarga)

#------------------------------------------------------------------------------#

def consola():

    '''
        Descripción:
    '''

    while True:

        opcion = input("SC --> ")

        if opcion == "NUMERO_DESCARGAS_VIDEO":
            numero_descargas_video()

        elif opcion == "VIDEOS_CLIENTE":
            videos_cliente()

        else:
            print("ERROR : La opción no es válida. Intente de nuevo")


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

def escuchar_cliente():

    '''
        Descripción:
    '''

    # Se crea el socket
    serversocket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM) 


    # Se obtiene el ip de la maquina
    server_ip = get_ip()

    # bind to the PORT_CLIENTE
    serversocket.bind((server_ip, PORT_CLIENTE))                                  

    # queue up to 5 requests
    serversocket.listen(5) 

    print("---- Se abrió socket para escuchar al cliente -----")
    while True:

        enviar_ack = False

        # Se establece la conexion
        clientsocket,addr = serversocket.accept()    
        data = clientsocket.recv(1024)
        mensaje = pickle.loads(data)

        if (mensaje.id == MENSAJE_INSCRIPCION):
            inscribir_cliente([mensaje.ip,mensaje.port])
            enviar_ack = True

        elif (mensaje.id == MENSAJE_MOSTRAR_VIDEO):
            
            print("Se está enviando la lista de vídeos disponibles al cliente...")
            videos = Mensaje_lista_videos(videos_disponibles)
            data_string = pickle.dumps(videos)
            clientsocket.send(data_string)
            clientsocket.close()
            enviar_ack = False

        elif (mensaje.id == MENSAJE_DESCARGA_VIDEO):

            if (mensaje.video in videos_disponibles):
                print("Se está procesando un vídeo para un cliente...")

                # Se abre un hilo para empezar a asignar tareas a los servidores
                # de descarga.
                _thread.start_new_thread(asignar_video_cliente,(mensaje.ip,
                                         mensaje.port,mensaje.video,))
                
                enviar_ack = True

            else:
                # Se envia un NACK
                ack = Mensaje_ack(mensaje.id,"nack")
                data_string = pickle.dumps(ack)
                clientsocket.send(data_string)
                clientsocket.close()

        # Se envia un mensaje ACK al cliente.
        if (enviar_ack):
            ack = Mensaje_ack(mensaje.id,"ack")
            data_string = pickle.dumps(ack)
            clientsocket.send(data_string)
            clientsocket.close()

#------------------------------------------------------------------------------#

def escuchar_servidor_descarga():

    '''
        Descripción:
    '''

    # Se crea el socket
    serversocket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM) 


    # Se obtiene el ip de la maquina
    server_ip = get_ip()                          

    # bind to the PORT_CLIENTE
    serversocket.bind((server_ip, PORT_SERVIDOR_DESCARGA))                                  

    # queue up to 5 requests
    serversocket.listen(5) 

    print("---- Se abrió socket para escuchar a Servidor de Descarga -----")
    while True:

        enviar_ack = False

        # Se establece la conexion
        clientsocket,addr = serversocket.accept()

        # Se recibe la información enviada por los SD.      
        data = clientsocket.recv(4096)
        mensaje = pickle.loads(data)


        if (mensaje.id  == MENSAJE_INSCRIPCION_SD):
            # Se almacena la información recibida
            inscribir_sd([mensaje.ip,mensaje.port],mensaje.videos)
            enviar_ack = True


        # Se envia un mensaje ACK al cliente.
        if (enviar_ack):
            ack = Mensaje_ack(mensaje.id,"ack")
            data_string = pickle.dumps(ack)
            clientsocket.send(data_string)
            clientsocket.close()


#------------------------------------------------------------------------------#
#                        INICIO DEL CÓDIGO PRINCIPAL                           #
#------------------------------------------------------------------------------#

# Se abre el hilo que se encargará de escuchar al servidor de descarga
_thread.start_new_thread(escuchar_servidor_descarga,())

# Se abre el hilo que se encargará de escuchar al cliente
_thread.start_new_thread(escuchar_cliente,())

# Se muestra la consola
consola()


#------------------------------------------------------------------------------#