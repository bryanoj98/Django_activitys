# Api para la gestion de Actividades con Django Rest Framework

Implementa un CRUD con Django Rest Framework en el cual, se pueden Agregar nuevas
actividades, Re-agendar, Cancelar y Listar las actividades

## Pre-requisitos

Se deben instalar las librerias y demas dependencias necesarias para la 
correcta ejecucion del proyecto
```sh
pip install -r requirements.txt
```
Es necesario la modificacion de los valores para la conexión a la BD de Postgres:
- En **settings.py** en el apartado *DATABASES*

Tambien puede crear los modelos con el comando:
```sh
python3 manage.py makemigrations
```

Para posteriormente reflejarlos como tablas en su DB, con el comando:
```sh
python3 manage.py migrate
```
El aplicativo esta diseñado para realizar CRUD para Actividades. Si desea
crear registros para Propiedades, debe acceder al apartado de administrador.
Para esto es necesario que cree un perfil administrador de la siguiente forma:
```sh
python3 manage.py createsuperuser
```
Posteriormente a llenar los campos solicitados: *Usuario*,*correo*,*contraseña*.
Ejecute la aplicacion y acceda a la ruta:
 - ***localhost***/admin 
 - ejemplo http://127.0.0.1:8000/admin/
 

## ¿Cómo se usa?

Ejecutar el siguiente comando sobre la ruta del proyecto:

```sh
 python3 manage.py runserver
```
