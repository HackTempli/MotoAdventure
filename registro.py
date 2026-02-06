import flet as ft
from flet import Alignment
import sqlite3
import os # Importamos la librería OS para gestionar rutas

# --- Configuración de la ruta absoluta de la base de datos ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "login.db")

#Funcion para crear la bade de datos
def create_database():
      conn = sqlite3.connect(DB_PATH)
      cursor = conn.cursor()

      
      #Crea la Tabla si no existe
      cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            moto_actual TEXT
        )
    """)

      conn.commit()
      conn.close()

create_database()

#Registra datos en la BD
def register_user(nombre, email, password, moto_actual):
      conn= sqlite3.connect(DB_PATH)
      cursor = conn.cursor()

      #Inserta los datos en la Tabla.
      try:
            cursor.execute("INSERT INTO users (nombre, email, password, moto_actual) VALUES (?, ?, ?, ?)", (nombre, email, password, moto_actual))
            conn.commit()
            print(f"DEBUG: Usuario {email} registrado exitosamente.")
            return True             #Registro correcto
      except sqlite3.IntegrityError:
            print(f"DEBUG: Error de integridad, el email {email} ya existe.")
            return False            #El email ya existe
      finally:
            conn.close()

# Limpia pagina actual
def on_login_click(page):
    import login
    # Limpia la página actual
    page.clean()
    login.show_login(page)


#Funcion Registro
# Función de registro
def on_register_click(page, nombre_field, email_field, password_field, moto_field):
    nombre = nombre_field.value
    email = email_field.value
    password = password_field.value
    moto_actual = moto_field.value

    # Función auxiliar rápida para Tkinter
    def lanzar_mensaje(titulo, mensaje, tipo="Info"):
         
        if page.web:
        # Si es WEB, usamos el SnackBar de Flet
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"{titulo}: {mensaje}"),
                bgcolor=ft.Colors.RED_700 if tipo=="error" else ft.Colors.GREEN_700
            )
            page.snack_bar.open = True
            page.update()
        else:
        # Si es ESCRITORIO, usamos tu solución de Tkinter que ya funciona
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            if tipo == "error":
                messagebox.showerror(titulo, mensaje)
            else:
                messagebox.showinfo(titulo, mensaje)
            root.destroy()


    if not nombre or not email or not password or not moto_actual:
        # Mensaje de campos vacíos
        lanzar_mensaje("Error de Validación", "Por favor, complete todos los campos.", "error")
        return # Salimos de la función para que no intente registrar
        
    elif register_user(nombre, email, password, moto_actual):
        # ÉXITO: Registro correcto
        lanzar_mensaje("Registro Completado", "¡Tu cuenta ha sido registrada exitosamente!")
        

        # Limpiamos los campos tras el registro exitoso
        nombre_field.value = ""
        email_field.value = ""
        password_field.value = ""
        moto_field.value = ""
        page.update()

         # Redirigir al login tras el éxito
        on_login_click(page)
                
                
    else:
        # ERROR: El email ya existe
        lanzar_mensaje("Error", "Este Email ya está registrado", "error")
    
     # Actualiza la página para mostrar el diálogo
    
      
def show_registro(page: ft.Page):
    page.clean()
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Definición de los campos del formulario
    nombre_field = ft.TextField(width=250, height=60, hint_text="Nombre", border="underline", color="black", prefix_icon=ft.Icons.PERSON)
    email_field = ft.TextField(label="Email", width=250, height=60, hint_text="Email", border="underline", color="black", prefix_icon=ft.Icons.EMAIL)
    password_field = ft.TextField(label="Password", width=250, height=60, hint_text="Password", border="underline", color="black", prefix_icon=ft.Icons.LOCK, password=True, can_reveal_password=True)
    moto_field = ft.TextField(label="¿Qué Moto tienes?", width=250, height=60, hint_text="Moto", border="underline", color="black", prefix_icon=ft.Icons.MOTORCYCLE)
#Configurar conteiner el Logo.
    conteiner = ft.Container(
        content=ft.Column([
             #Para el Logo
            ft.Container(
                content=ft.Image(src="images/motoAdventure.png", width=100, height=100),
                #content=ft.Icon(ft.Icons.APP_REGISTRATION, size=70, color="black"),         # Reemplazo por un icono si la imagen falla
                alignment=Alignment(0, 0),
                padding=ft.padding.only(top=15)
            ),
                    
            # Creamos Título "Inicar Sesión"                                                                                                                                     
            ft.Text("Registrar Cuenta", width=300, size=22, text_align="center", weight="w900"),
                
            # Campos de Registro
            ft.Container(nombre_field, padding=ft.padding.only(10,2)),  #Contruimos container para Campo Nombre
            ft.Container(email_field, padding=ft.padding.only(10,2)),   #Contruimos container para Campo Email                                     
            ft.Container(password_field, padding=ft.padding.only(10,2)),#Container para el campo de Password.
            ft.Container(moto_field, padding=ft.padding.only(10,2)),    #Container para el campo de Moto.

            
            #Contruimos container para Boton Registrar.
            ft.Container(                       
            
                content=ft.ElevatedButton(
                    "REGISTRAR",
                    width=250,
                    bgcolor="black",
                    on_click=lambda e: on_register_click(
                        page,                  #Pasa la página actual
                        nombre_field,  # Accede al valor del campo Nombre
                        email_field,   # Accede al valor del campo Email
                        password_field,  # Accede al valor del campo Password
                        moto_field  # Accede al valor del campo Password
                    )
                ),
                alignment=Alignment(0, 0),
                padding=ft.padding.only(top=15)

            ),
            # Contenedor para el texto y botón "Login"
            ft.Container(
                content=ft.Row([
                    ft.Text("Ya tengo cuenta", color="black"),
                    ft.TextButton("Login", style=ft.ButtonStyle(color=ft.Colors.BLACK), on_click= lambda e: on_login_click(page)),
                ],
                alignment=ft.MainAxisAlignment.CENTER),
                padding=ft.padding.only(bottom=15)
                
            )
        ],



        #Alinea la Columna
        alignment=ft.MainAxisAlignment.CENTER, 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.ADAPTIVE # <--- Esto permite hacer scroll si no cabe
        ),
            
        
        #establece colores de Background Gradiente
        border_radius=20,
        width=320,
        height=600,
        gradient= ft.LinearGradient([
            ft.Colors.RED,
            ft.Colors.ORANGE_800,
            ft.Colors.ORANGE_600
        ])
    )

    page.add(conteiner)
    page.update()



