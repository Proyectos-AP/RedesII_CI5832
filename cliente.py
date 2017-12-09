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

import socket
import pickle 
import re

#------------------------------------------------------------------------------#
#                                   NOTAS                                      #
#------------------------------------------------------------------------------#

# - Lo de verificar la inscripcion es posible caso de aspectos, aunque bueno 
#   aqui es que si aja solo dos veces, pero es mas tipo #elanalisis

#------------------------------------------------------------------------------#
#                              VARIABLES DE ESTADO                             #
#------------------------------------------------------------------------------#

inscrito = False # Indica si el cliente está inscrito o no
PORT = 9999
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

def inscribir_cliente(ip,port):
    '''
        Descripción:
    '''
    global inscrito
    global PORT

    if not(inscrito): 

        # Se realizan la inscripcion del servidor

        # Se crea el socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Se obtiene el hostname de la maquina
        host = socket.gethostname()
        
        # Conectamos el socket
        try:
            client_socket.connect((host, PORT))
        except:
            print("No se pudo establecer una conexón con el servidor central.")
        

        data_string = pickle.dumps([ip,port])
        client_socket.send(data_string)

        # Se espera el ACK
        msg = client_socket.recv(1024)                                     

        # Se cierra el socket
        client_socket.close()
        print (msg.decode('ascii'))

        # Se obtiene el resultado de la operacion

        inscrito = True
        print("El cliente se ha inscrito de forma satisfactoria")
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
        # Se hace la consulta de los videos 
        # disponibles

        # Se recibe la informacion
        videos_disponibles = [
            "La_Divaza_En_Mexico",
            "How_To_Flirt",
            "Frozen_iPhone",
            "Tove_Lo_Habits",
        ]

        # Se muestran los videos disponibles
        print("Los videos disponibles del servidor son:")

        for i in range(0,len(videos_disponibles)):
            print("- " + videos_disponibles[i])

#------------------------------------------------------------------------------#

def video(nombre_video):
    '''
        Descipción:
    '''
    if not (inscrito):
        print(error_no_inscrito)
    else:
        # Se inicia la descarga del video

        # Se crea la ventana que mostrará
        # el status de descarga del 
        # video 
        print("video")

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

            if (verificar_puerto(ip_port[1])):
                inscribir_cliente(ip_port[0],ip_port[1])

            else:
                print("No se han intoducido un número de puerto correcto.")

        else:
            print("No se han intoducido los parametros de la inscripción correctamente.")

    elif opcion[0] == "LISTA_VIDEOS":
        lista_videos()

    elif opcion[0] == "VIDEO":
        video("Video_A_Descargar")

    else:
        print("ERROR : La opción no es válida. Intente de nuevo")

#------------------------------------------------------------------------------#