import os

# Generar una clave secreta aleatoria
SECRET_KEY = os.urandom(24)
print(SECRET_KEY.hex())
