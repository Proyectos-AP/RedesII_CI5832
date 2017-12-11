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
from threading import Thread, Lock
import random
import os

#------------------------------------------------------------------------------#
#                            VARIABLES GLOBALES                                #
#------------------------------------------------------------------------------#


IP_SERVIDOR          = "192.168.0.106"

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
    "Video_1.mp4"
]

total_videos_descargando = set()
total_videos_descargados = set()

mutex = Lock()

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
    
    try:
        # Conectamos el socket
        sd_socket.connect((IP_SERVIDOR, PORT_ENVIO_SC))
    except:
        print("No se pudo establecer conexión con el Servidor Centra")
        exit(0)

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

    
    pass                                    

    # Se lee el ACK
    #mensaje_final = pickle.loads(msg)

    #return mensaje_final

#------------------------------------------------------------------------------#


def enviar_info(ip_cliente,port_cliente,mensaje):

    '''
        Descripción:
    '''

    # Se crea el socket
    sd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    try:
        sd_socket.connect((ip_cliente,port_cliente))
    except:
        print("No se pudo establecer una conexón.")
        exit(0)
    

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

    global mutex
    global total_videos_descargando
    global total_videos_descargados
    BUFFER = 1024

    # Se registra el vídeo que se esta descargando haciendo uso de semaforos.
    mutex.acquire()
    total_videos_descargando.add(video)
    mutex.release()


    # Se obtiene el ip de la maquina
    ip_sd = get_ip()

    print("Video a enviar",video)
    # Se abre la lectura del archivo
    video_a_enviar = open("./Video_1.mp4", "rb")
    info_video = video_a_enviar.read(BUFFER)

    # Se crea el socket
    sd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    try:
        sd_socket.connect((ip,port))
    except:
        print("No se pudo establecer una conexión.")
        exit(0)
    
    video_size = os.stat(video).st_size

    # Armo el mensaje que va a ser enviado al cliente.
    mensaje = Mensaje_enviar_video(ip_sd,PORT_ESCUCHA_SC,video_size,parte,video)
    data_string = pickle.dumps(mensaje)
    sd_socket.sendall(data_string)

    # Se empieza a enviar el vídeo
    while (info_video):
        
        # Se arma el mensaje que va a ser enviado al servidor.
        sd_socket.sendall(info_video)

        #Leo el vídeo que debo eviar
        info_video = video_a_enviar.read(BUFFER)

        #print("Estoy enviando un vídeo")


    print("Terminé de enviar el vídeo")
    sd_socket.close()

    # Se recibe un ACK del cliente y se verifica si el mismo es correcto.
    if (mensaje_respuesta.id  == mensaje.id and mensaje_respuesta.type == "ack"):
        print("Se envio una parte del vídeo al cliente...")

        # Se registra el vídeo atendido haciendo uso de semaforos.
        mutex.acquire()
        total_videos_descargando.discard(video)
        total_videos_descargados.add(video)
        mutex.release()

        # Se ĺe informa al servidor que el vídeo ya fué enviado
        ip,port,video,parte
        mensaje = Mensaje_video_atendido(ip,port,video,parte)
        ack = enviar_info(ip,PORT_ENVIO_SC,mensaje)
        print("Se recibió ACK del SC",ack)

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

            # Se crea un hilo para que se atienda la solicitud del cliente
            Thread(target=atender_cliente,args=(mensaje.ip_cliente,
                                    mensaje.port_cliente,mensaje.video,mensaje.parte,)).start()

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
    print("Los vídeos que se están descargando son: ",total_videos_descargando)

#------------------------------------------------------------------------------#

def videos_descargados():
    '''
        Descripción:
    '''

    print("Los vídeos descargandos son: ",total_videos_descargados)

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


# Verificar si el SC está conectado.

# Se abre hilo para el inicio de sesión del servidor de descarga
Thread(target=iniciar_servidor,args=()).start()

# Se abre hilo para escuchar las solicitudes del servidor central
Thread( target=escuchar_sc,args=() ).start()

# Se abre la consola
consola()

#------------------------------------------------------------------------------#