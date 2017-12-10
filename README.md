# Implementación de un servicio de descarga de videos

Aplicación que permite configurar un servicio a través del cuál un cliente puede descargar los videos que se encuentren disponibles en la plataforma. Esta funcionalidad es gestionada por un Servidor Central que se encarga del control de los denominados Servidores de Descarga.

Un cliente descarga un video en 3 partes. Cada una de ella de un Servidor de Descarga distinto. En caso de que alguno de ellos falle, los otros se encargan de retomar la descarga. 

Puede consultar el detalle de los requerimientos de la aplicación [aquí](./Enunciado.pdf)

Esta implementación corresponde al proyecto final del Laboratorio del curso "Redes de Computadoras II" de la Universidad Simón Bolívar durante el trimestre Septiembre - Diciembre 2017. 

## Autores
* Alejandra Cordero - [alejandra.corderogarcia21@gmail.com](mailto:alejandra.corderogarcia21@gmail.com)
* Pablo Maldonado - [prmm95@gmail.com](mailto:prmm95@gmail.com)

## Requerimientos de *software*

- Python 3
- PostgreSQL
- Ejecute el siguiente siguiente comando para instalar el resto de los requerimientos de la aplicación.

``` bash
pip3 install -r requirements.txt
```
# Base de Datos

En primer lugar, será necesario crear la base de datos en *postgres* y el usuario correspondiente. Para ello, ejecute los siguientes comandos:

Ingrese a *PostgreSQL*
``` bash
sudo -su postgres
psql
```
Cree el usuario y la base de datos del Servidor Central
``` psql
CREATE USER sistemavideo WITH PASSWORD '123123';
CREATE DATABASE servidorcentral WITH OWNER sistemavideo;
```
Cree las bases de datos de los Servidores de Descarga
``` psql
CREATE DATABASE servidordescarga1 WITH OWNER sistemavideo;
CREATE DATABASE servidordescarga2 WITH OWNER sistemavideo;
CREATE DATABASE servidordescarga3 WITH OWNER sistemavideo;
```

Salir del usuario *postgres*

Ejecute el archivo que define el modelo:
``` bash
python3 modelo-db.py
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
