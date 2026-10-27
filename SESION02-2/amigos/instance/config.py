# Definición de secretos a usar por la app
import os

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite://")