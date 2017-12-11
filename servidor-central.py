'''
    Archivo: servidor-central.py

    Descripción: Provee los métodos de la interfaz por cónsola del servidor
    central del servicio de descarga de videos.

    Autores:
        - Alejandra Cordero / 12-10645
        - Pablo Maldonado / 12-10561

    Última modificación: 11/12/2017
'''

#------------------------------------------------------------------------------#
#                                   IMPORTES                                   #
#------------------------------------------------------------------------------#

import _thread
from mensajes_cli_sc import *
from pony.orm import *
import socket
import pickle 
import modelo_db_sc
import random
import sys

#------------------------------------------------------------------------------#
#                            VARIABLES GLOBALES                                #
#------------------------------------------------------------------------------#

videos_disponibles      = set()
servidores_descarga     = {}
videos_atendidos        = {}
PORT_CLIENTE            = 9999
PORT_SERVIDOR_DESCARGA  = 9998 
MENSAJE_PING            = 20
MENSAJE_INSCRIPCION     = 21
MENSAJE_MOSTRAR_VIDEO   = 22
MENSAJE_DESCARGA_VIDEO  = 23
MENSAJE_INSCRIPCION_SD  = 11
MENSAJE_ATENDER_VIDEO   = 32
MENSAJE_VIDEO_ATENDIDO  = 13

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
    print("- El número de descargas realizadas es:",len(videos_atendidos))

#------------------------------------------------------------------------------#

def videos_cliente():

    '''
        Descripción:
    '''

    print("- Los vídeos atendidos son:")
    print(videos_atendidos)


#------------------------------------------------------------------------------#

def enviar_video_cliente(ip,port,video):

    '''
        Descripción:
    '''

    parte_video = 1

    sd_server, sd_videos = random.choice(list(servidores_descarga.items()))

    mensaje_recibido, sd_socket = asignar_video_sd(sd_server[0],sd_server[1],ip,port,video,0)

    # Se recibe el ACK del Servidor de Descarga.
    #print("Mensaje recibido",mensaje_recibido.id,mensaje_recibido.type)

    if (mensaje_recibido.id == MENSAJE_ATENDER_VIDEO and mensaje_recibido.type == "ack"):

        # Se espera a que el SD evíe el vídeo al cliente y envíe 
        # su confirmación
        #msg = sd_socket.recv(1024)
        print("- Se le asignó el vídeo ",video,"al Servidor de Descarga",sd_server[0])



#------------------------------------------------------------------------------#

def asignar_video_sd(ip_sd,port_sd,ip_cliente,port_cliente,video,parte):

    '''
        Descripción:
    '''

    # Se crea el socket
    sd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sd_socket.settimeout(8)
    
    # Conectamos el socket
    try:
        sd_socket.connect((ip_sd,port_sd))
    except:
        print("No se pudo establecer una conexón con el servidor descarga.")
        sys.exit()
    

    # Se arma el mensaje que va a ser enviado al servidor.
    mensaje = Mensaje_atender_video(ip_cliente,port_cliente,video,parte)
    data_string = pickle.dumps(mensaje)
    sd_socket.send(data_string)

    # Se espera el ACK
    msg = sd_socket.recv(1024) 

    sd_socket.close()                                    

    # Se lee el ACK
    mensaje_final = pickle.loads(msg)

    return mensaje_final,sd_socket

#------------------------------------------------------------------------------#

@db_session
def inscribir_cliente(addr):

    '''
        Descripción:
    '''
    # Se crea el cliente en la BD
    nuevo_cliente = modelo_db_sc.Cliente(direccion_ip=addr[0], 
                                        puerto=(addr[1]))
    commit()

    print("- Se ha inscrito el cliente",nuevo_cliente.direccion_ip, nuevo_cliente.puerto)


#------------------------------------------------------------------------------#

@db_session
def inscribir_sd(addr,videos):

    '''
        Descripción:
    '''
    global servidores_descarga
    global videos_disponibles

    videos_disponibles = videos_disponibles.union(set(videos))
    servidores_descarga[addr[0],addr[1]] = videos

    # Se crea el servidor de descarga en la BD
    nuevo_sd = modelo_db_sc.ServidorDescarga(direccion_ip=addr[0], 
                                            puerto=addr[1],
                                            estado="1")
    commit()

    # Se agregan los videos disponibles del servidor de descarga en la BD
    for video in videos:
        nuevo_video = modelo_db_sc.Video(nombre=video)
        # Se relaciona el video disponile con el servidor de descarga
        nuevo_sd.videos += nuevo_video
        commit()

    # - testing -
    # for video in nuevo_sd.videos:
    #     print(video.nombre)
    #print("VIDEOS DISPONIBLES",videos_disponibles)
    print("- Se ha inscrito el Servidor de descarga",nuevo_sd.direccion_ip, nuevo_sd.puerto)

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

def log_video_atendido(mensaje):

  '''
      Descripción:
  '''
 
  # Se introduce el vídeo en el log del servidor
  videos_atendidos[mensaje.ip_cliente,mensaje.port_cliente]= mensaje.video

#------------------------------------------------------------------------------#

@db_session
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

        if (mensaje.id == MENSAJE_PING):
            enviar_ack = True 

        elif (mensaje.id == MENSAJE_INSCRIPCION):
            inscribir_cliente([mensaje.ip,mensaje.port])
            enviar_ack = True

        elif (mensaje.id == MENSAJE_MOSTRAR_VIDEO):
            
            print("- Se está enviando la lista de vídeos disponibles al cliente ",addr,"...")


            # Se obtiene la lista de videos disponibles de la BD
            videos_disponibles_bd = modelo_db_sc.Video.select()            

            # - Testing -
            # print("-- Videos BD --")
            # for video in videos_disponibles_bd:
            #     print(video.nombre)

            videos = Mensaje_lista_videos(videos_disponibles)
            data_string = pickle.dumps(videos)
            clientsocket.send(data_string)
            clientsocket.close()
            enviar_ack = False

        elif (mensaje.id == MENSAJE_DESCARGA_VIDEO):

            # Se verifican cuantas descargas hay en el momento
            numero_descargas_actuales = len(modelo_db_sc.Descarga.select(
                                                lambda p: p.parte_actual < 4))

            # Testing
            print("El numero actual de descargas es --> " + 
                                                str(numero_descargas_actuales))

            if numero_descargas_actuales > 5:
                # Se debe crear una solicitud de descarga y 
                # poner al cliente en espera   
                pass        
            else: 
                # Se crea la descarga normal
                pass

            # Se busca el video solicitado en la BD (caso descarga posible)
            video_solicitado = modelo_db_sc.Video.get(nombre=mensaje.video)

            if video_solicitado:

                #print("Se encontro en la BD")

                # Se obtiene la entidad del cliente
                cliente_actual = modelo_db_sc.Cliente.get(direccion_ip=mensaje.ip)

                # Se crea la solicitud de la descarga 

                nueva_descarga = modelo_db_sc.Descarga(
                                                    cliente=cliente_actual,
                                                    video=video_solicitado,
                                                    parte_actual=1,
                                                )
                commit()

                # Se envia el video

                # Se actualiza el estado de la descgarga una vez que el video 
                # ha sido enviado en sus tres partes
                nueva_descarga.parte_actual = 4

            else:
                #print("No se encontro")
                pass

            if (mensaje.video in videos_disponibles):
                print("- Se está procesando un vídeo para un cliente ",addr,"...")

                # Se abre un hilo para empezar a asignar tareas a los servidores
                # de descarga.
                _thread.start_new_thread(enviar_video_cliente,(mensaje.ip,
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

        if (mensaje.id == MENSAJE_PING):
            enviar_ack = True 

        elif (mensaje.id  == MENSAJE_INSCRIPCION_SD):
            # Se almacena la información recibida
            inscribir_sd([mensaje.ip,mensaje.port],mensaje.videos)
            enviar_ack = True

        elif (mensaje.id == MENSAJE_VIDEO_ATENDIDO):
            print("- Llegó información estadística del servidor de descarga: ",addr)
            log_video_atendido(mensaje)
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