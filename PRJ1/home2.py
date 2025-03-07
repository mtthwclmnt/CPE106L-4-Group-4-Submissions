import flet as ft
import re
import pymongo

# MongoDB Connection
MONGO_URI = "mongodb+srv://group4:09009009999@cluster0.oov1f.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(MONGO_URI)
db = client["Vollink"]  
users_collection = db["users"]

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

        # Check if email is already in the database
        if users_collection.find_one({"email": email.value}):
            page.snack_bar = ft.SnackBar(content=ft.Text("Email already exists!"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        if errors:
            page.snack_bar = ft.SnackBar(content=ft.Text("Fill in the * required fields."), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        # Insert user into MongoDB
        users_collection.insert_one({
            "first_name": first_name.value,
            "last_name": last_name.value,
            "email": email.value,
            "password": password.value  # ⚠ In a real app, hash the password before storing!
        })

        page.snack_bar = ft.SnackBar(content=ft.Text("Account created successfully!"), bgcolor="green")
        page.snack_bar.open = True
        page.update()

        page.clean()
        main(page)

    page.title = "Sign Up"
    first_name = ft.TextField(label="First Name *", width=300)
    last_name = ft.TextField(label="Last Name *", width=300)
    email = ft.TextField(label="Email *", width=300)
    password = ft.TextField(label="Create Password *", password=True, width=300)

    btn_signup = ft.ElevatedButton("Sign Up", on_click=submit_signup, bgcolor="green", color="white", width=200)
    btn_back = ft.TextButton("Back", on_click=go_back)

    form_container = ft.Column(
        [first_name, last_name, email, password, btn_signup, btn_back], 
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

        # Check user credentials in MongoDB
        user = users_collection.find_one({"email": email.value, "password": password.value})

        if user:
            page.snack_bar = ft.SnackBar(content=ft.Text("Login successful!"), bgcolor="green")
            page.snack_bar.open = True
            page.update()
            page.clean()
            home_page(page)
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("Invalid email or password!"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

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
    
    main_content = ft.Text("Welcome! You are now logged in.", color="white", size=16, weight=ft.FontWeight.BOLD)
    
    layout = ft.Column([
        ft.Container(content=main_content, alignment=ft.alignment.center)
    ], expand=True)
    
    page.add(layout)
    page.update()

ft.app(target=main)
