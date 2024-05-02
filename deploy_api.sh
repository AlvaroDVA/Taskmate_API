#!/bin/bash

# Función para mostrar errores y salir
show_error_and_exit() {
    echo "Error: $1" >&2
    exit 1
}

# Actualizar el sistema
sudo apt update && sudo apt upgrade -y || show_error_and_exit "No se pudo actualizar el sistema"

# Instalar python3-venv
sudo apt install -y python3-venv || show_error_and_exit "No se pudo instalar python3-venv"

# Directorio de destino
API_DIR="/var/www/api"

# Eliminar el directorio existente si hay contenido
if [ -d "$API_DIR" ]; then
    sudo rm -rf "$API_DIR" || show_error_and_exit "No se pudo eliminar el directorio existente"
fi

# Clonar el repositorio desde cero
git clone https://github.com/AlvaroDVA/Taskmate_API.git "$API_DIR" || show_error_and_exit "No se pudo clonar el repositorio"

# Crear y activar un entorno virtual
VENV_DIR="$API_DIR/venv"
python3 -m venv "$VENV_DIR" || show_error_and_exit "No se pudo crear el entorno virtual"
source "$VENV_DIR/bin/activate" || show_error_and_exit "No se pudo activar el entorno virtual"

# Instalar las dependencias de Python
pip install fastapi uvicorn gunicorn || show_error_and_exit "No se pudieron instalar las dependencias de Python"

# Crear un archivo de servicio para systemd
sudo tee /etc/systemd/system/fastapi.service >/dev/null <<EOF || show_error_and_exit "No se pudo crear el archivo de servicio"
[Unit]
Description=FastAPI Service
After=network.target

[Service]
User=taskmate
Group=taskmate
WorkingDirectory=$API_DIR
ExecStart=$VENV_DIR/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app -b 0.0.0.0:15556
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Recargar y habilitar el servicio
sudo systemctl daemon-reload && sudo systemctl enable fastapi && sudo systemctl start fastapi || show_error_and_exit "No se pudo habilitar y arrancar el servicio"

echo "El script se ha ejecutado correctamente."
