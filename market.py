import flet as ft
import database_manager as db  # Importamos nuestro gestor de datos
import componentes as comp     # Importamos nuestras tarjetas visuales

def show_market(page: ft.Page):

    # 1. Definir la lógica de respuesta para la imagen
    def on_file_result(e):
        if e.files:
            # En modo local/escritorio guardamos la ruta del archivo
            ruta_imagen.value = e.files[0].path
            btn_imagen.text = "Imagen Seleccionada ✅"
            btn_imagen.icon = ft.Icons.CHECK
            page.update()


    # 2. CREACIÓN GARANTIZADA: No usamos next() para evitar el NoneType
    # Buscamos si ya existe, si no, lo creamos de forma segura
    file_picker = None
    for control in page.overlay:
        if isinstance(control, ft.FilePicker):
            file_picker = control
            break

    # Si NO existe, lo creamos primero
    if file_picker is None:
        file_picker = ft.FilePicker()
        page.overlay.append(file_picker)
        page.update() # Forzamos que el control se registre
    
    # AHORA que estamos seguros de que NO es None, asignamos el evento
    file_picker.on_result = on_file_result


    # 3. Título de la sección. Elementos del Interfaz
    header = ft.Container(
        content=ft.Row([
            ft.Text("MotoMarket", size=30, weight="bold", color="orange800"),
            ft.IconButton(icon=ft.Icons.FILTER_LIST, tooltip="Filtrar")
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=20
    )

    # Variable para guardar la ruta de la imagen seleccionada
    ruta_imagen = ft.Text("", visible=False)

    
    btn_imagen = ft.ElevatedButton(
        "Seleccionar Foto", 
        icon=ft.Icons.IMAGE, 
        on_click=lambda _: file_picker.pick_files(allow_multiple=False)
    )
    
    # --- CAMPOS DEL FORMULARIO ---
    txt_titulo = ft.TextField(label="¿Qué vendes?", border="underline")
    txt_descripcion = ft.TextField(label="Descripción detallada", multiline=True, min_lines=3, max_lines=5, border="outline")
    txt_precio = ft.TextField(label="Precio (€)", keyboard_type=ft.KeyboardType.NUMBER, border="underline") #Abre el Teclado númerico en móbiles.
    txt_telefono = ft.TextField(label="Teléfono de contacto", border="underline")
    dropdown_categoria = ft.Dropdown(
        label="Categoría",
        options=[
            ft.dropdown.Option("Motos"),
            ft.dropdown.Option("Equipamiento"),
            ft.dropdown.Option("Recambios"),
        ],
    
    )
    # 4. Función para guardar los datos del Formulario
    def guardar_click(e):
        if not txt_titulo.value or not txt_precio.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, rellena los campos básicos"))
            page.snack_bar.open = True
            page.update()
            return

        # Guardar en BD
        # En guardar_click, mejor usar el orden posicional:
        db.guardar_nuevo_anuncio(
            1,                        # user_id
            txt_titulo.value,         # titulo
            txt_descripcion.value,    # descripcion
            float(txt_precio.value),  # precio
            dropdown_categoria.value, # categoria
            ruta_imagen.value,        # imagen_url
            txt_telefono.value        # telefono
        )
        
        # Cerrar formulario y limpiar
        bs_market.open = False
        txt_titulo.value = ""
        txt_descripcion.value = ""
        txt_precio.value = ""
        ruta_imagen.value = ""
        btn_imagen.text = "Seleccionar Foto"
        txt_telefono.value = ""
        
        # Refrescar la lista de anuncios
        cargar_datos()
        page.update()

    # --- DISEÑO DEL FORMULARIO (BottomSheet) ---
    bs_market = ft.BottomSheet(
        ft.Container(
            padding=20,
            content=ft.Column([
                ft.Text("Publicar Nuevo Anuncio", size=20, weight="bold"),
                txt_titulo,
                txt_descripcion,
                ft.Row([txt_precio, txt_telefono]),
                dropdown_categoria,
                btn_imagen, # Botón para añaduir la Imagen
                ft.ElevatedButton("PUBLICAR ANUNCIO", on_click=guardar_click, bgcolor="orange800", color="white"),
            ], tight=True, spacing=20),
        ),
    )

     # Lo añadimos al overlay (home.py ya se encargó de limpiar el anterior)
    page.overlay.append(bs_market)
    
    # Evitar duplicar el BottomSheet
    # existing_bs = next((c for c in page.overlay if isinstance(c, ft.BottomSheet)), None)
    # if not existing_bs:
    #     page.overlay.append(bs_market)
    # else:
    #     bs_market = existing_bs # Reutilizamos el existente si ya estaba

    # 6. Botón Flotante para añadir anuncio
    btn_añadir = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        bgcolor="orange800",
        on_click=lambda _: (setattr(bs_market, "open", True), page.update(),
                            print("Abrir formulario de nuevo anuncio"))
    )

    # 5. Creamos la cuadrícula (GridView)
    # "runs_count" define cuántas columnas queremos. 
    # En móvil pondremos 2, en web Flet lo ajustará si usamos 'expand'.
    grid_anuncios = ft.GridView(
        expand=True,
        runs_count=2,               # 2 columnas por defecto
        max_extent=200,             # Ancho máximo de cada tarjeta antes de crear otra columna
        child_aspect_ratio=0.75,    # Proporción de la tarjeta (más alta que ancha)
        spacing=10,
        run_spacing=10,
    )

    # 6. Función para cargar anuncios desde la base de datos
    def cargar_datos():
        grid_anuncios.controls.clear()
        lista_anuncios = db.obtener_anuncios() # Llamamos al Gestor de BD

        if not lista_anuncios:
            # Si no hay anuncios, mostramos un mensaje
            grid_anuncios.controls.append(
                ft.Text("Aún no hay anuncios. ¡Sé el primero!", color="grey")
            )
        else:
            for anuncio in lista_anuncios:
                # El orden según nuestro SELECT en db_manager:
                # 0:titulo, 1:precio, 2:imagen, 3:vendedor, 4:categoria
                grid_anuncios.controls.append(
                    comp.CardAnuncio(
                        titulo=anuncio[0],
                        precio=anuncio[1],
                        imagen_url=anuncio[2],
                        vendedor=anuncio[3],
                        categoria=anuncio[4]
                    )
                )
                
        page.update()

    


    # Cargamos los datos inicialmente
    cargar_datos()


    # 7. Construcción de la vista
    # Usamos una Column para poner el Header arriba y el Grid abajo
    view = ft.Column([
        header,
        ft.Divider(height=1, color="grey300"),
        ft.Container(content=grid_anuncios, expand=True, padding=10)
    ], expand=True)

    return view, btn_añadir
