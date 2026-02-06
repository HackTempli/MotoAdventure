import flet as ft
import database_manager as db

def show_perfil(page: ft.Page):
    # Por ahora simulamos los datos (luego usaremos el ID del usuario logueado)
    nombre_user = "Motero Pro" 
    moto_user = "Honda CB500X"

    txt_nueva_moto = ft.TextField(label="Cambiar mi moto actual", width=300)

    def actualizar_datos(e):
        # Aquí llamaríamos a db.actualizar_moto(user_id, txt_nueva_moto.value)
        page.snack_bar = ft.SnackBar(ft.Text("Perfil actualizado correctamente"))
        page.snack_bar.open = True
        page.update()

    def cerrar_sesion(e):
        # En Flet 2026 para volver al login de forma limpia:
        import login
        page.clean()
        login.show_login(page)

    view = ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=100, color="orange800"),
                ft.Text(nombre_user, size=30, weight="bold"),
                ft.Text(f"Miembro de MotoAdventure", color="grey"),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            
            padding=20
        ),
        ft.Divider(),
        ft.Text("Configuración de Garaje", size=20, weight="bold"),
        ft.Row([
            ft.Icon(ft.Icons.MOTORCYCLE),
            ft.Text(f"Moto actual: {moto_user}", size=16),
        ]),
        txt_nueva_moto,
        ft.ElevatedButton("Guardar Cambios", on_click=actualizar_datos, bgcolor="orange800", color="white"),
        ft.Divider(),
        ft.TextButton("Cerrar Sesión", icon=ft.Icons.LOGOUT, icon_color="red", style=ft.ButtonStyle(color=ft.Colors.RED), on_click=cerrar_sesion)
    ], scroll=ft.ScrollMode.ADAPTIVE, expand=True)

    return view, None