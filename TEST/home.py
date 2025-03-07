import flet as ft
import re

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
        errors = False
        required_fields = [first_name, last_name, email, password]
        
        for field in required_fields:
            if not field.value.strip():
                field.border_color = "red"
                errors = True
            else:
                field.border_color = "gray"
        
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email.value):
            email.border_color = "red"
            errors = True
        
        if errors:
            page.snack_bar = ft.SnackBar(content=ft.Text("Fill in the * required fields."), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return
        
        page.clean()
        home_page(page)

    page.title = "Sign Up"
    first_name = ft.TextField(label="First Name *", width=300)
    last_name = ft.TextField(label="Last Name *", width=300)
    country = ft.TextField(label="Country", width=300)
    city = ft.TextField(label="City/Province", width=300)
    separator = ft.Container(height=1, bgcolor="white", width=250)
    email = ft.TextField(label="Email *", width=300)
    password = ft.TextField(label="Create Password *", password=True, width=300)

    btn_signup = ft.ElevatedButton("Sign Up", on_click=submit_signup, bgcolor="green", color="white", width=200)
    btn_back = ft.TextButton("Back", on_click=go_back)

    form_container = ft.Column(
        [first_name, last_name, country, city, separator, email, password, btn_signup, btn_back], 
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
        errors = False
        
        if not email.value.strip():
            email.border_color = "red"
            errors = True
        else:
            email.border_color = "gray"
        
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email.value):
            email.border_color = "red"
            errors = True
        
        if not password.value.strip():
            password.border_color = "red"
            errors = True
        else:
            password.border_color = "gray"
        
        if errors:
            page.snack_bar = ft.SnackBar(content=ft.Text("Fill in the * required fields."), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return
        
        page.clean()
        home_page(page)

    page.title = "Log In"
    email = ft.TextField(label="Email Address *", width=300)
    password = ft.TextField(label="Password *", password=True, width=300)
    btn_login = ft.ElevatedButton("Log In", on_click=submit_login, bgcolor="green", color="white", width=200)
    btn_back = ft.TextButton("Back", on_click=go_back)

    login_container = ft.Column(
        [email, password, btn_login, btn_back], 
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

    def navigate_to(page_name):
        main_content.clean()  # Clear the main content area
        if page_name == "User Profile":
            user_profile_page(main_content)
        elif page_name == "User Schedule":
            user_schedule_page(main_content)
        elif page_name == "Home Page":
            home_page(main_content)
        elif page_name == "Events Page":
            events_page(main_content)
        elif page_name == "Bookmarked Posts":
            bookmarked_posts_page(main_content)
        elif page_name == "Settings":
            settings_page(main_content)
        elif page_name == "Log Out":
            logout_user(page)

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
        ft.TextButton(
            content=ft.Row(
                [
                    ft.Icon(icon, color="white", size=20),
                    ft.Text(text, color="white", size=14)
                ],
                spacing=10
            ),
            on_click=lambda e, text=text: navigate_to(text)  # Make the entire row clickable
        )
        for icon, text in zip(sidebar_icons[1:], sidebar_texts[1:])  # Skip User Profile from here
    ]

    sidebar = ft.Column(
        [user_profile] + sidebar_items, 
        spacing=20  # Increased spacing
    )

    main_content = ft.Container(content=ft.Text("Welcome! Select an option from the navigation bar.", color="white", size=16, weight=ft.FontWeight.BOLD), expand=True, alignment=ft.alignment.center)
    
    layout = ft.Row([
        ft.Container(content=sidebar, width=250, bgcolor="#2A2A2A", padding=20, alignment=ft.alignment.top_center),
        main_content
    ], expand=True)
    
    page.add(layout)
    page.update()

def user_profile_page(container):
    container.content = ft.Column([
        ft.Text("User Profile Page", size=24, weight=ft.FontWeight.BOLD, color="white"),
        # Add more content
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    container.update()

def user_schedule_page(container):
    container.content = ft.Column([
        ft.Text("User Schedule Page", size=24, weight=ft.FontWeight.BOLD, color="white"),
        # Add more content
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    container.update()

def events_page(container):
    container.content = ft.Column([
        ft.Text("Events Page", size=24, weight=ft.FontWeight.BOLD, color="white"),
        # Add more content
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    container.update()

def bookmarked_posts_page(container):
    container.content = ft.Column([
        ft.Text("Bookmarked Posts Page", size=24, weight=ft.FontWeight.BOLD, color="white"),
        # Add more content
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    container.update()

def settings_page(container):
    container.content = ft.Column([
        ft.Text("Settings Page", size=24, weight=ft.FontWeight.BOLD, color="white"),
        # Add more content
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    container.update()

def logout_user(page):
    # Handle logout logic herex
    page.title = "Logged Out"
    page.clean()  # Clear the current page content
    main(page)  # Redirect to the main page

ft.app(target=main)
