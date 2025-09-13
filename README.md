

   # Vehicle Inventory Management System (VIMS)

## Author
Djimy Francillon

## Overview
This project is a **Vehicle Inventory Management System** written in Python using **SQLite** as the database.  
It allows users to manage vehicles, classifications, customers, and inquiries through a simple command-line interface (CLI).  

## Description
VIMS supports the following functionality:  
- **Vehicles:** Add, list, update price, and delete vehicles.  
- **Classifications:** Add new vehicle classifications (e.g., SUV, Sedan, Truck).  
- **Customers:** Add new customers.  
- **Inquiries:** Track customer inquiries about specific vehicles.  
- **Reports:** Count vehicles per classification.  

The system uses an SQLite database (`vehicles.db`) to persist all data, so information remains after the program closes.  

## Development Environment
- **Language:** Python 3.x  
- **Database:** SQLite3  
- **IDE/Editor:** VS Code  
- **Operating System:** Windows

## How It Works
1. The program initializes the database and seeds initial data if it doesn’t exist.  
2. The user interacts with a **menu-driven CLI** to perform CRUD operations.  
3. All modifications are saved to the SQLite database, so data persists between sessions.  

## How to Run
1. Clone the repository.
2. Run the following command:
   python main.py
