# ✈️ Airline Reservation System

## 📌 Overview

The **Airline Reservation System** is a desktop-based application developed using **Python (CustomTkinter)** and **MySQL**. It provides a complete solution for managing airline operations such as passenger registration, flight management, booking, payment processing, and boarding pass generation.

This system is designed to simulate real-world airline booking workflows with an interactive and user-friendly interface.

---

## 🚀 Features

### 🔐 Authentication System

* Secure login system for users
* Role-based access control
* Database validation for credentials

### 👤 Passenger Management

* Add, update, delete passenger details
* OTP-based email verification for new passengers
* Search functionality (name, email, passport)

### ✈️ Flight Management

* View all available flights
* Flight details including source, destination, timing, and status

### 🏢 Airport Management

* Manage airport data (city, country, IATA code)
* Search and filter airport records

### 🎫 Booking System

* Search flights based on source and destination
* Seat selection with real-time availability
* Passenger selection for booking

### 💳 Payment System

* Multiple payment methods (Card, UPI, Net Banking, Cash)
* Booking confirmation after successful payment

### 🪑 Seat Management

* Visual seat layout
* Prevent double booking using triggers
* Real-time seat availability updates

### 📄 Boarding Pass Generation

* Auto-generate PDF boarding pass
* Includes passenger, flight, and seat details
* Stored locally in `my_tickets` folder

### 📊 Dashboard & Analytics

* Total passengers
* Total flights
* Confirmed bookings
* Revenue tracking
* Recent bookings table

---

## 🛠️ Technologies Used

### 💻 Frontend

* Python
* CustomTkinter (Modern GUI)

### 🗄️ Backend

* MySQL Database

### 📚 Libraries

* `customtkinter`
* `tkinter`
* `mysql.connector`
* `reportlab`
* `smtplib`
* `random`
* `datetime`

---

## 🧱 Database Structure

Main tables used:

* **Users**
* **Passenger**
* **Flight**
* **Airport**
* **Seat**
* **Booking**
* **Payment**

### 🔄 Triggers Used

* Prevent booking if seat is already booked
* Auto-update seat status after booking
* Restore seat availability after booking deletion

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/airline-reservation-system.git
cd airline-reservation-system
```

### 2️⃣ Install Dependencies

```bash
pip install customtkinter mysql-connector-python reportlab
```

### 3️⃣ Setup MySQL Database

* Create database: `AIRLINE_RESERVATION`
* Import SQL tables and triggers
* Update credentials in code:

```python
host="localhost"
user="root"
password="your_password"
database="AIRLINE_RESERVATION"
```

### 4️⃣ Run the Application

```bash
python main.py
```

---

## 📁 Project Structure

```
📦 Airline-Reservation-System
 ┣ 📂 backend
 ┣ 📂 database
 ┣ 📂 my_tickets
 ┣ 📜 main.py
 ┣ 📜 README.md
```

---

## 👥 Team Members & Contributions

| Member            | Contribution                                                          |
| ----------------- | --------------------------------------------------------------------- |
| **Chirag Gandhi** | Core development, booking system, seat selection, payment integration |
| **Pragati**       | Passenger module, OTP verification, UI improvements                   |
| **Sarvesh**       | Database setup, queries, testing                                      |
| **Tejas**         | UI assistance, documentation, minor features                          |

---

## 🎯 Key Highlights

* Real-world airline workflow simulation
* OTP-based secure passenger registration
* Seat booking with conflict prevention (DB triggers)
* Automated PDF ticket generation
* Clean and interactive GUI

---

## ⚠️ Limitations

* Email OTP is simulated (not using real SMTP in demo)
* No online payment gateway integration
* Desktop-based (not web-based)

---

## 🔮 Future Enhancements

* Real email OTP integration
* Online payment gateway (Razorpay/Stripe)
* Web-based version
* Admin analytics dashboard
* AI-based flight recommendation

---

## 📸 Screenshots

*(Add your screenshots here for better presentation)*

---

## 📜 License

This project is developed for **academic purposes** and is free to use.

---

## 🙌 Acknowledgement

Special thanks to our faculty and team members for guidance and support throughout the project.

---
