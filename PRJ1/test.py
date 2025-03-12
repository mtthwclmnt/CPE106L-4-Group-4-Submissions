import flet as ft


def main(page: ft.Page):
    def handle_password_icon_click(e):
        if password_field.password:
            password_field.password = False
            password_field.suffix.icon = ft.icons.VISIBILITY
        else:
            password_field.password = True
            password_field.suffix.icon = ft.icons.VISIBILITY_OFF
        password_field.update()

    password_field = ft.TextField(
        password=True,
        suffix=ft.IconButton(
            icon=ft.icons.VISIBILITY_OFF,
            icon_color=ft.colors.GREEN,
            on_click=handle_password_icon_click,
        ),
    )
    page.add(password_field)


ft.app(target=main)