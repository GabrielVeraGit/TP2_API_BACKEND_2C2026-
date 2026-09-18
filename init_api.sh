#!/bin/bash
python3 -m venv .venv #crear entorno virtual
source .venv/bin/activate #activarlo

cp .env.example .env #copiar archivo de variables de entorno

pip install --upgrade pip #asegurar que pip este actualizado
pip install -r requirements.txt #instalar requerimientos/dependencias



#falta agregar mas codigo


#deactivate
