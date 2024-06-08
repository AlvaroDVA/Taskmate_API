# Taskmate API

API para mi Aplicación [Taskmate](https://github.com/AlvaroDVA/taskmate) . Esta api se encarga de almacenar, modificar y leer usuarios , tareas y notas almacenados en una base de datos MongoDB.

## Instalación

1. Ubuntu

   - Ejecuta el Script de lanzamiento.

   ```bash
   Ejectuta el archivo deploy_api.sh
   ```
   - Este Script se encargara de :
     - Intalar todos los requirements para su funcionamiento
     - Clonar el repositorio actualizado en su ultima versión
     - Crear un Servicio en systemd con la API bajo el nombre "fastapi"
   
   - Configurar config.json con los valores de su MongoDB
       ```bash
      # Example config.json

           "db_url": "mongodb://taskmate:taskmate@localhost:27017/",
           "username": "taskmate",
           "password": "taskmate",
           "db_name": "taskmate"
      ```

2. Windows
   
   - Clonar el repositorio
     
     ``` 
     git clone https://github.com/AlvaroDVA/Taskmate_API
      ```

   - Intalar las dependencias necesarias
     ```
     pip install -r requirements.txt
     ```

   - Configurar config.json con los valores de su MongoDB
       ```bash
      # Example config.json

           "db_url": "mongodb://taskmate:taskmate@localhost:27017/",
           "username": "taskmate",
           "password": "taskmate",
           "db_name": "taskmate"
      ```

## Uso

1. Windows:

   - Iniciar la API

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8091  
   ```

   - Visita [http://localhost:8091/docs](http://localhost:8091/docs) para ver la documentación interactiva de la API.

   - Realiza solicitudes a la API utilizando herramientas como cURL, Postman, o integrándola en tu aplicación.

2. Ubuntu
    - EL Script ya inicia como un servicio la API por defecto. En caso de necesitar consultar el servicio
    ```bash
    # En caso de necesitar consultar su estado :

    sudo systemctl status fastapi

    # En caso de reiniciar el servicio :

    sudo systemctl restart fastapi

    # En caso de iniciarlo desde cero:

    sudo systemctl start fastapi

## Llamadas

### Consultar documentación de los endpoints

Visita [http://localhost:8091/docs](http://localhost:8091/docs) para consultar toda la información sobre las llamadas.

#### Tener en cuenta :

   1. Todo usuario tiene : 
      1. Una id (idUser en el modelo, _id user en MongoDB) como String / Unico
      2. Un Usuario (username) como String / Unico
      3. Un Email (email) como String / Unico
      4. Una contraseña (password) como String 
         1. La API como tal no proporciona seguridad ni cifrado, esto esta al cargo del cliente.
      5. Un Avatar (avatar) como String
         1. Puede ser una url
         2. Puede ser un fichero decodificado y guardado directamente como una cadena de bytes
   2. Los cuadernos se almacena como una lista de paginas. Cada página se compone de:
      1. Un número de página (pageNumber) como un Entero
      2. Un texto (text) como String
   3. Las tareas se reciben como una lista de estas. Esta API solo se encarga de guardar y leer estas tareas y no ofrece ningún tipo de información sobre su contenido. Esto permite que cada desarrollador pueda componer sus propias tareas con la estructura que mas prefiera.


## Contribución

Si deseas contribuir a este proyecto, por favor abre un *issue* y sera revisado lo antes posible o envía un *pull request* con las mejoras y soluciones y será revisado lo antes posible.

Cualquier cambio solicitado en la rama principal será rechazado directamente, todos los cambios tienen que estar en una rama independiente y con suficiente información sobre las mejoras o los cambios.

## Autor

- Nombre: [AlvaroDVA](https://github.com/AlvaroDVA)
- Contacto: alvarodelvalarce@hotmail.com
