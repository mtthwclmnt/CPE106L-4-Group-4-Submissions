import flet as ft
import re
import json
import os

def main(page: ft.Page):
    page.title = "Event Platform - Sign Up"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    # Input fields
    first_name = ft.TextField(label="First Name *", autofocus=True)
    last_name = ft.TextField(label="Last Name *")
    email = ft.TextField(label="Email *", keyboard_type=ft.KeyboardType.EMAIL)
    contact = ft.TextField(label="Contact", keyboard_type=ft.KeyboardType.PHONE)
    company = ft.TextField(label="Company Name")
    country = ft.TextField(label="Country *")
    city = ft.TextField(label="City")
    
    status_text = ft.Text("", color="blue")
    
    def is_valid_email(email_str):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email_str)
    
    def save_to_json(user_data):
        file_path = os.path.join(os.path.dirname(__file__), "users.json")
        data = []
        
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as file:
                    data = json.load(file)
            except json.JSONDecodeError:
                data = []
        
        data.append(user_data)
        
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
    
    def go_to_home(e=None):
        page.clean()
        page.add(ft.Text("Welcome to the Home Page!", size=24, weight="bold"))
        page.update()
    
    def submit_form(e):
        errors = False
        
        # Reset field borders
        first_name.border_color = "black"
        last_name.border_color = "black"
        email.border_color = "black"
        country.border_color = "black"
        
        if not first_name.value:
            first_name.border_color = "red"
            errors = True
        if not last_name.value:
            last_name.border_color = "red"
            errors = True
        if not email.value or not is_valid_email(email.value):
            email.border_color = "red"
            errors = True
        if not country.value:
            country.border_color = "red"
            errors = True
        
        if errors:
            status_text.value = "Please fill in all * required fields correctly."
            status_text.color = "red"
            page.snack_bar = ft.SnackBar(content=ft.Text("Please fill in all required fields correctly."), bgcolor="red")
            page.snack_bar.open = True
            page.update()
        else:
            user_data = {
                "FirstName": first_name.value,
                "LastName": last_name.value,
                "Email": email.value,
                "Phone": contact.value,
                "Company": company.value,
                "Country": country.value,
                "City": city.value
            }
            save_to_json(user_data)
            
            status_text.value = "Sign-up Successful! Redirecting to Home..."
            status_text.color = "green"
            page.update()
            
            # Redirect to Home page after success
            page.clean()
            go_to_home()
    
    submit_btn = ft.ElevatedButton("Sign Up", on_click=submit_form)
    
    page.add(
        ft.Column(
            [
                first_name, last_name, email, contact, company, country, city, submit_btn, status_text
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

ft.app(main)
