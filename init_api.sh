#!/bin/bash

python -m venv .venv #crear entorno virtual
# 1. Cargar el entorno virtual dentro del subshell
if [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate       # En Windows (Git Bash)
else
    source .venv/bin/activate           # En Linux / WSL
fi

#source .venv/scripts/activate #activarlo

cp .env.example .env #copiar archivo de variables de entorno

python -m pip install --upgrade pip #asegurar que pip este actualizado
python -m pip install -r requirements.txt #instalar requerimientos/dependencias



#falta agregar mas codigo
# 3. Levantar la API de Flask
#python app.py

#deactivate
