import sqlite3
import os

# Ruta absoluta para que funcione en cualquier parte
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "login.db")

def ejecutar_consulta(query, params=(), fetch=False):
    """Función genérica para manejar la conexión y consultas."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        if fetch:
            resultado = cursor.fetchall()
            return resultado
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error en la BD: {e}")
    finally:
        conn.close()

def inicializar_tablas():
    """Crea TODAS las tablas de la App en una sola llamada."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabla de Usuarios (ya la tenías, añadimos moto_actual)
    ejecutar_consulta("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            moto_actual TEXT
        )
    """)
    
    # Tabla de Anuncios del Marketplace
    ejecutar_consulta("""
        CREATE TABLE IF NOT EXISTS anuncios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL,
            categoria TEXT,
            imagen_url TEXT,
            telefono TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    print("Base de datos sincronizada correctamente.")

     # Tabla Publicaciones (Feed Social) - NUEVA
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS publicaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            imagen_url TEXT,
            descripcion TEXT,
            moto_actual TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()
    print("Tablas sincronizadas: users, anuncios, publicaciones.")



# Funciones específicas para el Marketplace
def guardar_nuevo_anuncio(user_id, titulo, descripcion, precio, categoria, imagen_url, telefono):
    # Por ahora usamos user_id = 1 hasta que implementemos sesiones globales
    query = """
        INSERT INTO anuncios (user_id, titulo, descripcion, precio, categoria, imagen_url, telefono) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    ejecutar_consulta(query, (user_id, titulo, descripcion, precio, categoria, imagen_url, telefono))

def obtener_anuncios():
    # Esta consulta trae el anuncio y el nombre del vendedor (JOIN)
    query = """
        SELECT a.titulo, a.precio, a.imagen_url, u.nombre, a.categoria, a.descripcion, a.telefono
        FROM anuncios a
        JOIN users u ON a.user_id = u.id
        ORDER BY a.id DESC
    """
    return ejecutar_consulta(query, fetch=True)

# Unimos con 'users' para saber quién publicó la foto
def obtener_feed():
    
    query = """
        SELECT p.imagen_url, p.descripcion, u.nombre, p.fecha, u.moto_actual
        FROM publicaciones p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.id DESC
    """
    return ejecutar_consulta(query, fetch=True)

# Se crea publicacion de Feed
def crear_publicacion(user_id, imagen, descripcion):
    query = "INSERT INTO publicaciones (user_id, imagen_url, descripcion) VALUES (?, ?, ?)"
    ejecutar_consulta(query, (user_id, imagen, descripcion))

def guardar_publicacion(user_id, imagen, descripcion):
    query = """
        INSERT INTO publicaciones (user_id, imagen_url, descripcion) 
        VALUES (?, ?, ?)
    """
    # Usamos user_id=1 por ahora (luego lo haremos dinámico)
    ejecutar_consulta(query, (user_id, imagen, descripcion))
