from flask import Flask
import os
#version 1.0.1
app = Flask(__name__)

@app.route('/')
def hello():
    return "¡Hola desde la aplicación desplegada vía Jenkins CI/CD en Amazon EKS! Versión: v1.0.0\n"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)