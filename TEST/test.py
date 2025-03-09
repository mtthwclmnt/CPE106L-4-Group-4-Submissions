import flet as ft
import re  # For email validation

def main(page: ft.Page):
    page.title = "User Authentication"
    page.window_width = 1000
    page.window_height = 600
    page.window_resizable = False
    
    user_data = {}
    user_events = [
        {"title": "Community Cleanup", "date": "March 15, 2025", "location": "City Park"},
        {"title": "Charity Run", "date": "April 10, 2025", "location": "Downtown"},
    ] * 5  # Repeating events for demonstration

    def validate_email(email):
        """Checks if the email follows the correct format."""
        return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

    def validate_signup(e):
        """Validates the signup form and navigates to role selection if successful."""
        errors = False
        
        for field in [first_name, last_name, email, password]:
            if not field.value.strip():
                field.border_color = "red"
                field.error_text = "This field is required"
                errors = True
            else:
                field.border_color = None
                field.error_text = None

        # Validate email format
        if email.value.strip() and not validate_email(email.value):
            email.border_color = "red"
            email.error_text = "Enter a valid email (sample@dummy.com)"
            errors = True

        if not errors:
            print("Signup successful! Redirecting to role selection...")
            page.go("/role-selection")

        page.update()

    def validate_login(e):
        """Validates the login form and navigates to home if successful."""
        errors = False

        for field in [login_email, login_password]:
            if not field.value.strip():
                field.border_color = "red"
                field.error_text = "This field is required"
                errors = True
            else:
                field.border_color = None
                field.error_text = None

        # Validate email format
        if login_email.value.strip() and not validate_email(login_email.value):
            login_email.border_color = "red"
            login_email.error_text = "Enter a valid email (sample@dummy.com)"
            errors = True

        if not errors:
            print("Login successful! Redirecting to home...")
            page.go("/home")

        page.update()

    def handle_role_selection(e):
        """Redirects user based on role selection."""
        if e.control.text == "Organizer":
            page.go("/organizer-dashboard")
        else:
            page.go("/home")

    def update_content(content):
        """Updates the right-side content dynamically."""
        right_content.content = content
        page.update()
        
    def route_change(route):
        global first_name, last_name, country, city, email, password
        global login_email, login_password  # Ensure login fields are globally accessible

        page.views.clear()

        if page.route == "/auth":
            page.views.append(
                ft.View(
                    "/auth",
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Welcome!", size=30, weight=ft.FontWeight.BOLD),
                                    ft.Text("Please choose an option:", size=16),
                                    ft.ElevatedButton("Sign Up", on_click=lambda e: page.go("/signup"), width=200),
                                    ft.ElevatedButton("Log In", on_click=lambda e: page.go("/login"), width=200),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=20,
                            ),
                            alignment=ft.alignment.center,
                            expand=True,
                        )
                    ],
                )
            )

        elif page.route == "/signup":
            first_name = ft.TextField(label="First Name *", border_color=None, width=300)
            last_name = ft.TextField(label="Last Name *", border_color=None, width=300)
            country = ft.TextField(label="Country", width=300)
            city = ft.TextField(label="City/Province", width=300)
            email = ft.TextField(label="Email *", border_color=None, width=300)
            password = ft.TextField(label="Create Password *", password=True, border_color=None, width=300)

            page.views.append(
                ft.View(
                    "/signup",
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Sign Up", size=24, weight=ft.FontWeight.BOLD),
                                    first_name,
                                    last_name,
                                    country,
                                    city,
                                    ft.Container(ft.Divider(thickness=1), width=250),
                                    email,
                                    password,
                                    ft.ElevatedButton("Submit", on_click=validate_signup, width=200),
                                    ft.ElevatedButton("Back", on_click=lambda e: page.go("/auth"), width=200),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10,
                            ),
                            alignment=ft.alignment.center,
                            expand=True,
                        )
                    ],
                )
            )

        elif page.route == "/role-selection":
            page.views.append(
                ft.View(
                    "/role-selection",
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Select Your Role", size=24, weight=ft.FontWeight.BOLD),
                                    ft.ElevatedButton("Volunteer", on_click=handle_role_selection, width=200),
                                    ft.ElevatedButton("Organizer", on_click=handle_role_selection, width=200),
                                    ft.ElevatedButton("Back", on_click=lambda e: page.go("/signup"), width=200),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=20,
                            ),
                            alignment=ft.alignment.center,
                            expand=True,
                        )
                    ],
                )
            )

        elif page.route == "/login":
            login_email = ft.TextField(label="Email *", border_color=None, width=300)
            login_password = ft.TextField(label="Password *", password=True, border_color=None, width=300)

            page.views.append(
                ft.View(
                    "/login",
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Log In", size=24, weight=ft.FontWeight.BOLD),
                                    login_email,
                                    login_password,
                                    ft.ElevatedButton("Submit", on_click=validate_login, width=200),
                                    ft.ElevatedButton("Back", on_click=lambda e: page.go("/auth"), width=200),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10,
                            ),
                            alignment=ft.alignment.center,
                            expand=True,
                        )
                    ],
                )
            )

        elif page.route == "/organizer-dashboard":
            page.views.append(
                ft.View(
                    "/organizer-dashboard",
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Organizer Dashboard", size=24, weight=ft.FontWeight.BOLD),
                                    ft.ElevatedButton("Create New Event", width=200),
                                    ft.ElevatedButton("View My Events", width=200),
                                    ft.ElevatedButton("Back to Home", on_click=lambda e: page.go("/home"), width=200),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=20,
                            ),
                            alignment=ft.alignment.center,
                            expand=True,
                        )
                    ],
                )
            )

        elif page.route == "/home":
            global right_content
            
            page.views.clear()
            
            home_content = ft.Container(
                content=ft.Column(
                    [
                        ft.Text("User Profile", size=24, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                        ft.Text(f"Name: {user_data.get('first_name', 'N/A')} {user_data.get('last_name', 'N/A')}", color="#FFFFFF", size=18),
                        ft.Text(f"Email: {user_data.get('email', 'N/A')}", color="#FFFFFF", size=18),
                        ft.Text(f"Country: {user_data.get('country', 'N/A')}", color="#FFFFFF", size=18),
                        ft.Text(f"City/Province: {user_data.get('city', 'N/A')}", color="#FFFFFF", size=18),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                bgcolor="#1976D2",
                padding=20,
                border_radius=10,
                margin=5,
            )
            
            schedule_content = ft.ListView(
                controls=[
                    ft.Container(
                        content=ft.Row([
                            ft.Container(
                                content=ft.Image(src="event_placeholder.png", width=80, height=80, border_radius=10),
                                width=80,
                                height=80,
                                margin=ft.margin.only(right=10),
                            ),
                            ft.Column([
                                ft.Text(event["title"], size=18, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                                ft.Text(f"Date: {event['date']}", size=14, color="#FFFFFF"),
                                ft.Text(f"Location: {event['location']}", size=14, color="#FFFFFF"),
                            ])
                        ], alignment=ft.MainAxisAlignment.START),
                        padding=10,
                        border_radius=10,
                        bgcolor="#1976D2",
                        margin=5,
                    ) for event in user_events
                ],
                expand=True,
            )
            
            right_content = ft.Container(
                content=home_content,
                alignment=ft.alignment.center,
                expand=True,
            )
            
            sidebar = ft.Container(
                content=ft.Column([
                    ft.Text("User Profile", size=20, weight=ft.FontWeight.BOLD),
                    ft.Image(src="profile_placeholder.png", width=80, height=80),
                    ft.ElevatedButton("Home Page", on_click=lambda e: update_content(home_content)),
                    ft.ElevatedButton("User Schedule", on_click=lambda e: update_content(schedule_content)),
                    ft.ElevatedButton("Events Page", on_click=lambda e: update_content(ft.Text("Your Events", size=24, weight=ft.FontWeight.BOLD))),
                    ft.ElevatedButton("Bookmarked Posts", on_click=lambda e: update_content(ft.Text("Your Bookmarked Posts", size=24, weight=ft.FontWeight.BOLD))),
                    ft.ElevatedButton("Settings", on_click=lambda e: update_content(ft.Text("Settings", size=24, weight=ft.FontWeight.BOLD))),
                    ft.ElevatedButton("Logout", on_click=lambda e: page.go("/auth")),
                ], spacing=10),
                width=250,
                padding=10,
            )
            
            page.views.append(
                ft.View(
                    "/home",
                    [
                        ft.Row([
                            sidebar,
                            ft.VerticalDivider(width=1),
                            right_content,
                        ])
                    ],
                )
            )

        page.update()

    # Set initial route
    page.on_route_change = route_change
    page.go("/auth")

ft.app(target=main)
