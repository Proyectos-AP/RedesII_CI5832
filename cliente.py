'''
    Archivo: cliente.py

    Descripción: Provee los métodos de la interfaz por cónsola del cliente
    del servicio de descarga de videos.

    Autores:
        - Alejandra Cordero / 12-10645
        - Pablo Maldonado / 12-10561

    Última modificación: 
'''

#------------------------------------------------------------------------------#
#                                   IMPORTES                                   #
#------------------------------------------------------------------------------#

from mensajes_cli_sc import *
import _thread
import socket
import pickle 
import re

#------------------------------------------------------------------------------#
#                                   NOTAS                                      #
#------------------------------------------------------------------------------#

# - Lo de verificar la inscripcion es posible caso de aspectos, aunque bueno 
#   aqui es que si aja solo dos veces, pero es mas tipo #elanalisis

#------------------------------------------------------------------------------#
#                              VARIABLES GLOBALES                              #
#------------------------------------------------------------------------------#

inscrito = False # Indica si el cliente está inscrito o no
videos_disponibles   = []
PORT                 = 9999
PORT_ESCUCHA         = 0
IP                   = 0
MENSAJE_ENVIAR_VIDEO = 12
MENSAJE_LISTA_VIDEOS = 34

#------------------------------------------------------------------------------#
#                                   ERRORES                                    #
#------------------------------------------------------------------------------#

error_no_inscrito = "ERROR : El cliente no se ha inscrito"
error_ya_inscrito = "ERROR : El el cliente ya está inscrito" # es un error?

#------------------------------------------------------------------------------#
#                           DEFINICIÓN DE FUNCIONES                            #
#------------------------------------------------------------------------------#


def verificar_puerto(port):

    '''
        Descripción:
    '''

    result = re.match("(6553[0-5]|655[0-2][0-9]\d|65[0-4](\d){2}|6[0-4](\d){3}|[1-5](\d){4}|[1-9](\d){0,3})",port)

    if (result and result.group() == port ): 
        return True

    else:
        return False


#------------------------------------------------------------------------------#

def enviar_info(ip,port,mensaje):

    '''
        Descripción:
    '''

    # Se crea el socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    # Conectamos el socket
    try:
        client_socket.connect((ip, port))
    except:
        print("No se pudo establecer una conexón con el servidor central.")
        

    # Se arma el mensaje que va a ser enviado al servidor.
    data_string = pickle.dumps(mensaje)
    client_socket.send(data_string)

    # Se espera la respuesta del servidor central
    mensaje_videos = client_socket.recv(1024)                                     

    # Se cierra el socket
    client_socket.close()

    # Se lee el mensaje
    mensaje_retorno = pickle.loads(mensaje_videos)

    return mensaje_retorno

#------------------------------------------------------------------------------#

def inscribir_cliente(ip,port):

    '''
        Descripción:
    '''
    global inscrito
    global PORT_ESCUCHA
    global PORT
    global IP

    if not(inscrito): 

        # Se realizan la inscripcion del servidor

        PORT_ESCUCHA = int(port)

        mensaje = Mensaje_inscripcion(ip,port)

        # Se envía mensaje al Servidor Central
        ack = enviar_info(ip,PORT,mensaje)

        # Se verifica si el ACK es correcto.
        if (ack.id == mensaje.id and ack.type == "ack"):
            inscrito = True
            IP = ip
            print("El cliente se ha inscrito de forma satisfactoria")

        else:
            print("El cliente no se ha podido inscribir. Intentelo de nuevo.")

    else: 
        print(error_ya_inscrito)

#------------------------------------------------------------------------------#

def lista_videos():
    '''
        Descripción:
    '''
    if not(inscrito):
        print(error_no_inscrito)

    else:

        global videos_disponibles
        # Se hace la consulta de los videos disponibles

        mensaje = Mensaje_mostrar_videos()
        # Se envía mensaje al Servidor Central
        mensaje_videos = enviar_info(IP,PORT,mensaje)

        # Se verifica si el mensaje es correcto.
        if (mensaje_videos.id == MENSAJE_LISTA_VIDEOS):

            # Se muestran los videos disponibles
            print("Los videos disponibles del servidor son:")

            for i in range(0,len(mensaje_videos.videos)):
                print("- " + mensaje_videos.videos[i])

        else:
            print("El servidor no ha podido enviar los vídeos disponibles. Intentelo de nuevo.")


#------------------------------------------------------------------------------#

def video(nombre_video):
    '''
        Descipción:
    '''
    if not (inscrito):
        print(error_no_inscrito)
    else:

        # Se arma el mensaje que va a ser enviado al servidor.
        mensaje = Mensaje_descarga_videos(IP,PORT_ESCUCHA,nombre_video)

        # Se envía mensaje al Servidor Central
        ack = enviar_info(IP,PORT,mensaje)

        # Se verifica si el ACK es correcto.
        if (ack.id == mensaje.id and ack.type == "ack"):
            print("El vídeo se está procesando...")
            escuchar_servidor_descarga()

        elif (ack.id == mensaje.id and ack.type == "nack"):
            print("El vídeo introducido no se encuentra en la lista de vídeos disponibles.")

        else:
            print("El cliente no se ha podido hacer la petición al servidor. Intentelo de nuevo.")


#------------------------------------------------------------------------------#

def escuchar_servidor_descarga():

    '''
        Descripción:
    '''

    # Se crea el socket
    serversocket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM) 

                    
    # bind to the PORT_CLIENTE

    # Conectamos el socket
    try:
        serversocket.bind((IP, PORT_ESCUCHA))
    except:
        print("No se pudo establecer una conexón con el servidor central.")                                  

    # queue up to 5 requests
    serversocket.listen(3) 
    numero_videos = 0

    print("---- Se abrió socket para escuchar a Servidor de Descarga -----")
    while (numero_videos < 3 ):

        enviar_ack = False

        # Se establece la conexion
        clientsocket,addr = serversocket.accept()

        # Se recibe la información enviada por los SD.      
        data = clientsocket.recv(4096)
        mensaje = pickle.loads(data)


        if (mensaje.id  == MENSAJE_ENVIAR_VIDEO):

            # Se reciben las partes del vídeo
            print("Recibida parte",numero_videos)
            enviar_ack = True
            numero_videos += 1


        # Se envia un mensaje ACK al cliente.
        if (enviar_ack):
            ack = Mensaje_ack(mensaje.id,"ack")
            data_string = pickle.dumps(ack)
            clientsocket.send(data_string)
            clientsocket.close()

    print("Se recibió el vídeo completo")


#------------------------------------------------------------------------------#
#                        INICIO DEL CÓDIGO PRINCIPAL                           #
#------------------------------------------------------------------------------#

print("--- CLIENTE --- ")

while True:

    opcion = input("CL ---> ")
    argumento_recibido = ""

    opcion = opcion.split(" ")

    # Se extrae el valor del ip y el puerto
    if opcion[0] == "INSCRIBIR":

        # Se verifica si los parametros instroducidos son correctos
        if (len(opcion) == 2):
            ip_port = opcion[1].split(":")
            # Se verifica si el número de puerto es correcto.

            if ( len(ip_port)==2 and verificar_puerto(ip_port[1]) ):
                inscribir_cliente(ip_port[0],ip_port[1])

            else:
                print("No se han intoducido un número de puerto correcto.")

        else:
            print("No se han intoducido los parametros de la inscripción correctamente.")

    elif opcion[0] == "LISTA_VIDEOS":
        lista_videos()

    elif opcion[0] == "VIDEO":

        # Se verifica si los parametros instroducidos son correctos
        if (len(opcion) == 2):

            # Se abre el hilo que se encargará de escuchar al servidor de descarga
            _thread.start_new_thread(video,(opcion[1],))

        else:
            print("No se han intoducido los parametros del vídeo correctamente.")

    else:
        print("ERROR : La opción no es válida. Intente de nuevo")

#------------------------------------------------------------------------------#