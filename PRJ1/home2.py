import flet as ft
import re
import pymongo

# MongoDB Connection
MONGO_URI = "mongodb+srv://group4:09009009999@cluster0.oov1f.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(MONGO_URI)
db = client["Vollink"]
users_collection = db["users"]
events_collection = db["events"]

# Main Function
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
    button_container = ft.Column([
        title, btn_signup, btn_login
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)

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

        users_collection.insert_one({
            "first_name": first_name.value,
            "last_name": last_name.value,
            "email": email.value,
            "password": password.value,
            "role": "volunteer"
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

    form_container = ft.Column([
        first_name, last_name, email, password, btn_signup, btn_back
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

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

        user = users_collection.find_one({"email": email.value, "password": password.value})

        if user:
            page.clean()
            role_selection_page(page, user)
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("Invalid email or password!"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    page.title = "Log In"
    email = ft.TextField(label="Email Address *", width=300)
    password = ft.TextField(label="Password *", password=True, width=300)
    btn_login = ft.ElevatedButton("Log In", on_click=submit_login, bgcolor="green", color="white", width=200)
    btn_back = ft.TextButton("Back", on_click=go_back)

    login_container = ft.Column([
        email, password, btn_login, btn_back
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    page.add(ft.Container(content=login_container, alignment=ft.alignment.center, expand=True))
    page.update()

def role_selection_page(page, user):
    def select_role(role):
        page.clean()
        if role == "organizer":
            event_management_page(page)
        else:
            volunteer_dashboard(page, user)

    title = ft.Text("Select Your Role", size=20, weight=ft.FontWeight.BOLD, color="white")
    btn_organizer = ft.ElevatedButton("Organizer", on_click=lambda e: select_role("organizer"), bgcolor="blue", color="white", width=200)
    btn_volunteer = ft.ElevatedButton("Volunteer", on_click=lambda e: select_role("volunteer"), bgcolor="blue", color="white", width=200)
    btn_back = ft.TextButton("Back", on_click=lambda e: login_page(page))

    role_container = ft.Column([
        title, btn_organizer, btn_volunteer, btn_back
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    page.add(ft.Container(content=role_container, alignment=ft.alignment.center, expand=True))
    page.update()

def event_management_page(page):
    page.snack_bar = ft.SnackBar(content=ft.Text("Organizer Dashboard - Coming Soon"), bgcolor="yellow")
    page.snack_bar.open = True
    page.update()

def volunteer_dashboard(page, user):
    page.snack_bar = ft.SnackBar(content=ft.Text("Volunteer Dashboard - Coming Soon"), bgcolor="yellow")
    page.snack_bar.open = True
    page.update()

ft.app(target=main)
