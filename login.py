import flet as ft
import sqlite3
from flet import Alignment
import database_manager as db #Importamos el Gestor de la Base de Datos.
import os # Importamos la librería OS para gestionar rutas
import time # Añadimos time para un pequeño retraso de seguridad

# --- Configuración de la ruta absoluta de la base de datos ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "login.db")


# 1. Definiciones de funciones de apoyo (Helpers)
# Función de respuesta global (fuera de show_login)
def on_file_result_global(e):
    # Esto es solo un placeholder, la lógica real estará en market.py
    pass 

# Función para verificar si el usuario existe en la BD.
def verificar_usuario(email, password):
    #Conecta con la BD.
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print("Conectando con la Base de Datos")

    #Consultar la
    # 
    # 
    #  base de Datos.
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = cursor.fetchone()

    #Cerrar la conexión
    conn.close()

    return user is not None


def mostrar_mensaje_sistema(page: ft.Page, titulo, mensaje):
    if page.web:
        # --- LÓGICA PARA WEB (SnackBar) ---
        # El navegador no permite abrir ventanas de Tkinter, usamos SnackBar
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"{titulo}: {mensaje}", color="white"),
                bgcolor=ft.Colors.RED_700 if "Error" in titulo else ft.Colors.GREEN_700,
                duration=4000)
            page.snack_bar.open = True
            
    else:
        # --- LÓGICA PARA ESCRITORIO (Tkinter) ---
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.withdraw()  # Oculta la ventana principal de Tkinter
            root.attributes("-topmost", True)  # Asegura que salga al frente
            
            if "Error" in titulo:
                messagebox.showerror(titulo, mensaje)
            else:
                messagebox.showinfo(titulo, mensaje)
            root.destroy()
        except ImportError:
            # Caso de seguridad si Tkinter no está instalado en el sistema
            print(f"{titulo}: {mensaje}")

    page.update()


# 2. Configuración pagina de inicio de sesion. Vistas de la App
def show_registro(page):
    #Importación local para evitar importaciones circulares.
    import registro
    # Configuración de la página de registro
    registro.show_registro(page) #Llama a la función Registro de forma asincrona

def iniciar_sesion(page, email_field, password_field):
    # Obtener el valor del campo de email y contraseña
    email = email_field.value  # Obtener el valor del campo de email
    password = password_field.value  # Obtener el valor del campo de contraseña

     # Validación básica de campos vacíos antes de consultar la BD
    if not email or not password:
        # IMPORTANTE: Se añade 'page' como primer argumento
        mostrar_mensaje_sistema(page, "Error", "Por favor, rellena todos los campos")
        return

    # Verificar si el usuario existe en la base de datos
    if verificar_usuario(email, password):
        print("Estás Dentro")
        # IMPORTANTE: Se añade 'page' como primer argumento
        mostrar_mensaje_sistema(page, "Éxito", "Bienvenido a MotoAdventure")

        import home
        home.show_home(page)
    else:
        print("Usuario no encontrado o contraseña incorrecta")
        # IMPORTANTE: Se añade 'page' como primer argumento
        mostrar_mensaje_sistema(page, "Error", "Error en el Usuario o Password")



def show_login(page: ft.Page):
    page.clean()
    
    page.bgcolor = "BLACK"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

                                                 
       
    # Construcción del contenedor de inicio de sesión
    email_field = ft.TextField(
        label="Email",
        width=250,
        height=60,
        hint_text="Email",
        border="underline",
        color="black",
        prefix_icon=ft.Icons.EMAIL
    )

    password_field = ft.TextField(
        label="Password",
        width=250,
        height=60,
        hint_text="Password",
        border="underline",
        color="black",
        prefix_icon=ft.Icons.LOCK,
        password=True,
        can_reveal_password=True
    )
    
    conteiner = ft.Container(
        content=ft.Column([
             ft.Container(
                 ft.Image(src="images/motoAdventure.png",width=150,height=150),
                 alignment=Alignment(0, 0),
                 padding=ft.padding.only(top=20)         # Padding o margenes laterales.

            ),
        
            ft.Container(
                ft.Text("Iniciar Sesión",
                    width=320,
                    size=30,
                    text_align="center",
                    weight="w900"
                ),
                padding=ft.padding.only(10, 20)
            ),

            ft.Container(email_field, padding=ft.padding.only(10, 1)),
            ft.Container(password_field, padding=ft.padding.only(10, 1)),

            ft.Container(
                ft.ElevatedButton(
                    content=ft.Text("INICIAR"),
                    width=280,
                    bgcolor="black",
                    on_click=lambda e: iniciar_sesion(page, email_field, password_field)    #Pasa los campos a la función.
                ),
                alignment=Alignment(0, 0),
                padding=ft.padding.only(20,10)
            ),
            ft.Container(
                ft.Row([
                    ft.Text("¿No tiene una cuenta?", color="black"),
                    ft.TextButton("Crear Cuenta", style=ft.ButtonStyle(color=ft.Colors.BLUE_900),
                                   on_click=lambda e: show_registro(page)),  # Cambia a registro
                ],
                alignment=ft.MainAxisAlignment.CENTER
                ),
                
                padding=ft.padding.only(1, 1)
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        border_radius=20,
        width=320,
        height=600,
        gradient=ft.LinearGradient([
            ft.Colors.RED,
            ft.Colors.ORANGE_700,
            ft.Colors.ORANGE_400
        ])
    )

    page.add(conteiner)

# 3. Función Principal (Punto de entrada)
async def main(page: ft.Page):

    # Inicializar o crea la Base de Datos primero
    db.inicializar_tablas()

    # Configuraciones de página estándar
    page.title = "MotoAdventure"
    #page.update()

    #Pequeña pausa técnica (0.1s es suficiente) para que el navegador registre el control
    time.sleep(0.3)

    #Llama a la función Show_login
    show_login(page)  # Muestra la página de inicio de sesión al iniciar

# Asegurarnos de que la carpeta 'assets' exista para las imágenes
if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")

