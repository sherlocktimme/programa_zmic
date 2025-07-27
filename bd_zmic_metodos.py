import sqlite3

DB_NAME = "estudio.db"

# -------------------------------
# CONEXIÓN Y CREACIÓN DE TABLAS
# -------------------------------
def crear_tablas():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Tabla de usuarios
    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL
    )
    """)

    # Tabla de temas
    cur.execute("""
    CREATE TABLE IF NOT EXISTS temas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL
    )
    """)

    # Tabla de preguntas
    cur.execute("""
    CREATE TABLE IF NOT EXISTS preguntas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        texto TEXT NOT NULL,
        tema_id INTEGER,
        dificultad INTEGER CHECK(dificultad BETWEEN 1 AND 3),
        FOREIGN KEY (tema_id) REFERENCES temas(id)
    )
    """)

    # Tabla de opciones (multiple choice)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS opciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        texto TEXT NOT NULL,
        pregunta_id INTEGER,
        es_correcta INTEGER CHECK(es_correcta IN (0,1)),
        FOREIGN KEY (pregunta_id) REFERENCES preguntas(id)
    )
    """)

    # Tabla de progreso
    cur.execute("""
    CREATE TABLE IF NOT EXISTS progreso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        tema_id INTEGER,
        puntaje INTEGER DEFAULT 0,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY (tema_id) REFERENCES temas(id),
        UNIQUE(usuario_id, tema_id)
    )
    """)

    conn.commit()
    conn.close()

# -------------------------------
# FUNCIONES DE BASE DE DATOS
# -------------------------------

def obtener_usuario(nombre):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id FROM usuarios WHERE nombre = ?", (nombre,))
    resultado = cur.fetchone()

    if resultado:
        usuario_id = resultado[0]
    else:
        cur.execute("INSERT INTO usuarios (nombre) VALUES (?)", (nombre,))
        usuario_id = cur.lastrowid
        conn.commit()

    conn.close()
    return usuario_id

def agregar_tema(nombre):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO temas (nombre) VALUES (?)", (nombre,))
        conn.commit()
        print("✅ Tema agregado.")
    except sqlite3.IntegrityError:
        print("⚠️ El tema ya existe.")
    conn.close()

def obtener_temas():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, nombre FROM temas")
    temas = cur.fetchall()
    conn.close()
    return temas

def agregar_pregunta(texto, tema_id, dificultad, opciones, correcta):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO preguntas (texto, tema_id, dificultad) VALUES (?, ?, ?)
    """, (texto, tema_id, dificultad))
    pregunta_id = cur.lastrowid

    for opcion in opciones:
        es_correcta = 1 if opcion == correcta else 0
        cur.execute("""
            INSERT INTO opciones (texto, pregunta_id, es_correcta) VALUES (?, ?, ?)
        """, (opcion, pregunta_id, es_correcta))

    conn.commit()
    conn.close()

def obtener_preguntas_por_tema(tema_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id, p.texto, p.dificultad FROM preguntas p
        WHERE p.tema_id = ?
    """, (tema_id,))
    preguntas = cur.fetchall()
    conn.close()
    return preguntas

def obtener_opciones(pregunta_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT texto, es_correcta FROM opciones
        WHERE pregunta_id = ?
    """, (pregunta_id,))
    opciones = cur.fetchall()
    conn.close()
    return opciones

def actualizar_puntaje(usuario_id, tema_id, puntos):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO progreso (usuario_id, tema_id, puntaje)
        VALUES (?, ?, ?)
        ON CONFLICT(usuario_id, tema_id)
        DO UPDATE SET puntaje = puntaje + excluded.puntaje
    """, (usuario_id, tema_id, puntos))
    conn.commit()
    conn.close()

def obtener_puntaje(usuario_id, tema_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT puntaje FROM progreso
        WHERE usuario_id = ? AND tema_id = ?
    """, (usuario_id, tema_id))
    resultado = cur.fetchone()
    conn.close()
    return resultado[0] if resultado else 0
