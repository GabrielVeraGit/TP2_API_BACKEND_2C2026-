import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

# Cargar variables del .env
load_dotenv()

# 1. Crear la instancia global de SQLAlchemy
db = SQLAlchemy()


# 2. Configuración de la clase
class Config:
  SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
  SQLALCHEMY_TRACK_MODIFICATIONS = False


# Validación
if not Config.SQLALCHEMY_DATABASE_URI:
  raise ValueError(
      "ERROR: La variable DATABASE_URL no está configurada en el archivo .env"
  )