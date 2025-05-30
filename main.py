from flask import Flask, request, render_template, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret_key_muy_segura'

def coneccion_a_base_de_datos():
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')

        conn = coneccion_a_base_de_datos()
        user = conn.execute('SELECT * FROM usuarios WHERE usuario = ? AND password = ?', (usuario, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['nombre']
            return redirect(url_for('notas'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Notes routes
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('notas'))

@app.route('/notas')
def notas():
    busqueda = request.args.get('buscar', '')

    conn = coneccion_a_base_de_datos()


    if busqueda:
        # Si hay un término de búsqueda, filtramos por contenido
        notas = conn.execute(
            f"SELECT id, titulo, contenido, fecha_creacion FROM notas WHERE usuario_id = {session['user_id']} AND contenido LIKE '%{busqueda}%' ORDER BY fecha_creacion DESC"
        ).fetchall()
    else:
        # Si no hay término de búsqueda, mostramos todas las notas
        notas = conn.execute(f"SELECT * FROM notas WHERE usuario_id = {session['user_id']} ORDER BY fecha_creacion DESC").fetchall()

    conn.close()

    return render_template('notas.html', notas=notas)

@app.route('/notas/nueva', methods=['GET', 'POST'])
def nueva_nota():

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        contenido = request.form.get('contenido')

        conn = coneccion_a_base_de_datos()
        conn.executescript(f"INSERT INTO notas (usuario_id, titulo, contenido) VALUES ('{session['user_id']}', '{titulo}', '{contenido}')")
        conn.commit()
        conn.close()

        return redirect(url_for('notas'))

    return render_template('crear_notas.html')

@app.route('/notas/<int:id>/eliminar', methods=['POST'])
def eliminar_nota(id):

    conn = coneccion_a_base_de_datos()
    conn.execute('DELETE FROM notas WHERE id = ? AND usuario_id = ?', (id, session['user_id']))
    conn.commit()
    conn.close()

    return redirect(url_for('notas'))

def init_db():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS notas")
    cursor.execute("DROP TABLE IF EXISTS usuarios")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY, 
        nombre TEXT NOT NULL, 
        usuario TEXT UNIQUE NOT NULL, 
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notas (
        id INTEGER PRIMARY KEY,
        titulo TEXT NOT NULL,
        contenido TEXT NOT NULL,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        usuario_id INTEGER,
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
    )
    """)

    usuarios_ejemplo = [
        ('Luciano Martínez', 'luciano', 'luciano123'),
        ('Lucio Rivas', 'lucio', 'lucio123'),
        ('Máximo Ponce', 'maximo', 'maximo123'),
        ('Santiago Rodriguez', 'santiago', 'santiago123')
    ]
    cursor.executemany("INSERT INTO usuarios (nombre, usuario, password) VALUES (?, ?, ?)", usuarios_ejemplo)

    notas_ejemplo = [
        ('Primera nota', 'Contenido de mi primera nota', 1),
        ('Lista de compras', 'Leche, pan, huevos', 1),
        ('Recordatorio', 'Llamar al médico mañana', 2),
        ('Ideas para proyecto', 'Implementar autenticación de usuarios', 3)
    ]
    cursor.executemany("INSERT INTO notas (titulo, contenido, usuario_id) VALUES (?, ?, ?)", notas_ejemplo)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
