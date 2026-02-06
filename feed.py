import flet as ft
import database_manager as db
import componentes as comp


# Contenedor de la lista de publicaciones
def show_feed(page: ft.Page):

     # --- LÓGICA DE IMAGEN (Reutilizando el FilePicker global) ---
    ruta_imagen = ft.Text("", visible=False)

    def on_file_result(e):
        if e.files and len(e.files) > 0:
            ruta_imagen.value = e.files[0].path
            btn_imagen.text = "Foto de ruta lista ✅"
            btn_imagen.update()

    # Recuperamos el FilePicker que inyectamos en main
    file_picker = next((c for c in page.overlay if isinstance(c, ft.FilePicker)), None)
    if not file_picker:
        file_picker = ft.FilePicker(on_result=on_file_result)
        page.overlay.append(file_picker)
    else:
        file_picker.on_result = on_file_result

    # --- CAMPOS DEL FORMULARIO ---
    txt_desc = ft.TextField(
        label="¿Qué tal la ruta?", 
        multiline=True, 
        min_lines=3,
        hint_text="Describe tu aventura motera..."
    )
    
    btn_imagen = ft.ElevatedButton(
        "Añadir Foto de la Ruta",
        icon=ft.Icons.CAMERA_ALT,
        on_click=lambda _: file_picker.pick_files(allow_multiple=False)
    )

    def guardar_aventura(e):
        if not txt_desc.value:
            page.snack_bar = ft.SnackBar(ft.Text("Escribe una descripción"))
            page.snack_bar.open = True
            page.update()
            return

        # Guardar en BD (user_id=1 temporalmente)
        db.guardar_publicacion(1, ruta_imagen.value, txt_desc.value)
        
        # Limpiar y cerrar
        bs_feed.open = False
        txt_desc.value = ""
        ruta_imagen.value = ""
        btn_imagen.text = "Añadir Foto de la Ruta"
        
        cargar_publicaciones()
        page.update()

    # --- BOTTOM SHEET ---
    # Buscamos si ya hay un BottomSheet de "Aventura" para no duplicar

    bs_feed = ft.BottomSheet(
        ft.Container(
            padding=20,
            content=ft.Column([
                ft.Text("Nueva Aventura", size=20, weight="bold"),
                txt_desc,
                btn_imagen,
                ft.ElevatedButton(
                    "COMPARTIR", 
                    on_click=guardar_aventura, 
                    bgcolor="orange800", 
                    color="white",
                    width=400
                )
            ], tight=True, spacing=20)
        )
    )

    if bs_feed not in page.overlay:    
        page.overlay.append(bs_feed)

            
    btn_nueva = ft.FloatingActionButton(
        icon=ft.Icons.FEED,
        bgcolor="orange800",
        on_click=lambda _: (setattr(bs_feed, "open", True), page.update(),
                            print("Abrir formulario de nuevo FEED"))
    )
    page.update()


    lista_feed = ft.ListView(expand=True, spacing=20, padding=10)

    def cargar_publicaciones():
        lista_feed.controls.clear()
        posts = db.obtener_feed()
        if not posts:
            lista_feed.controls.append(
                ft.Container(
                content=ft.Text("No hay aventuras aún. ¡Sé el primero en publicar!", italic=True),
                alignment=ft.Alignment(0, 0),
                padding=50
                )
            )
        else:
            for p in posts:
                # p, p, p, p, p
                lista_feed.controls.append(
                    comp.CardFeed(usuario=p[2],
                                  moto_actual= p[4],
                                  imagen= p[0],
                                  descripcion= p[1],
                                  fecha= p[3])
                      
                )
        page.update()

         # --- BOTÓN FLOTANTE (Referencia directa al objeto BS) ---
    def abrir_form(e):
        bs_feed.open = True
        page.update()

    # Botón flotante para subir una nueva aventura
    btn_nueva_aventura = ft.FloatingActionButton(
        icon=ft.Icons.ADD_A_PHOTO,
        bgcolor=ft.Colors.ORANGE_800,
        on_click=abrir_form
        #print("Abrir formulario de publicación")
    )

    cargar_publicaciones()

    view = ft.Column([
        ft.Text("Aventuras de la Comunidad", size=25, weight="bold", color="orange800"),
        ft.Divider(),
        lista_feed
    ], expand=True)

    return view, btn_nueva_aventura