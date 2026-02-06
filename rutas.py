import flet as ft

def show_rutas(page: ft.Page):
    # Lista de rutas (esto vendría de tu SQLite en el futuro)
    rutas_data = [
        {"nombre": "Ruta Transpirenaica", "desc": "Curvas infinitas por el Pirineo.", "url": "https://www.boxrepsol.com/es/vive-tu-moto/la-ruta-transpirenaica-en-moto/"},
        {"nombre": "Sierra de Gredos", "desc": "Paisajes increíbles y buen asfalto.", "url": "https://tusguiasdeviaje.com/tus-rutas-en-moto-con-kambo-sierra-de-gredos-norte/"},
    ]

    def abrir_ruta(url):
        page.launch_url(url) # Abre Google Maps en una pestaña nueva


    lista_rutas = ft.ListView(expand=True, spacing=15)
        
    for r in rutas_data:
        # CREAMOS UN CONTENEDOR PARA DARLE EL ESTILO (Bordes y Fondo)
        tarjeta_ruta = ft.Container(
            content=ft.ListTile(
                leading=ft.Icon(ft.Icons.MAP_OUTLINED, color="orange800"),
                title=ft.Text(r["nombre"], weight="bold", color="blue"),
                subtitle=ft.Text(r["desc"], size=12, color="orange"),
                trailing=ft.IconButton(
                    icon=ft.Icons.EXPLORE,
                    icon_color="orange800",
                    on_click=lambda e, u=r["url"]: abrir_ruta(u)
                ),
            ),
            bgcolor=ft.Colors.WHITE, # Fondo para que resalte
            border_radius=15,        # Aquí sí funciona el border_radius
            padding=5,
            shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12)
        )
        lista_rutas.controls.append(tarjeta_ruta)
             

    view = ft.Column([
        ft.Text("Rutas Recomendadas", size=25, weight="bold", color="orange800"),
        ft.Text("Explora las mejores curvas con Google Maps", size=12, color="grey"),
        ft.Divider(),
        lista_rutas
    ], expand=True)

    return view, None # No necesita botón flotante por ahora

