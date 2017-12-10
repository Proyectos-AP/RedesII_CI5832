'''
    servidor-descarga.py

    Descripción: Provee los métodos de la interfaz por cónsola de un
    servidor de descarga del servicio de descarga de videos.

    Autores:
        - Alejandra Cordero / 12-10645
        - Pablo Maldonado / 12-10561

    Última modificación: 11/12/2017

'''


#------------------------------------------------------------------------------#
#                                   IMPORTES                                   #
#------------------------------------------------------------------------------#

from mensajes_cli_sc import *
import socket
import pickle 
import _thread
import random

#------------------------------------------------------------------------------#
#                            VARIABLES GLOBALES                                #
#------------------------------------------------------------------------------#

# Puerto para enviar info al Servidor Central
PORT_ENVIO_SC          = 9998

# Puerto para recibir info del Servidor Central
PORT_ESCUCHA_SC        = 0

MENSAJE_ATENDER_VIDEO  = 32

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
    
    global PORT_ESCUCHA_SC

    PORT_ESCUCHA_SC = random.randint(10000, 20000)
    
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
    sd_socket.connect((ip, PORT_ENVIO_SC))

    # Se prepara el mensaje para ser enviado
    mensaje = Mensaje_inscripcion_SD(ip,PORT_ESCUCHA_SC,videos_disponibles)
    data_string = pickle.dumps(mensaje)
    sd_socket.send(data_string)

    # Se espera el ACK
    msg = sd_socket.recv(1024)                                     

    # Se cierra el socket
    sd_socket.close()


    # Se lee el ACK
    ack = pickle.loads(msg)

    # Se verifica si el ACK es correcto.
    if (ack.id == mensaje.id and ack.type == "ack"):
        inscrito = True
        IP = ip
        print("El servidor se ha inscrito de forma satisfactoria.")

    else:
        print("El servidor no se ha podido inscribir. Intentelo de nuevo.")


#------------------------------------------------------------------------------#

def enviar_video_cliente(ip_cliente,port_cliente,mensaje):

    '''
        Descripción:
    '''

    # Se crea el socket
    sd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    # Se obtiene el ip de la maquina
    ip_sd = get_ip()

    try:
        sd_socket.connect((ip_sd,port_cliente))
    except:
        print("No se pudo establecer una conexón con el servidor descarga.")
    

    # Se arma el mensaje que va a ser enviado al servidor.
    data_string = pickle.dumps(mensaje)
    sd_socket.send(data_string)

    # Se espera el ACK
    msg = sd_socket.recv(1024) 

    sd_socket.close()                                    

    # Se lee el ACK
    mensaje_final = pickle.loads(msg)

    return mensaje_final

#------------------------------------------------------------------------------#

def atender_cliente(ip,port,video,parte):

    # Se obtiene el ip de la maquina
    ip_sd = get_ip()

    # Armo el mensaje que va a ser enviado al cliente.
    mensaje = Mensaje_enviar_video(ip_sd,port,video,parte)

    # Envio el mensaje al cliente.
    mensaje_respuesta = enviar_video_cliente(ip,port,mensaje)

    # Se verifica si el ACK es correcto.
    if (mensaje_respuesta.id  == mensaje.id and mensaje_respuesta.type == "ack"):
        print("Se envio una parte del vídeo al cliente...")

#------------------------------------------------------------------------------#

def escuchar_sc():

    '''
        Descripción:
    '''

    # Se crea el socket
    serversocket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM) 


    # Se obtiene el ip de la maquina
    server_ip = get_ip()                          

    # bind to the PORT_CLIENTE
    serversocket.bind((server_ip, PORT_ESCUCHA_SC))                                  

    # queue up to 5 requests
    serversocket.listen(5) 

    print("---- Se abrió socket para escuchar a Servidor de Central -----")

    while True:

        enviar_ack = False

        # Se establece la conexion
        clientsocket,addr = serversocket.accept()

        # Se recibe la información enviada por los SD.      
        data = clientsocket.recv(1024)
        mensaje = pickle.loads(data)

        if (mensaje.id == MENSAJE_ATENDER_VIDEO):

            atender_cliente(mensaje.ip_cliente,mensaje.port_cliente,
                            mensaje.video,mensaje.parte)
            enviar_ack = True


        # Se envia un mensaje ACK al Servidor Central.
        if (enviar_ack):
            ack = Mensaje_ack(mensaje.id,"ack")
            data_string = pickle.dumps(ack)
            clientsocket.send(data_string)
            clientsocket.close()



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
    print("videos_descargados")

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
            videos_descargados()
        else:
            print("ERROR : La opción no es válida. Intente de nuevo")

#------------------------------------------------------------------------------#
#                        INICIO DEL CÓDIGO PRINCIPAL                           #
#------------------------------------------------------------------------------#

# Se abre hilo para el inicio de sesión del servidor de descarga
_thread.start_new_thread(iniciar_servidor,())

# Se abre hilo para escuchar las solicitudes del servidor central
_thread.start_new_thread(escuchar_sc,())

# Se abre la consola
consola()


#------------------------------------------------------------------------------#