import flet as ft
from pymongo import MongoClient
import bcrypt

client = MongoClient("mongodb+srv://group4:09009009999@cluster0.oov1f.mongodb.net/")  # Change if using MongoDB Cloud
db = client["eventlink"]
users_collection = db["users"]

# Function to handle sign-up
def register_user(e):
    username = username_field.value
    email = email_field.value
    password = password_field.value.encode("utf-8")
    
    # Hash the password
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    # Check if account is already taken
    if users_collection.find_one({"email": email}):
        status_text.value = "Email already registered!"
    else:
        users_collection.insert_one({"username": username, "email": email, "password": hashed_password})
        status_text.value = "User registered successfully!"

    page.update()

# Start Flet app
def main(page: ft.Page):
    global username_field, email_field, password_field, status_text

    page.title = "Sign Up"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    username_field = ft.TextField(label="Username", width=300)
    email_field = ft.TextField(label="Email", width=300)
    password_field = ft.TextField(label="Password", password=True, width=300)

    signup_button = ft.ElevatedButton("Sign Up", on_click=register_user)
    status_text = ft.Text("", color="red")

    page.add(
        ft.Column(
            [
                ft.Text("Sign Up", size=24, weight="bold"),
                username_field,
                email_field,
                password_field,
                signup_button,
                status_text
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

ft.app(target=main)
