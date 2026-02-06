import flet as ft
import market   # Importamos el módulo del Marketplace.

def show_home(page: ft.Page):
    page.clean()
    page.title = "MotoAdventure - Comunidad"
    
    # 1. Cuerpo de la aplicación (donde cargaremos cada sección)
    # Contenedor donde se cargará el contenido de cada sección.
    container_principal = ft.Container(expand=True, padding=20)

    # 2. Función para cambiar de vista
    async def change_view(e):
        # e.control.selected_index nos dice qué icono se pulsó (0, 1, 2 o 3)
        index = e.control.selected_index

        # Limpiamos el botón flotante por defecto (lo activaremos solo en Market)
        page.floating_action_button = None

        # --- LIMPIEZA SELECTIVA (CORREGIDO) ---
        # Solo removemos los BottomSheets. 
        # NO usamos page.overlay.clear() porque borra el FilePicker y rompe la App.
        # Usamos una lista temporal para evitar errores de iteración
        for control in page.overlay[:]: 
            if isinstance(control, ft.BottomSheet):
                page.overlay.remove(control)

        page.update()

        #Botones de las opciones con los indices.
        try:
            if index == 0:
                # CARGAMOS EL FEED
                import importlib
                import feed
                importlib.reload(feed) # Esto fuerza a Python a leer los cambios del archivo
                vista_feed, boton_feed = feed.show_feed(page)
                container_principal.content = vista_feed
                page.floating_action_button = boton_feed

            elif index == 1:
                # CARGAMOS EL MARKETPLACE con manejo de errores
                import importlib
                import market
                importlib.reload(market) # Esto fuerza a Python a leer los cambios del archivo
                vista_market, boton_market = market.show_market(page)
                container_principal.content = vista_market
                page.floating_action_button = boton_market

            elif index == 2:
                import rutas
                vista, boton = rutas.show_rutas(page)
                container_principal.content = vista

            elif index == 3:
                import perfil
                vista, boton = perfil.show_perfil(page)
                container_principal.content = vista
            
                
        except Exception as ex:
            # Si algo falla (como el FilePicker), mostramos el error sin romper el menú
            print(f"Error al cambiar de vista: {ex}")
            container_principal.content = ft.Column([
                ft.Icon(ft.Icons.ERROR_OUTLINE, color="red", size=50),
                ft.Text(f"Error al cargar la sección: {ex}", color="red")
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        # 3. Actualizar la página al final
        page.update()


# 1. Aplicamos el color azul mediante el TEMA de la página (Evita errores de argumentos)
    page.theme = ft.Theme(
        navigation_rail_theme=ft.NavigationRailTheme(
            bgcolor=ft.Colors.BLUE_900,
            indicator_color=ft.Colors.BLUE_400,
            unselected_label_text_style=ft.TextStyle(color=ft.Colors.WHITE70),
            selected_label_text_style=ft.TextStyle(color=ft.Colors.WHITE),
            # En versiones recientes, el color del icono se hereda del estilo del texto o del icono directamente
        )
    )

# Tu NavigationRail (Barra lateral)
    rail = ft.NavigationRail(

        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        bgcolor=ft.Colors.BLUE_900,

        # Propiedades corregidas (añadiendo "_text_")
        # unselected_label_text_style=ft.TextStyle(color=ft.Colors.WHITE70),
        # selected_label_text_style=ft.TextStyle(color=ft.Colors.WHITE, weight="bold"),
    
        # # Ajuste de colores de iconos para contraste
        # unselected_icon_color=ft.Colors.WHITE70,
        # selected_icon_color=ft.Colors.WHITE,
        # indicator_color=ft.Colors.BLUE_400,

        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.HOME, label="Feed"),
            ft.NavigationRailDestination(icon=ft.Icons.SHOPPING_CART, label="Market"),
            ft.NavigationRailDestination(icon=ft.Icons.MAP, label="Rutas"),
            ft.NavigationRailDestination(icon=ft.Icons.PERSON, label="Perfil"),

    # Definimos un color blanco con opacidad para los elementos no seleccionados
      
        ],
        on_change=change_view
    )

# Carga inicial (Feed)
    container_principal.content = ft.Text("Bienvenido a MotoAdventure", size=25, weight="bold", text_align=ft.TextAlign.CENTER)

    page.add(
        ft.Row([
            rail,
            ft.VerticalDivider(width=1),
            container_principal
        ], expand=True)
    )