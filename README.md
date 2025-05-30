# UTNAySO-InyeccionSQL

Este es un proyecto educativo para el Trabajo Práctico Integrador de la materia
Arquitectura y Sistemas Operativos de la Tecnicatura en Programación a Distancia de la UTN.

El mismo está diseñado para demostrar vulnerabilidades de inyección SQL en aplicaciones web.
La aplicación es un sistema simple de notas con autenticación de usuarios que contiene vulnerabilidades intencionales para fines de aprendizaje.

## Descripción

La aplicación permite:
- Iniciar sesión con diferentes usuarios
- Crear, ver y eliminar notas
- Buscar notas por contenido

Las vulnerabilidades de inyección SQL están presentes intencionalmente como herramienta educativa para comprender los riesgos de seguridad en aplicaciones web.

## Requisitos

- Python 3 instalado
- pip (gestor de paquetes de Python)

## Configuración del entorno virtual

### Windows

1. Abre una terminal en la carpeta del proyecto

2. Crea un entorno virtual:
   ```
   python -m venv .venv
   ```

3. Activa el entorno virtual:
   ```
   .\.venv\Scripts\activate
   ```


## Instalación de dependencias

Con el entorno virtual activado, instala las dependencias del proyecto:

```
pip install -r requirements.txt
```

## Ejecución de la aplicación

Ya con el entorno virtual esté activado:

1. Ejecuta la aplicación:
   ```
   python main.py
   ```

2. La aplicación estará disponible en: http://127.0.0.1:5000/

3. Se puede iniciar sesión con cualquiera de los siguientes usuarios de ejemplo:
   - Usuario: luciano, Contraseña: luciano123
   - Usuario: lucio, Contraseña: lucio123
   - Usuario: maximo, Contraseña: maximo123
   - Usuario: sebastian, Contraseña: sebastian123

## Ejemplos de inyección SQL

En el archivo `scripts.txt` encontrarás ejemplos de inyecciones SQL que pueden utilizarse para explorar las vulnerabilidades de la aplicación.

## Nota importante

Esta aplicación contiene vulnerabilidades intencionales y su propósito es únicamente educativo para comprender los riesgos de seguridad y la importancia de implementar prácticas seguras de programación.