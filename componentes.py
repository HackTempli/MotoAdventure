import flet as ft

# Aquí guardaremos todos los elementos visuales reutilizables
def CardAnuncio(titulo, precio, imagen_url, vendedor, categoria):
    return ft.Container(
        content=ft.Column([
            # Imagen del producto
            ft.Image(
                src=imagen_url if imagen_url != "" else "https://via.placeholder.com", # Ruta por defecto segura
                error_content=ft.Icon(ft.Icons.IMAGE_NOT_SUPPORTED), # Si la ruta falla, muestra un icono en vez de romper la app
                width=150,
                height=120,
                fit="cover",
                border_radius=ft.border_radius.only(top_left=15, top_right=15),
                

            ),
            # Detalles
            ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text(titulo, size=14, weight="bold", max_lines=1),
                    ft.Text(f"{categoria}", size=11, color="grey500"),
                    ft.Row([
                        ft.Text(f"{precio} €", size=16, color="green700", weight="w900"),
                        ft.Text(vendedor, size=10, color="grey400"),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ], spacing=2)
            )
        ]),
        width=160,
        bgcolor=ft.Colors.WHITE,
        border_radius=15,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
    )

# Diseño de Feed estilo Intagram, imagen grande, Autor, Descripción.
def CardFeed(usuario, imagen, descripcion, fecha, moto_actual="Moto Desconocida"):
    return ft.Container(
        padding=10,
        border_radius=15,
        bgcolor=ft.Colors.WHITE,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
        content=ft.Column([
            # Cabecera: Usuario y Moto
            ft.ListTile(
                leading=ft.Icon(ft.Icons.PERSON_PIN, color="orange800"),
                title=ft.Text(f"{usuario} - Rodando en:{moto_actual}", weight="bold", color="blue"),
                subtitle=ft.Text((fecha),color="orange800")
            ),
            # Imagen de la Aventura
            ft.Image(
                src=imagen if imagen else "assets/default_ruta.png",
                width=400,
                height=300,
                fit="cover",
                border_radius=10
            ),
            # Pie de foto
            ft.Container(
                padding=5,
                content=ft.Column([
                    ft.Text(descripcion, size=16, color="black"),
                    ft.Row([
                        ft.IconButton(ft.Icons.FAVORITE_BORDER, icon_color="red"),
                        ft.IconButton(ft.Icons.COMMENT_OUTLINED),
                        ft.Text(f"Publicado: {fecha[:10]}", size=10, color="orange800")
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ])
            )
        ]
    )
)