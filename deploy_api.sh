#!/bin/bash

# Función para mostrar errores y salir
show_error_and_exit() {
    echo "Error: $1" >&2
    exit 1
}

# Directorio de destino
API_DIR="/var/www/api"

# Verificar si el directorio existe
if [ -d "$API_DIR" ]; then
    # Eliminar el contenido del directorio, excluyendo el directorio en sí
    sudo find "$API_DIR" -mindepth 1 -delete || show_error_and_exit "No se pudo borrar el contenido existente"
else
    # Si el directorio no existe, crearlo
    sudo mkdir -p "$API_DIR" || show_error_and_exit "No se pudo crear el directorio api"
fi

# Clonar el repositorio dentro de la carpeta api
git clone https://github.com/AlvaroDVA/Taskmate_API.git "$API_DIR" || show_error_and_exit "No se pudo clonar el repositorio"

# Instalar las dependencias de Python en el sistema
sudo apt install -y python3-fastapi python3-uvicorn python3-gunicorn || show_error_and_exit "No se pudieron instalar las dependencias de Python"

sudo apt install python3-bson python3-pymongo || show_error_and_exit 

# Crear un archivo de servicio para systemd
sudo tee /etc/systemd/system/fastapi.service >/dev/null <<EOF || show_error_and_exit "No se pudo crear el archivo de servicio"
[Unit]
Description=FastAPI Service
After=network.target

[Service]
User=taskmate
Group=taskmate
WorkingDirectory=$API_DIR
ExecStart=/usr/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app -b 0.0.0.0:15556
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Recargar y habilitar el servicio
sudo systemctl daemon-reload && sudo systemctl enable fastapi && (sleep 5 && sudo systemctl resstart fastapi) || show_error_and_exit "No se pudo habilitar y arrancar el servicio"

echo "El script se ha ejecutado correctamente."

