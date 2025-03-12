import flet as ft
import re
import pymongo
from datetime import datetime
from bson import ObjectId

# Mongo DB connection
MONGO_URI = "mongodb+srv://group4:09009009999@cluster0.oov1f.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(MONGO_URI)
db = client["Vollink"]
users_collection = db["users"]
events_collection = db["events"]

background_color = "#8c9657"
primary_color = "#473f34"
text_color = "#f0e5c7"
text_color_light = "white"
text_color_title = "white"
brdr_color = "white"
brdr_color_bookmarked = "green"
bookmark_color_bg = "#f0e5c7"
bookmark_color_bg_active = "yellow"
text_hov_color = primary_color
label_style_text = ft.TextStyle(color=text_color, italic=True)
button_style_back = ft.ButtonStyle(color=text_color)

def main(page: ft.Page):
    page.title = "User Authentication"
    page.bgcolor = background_color
    page.window_width = 1000
    page.window_height = 600
    page.window_resizable = False

    def go_to_signup(e):
        page.clean()
        signup_page(page)

    def go_to_login(e):
        page.clean()
        login_page(page)

    title = ft.Text("Vollink", size=50, weight=ft.FontWeight.BOLD, color=text_color)

    btn_signup = ft.ElevatedButton("Sign Up", on_click=go_to_signup, bgcolor=primary_color, color=text_color, width=170, height=40)
    btn_login = ft.ElevatedButton("Log In", on_click=go_to_login, bgcolor=primary_color, color=text_color, width=170, height=40)

    button_container = ft.Column(
        [title, btn_signup, btn_login],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
    )

    page.add(ft.Container(content=button_container, alignment=ft.alignment.center, expand=True))
    page.update()
    
def validate_email(email):
    """Checks if the email follows the correct format."""
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

def signup_page(page):
    def go_back(e):
        page.clean()
        main(page)
    
    def submit_signup(e):
        errors = False
        required_fields = [first_name, last_name, email, password]
        
        for field in [first_name, last_name, email, password]:
            if not field.value.strip():
                field.border_color = "red"
                field.error_text = "This field is required"
                errors = True
            else:
                field.border_color = None
                field.error_text = None
        
        if email.value.strip() and not validate_email(email.value):
            email.border_color = "red"
            email.error_text = "Enter a valid email (sample@email.com)"
            errors = True
        
        if errors:
            page.snack_bar = ft.SnackBar(content=ft.Text("Fill in the * required fields."), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        # Check if email already exists
        if users_collection.find_one({"email": email.value}):
            email.border_color = "red"
            email.error_text = "Email already exists!"
            page.update()
            return

        # Insert user into database
        user_data = {
            "first_name": first_name.value,
            "last_name": last_name.value,
            "email": email.value,
            "password": password.value,
            "country": country.value,
            "city": city.value,
            "created_at": datetime.utcnow(),
            "bookmarked_events": []  
        }
        
        result = users_collection.insert_one(user_data)
        user = users_collection.find_one({"_id": result.inserted_id})
        
        page.clean()
        role_selection_page(page, user)

    page.title = "Sign Up"
    first_name = ft.TextField(label="First Name *", width=300, border_radius=12, label_style=label_style_text)
    last_name = ft.TextField(label="Last Name *", width=300, border_radius=12, label_style=label_style_text)
    country = ft.TextField(label="Country", width=300, border_radius=12, label_style=label_style_text)
    city = ft.TextField(label="City/Province", width=300, border_radius=12, label_style=label_style_text)
    separator = ft.Container(height=2, bgcolor=primary_color, width=250, border_radius=10)
    email = ft.TextField(label="Email *", width=300, border_radius=12, label_style=label_style_text)
    password = ft.TextField(label="Create Password *", width=300, border_radius=12, label_style=label_style_text, password=True, can_reveal_password=True)

    btn_signup = ft.ElevatedButton("Sign Up", on_click=submit_signup, bgcolor=primary_color, color=text_color, width=170, height=40)
    btn_back = ft.TextButton("Back", on_click=go_back, style=button_style_back, width=170, height=40)

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
        required_fields = [email, password]

        # Check for empty fields
        for field in required_fields:
            if not field.value.strip():
                field.border_color = "red"
                field.error_text = "This field is required"
                errors = True
            else:
                field.border_color = None
                field.error_text = None

        # Check email format
        if email.value.strip():
            if not validate_email(email.value):
                email.border_color = "red"
                email.error_text = "Enter a valid email (sample@email.com)"
                errors = True
            else:
                # Reset email field error if the format is valid
                email.border_color = None
                email.error_text = None

        if errors:
            page.snack_bar = ft.SnackBar(content=ft.Text("Fill in the * required fields."), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        # Check if email exists in the database
        user = users_collection.find_one({"email": email.value})

        if not user:
            email.border_color = "red"
            email.error_text = "Email not found"
            page.snack_bar = ft.SnackBar(content=ft.Text("Email not found"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return
        else:
            # Reset email field error if the email exists
            email.border_color = None
            email.error_text = None

        # Check if the password is correct
        if user["password"] != password.value:
            password.border_color = "red"
            password.error_text = "Incorrect password"
            page.snack_bar = ft.SnackBar(content=ft.Text("Incorrect password"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return
        else:
            # Reset password field error if the password is correct
            password.border_color = None
            password.error_text = None
        
        if user:
            if not user.get("role"):
                page.clean()
                role_selection_page(page, user)
            else:
                page.clean()
                home_page(page, user)  # Now passing user data
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("Invalid credentials"))
            page.snack_bar.open = True
            page.update()
            return
            
        # Store user session info 
        page.client_storage.set("user_email", email.value)
        
    page.title = "Log In"
    email = ft.TextField(label="Email Address *", width=300, border_radius=12, label_style=label_style_text)
    password = ft.TextField(label="Password *", width=300, border_radius=12, label_style=label_style_text, password=True, can_reveal_password=True)
    btn_login = ft.ElevatedButton("Log In", on_click=submit_login, bgcolor=primary_color, color=text_color, width=170, height=40)
    btn_back = ft.TextButton("Back", on_click=go_back, style=button_style_back, width=170, height=40)

    login_container = ft.Column(
        [email, password, btn_login, btn_back], 
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(ft.Container(content=login_container, alignment=ft.alignment.center, expand=True))
    page.update()
    
def role_selection_page(page, user):
    def select_role(role):
        def handle(e):
            users_collection.update_one(
                {"_id": user["_id"]},
                {"$set": {"role": role}}
            )
            user["role"] = role
            page.clean()
            home_page(page, user)  
        return handle

    title = ft.Text("Select Your Role", size=30, weight=ft.FontWeight.BOLD, color="white")
    btn_organizer = ft.ElevatedButton("Organizer", on_click=select_role("organizer"), bgcolor="green", color="white", width=200)
    btn_volunteer = ft.ElevatedButton("Volunteer", on_click=select_role("volunteer"), bgcolor="green", color="white", width=200)

    content = ft.Column([
        title, btn_organizer, btn_volunteer
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)

    page.add(ft.Container(content=content, alignment=ft.alignment.center, expand=True))
    page.update()

def home_page(page, user):
    page.title = "Home"
    
    def switch_role(e):
        new_role = "volunteer" if user["role"] == "organizer" else "organizer"
        users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"role": new_role}}
        )
        user["role"] = new_role
        page.clean()
        home_page(page, user)
        
    # Modify sidebar based on user role
    if user.get("role") == "organizer":
        sidebar_icons = [
            "person", "swap_horiz", "add_circle", "calendar_today", "bookmark", "settings", "logout"
        ]
        
        sidebar_texts = [
            "User Profile", "Switch to Volunteer", "Create Event", "My Events", "Bookmarked Events", "Settings", "Log Out"
        ]
    else:  # volunteer
        sidebar_icons = [
            "person", "swap_horiz", "event", "calendar_today", "bookmark", "settings", "logout"
        ]
        
        sidebar_texts = [
            "User Profile", "Switch to Organizer", "Available Events", "My Volunteering", "Bookmarked Events", "Settings", "Log Out"
        ]

    def navigate_to(page_name):
        main_content.clean()
        if page_name == "User Profile":
            user_profile_page(main_content, user)
        elif page_name == "Switch to Volunteer" or page_name == "Switch to Organizer":
            switch_role(None)
        elif page_name == "Create Event":
            create_event_page(main_content, user)
        elif page_name == "My Events":
            my_events_page(main_content, user)
        elif page_name == "Available Events":
            available_events_page(main_content, user)
        elif page_name == "My Volunteering":
            my_volunteering_page(main_content, user)
        elif page_name == "Bookmarked Events":
            bookmarked_posts_page(main_content, user)
        elif page_name == "Settings":
            settings_page(main_content, user)
        elif page_name == "Log Out":
            logout_user(page)

    # User Profile section 
    user_profile = ft.Column(
        [
            ft.Container(
                content=ft.Icon("person", color=text_color, size=40),
                width=60, height=60, border_radius=30, bgcolor=background_color,
                alignment=ft.alignment.center
            ),
            ft.Text(f"{user['first_name']} {user['last_name']}", 
                   color=text_color, size=18, weight=ft.FontWeight.BOLD),
            ft.Text(f"Your role: {user['role'].capitalize()}", 
                   color=text_color, size=14, italic=True)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5
    )

    # Navigation menu items with increased spacing
    sidebar_items = [
        ft.Container(
            content=ft.TextButton(
                content=ft.Row(
                    [
                        ft.Icon(icon, color=text_color, size=20),
                        ft.Text(text, color=text_color, size=14)
                    ],
                    spacing=12  
                ),
                on_click=lambda e, text=text: navigate_to(text),
                style=ft.ButtonStyle(
                    bgcolor={"": primary_color, "hovered": text_hov_color},  # Background color & hover effect
                    padding=15,  # Adjust spacing inside the button
                    shape=ft.RoundedRectangleBorder(radius=8)  # Optional rounded corners
                )
            ),
            bgcolor=primary_color,  # Default background color for consistency
            border_radius=8,  # Rounded corners
            margin=ft.margin.only(bottom=5),  # Spacing between items
            shadow=ft.BoxShadow(
                blur_radius=10,
                spread_radius=2,
                color=ft.Colors.with_opacity(0.2, color="black"),
                offset=ft.Offset(3, 3) 
            )
        )
        for icon, text in zip(sidebar_icons, sidebar_texts)
    ]

    sidebar = ft.Column(
        [user_profile] + sidebar_items, 
        spacing=24
    )

    main_content = ft.Container(
        content=ft.Text("Welcome! Select an option from the navigation bar.", 
                       color=text_color, size=16, weight=ft.FontWeight.BOLD), 
        expand=True, 
        alignment=ft.alignment.center
    )
    
    layout = ft.Row([
        ft.Container(content=sidebar, width=250, bgcolor=primary_color, padding=20, alignment=ft.alignment.top_center),
        main_content
    ], expand=True)
    
    page.add(layout)
    page.update()
def create_event_page(container, user):
    def submit_event(e):
        if not all([name.value, date.value, address.value]):
            container.page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Please fill all required fields"),
                    bgcolor="red",
                    action="Dismiss"
                )
            )
            return

        new_event = {
            "name": name.value,
            "date": date.value,
            "address": address.value,
            "description": description.value,  
            "organizer_id": str(user["_id"]),
            "organizer_name": f"{user['first_name']} {user['last_name']}",
            "volunteers": []
        }
        
        events_collection.insert_one(new_event)
        
       
        def close_dlg(e):
            dlg.open = False
            container.page.update()
            
        dlg = ft.AlertDialog(
            title=ft.Text("Success!"),
            content=ft.Text("Event created successfully!"),
            actions=[
                ft.TextButton("OK", on_click=close_dlg)
            ]
        )
        
        container.page.dialog = dlg
        dlg.open = True
        container.page.update()
        
     
        name.value = date.value = address.value = description.value = ""
        container.update()

    name = ft.TextField(label="Event Name *", width=300, label_style=label_style_text)
    date = ft.TextField(label="Event Date (YYYY-MM-DD) *", width=300, label_style=label_style_text)
    address = ft.TextField(label="Event Address *", width=300, label_style=label_style_text)
    description = ft.TextField(
        label="Event Description",
        width=300,
        multiline=True,
        min_lines=3,
        max_lines=5,
        label_style=label_style_text
    )
    
    container.content = ft.Column([
        ft.Text("Create New Event", size=24, weight=ft.FontWeight.BOLD, color=text_color),
        name,
        date,
        address,
        description,
        ft.ElevatedButton("Create Event", on_click=submit_event, bgcolor="green", color="white", width=170, height=40)
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
    container.update()

def available_events_page(container, user):
    def join_event(event_id):
        def handle_join(e):
            events_collection.update_one(
                {"_id": event_id},
                {"$addToSet": {"volunteers": str(user["_id"])}}
            )
            
           
            def close_dlg(e):
                dlg.open = False
                container.page.update()
                available_events_page(container, user)  # Refresh the page
                
            dlg = ft.AlertDialog(
                title=ft.Text("Success!"),
                content=ft.Text("You have successfully joined the event!"),
                actions=[
                    ft.TextButton("OK", on_click=close_dlg)
                ]
            )
            
            container.page.dialog = dlg
            dlg.open = True
            container.page.update()
            
        return handle_join

    events = list(events_collection.find(
        {"volunteers": {"$nin": [str(user["_id"])]}}
    ))
    
    events_list = ft.ListView(spacing=10, expand=True)
    
    if not events:
        events_list.controls.append(
            ft.Text("No available events.", color="white")
        )
    else:
        for event in events:
            event_card = ft.Container(
                content=ft.Column([
                    ft.Text(f"Event: {event['name']}", color="white", weight=ft.FontWeight.BOLD),
                    ft.Text(f"Organized by: {event['organizer_name']}", color="white"),
                    ft.Text(f"Date: {event['date']}", color="white"),
                    ft.Text(f"Address: {event['address']}", color="white"),
                    ft.Text("Description:", color="white", weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Text(
                            event.get('description', 'No description provided.'),
                            color="white"
                        ),
                        padding=10,
                        border=ft.border.all(1, "white"),
                        border_radius=5
                    ),
                    ft.ElevatedButton("Join Event", 
                                    on_click=join_event(event["_id"]),
                                    bgcolor="green",
                                    color="white", width=120, height=35)
                ]),
                padding=20,
                border=ft.border.all(1, "white"),
                border_radius=10,
                margin=5
            )
            events_list.controls.append(event_card)

    container.content = ft.Column([
        ft.Text("Available Events", size=24, weight=ft.FontWeight.BOLD, color=text_color_title),
        ft.Container(
            content=events_list,
            expand=True,
            border=ft.border.all(3, primary_color),
            border_radius=10,
            padding=10
        )
    ], expand=True)
    container.update()

def my_events_page(container, user):
    def toggle_bookmark(event_id):
        def handle_bookmark(e):
            if str(event_id) in user.get("bookmarked_events", []):
                users_collection.update_one(
                    {"_id": user["_id"]},
                    {"$pull": {"bookmarked_events": str(event_id)}}
                )
                user["bookmarked_events"].remove(str(event_id))
                e.control.icon = "bookmark_outline"
                e.control.bgcolor = bookmark_color_bg
            else:
                users_collection.update_one(
                    {"_id": user["_id"]},
                    {"$addToSet": {"bookmarked_events": str(event_id)}}
                )
                if "bookmarked_events" not in user:
                    user["bookmarked_events"] = []
                user["bookmarked_events"].append(str(event_id))
                e.control.icon = "bookmark"
                e.control.bgcolor = bookmark_color_bg_active
            container.update()
        return handle_bookmark

    def handle_delete_event(event_id):
        def handle_click(e):
            events_collection.delete_one({"_id": ObjectId(event_id)})
            
            success_dlg = ft.AlertDialog(
                title=ft.Text("Success"),
                content=ft.Text("Event has been permanently deleted!"),
                actions=[
                    ft.TextButton("OK", on_click=lambda e: refresh_page())
                ]
            )
            container.page.dialog = success_dlg
            success_dlg.open = True
            container.page.update()
        
        def refresh_page():
            my_events_page(container, user)
            
        return handle_click

    events = list(events_collection.find({"organizer_id": str(user["_id"])}))
    events_list = ft.ListView(spacing=10, expand=True)  
    
    if not events:
        events_list.controls.append(
            ft.Text("You haven't created any events yet.", color=text_color_light, size=13)
        )
    else:
        bookmarked_events = []
        other_events = []
        
        for event in events:
            is_bookmarked = str(event["_id"]) in user.get("bookmarked_events", [])
            bookmark_button = ft.IconButton(
                icon="bookmark" if is_bookmarked else "bookmark_outline",
                bgcolor=bookmark_color_bg_active if is_bookmarked else bookmark_color_bg,
                on_click=toggle_bookmark(event["_id"])
            )

            delete_button = ft.ElevatedButton(
                "Delete Event",
                on_click=handle_delete_event(str(event["_id"])),
                bgcolor="red",
                color="white",
                width=120, 
                height=35
            )

            event_card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(f"Event: {event['name']}", 
                               color="white", 
                               weight=ft.FontWeight.BOLD,
                               expand=True),
                        bookmark_button
                    ]),
                    ft.Text(f"Date: {event['date']}", color="white"),
                    ft.Text(f"Address: {event['address']}", color="white"),
                    ft.Text(f"Number of Volunteers: {len(event['volunteers'])}", color="white"),
                    ft.Text("Description:", color="white", weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Text(
                            event.get('description', 'No description provided.'),
                            color="white"
                        ),
                        padding=10,
                        border=ft.border.all(1, "white"),
                        border_radius=5
                    ),
                    ft.Row([
                        delete_button
                    ], alignment=ft.MainAxisAlignment.END)
                ]),
                padding=20,
                border=ft.border.all(3, brdr_color_bookmarked if is_bookmarked else brdr_color),
                border_radius=10,
                margin=5
            )
            
            if is_bookmarked:
                bookmarked_events.append(event_card)
            else:
                other_events.append(event_card)
        
        events_list.controls.extend(bookmarked_events)
        events_list.controls.extend(other_events)
    
    container.content = ft.Column([
        ft.Text("My Created Events", size=24, weight=ft.FontWeight.BOLD, color="white"),
        ft.Container(
            content=events_list,
            expand=True,
            border=ft.border.all(3, primary_color),
            border_radius=10,
            padding=10
        )
    ], expand=True)
    container.update()

def my_volunteering_page(container, user):
    def toggle_bookmark(event_id):
        def handle_bookmark(e):
            if str(event_id) in user.get("bookmarked_events", []):
                users_collection.update_one(
                    {"_id": user["_id"]},
                    {"$pull": {"bookmarked_events": str(event_id)}}
                )
                user["bookmarked_events"].remove(str(event_id))
                e.control.icon = "bookmark_outline"
                e.control.bgcolor = bookmark_color_bg
            else:
                users_collection.update_one(
                    {"_id": user["_id"]},
                    {"$addToSet": {"bookmarked_events": str(event_id)}}
                )
                if "bookmarked_events" not in user:
                    user["bookmarked_events"] = []
                user["bookmarked_events"].append(str(event_id))
                e.control.icon = "bookmark"
                e.control.bgcolor = bookmark_color_bg_active
            container.update()
        return handle_bookmark

    def handle_leave_event(event_id):
        def handle_click(e):
            # Remove user from event's volunteers list
            events_collection.update_one(
                {"_id": ObjectId(event_id)},
                {"$pull": {"volunteers": str(user["_id"])}}
            )
            
            success_dlg = ft.AlertDialog(
                title=ft.Text("Success"),
                content=ft.Text("You have left the event successfully!"),
                actions=[
                    ft.TextButton("OK", on_click=lambda e: refresh_page())
                ]
            )
            container.page.dialog = success_dlg
            success_dlg.open = True
            container.page.update()
        
        def refresh_page():
            my_volunteering_page(container, user)
            
        return handle_click

    # Get events where the user is a volunteer
    events = list(events_collection.find(
        {"volunteers": str(user["_id"])}
    ))
    
    events_list = ft.ListView(spacing=10, expand=True)

    main_column = ft.Column(spacing=20)
    main_column.controls.append(
        ft.Text("My Volunteering Events", 
            size=24, 
            weight=ft.FontWeight.BOLD, 
            color=text_color_title),
    )

    if not events:
        main_column.controls.append(
            ft.Text("You haven't joined any events yet.", color=text_color_light, size=13)
        )
    else:
        bookmarked_events = []
        other_events = []
        
        for event in events:
            is_bookmarked = str(event["_id"]) in user.get("bookmarked_events", [])
            bookmark_button = ft.IconButton(
                icon="bookmark" if is_bookmarked else "bookmark_outline",
                bgcolor=bookmark_color_bg_active if is_bookmarked else bookmark_color_bg,
                on_click=toggle_bookmark(event["_id"])
            )

            leave_button = ft.ElevatedButton(
                "Leave Event",
                on_click=handle_leave_event(str(event["_id"])),
                bgcolor="red",
                color="white", width=120, height=35
            )

            event_card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(f"Event: {event['name']}", 
                               color="white", 
                               weight=ft.FontWeight.BOLD,
                               expand=True),
                        bookmark_button
                    ]),
                    ft.Text(f"Organized by: {event['organizer_name']}", color="white"),
                    ft.Text(f"Date: {event['date']}", color="white"),
                    ft.Text(f"Address: {event['address']}", color="white"),
                    ft.Text("Description:", color="white", weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Text(
                            event.get('description', 'No description provided.'),
                            color="white"
                        ),
                        padding=10,
                        border=ft.border.all(1, "white"),
                        border_radius=5
                    ),
                    ft.Row([
                        leave_button
                    ], alignment=ft.MainAxisAlignment.END)
                ]),
                padding=20,
                border=ft.border.all(3, brdr_color_bookmarked if is_bookmarked else brdr_color),
                border_radius=10,
                margin=5,
                bgcolor="#2A2A2A"  
            )
            
            if is_bookmarked:
                bookmarked_events.append(event_card)
            else:
                other_events.append(event_card)
        
        events_list.controls.extend(bookmarked_events)
        events_list.controls.extend(other_events)
        main_column.controls.append(events_list)

    # Create main container 
    container.content = ft.Container(
        content=ft.Column([
            ft.Text("My Volunteering Events", 
                   size=24, 
                   weight=ft.FontWeight.BOLD, 
                   color=text_color_title),
            ft.Container(
            content=events_list,
            expand=True,
            border=ft.border.all(3, primary_color),
            border_radius=10,
            padding=10
        )
    ], expand=True)
    )
    
    container.update()

def settings_page(container, user):
    def change_password(e):
        if not current_password.value:
            error_text.value = "Please enter your current password"
            error_text.color = "red"
            container.update()
            return
            
        if not new_password.value:
            error_text.value = "Please enter a new password"
            error_text.color = "red"
            container.update()
            return

        # Verify current password
        user_check = users_collection.find_one({
            "_id": user["_id"],
            "password": current_password.value
        })

        if not user_check:
            error_text.value = "Current password is incorrect"
            error_text.color = "red"
            container.update()
            return

        # Update password in database
        users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"password": new_password.value}}
        )

        
        error_text.value = "Password changed successfully!"
        error_text.color = "green"
        
        # Clear password fields
        current_password.value = ""
        new_password.value = ""
        container.update()

    current_password = ft.TextField(
        label="Current Password",
        password=True,
        width=300,
        border_color="white"
    )
    
    new_password = ft.TextField(
        label="New Password",
        password=True,
        width=300,
        border_color="white"
    )

    error_text = ft.Text(
        "",  # Initially empty
        size=14,
        weight=ft.FontWeight.BOLD
    )

    btn_change = ft.ElevatedButton(
        "Change Password",
        on_click=change_password,
        bgcolor="green", 
        color="white", 
        width=170, 
        height=40
    )

    container.content = ft.Column([
        ft.Text("Settings", size=24, weight=ft.FontWeight.BOLD, color=text_color_title),
        ft.Divider(height=20, color="transparent"),
        ft.Text("Change Password", size=16, weight=ft.FontWeight.BOLD, color="white"),
        current_password,
        new_password,
        error_text, 
        btn_change
    ], 
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    spacing=20)
    
    container.update()
def bookmarked_posts_page(container, user):
    def toggle_bookmark(event_id):
        def handle_bookmark(e):
            if str(event_id) in user.get("bookmarked_events", []):
                users_collection.update_one(
                    {"_id": user["_id"]},
                    {"$pull": {"bookmarked_events": str(event_id)}}
                )
                user["bookmarked_events"].remove(str(event_id))
                # Refresh the page after removing bookmark
                bookmarked_posts_page(container, user)
            container.update()
        return handle_bookmark

    # Get all bookmarked event IDs for the user
    bookmarked_ids = user.get("bookmarked_events", [])
    
    # Convert string IDs to ObjectId for Mongo
    object_ids = [ObjectId(id_str) for id_str in bookmarked_ids]
    
    # Fetch bookmarked events
    events = list(events_collection.find({"_id": {"$in": object_ids}}))
    
    events_list = ft.ListView(spacing=10, expand=True)
    
    if not events:
        events_list.controls.append(
            ft.Text("No bookmarked events.", color=text_color_light, size=13)
        )
    else:
        for event in events:
            event_card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(f"Event: {event['name']}", 
                               color="white", 
                               weight=ft.FontWeight.BOLD,
                               expand=True),
                        ft.IconButton(
                            icon="bookmark",
                            bgcolor="yellow",
                            on_click=toggle_bookmark(event["_id"])
                        )
                    ]),
                    ft.Text(f"Organized by: {event['organizer_name']}", color="white"),
                    ft.Text(f"Date: {event['date']}", color="white"),
                    ft.Text(f"Address: {event['address']}", color="white"),
                    ft.Text("Description:", color="white", weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Text(
                            event.get('description', 'No description provided.'),
                            color="white"
                        ),
                        padding=10,
                        border=ft.border.all(1, "white"),
                        border_radius=5
                    ),
                ]),
                padding=20,
                border=ft.border.all(3, brdr_color_bookmarked),
                border_radius=10,
                margin=5,
                bgcolor="#2A2A2A"
            )
            events_list.controls.append(event_card)

    container.content = ft.Column([
        ft.Text("Bookmarked Events", 
               size=24, 
               weight=ft.FontWeight.BOLD, 
               color=text_color_title),
        ft.Container(
            content=events_list,
            expand=True,
            border=ft.border.all(3, primary_color),
            border_radius=10,
            padding=10
        )
    ], expand=True)
    container.update()

def user_profile_page(container, user):
    # Create text fields for editing
    first_name = ft.TextField(
        label="First Name",
        value=user['first_name'],
        width=300,
        border_color="white"
    )
    
    last_name = ft.TextField(
        label="Last Name",
        value=user['last_name'],
        width=300,
        border_color="white"
    )
    
    country = ft.TextField(
        label="Country",
        value=user.get('country', ''),  
        width=300,
        border_color="white"
    )
    
    city = ft.TextField(
        label="City/Province",
        value=user.get('city', ''),  
        width=300,
        border_color="white"
    )

    # Status text for showing success/error messages
    status_text = ft.Text("", color="white")

    def save_changes(e):
        # Update user information in database
        users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {
                "first_name": first_name.value,
                "last_name": last_name.value,
                "country": country.value,
                "city": city.value
            }}
        )
        
        # Update local user object
        user['first_name'] = first_name.value
        user['last_name'] = last_name.value
        user['country'] = country.value
        user['city'] = city.value

       
        status_text.value = "Profile updated successfully!"
        status_text.color = "green"
        container.update()

        
        success_dlg = ft.AlertDialog(
            title=ft.Text("Success"),
            content=ft.Text("Your profile has been updated successfully!"),
            actions=[
                ft.TextButton("OK", on_click=lambda e: close_dialog(success_dlg))
            ]
        )
        container.page.dialog = success_dlg
        success_dlg.open = True
        container.page.update()

    def close_dialog(dialog):
        dialog.open = False
        container.page.update()

    container.content = ft.Column([
        ft.Text("My Profile", size=24, weight=ft.FontWeight.BOLD, color=text_color_title),
        ft.Divider(height=20, color="transparent"),
        
        # Personal Information Section
        ft.Text("Personal Information", size=16, weight=ft.FontWeight.BOLD, color=text_color),
        first_name,
        last_name,
        ft.Divider(height=20, color="transparent"),
        
        # Location Information Section
        ft.Text("Location", size=16, weight=ft.FontWeight.BOLD, color=text_color),
        country,
        city,
        ft.Divider(height=20, color="transparent"),
        
        # Account Information Section (read-only)
        ft.Text("Account Information", size=16, weight=ft.FontWeight.BOLD, color=text_color),
        ft.Text(f"Email: {user['email']}", color=text_color),
        ft.Text(f"Role: {user['role'].capitalize()}", color=text_color),
        ft.Divider(height=20, color="transparent"),
        
        # Save Button
        ft.ElevatedButton(
            "Save Changes", 
            on_click=save_changes, 
            bgcolor="green", 
            color="white", 
            width=170, 
            height=40
        ),
        
        status_text
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    spacing=10)
    
    container.update()
def logout_user(page):
    # Handle logout logic herex
    page.title = "Logged Out"
    page.clean()  
    main(page)  

ft.app(target=main)
