# Implementación de un servicio de descarga de videos

Aplicación que permite configurar un servicio a través del cuál un cliente puede descargar los videos que se encuentren disponibles en la plataforma. Esta funcionalidad es gestionada por un Servidor Central que se encarga del control de los denominados Servidores de Descarga.

Un cliente descarga un video en 3 partes. Cada una de ella de un Servidor de Descarga distinto. En caso de que alguno de ellos falle, los otros se encargan de retomar la descarga. 

Puede consultar el detalle de los requerimientos de la aplicación [aquí](./Enunciado.pdf)

Esta implementación corresponde al proyecto final del Laboratorio del curso "Redes de Computadoras II" de la Universidad Simón Bolívar. 

## Autores
* Alejandra Cordero - [alejandra.corderogarcia21@gmail.com](mailto:alejandra.corderogarcia21@gmail.com)
* Pablo Maldonado - [prmm95@gmail.com](mailto:prmm95@gmail.com)

## Requerimientos de *software*

- Python 3
- PostgreSQL
- Ejecute el siguiente siguiente comando para instalar el resto de los requerimientos de la aplicación.

``` bash
pip install -r requirements.txt
```

## Ejecución 

### Cliente

``` bash
python3 cliente.py
```

### Servidor de Descarga

``` bash
python3 servidor-descarga.py
```

### Servidor Central 

``` bash
python3 servidor-central.py
```
