from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

def filtrar_usuarios_por_nombre_de_forma_segura(nombre=None, modo='seguro'):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    if nombre and nombre.strip():
        if modo == 'seguro':
            # Usar parámetros para evitar inyección SQL
            cursor.execute("SELECT id, nombre, email FROM usuarios WHERE nombre LIKE ?", ('%' + nombre + '%',))
        else:
            # Concatenamos el string, muy inseguro
            cursor.execute("SELECT nombre, email FROM usuarios WHERE email = '" + nombre + "'")
    else:
        # Si no hay nombre, devolver todos los usuarios
        cursor.execute("SELECT id, nombre, email FROM usuarios")

    resultados = cursor.fetchall()
    conn.close()
    return resultados


@app.route("/", methods=['GET', 'POST'])
def buscar_usuario():
    nombre_busqueda = request.form.get('nombre', '') if request.method == 'POST' else ''
    modo = request.form.get('modo')
    usuarios = filtrar_usuarios_por_nombre_de_forma_segura(nombre_busqueda, modo)
    return render_template('usuarios.html', usuarios=usuarios, filtro=nombre_busqueda)

if __name__ == '__main__':
    # Crear una tabla de ejemplo y agregar datos de prueba
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    # Crear la tabla si no existe
    cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, nombre TEXT, email TEXT)")

    # Verificar si ya hay datos en la tabla
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    count = cursor.fetchone()[0]

    # Agregar datos de ejemplo solo si la tabla está vacía
    if count == 0:
        usuarios_ejemplo = [
            ('Juan Pérez', 'juan@ejemplo.com'),
            ('María García', 'maria@ejemplo.com'),
            ('Carlos López', 'carlos@ejemplo.com'),
            ('Ana Martínez', 'ana@ejemplo.com'),
            ('Pedro Rodríguez', 'pedro@ejemplo.com'),
            ('Laura Sánchez', 'laura@ejemplo.com'),
            ('Miguel González', 'miguel@ejemplo.com'),
            ('Sofía Fernández', 'sofia@ejemplo.com')
        ]
        cursor.executemany("INSERT INTO usuarios (nombre, email) VALUES (?, ?)", usuarios_ejemplo)
    conn.commit()
    conn.close()

    app.run(debug=True)
