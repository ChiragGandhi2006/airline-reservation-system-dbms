import customtkinter as ctk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime
import os
import webbrowser
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AirlineReservationSystem:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Airline Reservation System")
        self.root.geometry("1400x800")
         
        # Database connection
        self.conn = None
        self.cursor = None
        self.current_user = None
        
        # OTP storage
        self.pending_otp = {}
        
        # Show login screen
        self.show_login()
        
        self.root.mainloop()
    
    def connect_db(self):
        """Establish database connection"""
        try:
            self.conn = mysql.connector.connect(
                host="localhost", 
                user="root",
                password="Pass@123",
                database="AIRLINE_RESERVATION"
            )
            self.cursor = self.conn.cursor()
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Connection failed: {err}")
            return False
    
    def generate_otp(self):
        """Generate a 6-digit OTP"""
        return str(random.randint(100000, 999999))
    
    def send_otp_email(self, email, otp):
        """Send OTP via email (simulated - configure with your SMTP settings)"""
        try:
            # For demo purposes, we'll just show the OTP in a message box
            # In production, configure SMTP settings below
            
            """
            # Uncomment and configure for real email sending:
            sender_email = "your-email@gmail.com"
            sender_password = "your-app-password"
            
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = email
            message["Subject"] = "Airline Reservation System - OTP Verification"
            
            body = f'''
            Dear Passenger,
            
            Your OTP for registration is: {otp}
            
            This OTP is valid for 5 minutes.
            
            Thank you for choosing our airline!
            '''
            
            message.attach(MIMEText(body, "plain"))
            
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(message)
            
            return True
            """
            
            # Demo mode - show OTP in message box
            messagebox.showinfo("OTP Sent", f"Demo Mode: Your OTP is {otp}\n\n(In production, this would be sent to {email})")
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send OTP: {e}")
            return False
    
    def show_login(self):
        """Display login screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        login_frame = ctk.CTkFrame(self.root, width=450, height=500, corner_radius=15)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        title = ctk.CTkLabel(
            login_frame, 
            text="✈ Airline Reservation System",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(40, 10))
        
        subtitle = ctk.CTkLabel(
            login_frame,
            text="Please login to continue",
            font=ctk.CTkFont(size=15),
            text_color="gray"
        )
        subtitle.pack(pady=(0, 30))
        
        username_label = ctk.CTkLabel(login_frame, text="Username", font=ctk.CTkFont(size=14))
        username_label.pack(pady=(10, 5))
        
        self.username_entry = ctk.CTkEntry(
            login_frame,
            width=300,
            height=45,
            placeholder_text="Enter username",
            font=ctk.CTkFont(size=13)
        )
        self.username_entry.pack(pady=(0, 15))
        
        password_label = ctk.CTkLabel(login_frame, text="Password", font=ctk.CTkFont(size=14))
        password_label.pack(pady=(10, 5))
        
        self.password_entry = ctk.CTkEntry(
            login_frame,
            width=300,
            height=45,
            placeholder_text="Enter password",
            show="*",
            font=ctk.CTkFont(size=13)
        )
        self.password_entry.pack(pady=(0, 25))
        
        login_btn = ctk.CTkButton(
            login_frame,
            text="Login",
            width=300,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.perform_login
        )
        login_btn.pack(pady=(10, 20))
        
        self.password_entry.bind('<Return>', lambda e: self.perform_login())
    
    def perform_login(self):
        """Authenticate user"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        if not self.connect_db():
            return
        
        try:
            query = "SELECT UserID, Username, Role FROM Users WHERE Username=%s AND Password=%s"
            self.cursor.execute(query, (username, password))
            result = self.cursor.fetchone() # fetchone() means “give me the next single row from the query result”.
            
            if result:
                self.current_user = {
                    'id': result[0],
                    'username': result[1],
                    'role': result[2]
                }
                self.show_dashboard()
            else:
                messagebox.showerror("Error", "Invalid username or password")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Login failed: {err}")
    
    def show_dashboard(self):
        """Display main dashboard with navigation"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        nav_frame = ctk.CTkFrame(main_container, height=70, corner_radius=0)
        nav_frame.pack(fill="x", side="top")
        
        title = ctk.CTkLabel(
            nav_frame,
            text="✈ Airline Reservation System",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(side="left", padx=30, pady=20)
        # Shows logged-in username and role on the right.
        user_label = ctk.CTkLabel(
            nav_frame,
            text=f"Welcome, {self.current_user['username']} ({self.current_user['role']})",
            font=ctk.CTkFont(size=14)
        )
        user_label.pack(side="right", padx=20)
        # Logout button that calls self.logout to disconnect and return to login.
        logout_btn = ctk.CTkButton(
            nav_frame,
            text="Logout",
            width=100,
            height=35,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            command=self.logout
        )
        logout_btn.pack(side="right", padx=(0, 10))
        
        content_container = ctk.CTkFrame(main_container, fg_color="transparent")
        content_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        sidebar = ctk.CTkFrame(content_container, width=250, corner_radius=0)
        sidebar.pack(fill="y", side="left")
        
        menu_items = [
            ("🏠 Dashboard", self.show_dashboard_page),
            ("👥 Passengers", self.show_passengers),
            ("✈ Flights", self.show_flights),
            ("🏢 Airports", self.show_airports),
            ("🎫 Bookings", self.show_bookings),
            ("🗑 Manage Bookings", self.show_manage_bookings),
            ("📊 Analysis", self.show_analysis)
        ]
        
        for text, command in menu_items:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                width=230,
                height=45,
                corner_radius=8,
                font=ctk.CTkFont(size=15),
                anchor="w",
                command=command,
                fg_color="transparent",
                hover_color=("gray70", "gray30")
            )
            btn.pack(padx=10, pady=5)
        
        self.content_frame = ctk.CTkFrame(content_container, corner_radius=0)
        self.content_frame.pack(fill="both", expand=True, side="right")
        
        self.show_dashboard_page()#Widges bata ye ga

    
    def logout(self):
        """Logout and return to login screen"""
        if self.conn:
            self.conn.close()
        self.current_user = None
        self.show_login()
    
    def clear_content(self):
        """Clear content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard_page(self):
        """Display dashboard with statistics"""
        self.clear_content()
        #Header area for dashboard title.
        header_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(20, 10))
        
        title = ctk.CTkLabel(
            header_frame,
            text="Dashboard Overview",
            font=ctk.CTkFont(size=30, weight="bold")
        )
        title.pack(side="left")
        
        stats_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=30, pady=20)
        
        try:
            self.cursor.execute("SELECT COUNT(*) FROM Passenger")
            total_passengers = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM Flight")
            total_flights = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM Booking WHERE BookingStatus='Confirmed'")
            confirmed_bookings = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT SUM(Amount) FROM Payment WHERE PaymentStatus='Success'")
            revenue = self.cursor.fetchone()[0] or 0
            
            stats = [
                ("Total Passengers", total_passengers, "#3498DB"),
                ("Total Flights", total_flights, "#9B59B6"),
                ("Confirmed Bookings", confirmed_bookings, "#27AE60"),
                ("Total Revenue", f"₹{revenue:,.2f}", "#E74C3C")
            ]
            
            for i, (label, value, color) in enumerate(stats):
                card = ctk.CTkFrame(stats_frame, fg_color=color, corner_radius=10)
                card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
                stats_frame.grid_columnconfigure(i, weight=1)
                
                ctk.CTkLabel(
                    card,
                    text=label,
                    font=ctk.CTkFont(size=15),
                    text_color="white"
                ).pack(pady=(20, 5))
                
                ctk.CTkLabel(
                    card,
                    text=str(value),
                    font=ctk.CTkFont(size=26, weight="bold"),
                    text_color="white"
                ).pack(pady=(0, 20))
        
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load statistics: {err}")
        # Recent Booking Section
        activity_frame = ctk.CTkFrame(self.content_frame)
        activity_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        ctk.CTkLabel(
            activity_frame,
            text="Recent Bookings",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=15)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                       background="#2b2b2b",
                       foreground="white",
                       rowheight=32,
                       fieldbackground="#2b2b2b",
                       borderwidth=0,
       
                       font=('Arial', 11))
        style.map('Treeview', background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading",
                       background="#1f538d",
                       foreground="white",
                       relief="flat",
                       font=('Arial', 12, 'bold'))
        
        tree_frame = ctk.CTkFrame(activity_frame, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical")
        
        columns = ("Booking ID", "Passenger", "Flight", "Status", "Date")
        recent_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=tree_scroll.set
        )
        
        tree_scroll.config(command=recent_tree.yview)
        
        for col in columns:
            recent_tree.heading(col, text=col)
            recent_tree.column(col, width=150, anchor="center")
        
        tree_scroll.pack(side="right", fill="y")
        recent_tree.pack(fill="both", expand=True)
        
        try:
            query = """
                SELECT b.BookingID, CONCAT(p.FirstName, ' ', p.LastName), 
                       f.FlightNumber, b.BookingStatus, b.BookingDate
                FROM Booking b
                JOIN Passenger p ON b.PassengerID = p.PassengerID
                JOIN Flight f ON b.FlightID = f.FlightID
                ORDER BY b.BookingDate DESC
                LIMIT 10
            """
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                recent_tree.insert("", "end", values=row)
        except:
            pass
    #Passenger Management Section
    def show_passengers(self):
        """Display Passengers CRUD interface"""
        self.clear_content()
        #Header Title
        header_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(20, 10))
        
        title = ctk.CTkLabel(
            header_frame,
            text="Passenger Management",
            font=ctk.CTkFont(size=30, weight="bold")
        )
        title.pack(side="left")
        #----------------------
        actions_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        actions_frame.pack(fill="x", padx=30, pady=10)
        
        self.passenger_search = ctk.CTkEntry(
            actions_frame,
            placeholder_text="Search by name, email, or passport...",
            width=300,
            height=38,
            font=ctk.CTkFont(size=13)
        )
        self.passenger_search.pack(side="left", padx=(0, 10))
        
        search_btn = ctk.CTkButton(
            actions_frame,
            text="Search",
            width=100,
            height=38,
            font=ctk.CTkFont(size=13),
            command=self.search_passengers
        )
        search_btn.pack(side="left", padx=5)
        
        refresh_btn = ctk.CTkButton(
            actions_frame,
            text="Refresh",
            width=100,
            height=38,
            font=ctk.CTkFont(size=13),
            fg_color="gray",
            hover_color="darkgray",
            command=self.load_passengers
        )
        refresh_btn.pack(side="left", padx=5)
        #Add passenger button opens a form (with OTP) via self.add_passenger.
        add_btn = ctk.CTkButton(
            actions_frame,
            text="+ Add Passenger",
            width=150,
            height=38,
            font=ctk.CTkFont(size=13),
            fg_color="#27AE60",
            hover_color="#229954",
            command=self.add_passenger
        )
        add_btn.pack(side="right", padx=5)
        
        table_frame = ctk.CTkFrame(self.content_frame)
        table_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                       background="#2b2b2b",
                       foreground="white",
                       rowheight=32,
                       fieldbackground="#2b2b2b",
                       borderwidth=0,
                       font=('Arial', 11))
        style.map('Treeview', background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading",
                       background="#1f538d",
                       foreground="white",
                       relief="flat",
                       font=('Arial', 12, 'bold'))
        
        tree_scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
        tree_scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        
        columns = ("ID", "Full Name", "DOB", "Gender", "Phone", "Email", "Passport ID")
        self.passenger_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
            selectmode="browse"
        )
        
        tree_scroll_y.config(command=self.passenger_tree.yview)
        tree_scroll_x.config(command=self.passenger_tree.xview)
        
        column_widths = [60, 200, 120, 100, 130, 220, 130]
        for col, width in zip(columns, column_widths):
            self.passenger_tree.heading(col, text=col)
            self.passenger_tree.column(col, width=width, anchor="center")
        
        tree_scroll_y.pack(side="right", fill="y")
        tree_scroll_x.pack(side="bottom", fill="x")
        self.passenger_tree.pack(fill="both", expand=True)
        
        btn_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=10)
        
        edit_btn = ctk.CTkButton(
            btn_frame,
            text="Edit Selected",
            width=130,
            height=38,
            font=ctk.CTkFont(size=13),
            fg_color="#3498DB",
            hover_color="#2980B9",
            command=self.edit_passenger#The command parameter tells the button what function to run when it is clicked.
        )
        edit_btn.pack(side="left", padx=5)
        
        delete_btn = ctk.CTkButton(
            btn_frame,
            text="Delete Selected",
            width=130,
            height=38,
            font=ctk.CTkFont(size=13),
            fg_color="#E74C3C",
            hover_color="#C0392B",
            command=self.delete_passenger
        )
        delete_btn.pack(side="left", padx=5)
        
        self.load_passengers()
    
    def load_passengers(self, search_term=""):
        """Load passengers from database"""
        for item in self.passenger_tree.get_children():
            self.passenger_tree.delete(item)
        
        try:
            if search_term:
                query = """
                    SELECT PassengerID, CONCAT(FirstName, ' ', LastName), DOB, Gender, 
                           Phone, Email, PassportNo
                    FROM Passenger 
                    WHERE FirstName LIKE %s OR LastName LIKE %s OR Email LIKE %s OR PassportNo LIKE %s
                """
                self.cursor.execute(query, (f"%{search_term}%", f"%{search_term}%", 
                                           f"%{search_term}%", f"%{search_term}%"))
            else:
                query = """
                    SELECT PassengerID, CONCAT(FirstName, ' ', LastName), DOB, Gender, 
                           Phone, Email, PassportNo
                    FROM Passenger
                """
                self.cursor.execute(query)
            
            rows = self.cursor.fetchall()
            for row in rows:
                self.passenger_tree.insert("", "end", values=row)
                
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load passengers: {err}")
    
    def search_passengers(self):
        """Search passengers"""
        search_term = self.passenger_search.get()
        self.load_passengers(search_term)
    
    def add_passenger(self):
        """Open form to add new passenger with OTP"""
        self.passenger_form_with_otp("Add Passenger")
    #edit_passenger requires a selection in the tree. If none, shows a warning.
    def edit_passenger(self):
        """Open form to edit selected passenger"""
        selected = self.passenger_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a passenger to edit")
            return
        
        passenger_id = self.passenger_tree.item(selected[0])['values'][0]
        
        try:
            query = """
                SELECT PassengerID, FirstName, LastName, DOB, Gender, Phone, Email, PassportNo
                FROM Passenger WHERE PassengerID = %s
            """
            self.cursor.execute(query, (passenger_id,))
            data = self.cursor.fetchone()
            
            if data:
                self.passenger_form("Edit Passenger", data)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to fetch passenger data: {err}")
    
    def passenger_form_with_otp(self, title):
        """Display passenger form with OTP verification for new registration"""
        form_window = ctk.CTkToplevel(self.root)#creates a popup linked to main window.
        form_window.title(title)#sets its window title (e.g., "Add Passenger").
        form_window.geometry("550x750")#sets its size.
        form_window.transient(self.root)#makes it a transient window (keeps it on top of parent).
        form_window.grab_set()#makes it modal — user must interact with this window before returning to the main app.
        
        form_window.update_idletasks()#Forces Tkinter to update all pending GUI operations (so window size is calculated correctly before centering).
        width = form_window.winfo_width()#Gets the current width of the popup window
        height = form_window.winfo_height()#Gets the height of the popup window.
        x = (form_window.winfo_screenwidth() // 2) - (width // 2)#Calculates the X position to center the window horizontally on the screen.
        y = (form_window.winfo_screenheight() // 2) - (height // 2)#Calculates the Y position to center the window vertically.
        form_window.geometry(f'{width}x{height}+{x}+{y}')#Moves the window to that centered position on screen.
        
        main_frame = ctk.CTkScrollableFrame(form_window)
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text=title,
            font=ctk.CTkFont(size=26, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        fields = {}
        
        ctk.CTkLabel(main_frame, text="First Name *", anchor="w", font=ctk.CTkFont(size=13)).pack(fill="x", pady=(10, 5))
        fields['FirstName'] = ctk.CTkEntry(main_frame, height=38, placeholder_text="Enter first name", font=ctk.CTkFont(size=13))
        fields['FirstName'].pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(main_frame, text="Last Name *", anchor="w", font=ctk.CTkFont(size=13)).pack(fill="x", pady=(10, 5))
        fields['LastName'] = ctk.CTkEntry(main_frame, height=38, placeholder_text="Enter last name", font=ctk.CTkFont(size=13))
        fields['LastName'].pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(main_frame, text="Date of Birth (YYYY-MM-DD) *", anchor="w", font=ctk.CTkFont(size=13)).pack(fill="x", pady=(10, 5))
        fields['DOB'] = ctk.CTkEntry(main_frame, height=38, placeholder_text="1990-01-01", font=ctk.CTkFont(size=13))
        fields['DOB'].pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(main_frame, text="Gender *", anchor="w", font=ctk.CTkFont(size=13)).pack(fill="x", pady=(10, 5))
        fields['Gender'] = ctk.CTkComboBox(main_frame, height=38, values=["Male", "Female", "Other"], font=ctk.CTkFont(size=13))
        fields['Gender'].pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(main_frame, text="Phone *", anchor="w", font=ctk.CTkFont(size=13)).pack(fill="x", pady=(10, 5))
        fields['Phone'] = ctk.CTkEntry(main_frame, height=38, placeholder_text="1234567890", font=ctk.CTkFont(size=13))
        fields['Phone'].pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(main_frame, text="Email *", anchor="w", font=ctk.CTkFont(size=13)).pack(fill="x", pady=(10, 5))
        fields['Email'] = ctk.CTkEntry(main_frame, height=38, placeholder_text="email@example.com", font=ctk.CTkFont(size=13))
        fields['Email'].pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(main_frame, text="Passport ID *", anchor="w", font=ctk.CTkFont(size=13)).pack(fill="x", pady=(10, 5))
        fields['PassportNo'] = ctk.CTkEntry(main_frame, height=38, placeholder_text="P1234567", font=ctk.CTkFont(size=13))
        fields['PassportNo'].pack(fill="x", pady=(0, 10))
        
        # OTP Section
        otp_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        otp_frame.pack(fill="x", pady=(20, 10))
        
        send_otp_btn = ctk.CTkButton(
            otp_frame,
            text="Send OTP to Email",
            width=200,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#9B59B6",
            hover_color="#8E44AD"
        )
        send_otp_btn.pack(pady=5)
        
        ctk.CTkLabel(main_frame, text="Enter OTP *", anchor="w", font=ctk.CTkFont(size=13)).pack(fill="x", pady=(10, 5))
        otp_entry = ctk.CTkEntry(main_frame, height=38, placeholder_text="Enter 6-digit OTP", font=ctk.CTkFont(size=13))
        otp_entry.pack(fill="x", pady=(0, 10))
        otp_entry.configure(state="disabled")
        
        def send_otp():#Defines a function named send_otp. This is called when the user clicks the Send OTP to Email button.
            email = fields['Email'].get()
            if not email:
                messagebox.showerror("Error", "Please enter email address first")
                return
            
            otp = self.generate_otp()
            if self.send_otp_email(email, otp):#If the email was sent successfully:
                self.pending_otp[email] = otp
                otp_entry.configure(state="normal")
                send_otp_btn.configure(text="Resend OTP")
                messagebox.showinfo("Success", "OTP sent to your email!")
        
        send_otp_btn.configure(command=send_otp)
        
        def save_passenger():
            if not all([fields['FirstName'].get(), fields['LastName'].get(), 
                       fields['DOB'].get(), fields['Gender'].get(), 
                       fields['Phone'].get(), fields['Email'].get(), 
                       fields['PassportNo'].get()]):
                messagebox.showerror("Error", "All fields are required")
                return
            
            email = fields['Email'].get()
            entered_otp = otp_entry.get()#Reads the email again and reads the OTP the user typed into the OTP entry (otp_entry.get()).
            
            if email not in self.pending_otp:
                messagebox.showerror("Error", "Please request OTP first")
                return
            
            if entered_otp != self.pending_otp[email]:
                messagebox.showerror("Error", "Invalid OTP. Please try again.")
                return
            
            try:
                query = """
                    INSERT INTO Passenger 
                    (FirstName, LastName, DOB, Gender, Phone, Email, PassportNo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    fields['FirstName'].get(),
                    fields['LastName'].get(),
                    fields['DOB'].get(),
                    fields['Gender'].get(),
                    fields['Phone'].get(),
                    fields['Email'].get(),
                    fields['PassportNo'].get()
                )
                
                self.cursor.execute(query, values)
                self.conn.commit()
                
                # Clear OTP after successful registration
                del self.pending_otp[email]
                
                messagebox.showinfo("Success", "Passenger registered successfully!")
                form_window.destroy()
                self.load_passengers()
                
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to save passenger: {err}")
        
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(20, 0))
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="Register Passenger",
            width=200,
            height=42,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#27AE60",
            hover_color="#229954",
            command=save_passenger
        )
        save_btn.pack(side="left", padx=(0, 10))
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=150,
            height=42,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="gray",
            hover_color="darkgray",
            command=form_window.destroy
        )
        cancel_btn.pack(side="left")
    
    def passenger_form(self, title, data=None):
        """Display passenger form for edit (without OTP)"""
        form_window = ctk.CTkToplevel(self.root)
        form_window.title(title)
        form_window.geometry("550x700")
        form_window.transient(self.root)
        form_window.grab_set()
        
        form_window.update_idletasks()
        width = form_window.winfo_width()
        height = form_window.winfo_height()
        x = (form_window.winfo_screenwidth() // 2) - (width // 2)
        y = (form_window.winfo_screenheight() // 2) - (height // 2)
        form_window.geometry(f'{width}x{height}+{x}+{y}')
        
        main_frame = ctk.CTkFrame(form_window)
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text=title,
            font=ctk.CTkFont(size=26, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        fields = {}
        
        ctk.CTkLabel(main_frame, text="First Name *", anchor="w", font=ctk.CTkFont(size=13)).pack(fill="x", pady=(10, 5))
        fields['FirstName'] = ctk.CTkEntry(main_frame, height=38, placeholder_text="Enter first name", font=ctk.CTkFont(size=13))
        fields['FirstName'].pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(main_frame, text="Last Name *", anchor="w", font=ctk.CTkFont(size=13)).pack(fill="x", pady=(10, 5))
        fields['LastName'] = ctk.CTkEntry(main_frame, height=38, placeholder_text="Enter last name", font=ctk.CTkFont(size=13))
        fields['LastName'].pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(main_frame, text="Date of Birth (YYYY-MM-DD) *", anchor="w", font=ctk.CTkFont(size=13)).pack(fill="x", pady=(10, 5))
        fields['DOB'] = ctk.CTkEntry(main_frame, height=38, placeholder_text="1990-01-01", font=ctk.CTkFont(size=13))
        fields['DOB'].pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(main_frame, text="Gender *", anchor="w", font=ctk.CTkFont(size=13)).pack(fill="x", pady=(10, 5))
        fields['Gender'] = ctk.CTkComboBox(main_frame, height=38, values=["Male", "Female", "Other"], font=ctk.CTkFont(size=13))
        fields['Gender'].pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(main_frame, text="Phone *", anchor="w", font=ctk.CTkFont(size=13)).pack(fill="x", pady=(10, 5))
        fields['Phone'] = ctk.CTkEntry(main_frame, height=38, placeholder_text="1234567890", font=ctk.CTkFont(size=13))
        fields['Phone'].pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(main_frame, text="Email *", anchor="w", font=ctk.CTkFont(size=13)).pack(fill="x", pady=(10, 5))
        fields['Email'] = ctk.CTkEntry(main_frame, height=38, placeholder_text="email@example.com", font=ctk.CTkFont(size=13))
        fields['Email'].pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(main_frame, text="Passport ID *", anchor="w", font=ctk.CTkFont(size=13)).pack(fill="x", pady=(10, 5))
        fields['PassportNo'] = ctk.CTkEntry(main_frame, height=38, placeholder_text="P1234567", font=ctk.CTkFont(size=13))
        fields['PassportNo'].pack(fill="x", pady=(0, 10))
        
        if data:
            fields['FirstName'].insert(0, data[1])
            fields['LastName'].insert(0, data[2])
            fields['DOB'].insert(0, str(data[3]))
            fields['Gender'].set(data[4])
            fields['Phone'].insert(0, data[5])
            fields['Email'].insert(0, data[6])
            fields['PassportNo'].insert(0, data[7])
        
        def save_passenger():
            if not all([fields['FirstName'].get(), fields['LastName'].get(), 
                       fields['DOB'].get(), fields['Gender'].get(), 
                       fields['Phone'].get(), fields['Email'].get(), 
                       fields['PassportNo'].get()]):
                messagebox.showerror("Error", "All fields are required")
                return
            
            try:
                query = """
                    UPDATE Passenger 
                    SET FirstName=%s, LastName=%s, DOB=%s, Gender=%s, 
                        Phone=%s, Email=%s, PassportNo=%s
                    WHERE PassengerID=%s
                """
                values = (
                    fields['FirstName'].get(),
                    fields['LastName'].get(),
                    fields['DOB'].get(),
                    fields['Gender'].get(),
                    fields['Phone'].get(),
                    fields['Email'].get(),
                    fields['PassportNo'].get(),
                    data[0]
                )
                
                self.cursor.execute(query, values)
                self.conn.commit()
                
                messagebox.showinfo("Success", "Passenger updated successfully!")
                form_window.destroy()
                self.load_passengers()
                
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to save passenger: {err}")
        
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(20, 0))
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="Save",
            width=150,
            height=42,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#27AE60",
            hover_color="#229954",
            command=save_passenger
        )
        save_btn.pack(side="left", padx=(0, 10))
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=150,
            height=42,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="gray",
            hover_color="darkgray",
            command=form_window.destroy
        )
        cancel_btn.pack(side="left")
    
    def delete_passenger(self):
        """Delete selected passenger"""
        selected = self.passenger_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a passenger to delete")
            return
        
        passenger_id = self.passenger_tree.item(selected[0])['values'][0]
        passenger_name = self.passenger_tree.item(selected[0])['values'][1]
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete passenger:\n{passenger_name}?"):
            try:
                query = "DELETE FROM Passenger WHERE PassengerID = %s"
                self.cursor.execute(query, (passenger_id,))
                self.conn.commit()
                
                messagebox.showinfo("Success", "Passenger deleted successfully!")
                self.load_passengers()
                
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to delete passenger: {err}")
    
    def show_flights(self):
        """Display Flights management interface"""
        self.clear_content()
        
        header_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(20, 10))
        
        title = ctk.CTkLabel(
            header_frame,
            text="Flight Management",
            font=ctk.CTkFont(size=30, weight="bold")
        )
        title.pack(side="left")
        
        actions_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        actions_frame.pack(fill="x", padx=30, pady=10)
        
        refresh_btn = ctk.CTkButton(
            actions_frame,
            text="Refresh",
            width=110,
            height=38,
            font=ctk.CTkFont(size=13),
            command=self.load_flights
        )
        refresh_btn.pack(side="left", padx=5)
        
        table_frame = ctk.CTkFrame(self.content_frame)
        table_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                       background="#2b2b2b",
                       foreground="white",
                       rowheight=32,
                       fieldbackground="#2b2b2b",
                       borderwidth=0,
                       font=('Arial', 11))
        style.map('Treeview', background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading",
                       background="#1f538d",
                       foreground="white",
                       relief="flat",
                       font=('Arial', 12, 'bold'))
        
        tree_scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
        tree_scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        
        columns = ("FlightID", "Flight#", "Airline", "Source", "Destination", "Departure", "Arrival", "Duration", "Status")
        self.flight_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set
        )
        
        tree_scroll_y.config(command=self.flight_tree.yview)
        tree_scroll_x.config(command=self.flight_tree.xview)
        
        column_widths = [80, 100, 120, 130, 130, 150, 150, 80, 100]
        for col, width in zip(columns, column_widths):
            self.flight_tree.heading(col, text=col)
            self.flight_tree.column(col, width=width, anchor="center")
        
        tree_scroll_y.pack(side="right", fill="y")
        tree_scroll_x.pack(side="bottom", fill="x")
        self.flight_tree.pack(fill="both", expand=True)
        
        self.load_flights()
    
    def load_flights(self):
        """Load flights from database"""
        for item in self.flight_tree.get_children():
            self.flight_tree.delete(item)
        
        try:
            query = """
                SELECT f.FlightID, f.FlightNumber, f.AirlineName,
                       src.City, dst.City, f.DepartureTime, f.ArrivalTime, 
                       f.Duration, f.Status
                FROM Flight f
                JOIN Airport src ON f.SourceAirportID = src.AirportID
                JOIN Airport dst ON f.DestinationAirportID = dst.AirportID
                ORDER BY f.DepartureTime
            """
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                self.flight_tree.insert("", "end", values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load flights: {err}")
    
    def show_airports(self):
        """Display Airports management interface"""
        self.clear_content()
        
        header_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(20, 10))
        
        title = ctk.CTkLabel(
            header_frame,
            text="Airport Management",
            font=ctk.CTkFont(size=30, weight="bold")
        )
        title.pack(side="left")
        
        actions_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        actions_frame.pack(fill="x", padx=30, pady=10)
        
        self.airport_search = ctk.CTkEntry(
            actions_frame,
            placeholder_text="Search by city or IATA code...",
            width=300,
            height=38,
            font=ctk.CTkFont(size=13)
        )
        self.airport_search.pack(side="left", padx=(0, 10))
        
        search_btn = ctk.CTkButton(
            actions_frame,
            text="Search",
            width=100,
            height=38,
            font=ctk.CTkFont(size=13),
            command=self.search_airports
        )
        search_btn.pack(side="left", padx=5)
        
        refresh_btn = ctk.CTkButton(
            actions_frame,
            text="Refresh",
            width=100,
            height=38,
            font=ctk.CTkFont(size=13),
            command=self.load_airports
        )
        refresh_btn.pack(side="left", padx=5)
        
        table_frame = ctk.CTkFrame(self.content_frame)
        table_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                       background="#2b2b2b",
                       foreground="white",
                       rowheight=32,
                       fieldbackground="#2b2b2b",
                       borderwidth=0,
                       font=('Arial', 11))
        style.map('Treeview', background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading",
                       background="#1f538d",
                       foreground="white",
                       relief="flat",
                       font=('Arial', 12, 'bold'))
        
        tree_scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
        tree_scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        
        columns = ("AirportID", "Airport Name", "City", "Country", "IATA Code")
        self.airport_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set
        )
        
        tree_scroll_y.config(command=self.airport_tree.yview)
        tree_scroll_x.config(command=self.airport_tree.xview)
        
        column_widths = [100, 350, 150, 120, 100]
        for col, width in zip(columns, column_widths):
            self.airport_tree.heading(col, text=col)
            self.airport_tree.column(col, width=width, anchor="center")
        
        tree_scroll_y.pack(side="right", fill="y")
        tree_scroll_x.pack(side="bottom", fill="x")
        self.airport_tree.pack(fill="both", expand=True)
        
        self.load_airports()
    
    def load_airports(self, search_term=""):
        """Load airports from database"""
        for item in self.airport_tree.get_children():
            self.airport_tree.delete(item)
        
        try:
            if search_term:
                query = """
                    SELECT AirportID, AirportName, City, Country, IATA_Code
                    FROM Airport
                    WHERE City LIKE %s OR IATA_Code LIKE %s OR AirportName LIKE %s
                    ORDER BY City
                """
                self.cursor.execute(query, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
            else:
                query = """
                    SELECT AirportID, AirportName, City, Country, IATA_Code
                    FROM Airport
                    ORDER BY City
                """
                self.cursor.execute(query)
            
            for row in self.cursor.fetchall():
                self.airport_tree.insert("", "end", values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load airports: {err}")
    
    def search_airports(self):
        """Search airports"""
        search_term = self.airport_search.get()
        self.load_airports(search_term)
    
    def show_bookings(self):
        """Display Bookings interface"""
        self.clear_content()
        
        header_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(20, 10))
        
        title = ctk.CTkLabel(
            header_frame,
            text="Flight Booking System",
            font=ctk.CTkFont(size=30, weight="bold")
        )
        title.pack(side="left")
        
        search_frame = ctk.CTkFrame(self.content_frame)
        search_frame.pack(fill="x", padx=30, pady=10)
        
        ctk.CTkLabel(
            search_frame,
            text="Search Flights",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=15)
        
        inputs_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        inputs_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(inputs_frame, text="From:", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.source_combo = ctk.CTkComboBox(inputs_frame, width=250, height=38, font=ctk.CTkFont(size=13))
        self.source_combo.grid(row=0, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(inputs_frame, text="To:", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.dest_combo = ctk.CTkComboBox(inputs_frame, width=250, height=38, font=ctk.CTkFont(size=13))
        self.dest_combo.grid(row=0, column=3, padx=10, pady=10)
        
        search_flights_btn = ctk.CTkButton(
            inputs_frame,
            text="Search Flights",
            width=160,
            height=40,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.search_flights_for_booking
        )
        search_flights_btn.grid(row=0, column=4, padx=20, pady=10)
        
        self.load_airport_combos()
        
        flights_frame = ctk.CTkFrame(self.content_frame)
        flights_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        ctk.CTkLabel(
            flights_frame,
            text="Available Flights",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=15)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                       background="#2b2b2b",
                       foreground="white",
                       rowheight=32,
                       fieldbackground="#2b2b2b",
                       borderwidth=0,
                       font=('Arial', 11))
        style.map('Treeview', background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading",
                       background="#1f538d",
                       foreground="white",
                       relief="flat",
                       font=('Arial', 12, 'bold'))
        
        tree_frame = ctk.CTkFrame(flights_frame, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical")
        
        columns = ("FlightID", "Flight#", "Airline", "Departure", "Arrival", "Duration", "Status")
        self.booking_flights_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=tree_scroll.set,
            height=10
        )
        
        tree_scroll.config(command=self.booking_flights_tree.yview)
        
        column_widths = [80, 100, 130, 150, 150, 80, 100]
        for col, width in zip(columns, column_widths):
            self.booking_flights_tree.heading(col, text=col)
            self.booking_flights_tree.column(col, width=width, anchor="center")
        
        tree_scroll.pack(side="right", fill="y")
        self.booking_flights_tree.pack(fill="both", expand=True)
        
        book_btn = ctk.CTkButton(
            flights_frame,
            text="Select Flight & Book Seat",
            width=260,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#27AE60",
            hover_color="#229954",
            command=self.book_selected_flight
        )
        book_btn.pack(pady=15)
    
    def load_airport_combos(self):
        """Load airports into combo boxes"""
        try:
            query = "SELECT AirportID, City, IATA_Code FROM Airport ORDER BY City"
            self.cursor.execute(query)
            airports = self.cursor.fetchall()
            
            airport_list = [f"{row[1]} ({row[2]})" for row in airports]
            self.airport_dict = {f"{row[1]} ({row[2]})": row[0] for row in airports}
            
            self.source_combo.configure(values=airport_list)
            self.dest_combo.configure(values=airport_list)
            
            if airport_list:
                self.source_combo.set(airport_list[0])
                if len(airport_list) > 1:
                    self.dest_combo.set(airport_list[1])
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load airports: {err}")
    
    def search_flights_for_booking(self):
        """Search flights based on source and destination"""
        source = self.source_combo.get()
        dest = self.dest_combo.get()
        
        if not source or not dest:
            messagebox.showwarning("Warning", "Please select both source and destination")
            return
        
        if source == dest:
            messagebox.showwarning("Warning", "Source and destination cannot be the same")
            return
        
        source_id = self.airport_dict.get(source)
        dest_id = self.airport_dict.get(dest)
        
        for item in self.booking_flights_tree.get_children():
            self.booking_flights_tree.delete(item)
        
        try:
            query = """
                SELECT FlightID, FlightNumber, AirlineName, DepartureTime, 
                       ArrivalTime, Duration, Status
                FROM Flight
                WHERE SourceAirportID = %s AND DestinationAirportID = %s
                AND Status != 'Cancelled'
                ORDER BY DepartureTime
            """
            self.cursor.execute(query, (source_id, dest_id))
            flights = self.cursor.fetchall()
            
            if not flights:
                messagebox.showinfo("No Flights", "No flights found for this route")
                return
            
            for row in flights:
                self.booking_flights_tree.insert("", "end", values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to search flights: {err}")
    
    def book_selected_flight(self):
        """Open seat selection for selected flight"""
        selected = self.booking_flights_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a flight")
            return
        
        flight_id = self.booking_flights_tree.item(selected[0])['values'][0]
        self.show_seat_selection(flight_id)
    
    def show_seat_selection(self, flight_id):
        """Show seat selection window"""
        seat_window = ctk.CTkToplevel(self.root)
        seat_window.title("Select Seat")
        seat_window.geometry("950x750")
        seat_window.transient(self.root)
        seat_window.grab_set()
        
        seat_window.update_idletasks()
        width = seat_window.winfo_width()
        height = seat_window.winfo_height()
        x = (seat_window.winfo_screenwidth() // 2) - (width // 2)
        y = (seat_window.winfo_screenheight() // 2) - (height // 2)
        seat_window.geometry(f'{width}x{height}+{x}+{y}')
        
        main_frame = ctk.CTkFrame(seat_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="Select Passenger and Seat",
            font=ctk.CTkFont(size=26, weight="bold")
        ).pack(pady=(0, 20))
        
        passenger_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        passenger_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            passenger_frame,
            text="Select Passenger:",
            font=ctk.CTkFont(size=15)
        ).pack(side="left", padx=10)
        
        passenger_combo = ctk.CTkComboBox(passenger_frame, width=450, height=40, font=ctk.CTkFont(size=13))
        passenger_combo.pack(side="left", padx=10)
        
        try:
            query = "SELECT PassengerID, FirstName, LastName, Email FROM Passenger"
            self.cursor.execute(query)
            passengers = self.cursor.fetchall()
            passenger_list = [f"{row[1]} {row[2]} - {row[3]}" for row in passengers]
            passenger_dict = {f"{row[1]} {row[2]} - {row[3]}": row[0] for row in passengers}
            passenger_combo.configure(values=passenger_list)
            if passenger_list:
                passenger_combo.set(passenger_list[0])
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load passengers: {err}")
            return
        
        seats_container = ctk.CTkScrollableFrame(main_frame, height=380)
        seats_container.pack(fill="both", expand=True, pady=10)
        
        ctk.CTkLabel(
            seats_container,
            text="Select Your Seat",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)
        
        try:
            query = """
                SELECT SeatID, SeatNumber, Class, Availability, Price
                FROM Seat
                WHERE FlightID = %s
                ORDER BY SeatNumber
            """
            self.cursor.execute(query, (flight_id,))
            seats = self.cursor.fetchall()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load seats: {err}")
            return
        
        selected_seat = {"id": None, "price": 0}
        seat_buttons = []
        
        def select_seat(seat_id, price, button):
            for btn in seat_buttons:
                if btn != button:
                    btn.configure(fg_color=btn.original_color)
            
            selected_seat["id"] = seat_id
            selected_seat["price"] = price
            button.configure(fg_color="#E74C3C")
            price_label.configure(text=f"Selected Seat Price: ₹{price:,.2f}")
        
        seats_grid = ctk.CTkFrame(seats_container, fg_color="transparent")
        seats_grid.pack(pady=10)
        
        row_num = 0
        col_num = 0
        for seat in seats:
            seat_id, seat_num, seat_class, availability, price = seat
            
            if availability == "Available":
                color = "#27AE60"
                state = "normal"
            else:
                color = "#7F8C8D"
                state = "disabled"
            
            btn = ctk.CTkButton(
                seats_grid,
                text=f"{seat_num}\n{seat_class}\n₹{price}",
                width=100,
                height=75,
                fg_color=color,
                font=ctk.CTkFont(size=12),
                state=state
            )
            btn.original_color = color
            
            if state == "normal":
                btn.configure(command=lambda s=seat_id, p=price, b=btn: select_seat(s, p, b))
            
            btn.grid(row=row_num, column=col_num, padx=5, pady=5)
            seat_buttons.append(btn)
            
            col_num += 1
            if col_num >= 6:
                col_num = 0
                row_num += 1
        
        price_label = ctk.CTkLabel(
            main_frame,
            text="Select a seat to see price",
            font=ctk.CTkFont(size=17, weight="bold")
        )
        price_label.pack(pady=10)
        
        def confirm_booking():
            if not selected_seat["id"]:
                messagebox.showwarning("Warning", "Please select a seat")
                return
            
            passenger_key = passenger_combo.get()
            if not passenger_key:
                messagebox.showwarning("Warning", "Please select a passenger")
                return
            
            passenger_id = passenger_dict[passenger_key]
            self.process_booking(flight_id, passenger_id, selected_seat["id"], selected_seat["price"], seat_window)
        
        book_btn = ctk.CTkButton(
            main_frame,
            text="Proceed to Payment",
            width=220,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#27AE60",
            hover_color="#229954",
            command=confirm_booking
        )
        book_btn.pack(pady=10)
    
    def process_booking(self, flight_id, passenger_id, seat_id, price, parent_window):
        """Process booking and payment"""
        try:
            self.cursor.execute("SELECT Availability FROM Seat WHERE SeatID = %s", (seat_id,))
            availability = self.cursor.fetchone()
            if availability and availability[0] == 'Booked':
                messagebox.showerror("Error", "This seat is already booked!")
                return
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to check seat availability: {err}")
            return
        
        payment_window = ctk.CTkToplevel(parent_window)
        payment_window.title("Payment")
        payment_window.geometry("500x550")
        payment_window.transient(parent_window)
        payment_window.grab_set()
        
        payment_window.update_idletasks()
        width = payment_window.winfo_width()
        height = payment_window.winfo_height()
        x = (payment_window.winfo_screenwidth() // 2) - (width // 2)
        y = (payment_window.winfo_screenheight() // 2) - (height // 2)
        payment_window.geometry(f'{width}x{height}+{x}+{y}')
        
        main_frame = ctk.CTkFrame(payment_window)
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(
            main_frame,
            text="Payment Details",
            font=ctk.CTkFont(size=26, weight="bold")
        ).pack(pady=(0, 20))
        
        ctk.CTkLabel(
            main_frame,
            text=f"Amount to Pay: ₹{price:,.2f}",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#27AE60"
        ).pack(pady=20)
        
        ctk.CTkLabel(
            main_frame,
            text="Select Payment Method:",
            font=ctk.CTkFont(size=15)
        ).pack(pady=(20, 10))
        
        payment_method = ctk.StringVar(value="Card")
        
        methods_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        methods_frame.pack(pady=10)
        
        for method in ["Card", "UPI", "NetBanking", "Cash"]:
            ctk.CTkRadioButton(
                methods_frame,
                text=method,
                variable=payment_method,
                value=method,
                font=ctk.CTkFont(size=14)
            ).pack(pady=5)
        
        def complete_payment():
            try:
                self.cursor.execute("SELECT Availability FROM Seat WHERE SeatID = %s FOR UPDATE", (seat_id,))
                availability = self.cursor.fetchone()
                if availability and availability[0] == 'Booked':
                    messagebox.showerror("Error", "This seat was just booked by someone else!")
                    payment_window.destroy()
                    return
                
                self.cursor.execute("SELECT DATE(DepartureTime) FROM Flight WHERE FlightID = %s", (flight_id,))
                travel_date = self.cursor.fetchone()[0]
                
                booking_query = """
                    INSERT INTO Booking (PassengerID, FlightID, SeatID, BookingDate, TravelDate, BookingStatus)
                    VALUES (%s, %s, %s, NOW(), %s, 'Confirmed')
                """
                self.cursor.execute(booking_query, (passenger_id, flight_id, seat_id, travel_date))
                booking_id = self.cursor.lastrowid
                
                self.cursor.execute("UPDATE Seat SET Availability='Booked' WHERE SeatID=%s", (seat_id,))
                
                payment_query = """
                    INSERT INTO Payment (BookingID, Amount, PaymentMethod, PaymentStatus, TransactionDate)
                    VALUES (%s, %s, %s, 'Success', NOW())
                """
                self.cursor.execute(payment_query, (booking_id, price, payment_method.get()))
                
                self.conn.commit()
                
                messagebox.showinfo("Success", "Booking confirmed successfully!")
                
                self.generate_boarding_pass_pdf(booking_id)
                
                payment_window.destroy()
                parent_window.destroy()
                
            except mysql.connector.Error as err:
                self.conn.rollback()
                messagebox.showerror("Error", f"Booking failed: {err}")
        
        pay_btn = ctk.CTkButton(
            main_frame,
            text="Pay Now",
            width=200,
            height=48,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#27AE60",
            hover_color="#229954",
            command=complete_payment
        )
        pay_btn.pack(pady=30)
    
    def generate_boarding_pass_pdf(self, booking_id):
        """Generate and save boarding pass as PDF"""
        if not os.path.exists("my_tickets"):
            os.makedirs("my_tickets")
        
        try:
            query = """
                SELECT p.FirstName, p.LastName, p.PassportNo, p.Email, p.Phone,
                       f.FlightNumber, f.AirlineName, f.DepartureTime, f.ArrivalTime,
                       s.SeatNumber, s.Class, s.Price,
                       src.City, src.IATA_Code, src.AirportName,
                       dst.City, dst.IATA_Code, dst.AirportName,
                       b.BookingDate, b.TravelDate, f.Duration
                FROM Booking b
                JOIN Passenger p ON b.PassengerID = p.PassengerID
                JOIN Flight f ON b.FlightID = f.FlightID
                JOIN Seat s ON b.SeatID = s.SeatID
                JOIN Airport src ON f.SourceAirportID = src.AirportID
                JOIN Airport dst ON f.DestinationAirportID = dst.AirportID
                WHERE b.BookingID = %s
            """
            self.cursor.execute(query, (booking_id,))
            data = self.cursor.fetchone()
            
            if not data:
                messagebox.showerror("Error", "Booking data not found")
                return
            
            filename = f"my_tickets/BoardingPass_{booking_id}_{data[0]}_{data[1]}.pdf"
            
            c = canvas.Canvas(filename, pagesize=A4)
            width, height = A4
            
            c.setStrokeColor(colors.HexColor("#1f538d"))
            c.setLineWidth(3)
            c.rect(30, 30, width-60, height-60, stroke=1, fill=0)
            
            c.setFillColor(colors.HexColor("#1f538d"))
            c.rect(30, height-150, width-60, 120, stroke=0, fill=1)
            
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 32)
            c.drawCentredString(width/2, height-80, "BOARDING PASS")
            
            c.setFont("Helvetica", 14)
            c.drawCentredString(width/2, height-110, f"{data[6]} - Flight {data[5]}")
            
            c.setFillColor(colors.black)
            
            y_pos = height - 190
            c.setFont("Helvetica-Bold", 11)
            c.drawString(50, y_pos, "Booking ID:")
            c.setFont("Helvetica", 11)
            c.drawString(140, y_pos, str(booking_id))
            
            c.setFont("Helvetica-Bold", 11)
            c.drawRightString(width-50, y_pos, "Booking Date:")
            c.setFont("Helvetica", 11)
            c.drawRightString(width-50, y_pos-20, str(data[18]))
            
            y_pos -= 60
            c.setFillColor(colors.HexColor("#2c3e50"))
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y_pos, "PASSENGER INFORMATION")
            
            y_pos -= 30
            c.setFont("Helvetica-Bold", 11)
            c.setFillColor(colors.black)
            c.drawString(50, y_pos, "Name:")
            c.setFont("Helvetica", 11)
            c.drawString(150, y_pos, f"{data[0]} {data[1]}")
            
            y_pos -= 25
            c.setFont("Helvetica-Bold", 11)
            c.drawString(50, y_pos, "Passport:")
            c.setFont("Helvetica", 11)
            c.drawString(150, y_pos, data[2])
            
            y_pos -= 25
            c.setFont("Helvetica-Bold", 11)
            c.drawString(50, y_pos, "Email:")
            c.setFont("Helvetica", 11)
            c.drawString(150, y_pos, data[3])
            
            y_pos -= 25
            c.setFont("Helvetica-Bold", 11)
            c.drawString(50, y_pos, "Phone:")
            c.setFont("Helvetica", 11)
            c.drawString(150, y_pos, data[4])
            
            y_pos -= 50
            c.setFillColor(colors.HexColor("#2c3e50"))
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y_pos, "FLIGHT INFORMATION")
            
            y_pos -= 40
            c.setFont("Helvetica-Bold", 24)
            c.setFillColor(colors.HexColor("#e74c3c"))
            c.drawString(80, y_pos, data[13])
            
            c.setFont("Helvetica", 20)
            c.setFillColor(colors.black)
            c.drawString(180, y_pos+5, "→")
            
            c.setFont("Helvetica-Bold", 24)
            c.setFillColor(colors.HexColor("#27ae60"))
            c.drawString(230, y_pos, data[16])
            
            y_pos -= 25
            c.setFont("Helvetica", 11)
            c.setFillColor(colors.black)
            c.drawString(60, y_pos, data[12])
            c.drawString(210, y_pos, data[15])
            
            y_pos -= 40
            c.setFont("Helvetica-Bold", 11)
            c.drawString(50, y_pos, "Flight Number:")
            c.setFont("Helvetica", 11)
            c.drawString(160, y_pos, data[5])
            
            c.setFont("Helvetica-Bold", 11)
            c.drawString(300, y_pos, "Airline:")
            c.setFont("Helvetica", 11)
            c.drawString(370, y_pos, data[6])
            
            y_pos -= 25
            c.setFont("Helvetica-Bold", 11)
            c.drawString(50, y_pos, "Departure:")
            c.setFont("Helvetica", 11)
            c.drawString(160, y_pos, str(data[7]))
            
            y_pos -= 25
            c.setFont("Helvetica-Bold", 11)
            c.drawString(50, y_pos, "Arrival:")
            c.setFont("Helvetica", 11)
            c.drawString(160, y_pos, str(data[8]))
            
            y_pos -= 25
            c.setFont("Helvetica-Bold", 11)
            c.drawString(50, y_pos, "Duration:")
            c.setFont("Helvetica", 11)
            c.drawString(160, y_pos, data[20])
            
            c.setFont("Helvetica-Bold", 11)
            c.drawString(300, y_pos, "Travel Date:")
            c.setFont("Helvetica", 11)
            c.drawString(390, y_pos, str(data[19]))
            
            y_pos -= 50
            c.setFillColor(colors.HexColor("#2c3e50"))
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y_pos, "SEAT INFORMATION")
            
            y_pos -= 35
            c.setFont("Helvetica-Bold", 36)
            c.setFillColor(colors.HexColor("#3498db"))
            c.drawString(80, y_pos-10, data[9])
            
            c.setFont("Helvetica-Bold", 11)
            c.setFillColor(colors.black)
            c.drawString(200, y_pos, "Class:")
            c.setFont("Helvetica", 11)
            c.drawString(250, y_pos, data[10])
            
            c.setFont("Helvetica-Bold", 11)
            c.drawString(200, y_pos-25, "Fare:")
            c.setFont("Helvetica", 11)
            c.drawString(250, y_pos-25, f"{data[11]:,.2f}")
            
            y_pos -= 70
            c.setFillColor(colors.HexColor("#f39c12"))
            c.rect(50, y_pos-35, width-100, 50, stroke=1, fill=1)
            
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 11)
            c.drawCentredString(width/2, y_pos-10, "IMPORTANT NOTICE")
            c.setFont("Helvetica", 9)
            c.drawCentredString(width/2, y_pos-25, "Please arrive at the airport at least 2 hours before departure.")
            
            c.setFillColor(colors.gray)
            c.setFont("Helvetica", 8)
            c.drawCentredString(width/2, 60, "This is a computer-generated boarding pass. No signature required.")
            c.drawCentredString(width/2, 45, "Please carry a valid photo ID proof along with this boarding pass.")
            
            c.save()
            
            messagebox.showinfo("Boarding Pass Generated", 
                              f"Boarding pass saved successfully!\n\nLocation: {filename}\n\nYou can find it in the 'my_tickets' folder.")
        
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to generate boarding pass: {err}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create PDF: {e}")
    
    def show_manage_bookings(self):
        """Display Manage Bookings interface with delete option"""
        self.clear_content()
        
        header_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(20, 10))
        
        title = ctk.CTkLabel(
            header_frame,
            text="Manage Bookings",
            font=ctk.CTkFont(size=30, weight="bold")
        )
        title.pack(side="left")
        
        actions_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        actions_frame.pack(fill="x", padx=30, pady=10)
        
        self.booking_search = ctk.CTkEntry(
            actions_frame,
            placeholder_text="Search by Booking ID or Passenger name...",
            width=300,
            height=38,
            font=ctk.CTkFont(size=13)
        )
        self.booking_search.pack(side="left", padx=(0, 10))
        
        search_btn = ctk.CTkButton(
            actions_frame,
            text="Search",
            width=100,
            height=38,
            font=ctk.CTkFont(size=13),
            command=self.search_bookings
        )
        search_btn.pack(side="left", padx=5)
        
        refresh_btn = ctk.CTkButton(
            actions_frame,
            text="Refresh",
            width=100,
            height=38,
            font=ctk.CTkFont(size=13),
            fg_color="gray",
            hover_color="darkgray",
            command=self.load_manage_bookings
        )
        refresh_btn.pack(side="left", padx=5)
        
        table_frame = ctk.CTkFrame(self.content_frame)
        table_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                       background="#2b2b2b",
                       foreground="white",
                       rowheight=32,
                       fieldbackground="#2b2b2b",
                       borderwidth=0,
                       font=('Arial', 11))
        style.map('Treeview', background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading",
                       background="#1f538d",
                       foreground="white",
                       relief="flat",
                       font=('Arial', 12, 'bold'))
        
        tree_scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
        tree_scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        
        columns = ("BookingID", "Passenger", "Flight", "Seat", "Status", "Amount", "Booking Date", "Travel Date")
        self.manage_bookings_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
            selectmode="browse"
        )
        
        tree_scroll_y.config(command=self.manage_bookings_tree.yview)
        tree_scroll_x.config(command=self.manage_bookings_tree.xview)
        
        column_widths = [100, 180, 120, 80, 100, 120, 150, 120]
        for col, width in zip(columns, column_widths):
            self.manage_bookings_tree.heading(col, text=col)
            self.manage_bookings_tree.column(col, width=width, anchor="center")
        
        tree_scroll_y.pack(side="right", fill="y")
        tree_scroll_x.pack(side="bottom", fill="x")
        self.manage_bookings_tree.pack(fill="both", expand=True)
        
        btn_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=10)
        
        view_btn = ctk.CTkButton(
            btn_frame,
            text="View Details",
            width=130,
            height=38,
            font=ctk.CTkFont(size=13),
            fg_color="#3498DB",
            hover_color="#2980B9",
            command=self.view_booking_details
        )
        view_btn.pack(side="left", padx=5)
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel Booking",
            width=150,
            height=38,
            font=ctk.CTkFont(size=13),
            fg_color="#F39C12",
            hover_color="#E67E22",
            command=self.cancel_booking
        )
        cancel_btn.pack(side="left", padx=5)
        
        delete_btn = ctk.CTkButton(
            btn_frame,
            text="Delete Booking",
            width=150,
            height=38,
            font=ctk.CTkFont(size=13),
            fg_color="#E74C3C",
            hover_color="#C0392B",
            command=self.delete_booking
        )
        delete_btn.pack(side="left", padx=5)
        
        self.load_manage_bookings()
    
    def load_manage_bookings(self, search_term=""):
        """Load bookings from database"""
        for item in self.manage_bookings_tree.get_children():
            self.manage_bookings_tree.delete(item)
        
        try:
            if search_term:
                query = """
                    SELECT b.BookingID,
                           CONCAT(p.FirstName, ' ', p.LastName),
                           f.FlightNumber,
                           s.SeatNumber,
                           b.BookingStatus,
                           COALESCE(pay.Amount, 0),
                           b.BookingDate,
                           b.TravelDate
                    FROM Booking b
                    JOIN Passenger p ON b.PassengerID = p.PassengerID
                    JOIN Flight f ON b.FlightID = f.FlightID
                    JOIN Seat s ON b.SeatID = s.SeatID
                    LEFT JOIN Payment pay ON b.BookingID = pay.BookingID
                    WHERE b.BookingID LIKE %s OR p.FirstName LIKE %s OR p.LastName LIKE %s
                    ORDER BY b.BookingDate DESC
                """
                self.cursor.execute(query, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
            else:
                query = """
                    SELECT b.BookingID,
                           CONCAT(p.FirstName, ' ', p.LastName),
                           f.FlightNumber,
                           s.SeatNumber,
                           b.BookingStatus,
                           COALESCE(pay.Amount, 0),
                           b.BookingDate,
                           b.TravelDate
                    FROM Booking b
                    JOIN Passenger p ON b.PassengerID = p.PassengerID
                    JOIN Flight f ON b.FlightID = f.FlightID
                    JOIN Seat s ON b.SeatID = s.SeatID
                    LEFT JOIN Payment pay ON b.BookingID = pay.BookingID
                    ORDER BY b.BookingDate DESC
                """
                self.cursor.execute(query)
            
            rows = self.cursor.fetchall()
            for row in rows:
                self.manage_bookings_tree.insert("", "end", values=row)
                
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load bookings: {err}")
    
    def search_bookings(self):
        """Search bookings"""
        search_term = self.booking_search.get()
        self.load_manage_bookings(search_term)
    
    def view_booking_details(self):
        """View detailed booking information"""
        selected = self.manage_bookings_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a booking to view")
            return
        
        booking_id = self.manage_bookings_tree.item(selected[0])['values'][0]
        
        try:
            query = """
                SELECT b.BookingID, 
                       CONCAT(p.FirstName, ' ', p.LastName) AS Passenger,
                       p.Email, p.Phone,
                       f.FlightNumber, f.AirlineName,
                       src.City AS Source, dst.City AS Destination,
                       f.DepartureTime, f.ArrivalTime,
                       s.SeatNumber, s.Class, s.Price,
                       b.BookingStatus, b.BookingDate, b.TravelDate,
                       pay.PaymentMethod, pay.PaymentStatus
                FROM Booking b
                JOIN Passenger p ON b.PassengerID = p.PassengerID
                JOIN Flight f ON b.FlightID = f.FlightID
                JOIN Seat s ON b.SeatID = s.SeatID
                JOIN Airport src ON f.SourceAirportID = src.AirportID
                JOIN Airport dst ON f.DestinationAirportID = dst.AirportID
                LEFT JOIN Payment pay ON b.BookingID = pay.BookingID
                WHERE b.BookingID = %s
            """
            self.cursor.execute(query, (booking_id,))
            details = self.cursor.fetchone()
            
            if details:
                details_window = ctk.CTkToplevel(self.root)
                details_window.title("Booking Details")
                details_window.geometry("600x700")
                details_window.transient(self.root)
                
                details_window.update_idletasks()
                width = details_window.winfo_width()
                height = details_window.winfo_height()
                x = (details_window.winfo_screenwidth() // 2) - (width // 2)
                y = (details_window.winfo_screenheight() // 2) - (height // 2)
                details_window.geometry(f'{width}x{height}+{x}+{y}')
                
                main_frame = ctk.CTkScrollableFrame(details_window)
                main_frame.pack(fill="both", expand=True, padx=30, pady=30)
                
                ctk.CTkLabel(
                    main_frame,
                    text="Booking Details",
                    font=ctk.CTkFont(size=28, weight="bold")
                ).pack(pady=(0, 20))
                
                info_frame = ctk.CTkFrame(main_frame)
                info_frame.pack(fill="x", pady=10)
                
                info_text = f"""
Booking ID: {details[0]}

PASSENGER INFORMATION:
Name: {details[1]}
Email: {details[2]}
Phone: {details[3]}

FLIGHT INFORMATION:
Flight: {details[4]} ({details[5]})
Route: {details[6]} → {details[7]}
Departure: {details[8]}
Arrival: {details[9]}

SEAT INFORMATION:
Seat: {details[10]}
Class: {details[11]}
Price: ₹{details[12]:,.2f}

BOOKING INFORMATION:
Status: {details[13]}
Booking Date: {details[14]}
Travel Date: {details[15]}

PAYMENT INFORMATION:
Payment Method: {details[16] if details[16] else 'N/A'}
Payment Status: {details[17] if details[17] else 'N/A'}
                """
                
                ctk.CTkLabel(
                    info_frame,
                    text=info_text,
                    font=ctk.CTkFont(size=13),
                    justify="left"
                ).pack(padx=20, pady=20)
                
                close_btn = ctk.CTkButton(
                    main_frame,
                    text="Close",
                    width=150,
                    height=40,
                    font=ctk.CTkFont(size=14),
                    command=details_window.destroy
                )
                close_btn.pack(pady=20)
                
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to fetch booking details: {err}")
    
    def cancel_booking(self):
        """Cancel selected booking"""
        selected = self.manage_bookings_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a booking to cancel")
            return
        
        booking_id = self.manage_bookings_tree.item(selected[0])['values'][0]
        booking_status = self.manage_bookings_tree.item(selected[0])['values'][4]
        
        if booking_status == "Cancelled":
            messagebox.showinfo("Info", "This booking is already cancelled")
            return
        
        if messagebox.askyesno("Confirm Cancellation", 
                              f"Are you sure you want to cancel Booking ID: {booking_id}?\n\nThis will free up the seat and update the status to 'Cancelled'."):
            try:
                # Get seat ID
                self.cursor.execute("SELECT SeatID FROM Booking WHERE BookingID = %s", (booking_id,))
                seat_id = self.cursor.fetchone()[0]
                
                # Update booking status
                self.cursor.execute("UPDATE Booking SET BookingStatus='Cancelled' WHERE BookingID=%s", (booking_id,))
                
                # Free up the seat
                self.cursor.execute("UPDATE Seat SET Availability='Available' WHERE SeatID=%s", (seat_id,))
                
                self.conn.commit()
                
                messagebox.showinfo("Success", "Booking cancelled successfully!")
                self.load_manage_bookings()
                
            except mysql.connector.Error as err:
                self.conn.rollback()
                messagebox.showerror("Error", f"Failed to cancel booking: {err}")
    
    def delete_booking(self):
        """Delete selected booking permanently"""
        selected = self.manage_bookings_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a booking to delete")
            return
        
        booking_id = self.manage_bookings_tree.item(selected[0])['values'][0]
        passenger_name = self.manage_bookings_tree.item(selected[0])['values'][1]
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to permanently delete this booking?\n\nBooking ID: {booking_id}\nPassenger: {passenger_name}\n\nThis action cannot be undone!"):
            try:
                # Get seat ID before deletion
                self.cursor.execute("SELECT SeatID FROM Booking WHERE BookingID = %s", (booking_id,))
                seat_result = self.cursor.fetchone()
                
                if seat_result:
                    seat_id = seat_result[0]
                    
                    # Delete payment first (foreign key constraint)
                    self.cursor.execute("DELETE FROM Payment WHERE BookingID = %s", (booking_id,))
                    
                    # Delete booking
                    self.cursor.execute("DELETE FROM Booking WHERE BookingID = %s", (booking_id,))
                    
                    # Free up the seat
                    # Free up the seat
                    self.cursor.execute("UPDATE Seat SET Availability='Available' WHERE SeatID=%s", (seat_id,))
                    
                    self.conn.commit()
                    
                    messagebox.showinfo("Success", "Booking deleted successfully!")
                    self.load_manage_bookings()
                
            except mysql.connector.Error as err:
                self.conn.rollback()
                messagebox.showerror("Error", f"Failed to delete booking: {err}")
    
    def show_analysis(self):
        """Display booking analysis and statistics"""
        self.clear_content()
        
        header_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(20, 10))
        
        title = ctk.CTkLabel(
            header_frame,
            text="Booking Analysis & Reports",
            font=ctk.CTkFont(size=30, weight="bold")
        )
        title.pack(side="left")
        
        stats_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=30, pady=20)
        
        try:
            self.cursor.execute("SELECT COUNT(*) FROM Booking")
            total_bookings = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM Booking WHERE BookingStatus='Confirmed'")
            confirmed = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM Booking WHERE BookingStatus='Pending'")
            pending = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM Booking WHERE BookingStatus='Cancelled'")
            cancelled = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT SUM(Amount) FROM Payment WHERE PaymentStatus='Success'")
            total_revenue = self.cursor.fetchone()[0] or 0
            
            self.cursor.execute("SELECT AVG(Amount) FROM Payment WHERE PaymentStatus='Success'")
            avg_revenue = self.cursor.fetchone()[0] or 0
            
            stats_data = [
                ("Total Bookings", total_bookings, "#3498DB"),
                ("Confirmed", confirmed, "#27AE60"),
                ("Pending", pending, "#F39C12"),
                ("Cancelled", cancelled, "#E74C3C"),
                ("Total Revenue", f"₹{total_revenue:,.2f}", "#9B59B6"),
                ("Avg. Booking Value", f"₹{avg_revenue:,.2f}", "#1ABC9C")
            ]
            
            for i, (label, value, color) in enumerate(stats_data):
                row = i // 3
                col = i % 3
                
                card = ctk.CTkFrame(stats_frame, fg_color=color, corner_radius=10)
                card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                stats_frame.grid_columnconfigure(col, weight=1)
                
                ctk.CTkLabel(
                    card,
                    text=label,
                    font=ctk.CTkFont(size=14),
                    text_color="white"
                ).pack(pady=(15, 5))
                
                ctk.CTkLabel(
                    card,
                    text=str(value),
                    font=ctk.CTkFont(size=22, weight="bold"),
                    text_color="white"
                ).pack(pady=(0, 15))
        
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load statistics: {err}")
        
        bookings_frame = ctk.CTkFrame(self.content_frame)
        bookings_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        ctk.CTkLabel(
            bookings_frame,
            text="Recent Bookings",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=15)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                       background="#2b2b2b",
                       foreground="white",
                       rowheight=32,
                       fieldbackground="#2b2b2b",
                       borderwidth=0,
                       font=('Arial', 11))
        style.map('Treeview', background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading",
                       background="#1f538d",
                       foreground="white",
                       relief="flat",
                       font=('Arial', 12, 'bold'))
        
        tree_frame = ctk.CTkFrame(bookings_frame, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient="vertical")
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        columns = ("BookingID", "Passenger", "Flight", "Seat", "Status", "Amount", "Date")
        analysis_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set
        )
        
        tree_scroll_y.config(command=analysis_tree.yview)
        tree_scroll_x.config(command=analysis_tree.xview)
        
        column_widths = [100, 180, 120, 80, 100, 120, 150]
        for col, width in zip(columns, column_widths):
            analysis_tree.heading(col, text=col)
            analysis_tree.column(col, width=width, anchor="center")
        
        tree_scroll_y.pack(side="right", fill="y")
        tree_scroll_x.pack(side="bottom", fill="x")
        analysis_tree.pack(fill="both", expand=True)
        
        try:
            query = """
                SELECT b.BookingID,
                       CONCAT(p.FirstName, ' ', p.LastName),
                       f.FlightNumber,
                       s.SeatNumber,
                       b.BookingStatus,
                       COALESCE(pay.Amount, 0),
                       b.BookingDate
                FROM Booking b
                JOIN Passenger p ON b.PassengerID = p.PassengerID
                JOIN Flight f ON b.FlightID = f.FlightID
                JOIN Seat s ON b.SeatID = s.SeatID
                LEFT JOIN Payment pay ON b.BookingID = pay.BookingID
                ORDER BY b.BookingDate DESC
                LIMIT 50
            """
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                analysis_tree.insert("", "end", values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load bookings: {err}")
        
        btn_frame = ctk.CTkFrame(bookings_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        def open_powerbi_dashboard():
            powerbi_url = "D:/VIT,Pune/SEM 3/DBMS/DBMS CP2.pbix"
            try:
                webbrowser.open(powerbi_url)
                messagebox.showinfo("Power BI Dashboard", "Opening Power BI Dashboard in your browser...")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open Power BI Dashboard: {e}")
        
        def export_report():
            try:
                filename = f"booking_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                filepath = os.path.join("my_tickets", filename)
                
                if not os.path.exists("my_tickets"):
                    os.makedirs("my_tickets")
                
                with open(filepath, 'w') as f:
                    f.write("="*80 + "\n")
                    f.write("AIRLINE RESERVATION SYSTEM - BOOKING REPORT\n")
                    f.write("="*80 + "\n\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    
                    f.write("SUMMARY STATISTICS\n")
                    f.write("-"*80 + "\n")
                    f.write(f"Total Bookings: {total_bookings}\n")
                    f.write(f"Confirmed: {confirmed}\n")
                    f.write(f"Pending: {pending}\n")
                    f.write(f"Cancelled: {cancelled}\n")
                    f.write(f"Total Revenue: Rs. {total_revenue:,.2f}\n")
                    f.write(f"Average Booking Value: Rs. {avg_revenue:,.2f}\n\n")
                    
                    f.write("RECENT BOOKINGS\n")
                    f.write("-"*80 + "\n")
                    
                    query = """
                        SELECT b.BookingID,
                               CONCAT(p.FirstName, ' ', p.LastName),
                               f.FlightNumber,
                               s.SeatNumber,
                               b.BookingStatus,
                               COALESCE(pay.Amount, 0),
                               b.BookingDate
                        FROM Booking b
                        JOIN Passenger p ON b.PassengerID = p.PassengerID
                        JOIN Flight f ON b.FlightID = f.FlightID
                        JOIN Seat s ON b.SeatID = s.SeatID
                        LEFT JOIN Payment pay ON b.BookingID = pay.BookingID
                        ORDER BY b.BookingDate DESC
                    """
                    self.cursor.execute(query)
                    
                    for row in self.cursor.fetchall():
                        f.write(f"\nBooking ID: {row[0]}\n")
                        f.write(f"Passenger: {row[1]}\n")
                        f.write(f"Flight: {row[2]} | Seat: {row[3]}\n")
                        f.write(f"Status: {row[4]} | Amount: Rs. {row[5]:,.2f}\n")
                        f.write(f"Date: {row[6]}\n")
                        f.write("-"*40 + "\n")
                    
                    f.write("\n" + "="*80 + "\n")
                    f.write("END OF REPORT\n")
                    f.write("="*80 + "\n")
                
                messagebox.showinfo("Success", f"Report exported successfully!\n\nLocation: {filepath}")
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export report: {e}")
        
        powerbi_btn = ctk.CTkButton(
            btn_frame,
            text="📊 Open Power BI Dashboard",
            width=220,
            height=42,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#F2C811",
            hover_color="#D4A017",
            text_color="black",
            command=open_powerbi_dashboard
        )
        powerbi_btn.pack(side="left", padx=5)
        
        export_btn = ctk.CTkButton(
            btn_frame,
            text="Export Report",
            width=150,
            height=38,
            font=ctk.CTkFont(size=13),
            fg_color="#3498DB",
            hover_color="#2980B9",
            command=export_report
        )
        export_btn.pack(side="left", padx=5)
        
        refresh_btn = ctk.CTkButton(
            btn_frame,
            text="Refresh Data",
            width=150,
            height=38,
            font=ctk.CTkFont(size=13),
            command=self.show_analysis
        )
        refresh_btn.pack(side="left", padx=5)


if __name__ == "__main__":
    app = AirlineReservationSystem()