import flet as ft
import os

# Función para ir a registro.py
def on_registro_click(e):
        os.system("python registro.py")

        
# Visualizar el proyecto in life, Dentro de la carpeta del proyecto: flet -r name.py
# Configuracion del container, tamaño y colores.

conteiner = ft.Container(
    ft.Column([
                                                    #Configurar conteiner el Logo.
        ft.Container(                               #Creamos Container para el Texto "Inicar Sesión"                           
            ft.Image(src="images/motoAdventure.png",
                width=100,
                height=100,
                
                
            ),
            
            padding=ft.padding.only(110,15)         # Padding o margenes laterales.
        ),
        
        ft.Container(
                                                    #Configurar Container para Texto
                                                    #Creamos Container para el Texto "Inicar Sesión"                           
            ft.Text("Inicar Sesión",
                width=320,
                size=30,
                text_align="center",
                weight="w900"
            ),
            padding=ft.padding.only(10,1)          # Padding o margenes laterales.
        ),

    
        ft.Container(                               #Contruimos container para Campo Email
            #Container para el campo de Email.
            ft.TextField(
                label="Email",
                width=250,
                height=60,
                hint_text="Email",
                #text_color=("blue"),
                border="underline",
                color="black",
                prefix_icon=ft.Icons.EMAIL,
                
                    #hint_style=ft.Colors.BLACK,
                    #text_style=ft.Colors.BLUE
                
            ),
            padding=ft.padding.only(10,1)
        ),

        ft.Container(        
                                                    #Container para el campo de Password.
            ft.TextField(
                label="Password",
                width=250,
                height=60,
                hint_text="Password",
                border="underline",
                color="black",
                prefix_icon=ft.Icons.LOCK,
                password=True
            ),

            padding=ft.padding.only(10,1)
        ),
        
        ft.Container(
                                            #Contanier para CheckBox de "Recordar Contraseña"
            ft.Checkbox(
                label ="Recordar Password",
                check_color=ft.Colors.BLACK
            ),
            padding=ft.padding.only(70,1)
        ),

        ft.Container(                       #Contruimos container para Boton Iniciar
            ft.ElevatedButton(
                ft.Text("INICIAR"),
                width=280,
                bgcolor="black"

            ),
            padding=ft.padding.only(20,1)

        ),
        #ft.Text("Iniciar sesión con",
        #      text_align="center",
        #      width=320),


        ft.Container(                       #Contruimos container para Iconos.
            ft.Row([
                ft.IconButton(
                    icon=ft.Icons.EMAIL,
                    tooltip="Google",
                    icon_size=20
                ), 
                ft.IconButton(
                    icon=ft.Icons.FACEBOOK,
                    tooltip="Facebook",
                    icon_size=20
                ),
                ft.IconButton(
                    icon=ft.Icons.PADDING_ROUNDED,
                    tooltip="Instagram",
                    icon_size=20
                )    
            ],
            alignment=ft.MainAxisAlignment.CENTER 
            ),
            padding=ft.padding.only(1,1)
        ),
        ft.Container(
            ft.Row([
                ft.Text("¿No tiene una cuenta?"),
                ft.TextButton("Crear Cuenta", on_click=on_registro_click
                ),
             ],
            alignment=ft.MainAxisAlignment.CENTER
            ),
            padding=ft.padding.only(1,1)
        )

    ],
    alignment=ft.MainAxisAlignment.CENTER       #Alinea la Columna
    ),    
    
    border_radius=20,
    width=320,
    height=500,
    gradient= ft.LinearGradient([
        ft.Colors.RED,
        ft.Colors.ORANGE_800,
        ft.Colors.ORANGE_600
    ])
)


def main(page: ft.Page):

    #Muestra por pantalla el conteiner y su configuracion.
    page.bgcolor="BLACK"
    page.vertical_alignment="center"
    page.horizontal_alignment="center"

    page.add(conteiner)


ft.run(main)
