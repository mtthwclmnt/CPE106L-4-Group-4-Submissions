import flet as ft

def main(page: ft.Page):
    page.title = "Event Platform"
    page.bgcolor = "#1E1E1E"

    def go_to_signup(e):
        page.clean()
        signup_page(page)

    def go_to_login(e):
        page.clean()
        login_page(page)

    title = ft.Text("Vollink", size=30, weight=ft.FontWeight.BOLD, color="white")

    btn_signup = ft.ElevatedButton("Sign Up", on_click=go_to_signup, bgcolor="green", color="white", width=200)
    btn_login = ft.ElevatedButton("Log In", on_click=go_to_login, bgcolor="green", color="white", width=200)

    button_container = ft.Column(
        [title, btn_signup, btn_login],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
    )

    page.add(ft.Container(content=button_container, alignment=ft.alignment.center, expand=True))
    page.update()

def signup_page(page):
    def go_back(e):
        page.clean()
        main(page)
    
    def submit_signup(e):
        page.clean()
        home_page(page)

    page.title = "Sign Up"
    fields = [
        ft.TextField(label="First Name *", width=300),
        ft.TextField(label="Last Name *", width=300),
        ft.TextField(label="Country", width=300),
        ft.TextField(label="City/Province", width=300),
        ft.TextField(label="Email *", width=300),
        ft.TextField(label="Create Password *", password=True, width=300),
    ]

    btn_signup = ft.ElevatedButton("Sign Up", on_click=submit_signup, bgcolor="green", color="white", width=200)
    btn_back = ft.TextButton("Back", on_click=go_back)

    form_container = ft.Column(
        fields + [btn_signup, btn_back], 
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(ft.Container(content=form_container, alignment=ft.alignment.center, expand=True))
    page.update()

def login_page(page):
    def go_back(e):
        page.clean()
        main(page)
    
    def submit_login(e):
        page.clean()
        home_page(page)

    page.title = "Log In"

    email_field = ft.TextField(label="Email Address", width=300)
    password_field = ft.TextField(label="Password", password=True, width=300)
    btn_login = ft.ElevatedButton("Log In", on_click=submit_login, bgcolor="green", color="white", width=200)
    btn_back = ft.TextButton("Back", on_click=go_back)

    login_container = ft.Column(
        [email_field, password_field, btn_login, btn_back], 
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(ft.Container(content=login_container, alignment=ft.alignment.center, expand=True))
    page.update()

def home_page(page):
    page.title = "Home"
    
    sidebar_icons = [
        "person", "calendar_today", "home", "event", "bookmark", "settings", "logout"
    ]
    
    sidebar_texts = [
        "User Profile", "User Schedule", "Home Page", "Events Page", "Bookmarked Posts", "Settings", "Log Out"
    ]

    # User Profile section (emphasized)
    user_profile = ft.Column(
        [
            ft.Container(
                content=ft.Icon("person", color="white", size=40),
                width=60, height=60, border_radius=30, bgcolor="#2E2E2E",
                alignment=ft.alignment.center
            ),
            ft.Text("User Profile", color="white", size=18, weight=ft.FontWeight.BOLD)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5
    )

    # Navigation menu items with increased spacing
    sidebar_items = [
        ft.Row(
            [
                ft.Container(
                    ft.Icon(icon, color="white", size=20),
                    width=40, height=40, border_radius=20, bgcolor="#2E2E2E",
                    alignment=ft.alignment.center
                ),
                ft.Text(text, color="white", size=14)
            ],
            spacing=10
        )
        for icon, text in zip(sidebar_icons[1:], sidebar_texts[1:])  # Skip User Profile from here
    ]

    sidebar = ft.Column(
        [user_profile] + sidebar_items, 
        spacing=20  # Increased spacing
    )

    main_content = ft.Text("Welcome! Select an option from the navigation bar.", color="white", size=16, weight=ft.FontWeight.BOLD)
    
    layout = ft.Row([
        ft.Container(content=sidebar, width=250, bgcolor="#2A2A2A", padding=20, alignment=ft.alignment.top_center),
        ft.Container(content=main_content, expand=True, alignment=ft.alignment.center)
    ])
    
    page.add(layout)
    page.update()

ft.app(target=main)
