import flet as ft
import re
import os
import pymongo

# MongoDB Connection Setup
MONGO_URI = "mongodb+srv://group4:09009009999@cluster0.oov1f.mongodb.net/"
client = pymongo.MongoClient(MONGO_URI)
db = client["Vollink"]  
users_collection = db["users"] 

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
    
    def save_to_mongodb(user_data):
        try:
            users_collection.insert_one(user_data)
            return True
        except Exception as e:
            print(f"Error saving to MongoDB: {e}")
            return False
    
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
            
            if save_to_mongodb(user_data):
                status_text.value = "Sign-up Successful! Redirecting to Home..."
                status_text.color = "green"
                page.update()
                
                # Redirect to Home page after success
                page.clean()
                go_to_home()
            else:
                status_text.value = "Error saving data. Try again."
                status_text.color = "red"
                page.update()
    
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

