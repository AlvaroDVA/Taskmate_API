#!/bin/bash

# Función para mostrar errores y salir
show_error_and_exit() {
    echo "Error: $1" >&2
    exit 1
}

# Actualizar el sistema
sudo apt update && sudo apt upgrade -y || show_error_and_exit "No se pudo actualizar el sistema"

# Instalar las dependencias necesarias
sudo apt install -y python3-pip || show_error_and_exit "No se pudieron instalar las dependencias de Python"

# Instalar las dependencias de Python
pip3 install fastapi uvicorn gunicorn || show_error_and_exit "No se pudieron instalar las dependencias de Python"

# Directorio de destino
API_DIR="/var/www/api"

# Clonar el repositorio si no existe
if [ ! -d "$API_DIR" ]; then
    git clone https://github.com/AlvaroDVA/Taskmate_API.git "$API_DIR" || show_error_and_exit "No se pudo clonar el repositorio"
else
    # Si el repositorio ya existe, actualizarlo si hay cambios
    cd "$API_DIR" || show_error_and_exit "No se pudo cambiar al directorio del repositorio"
    git pull origin master >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        show_error_and_exit "No se pudo actualizar el repositorio"
    fi
fi

# Cambiar al directorio de la API
cd "$API_DIR" || show_error_and_exit "No se pudo cambiar al directorio de la API"

# Iniciar Gunicorn
nohup gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app -b 0.0.0.0:15556 & || show_error_and_exit "No se pudo iniciar Gunicorn"

# Crear un archivo de servicio para systemd
sudo tee /etc/systemd/system/fastapi.service >/dev/null <<EOF || show_error_and_exit "No se pudo crear el archivo de servicio"
[Unit]
Description=FastAPI Service
After=network.target

[Service]
User=taskmate
Group=taskmate
WorkingDirectory=$API_DIR
ExecStart=/usr/local/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app -b 0.0.0.0:15556
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Habilitar y arrancar el servicio
sudo systemctl daemon-reload && sudo systemctl enable fastapi && sudo systemctl start fastapi || show_error_and_exit "No se pudo habilitar y arrancar el servicio"

echo "El script se ha ejecutado correctamente."

