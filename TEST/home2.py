import flet as ft
import re
import pymongo
from datetime import datetime

# MongoDB Connection
MONGO_URI = "mongodb+srv://group4:09009009999@cluster0.oov1f.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(MONGO_URI)
db = client["Vollink"]
users_collection = db["users"]
events_collection = db["events"]  

def main(page: ft.Page):
    page.title = "Event Platform"
    page.bgcolor = "#E8F5E9"

    def go_to_signup(e):
        page.clean()
        signup_page(page)

    def go_to_login(e):
        page.clean()
        login_page(page)

    title = ft.Text("Vollink", size=30, weight=ft.FontWeight.BOLD, color="black")

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
    page.bgcolor = "#E8F5E9"
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
            page.views.pop()
            page.views.append(role_selection_page(page, user))
            page.update()
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

def role_selection_page(page, user):
    page.bgcolor = "#E8F5E9"

    def go_to_organizer(e):
        page.views.append(organizer_dashboard(page, user))
        page.update()

    def go_to_volunteer(e):
        page.views.append(volunteer_dashboard(page, user))
        page.update()

    title = ft.Text("Select Your Role", size=24, weight=ft.FontWeight.BOLD, color="black")
    btn_organizer = ft.ElevatedButton("Organizer", on_click=go_to_organizer, bgcolor="green", color="white", width=200)
    btn_volunteer = ft.ElevatedButton("Volunteer", on_click=go_to_volunteer, bgcolor="green", color="white", width=200)

    role_container = ft.Column([
        title, btn_organizer, btn_volunteer
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)

    return ft.View("/role-selection", [ft.Container(content=role_container, alignment=ft.alignment.center, expand=True)])

def organizer_dashboard(page, user):
    page.bgcolor = "#E8F5E9"
    def go_back(e):
        page.views.pop()
        page.update()

    def create_event_view(e):
        page.views.append(create_event_page(page, user))
        page.update()

    def view_my_events(e):
        page.views.append(my_events_page(page, user))
        page.update()

    title = ft.Text("Organizer Dashboard", size=24, weight=ft.FontWeight.BOLD, color="black")
    btn_create = ft.ElevatedButton("Create New Event", on_click=create_event_view, bgcolor="green", color="white", width=200)
    btn_view = ft.ElevatedButton("View My Events", on_click=view_my_events, bgcolor="green", color="white", width=200)
    btn_back = ft.TextButton("Back", on_click=go_back)

    dashboard_container = ft.Column([
        title, btn_create, btn_view, btn_back
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)

    return ft.View("/organizer-dashboard", [ft.Container(content=dashboard_container, alignment=ft.alignment.center, expand=True)])
def create_event_page(page, user):
    page.bgcolor = "#E8F5E9"
    def go_back(e):  # Add this function at the beginning
        page.views.pop()
        page.update()

    def submit_event(e):
        errors = False
        required_fields = [event_name, event_date, event_address]

        for field in required_fields:
            if not field.value.strip():
                field.border_color = "red"
                errors = True
            else:
                field.border_color = "gray"

        if errors:
            page.snack_bar = ft.SnackBar(content=ft.Text("Fill in all required fields."), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        new_event = {
            "name": event_name.value.strip(),
            "date": event_date.value.strip(),
            "address": event_address.value.strip(),
            "organizer_id": str(user["_id"]),
            "organizer_name": f"{user['first_name']} {user['last_name']}",  # Add organizer's name
            "volunteers": []
        }
        
        events_collection.insert_one(new_event)

        page.snack_bar = ft.SnackBar(content=ft.Text("Event created successfully!"), bgcolor="green")
        page.snack_bar.open = True
        page.views.pop()
        page.update()

    event_name = ft.TextField(label="Event Name *", width=300)
    event_date = ft.TextField(label="Event Date (YYYY-MM-DD) *", width=300)
    event_address = ft.TextField(label="Event Address *", width=300)
    btn_create = ft.ElevatedButton("Create Event", on_click=submit_event, bgcolor="green", color="white", width=200)
    btn_back = ft.TextButton("Back", on_click=go_back)

    create_container = ft.Column([
        event_name, event_date, event_address, btn_create, btn_back
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)

    return ft.View("/create-event", [ft.Container(content=create_container, alignment=ft.alignment.center, expand=True)])

def volunteer_dashboard(page, user):
    page.bgcolor = "#E8F5E9"
    def go_back(e):
        page.views.pop()
        page.update()

    def view_available_events(e):
        page.views.append(available_events_page(page, user))
        page.update()

    def view_my_volunteering(e):
        page.views.append(my_volunteering_page(page, user))
        page.update()

    title = ft.Text("Volunteer Dashboard", size=24, weight=ft.FontWeight.BOLD, color="black")
    btn_available = ft.ElevatedButton("Available Events", on_click=view_available_events, bgcolor="green", color="white", width=200)
    btn_my_events = ft.ElevatedButton("My Volunteering", on_click=view_my_volunteering, bgcolor="green", color="white", width=200)
    btn_back = ft.TextButton("Back", on_click=go_back)

    dashboard_container = ft.Column([
        title, btn_available, btn_my_events, btn_back
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)

    return ft.View("/volunteer-dashboard", [ft.Container(content=dashboard_container, alignment=ft.alignment.center, expand=True)])

def my_events_page(page, user):
    page.bgcolor = "#E8F5E9"
    def go_back(e):
        page.views.pop()
        page.update()

    my_events = list(events_collection.find({"organizer_id": str(user["_id"])}))
    events_list = ft.Column(spacing=10)

    if not my_events:
        events_list.controls.append(ft.Text("No events created yet.", color="black"))
    else:
        for event in my_events:
            event_card = ft.Container(
                content=ft.Column([
                    ft.Text(f"Event: {event['name']}", color="black"),
                    ft.Text(f"Date: {event['date']}", color="black"),
                    ft.Text(f"Address: {event['address']}", color="black"),
                    ft.Text(f"Volunteers: {len(event['volunteers'])}", color="black")
                ]),
                padding=10,
                border=ft.border.all(1, "blue"),
                border_radius=10,
                margin=5
            )
            events_list.controls.append(event_card)

    content = ft.Column([
        ft.Text("My Events", size=24, weight=ft.FontWeight.BOLD, color="black"),
        events_list,
        ft.TextButton("Back", on_click=go_back)
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)

    return ft.View("/my-events", [ft.Container(content=content, alignment=ft.alignment.center, expand=True)])

def available_events_page(page, user):
    page.bgcolor = "#E8F5E9"
    def go_back(e):
        page.views.pop()
        page.update()

    def join_event(event_id):
        def handle_join(e):
            events_collection.update_one(
                {"_id": event_id},
                {"$addToSet": {"volunteers": str(user["_id"])}}
            )
            page.snack_bar = ft.SnackBar(content=ft.Text("Successfully joined the event!"), bgcolor="green")
            page.snack_bar.open = True
            page.views.pop()
            page.update()
        return handle_join

    available_events = list(events_collection.find(
        {"volunteers": {"$nin": [str(user["_id"])]}}
    ))
    events_list = ft.Column(spacing=10)

    if not available_events:
        events_list.controls.append(ft.Text("No available events.", color="#2E7D32"))  # Darker green color for text
    else:
        for event in available_events:
            try:
                event_card = ft.Container(
                    content=ft.Column([
                        ft.Text(f"Event: {event.get('name', 'No name')}", 
                               color="#2E7D32", 
                               weight=ft.FontWeight.BOLD),
                        ft.Text(f"Organized by: {event.get('organizer_name', 'Unknown')}", 
                               color="#2E7D32",
                               italic=True),
                        ft.Text(f"Date: {event.get('date', 'No date')}", 
                               color="#2E7D32"),
                        ft.Text(f"Address: {event.get('address', 'No address')}", 
                               color="#2E7D32"),
                        ft.ElevatedButton("Join Event", 
                                        on_click=join_event(event["_id"]), 
                                        bgcolor="green", 
                                        color="white")
                    ]),
                    padding=20,
                    border=ft.border.all(1, "#2E7D32"),
                    border_radius=10,
                    margin=5,
                    bgcolor="#F1F8E9"  # Very light green background for cards
                )
                events_list.controls.append(event_card)
            except Exception as e:
                print(f"Error processing event: {e}")
                continue

    content = ft.Column([
        ft.Text("Available Events", 
               size=24, 
               weight=ft.FontWeight.BOLD, 
               color="#2E7D32"),
        events_list,
        ft.TextButton("Back", on_click=go_back)
    ], alignment=ft.MainAxisAlignment.CENTER, 
       horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
       spacing=20)

    return ft.View("/available-events", [ft.Container(content=content, alignment=ft.alignment.center, expand=True)])
def my_volunteering_page(page, user):
    page.bgcolor = "#E8F5E9"
    def go_back(e):
        page.views.pop()
        page.update()

    my_events = list(events_collection.find(
        {"volunteers": str(user["_id"])}
    ))
    events_list = ft.Column(spacing=10)

    if not my_events:
        events_list.controls.append(ft.Text("You haven't joined any events yet.", 
                                          color="#2E7D32"))
    else:
        for event in my_events:
            try:
                event_card = ft.Container(
                    content=ft.Column([
                        ft.Text(f"Event: {event.get('name', 'No name')}", 
                               color="#2E7D32",
                               weight=ft.FontWeight.BOLD),
                        ft.Text(f"Organized by: {event.get('organizer_name', 'Unknown')}", 
                               color="#2E7D32",
                               italic=True),
                        ft.Text(f"Date: {event.get('date', 'No date')}", 
                               color="#2E7D32"),
                        ft.Text(f"Address: {event.get('address', 'No address')}", 
                               color="#2E7D32")
                    ]),
                    padding=20,
                    border=ft.border.all(1, "#2E7D32"),
                    border_radius=10,
                    margin=5,
                    bgcolor="#F1F8E9"
                )
                events_list.controls.append(event_card)
            except Exception as e:
                print(f"Error processing event: {e}")
                continue

    content = ft.Column([
        ft.Text("My Volunteering", 
               size=24, 
               weight=ft.FontWeight.BOLD, 
               color="#2E7D32"),
        events_list,
        ft.TextButton("Back", on_click=go_back)
    ], alignment=ft.MainAxisAlignment.CENTER, 
       horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
       spacing=20)

    return ft.View("/my-volunteering", [ft.Container(content=content, alignment=ft.alignment.center, expand=True)])

def home_page(page):
    page.title = "Home"
    main_content = ft.Text("Welcome to the Home Page!", color="black", size=24, weight=ft.FontWeight.BOLD)
    page.add(ft.Container(content=main_content, alignment=ft.alignment.center, expand=True))
    page.update()

ft.app(target=main)
