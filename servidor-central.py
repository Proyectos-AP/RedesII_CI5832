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
MENSAJE_INSCRIPCION     = 1
MENSAJE_MOSTRAR_VIDEO   = 2
MENSAJE_DESCARGA_VIDEO  = 3    

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

    servidores_descarga[addr[0],addr[1]] = videos

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

    print(ip)

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

    print("---- SERVIDOR CENTRAL -----")
    while True:

        # Se establece la conexion
        clientsocket,addr = serversocket.accept()    
        data = clientsocket.recv(1024)
        mensaje = pickle.loads(data)

        if (mensaje.id == MENSAJE_INSCRIPCION):
            inscribir_cliente([mensaje.ip,mensaje.port])

        elif (mensaje.id == MENSAJE_MOSTRAR_VIDEO):
            videos_cliente()

        elif (mensaje.id == MENSAJE_DESCARGA_VIDEO):
            print("INFORMAR AL SERVIDOR DE DESCARGA")

        # Se envia un mensaje ACK al cliente.
        ack = Mensaje_ack(mensaje.id)
        data_string = pickle.dumps(mensaje)
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


    # Se obtiene el hostname de la maquina
    host = socket.gethostname()                           

    # bind to the PORT_CLIENTE
    serversocket.bind((host, PORT_SERVIDOR_DESCARGA))                                  

    # queue up to 5 requests
    serversocket.listen(5) 

    print("---- SERVIDOR CENTRAL -----")
    while True:

        # Se establece la conexion
        clientsocket,addr = serversocket.accept()

        # Se recibe la información enviada por los SD.      
        data = clientsocket.recv(4096)
        videos_disponibles = pickle.loads(data)

        # Se almacena la información recibida
        inscribir_sd(addr,videos_disponibles)

        # Se envia el ACK
        msg = 'ACK'+ "\r\n"
        clientsocket.send(msg.encode('ascii'))
        clientsocket.close()


#------------------------------------------------------------------------------#
#                        INICIO DEL CÓDIGO PRINCIPAL                           #
#------------------------------------------------------------------------------#

#escuchar_servidor_descarga()
escuchar_cliente()

#------------------------------------------------------------------------------#