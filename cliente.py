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
#                                   NOTAS                                      #
#------------------------------------------------------------------------------#

# - Lo de verificar la inscripcion es posible caso de aspectos, aunque bueno 
#   aqui es que si aja solo dos veces, pero es mas tipo #elanalisis

#------------------------------------------------------------------------------#
#                              VARIABLES DE ESTADO                             #
#------------------------------------------------------------------------------#

inscrito = False # Indica si el cliente está inscrito o no

#------------------------------------------------------------------------------#
#                                   ERRORES                                    #
#------------------------------------------------------------------------------#

error_no_inscrito = "ERROR : El cliente no se ha inscrito"
error_ya_inscrito = "ERROR : El el cliente ya está inscrito" # es un error?

#------------------------------------------------------------------------------#
#                           DEFINICIÓN DE FUNCIONES                            #
#------------------------------------------------------------------------------#

def inscribir_cliente():
    '''
        Descripción:
    '''
    global inscrito

    if not(inscrito): 

        # Se realizan la inscripcion del servidor

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

    # Pensar como se haria para extraer el valor en inscribir

    if opcion == "INSCRIBIR":
        inscribir_cliente()

    elif opcion == "LISTA_VIDEOS":
        lista_videos()

    elif opcion == "VIDEO":
        video("Video_A_Descargar")

    else:
        print("ERROR : La opción no es válida. Intente de nuevo")

#------------------------------------------------------------------------------#