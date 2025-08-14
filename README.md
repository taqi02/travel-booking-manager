# Travel Booking Manager

Travel Booking Manager is a Python-based desktop application with a Tkinter GUI that allows users to manage travel bookings efficiently.  
It provides features to add, edit, cancel, and view passenger booking records, with all data stored securely in a MongoDB database.

---

## Features

1. Add New Bookings – Store passenger details including name, destination, date, and status.
2. Edit Bookings – Update booking information from the GUI.
3. Cancel Bookings – Remove bookings from the database with confirmation.
4. View Records – Display all bookings in a sortable table.
5. Clear & Refresh – Reset form fields or reload data.
6. Database Storage – MongoDB for persistent data storage.

---

## Technologies Used

- Python 3
- Tkinter – GUI framework
- tkcalendar – Date picker widget
- MongoDB – NoSQL database
- uuid – Unique booking ID generator
- pymongo – MongoDB Python driver

---

1. Install dependencies:

pip install tkcalendar pymongo


2. Start MongoDB locally:

mongod --dbpath "C:\path\to\mongodb\data"


3.Run the application:

python booking_manager.py

##How to Use

1. Enter Passenger Name, Destination, Travel Date, and Status.
2. Click Add Booking to save the record in MongoDB.
3. Select a booking to Edit or Cancel.
4. Click Refresh List to update the displayed data.

##Screenshots

