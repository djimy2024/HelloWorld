# Library to work with SQLite databases.
import sqlite3

# Library for interacting with the operating system.
import os

# Database file name.
DB_FILE = "vehicles.db"

def get_connection():
    
    # Open and return a connection to the SQLite database.
    return sqlite3.connect(DB_FILE)

def init_db():
    # Open a database connection.
    conn = get_connection()
    
    # Create a cursor to execute SQL commands.
    cursor = conn.cursor()
     
     # Create tables, triggers, and views if they don't exist.
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS classifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        make TEXT NOT NULL,
        model TEXT NOT NULL,
        year INTEGER NOT NULL,
        price REAL NOT NULL,
        classification_id INTEGER,
        FOREIGN KEY (classification_id) REFERENCES classifications(id)
    );

    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS inquiries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        vehicle_id INTEGER NOT NULL,
        message TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(id),
        FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
    );

    CREATE INDEX IF NOT EXISTS idx_vehicle_classification
    ON vehicles(classification_id);

    -- Corrected view
    CREATE VIEW IF NOT EXISTS vehicle_overview AS
    SELECT v.id, v.make, v.model, v.year, v.price, c.name AS classification
    FROM vehicles v
    LEFT JOIN classifications c ON v.classification_id = c.id;

    -- Trigger to prevent negative price insert
    CREATE TRIGGER IF NOT EXISTS validate_price
    BEFORE INSERT ON vehicles
    FOR EACH ROW
    BEGIN
        SELECT
            CASE
                WHEN NEW.price < 0 THEN RAISE(ABORT, 'Price cannot be negative')
            END;
    END;

    -- Trigger to prevent negative price update
    CREATE TRIGGER IF NOT EXISTS validate_update_price
    BEFORE UPDATE OF price ON vehicles
    FOR EACH ROW
    BEGIN
        SELECT
            CASE
                WHEN NEW.price < 0 THEN RAISE(ABORT, 'Price cannot be negative')
            END;
    END;
    """)

    # Save changes to the database
    conn.commit()
    
    # Close the connection
    conn.close()


def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Seed classifications
    cursor.execute("INSERT OR IGNORE INTO classifications (id, name) VALUES (?, ?)", (1, "SUV"))
    cursor.execute("INSERT OR IGNORE INTO classifications (id, name) VALUES (?, ?)", (2, "Sedan"))
    cursor.execute("INSERT OR IGNORE INTO classifications (id, name) VALUES (?, ?)", (3, "Truck"))

    # Seed vehicles
    cursor.execute("""
    INSERT OR IGNORE INTO vehicles (id, make, model, year, price, classification_id)
    VALUES (1, 'Toyota', 'RAV4', 2021, 28000, 1)
    """)
    cursor.execute("""
    INSERT OR IGNORE INTO vehicles (id, make, model, year, price, classification_id)
    VALUES (2, 'Honda', 'Civic', 2022, 22000, 2)
    """)
    cursor.execute("""
    INSERT OR IGNORE INTO vehicles (id, make, model, year, price, classification_id)
    VALUES (3, 'Ford', 'F-150', 2023, 35000, 3)
    """)

    # Seed customers
    cursor.execute("""
    INSERT OR IGNORE INTO customers (id, name, email)
    VALUES (1, 'John Doe', 'john@example.com')
    """)
    cursor.execute("""
    INSERT OR IGNORE INTO customers (id, name, email)
    VALUES (2, 'Jane Smith', 'jane@example.com')
    """)
    cursor.execute("""
    INSERT OR IGNORE INTO customers (id, name, email)
    VALUES (3, 'Djimy Francillon', 'djimy@example.com')
    """)

    # Seed inquiries
    cursor.execute("""
    INSERT OR IGNORE INTO inquiries (id, customer_id, vehicle_id, message)
    VALUES (1, 1, 1, 'Is this vehicle still available?')
    """)
    cursor.execute("""
    INSERT OR IGNORE INTO inquiries (id, customer_id, vehicle_id, message)
    VALUES (2, 2, 2, 'Can I schedule a test drive?')
    """)
    cursor.execute("""
    INSERT OR IGNORE INTO inquiries (id, customer_id, vehicle_id, message)
    VALUES (3, 3, 3, 'Is financing available for this vehicle?')
    """)

     # Save seeded data.
    conn.commit()
    
    # Close the connection.
    conn.close()

# ----------------- CRUD FUNCTIONS -----------------

def list_vehicles():
    # List all vehicles using the vehicle_overview view.
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehicle_overview")
    rows = cursor.fetchall()
    conn.close()
    print("\n--- Vehicles ---")
    for row in rows:
        print(row)

def add_vehicle():
    # Add a new vehicle via user input.
    make = input("Enter make: ")
    model = input("Enter model: ")
    year = int(input("Enter year: "))
    price = float(input("Enter price: "))
    classification_id = int(input("Enter classification ID: "))

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO vehicles (make, model, year, price, classification_id)
            VALUES (?, ?, ?, ?, ?)
        """, (make, model, year, price, classification_id))
        conn.commit()
        print("✅ Vehicle added successfully.")
    except sqlite3.IntegrityError as e:
        
        # Handle foreign key or other integrity errors.
        print("Error:", e)
    finally:
        conn.close()

def update_vehicle_price():
    # Update the price of a vehicle.
    vid = int(input("Enter vehicle ID: "))
    new_price = float(input("Enter new price: "))

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE vehicles SET price = ? WHERE id = ?", (new_price, vid))
        conn.commit()
        if cursor.rowcount > 0:
            print("✅ Vehicle price updated.")
        else:
            print("⚠️ Vehicle not found.")
    except sqlite3.IntegrityError as e:
        print("Error:", e)
    finally:
        conn.close()

def delete_vehicle():
    # Delete a vehicle by ID.
    vid = int(input("Enter vehicle ID to delete: "))
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vehicles WHERE id = ?", (vid,))
    conn.commit()
    if cursor.rowcount > 0:
        print("✅ Vehicle deleted.")
    else:
        print("⚠️ Vehicle not found.")
    conn.close()

def vehicles_per_classification():
    # Count the number of vehicles in each classification.
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.name, COUNT(v.id)
        FROM classifications c
        LEFT JOIN vehicles v ON c.id = v.classification_id
        GROUP BY c.name
    """)
    rows = cursor.fetchall()
    conn.close()
    print("\n--- Vehicles per Classification ---")
    for row in rows:
        print(row)

def add_classification():
    # Add a new classification.
    name = input("Enter classification name: ")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO classifications (name) VALUES (?)", (name,))
        conn.commit()
        print("✅ Classification added.")
    except sqlite3.IntegrityError as e:
        print("Error:", e)
    finally:
        conn.close()

def list_inquiries():
     # List all customer inquiries.
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.id, cu.name, cu.email, v.make || ' ' || v.model, i.message
        FROM inquiries i
        JOIN customers cu ON i.customer_id = cu.id
        JOIN vehicles v ON i.vehicle_id = v.id
    """)
    rows = cursor.fetchall()
    conn.close()
    print("\n--- Inquiries ---")
    for row in rows:
        print(row)

def add_customer():
    # Add a new customer.
    name = input("Enter customer name: ")
    email = input("Enter customer email: ")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO customers (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        print("✅ Customer added.")
    except sqlite3.IntegrityError as e:
        print("Error:", e)
    finally:
        conn.close()

def add_inquiry():
     # Add a new inquiry.
    customer_id = int(input("Enter customer ID: "))
    vehicle_id = int(input("Enter vehicle ID: "))
    message = input("Enter message: ")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO inquiries (customer_id, vehicle_id, message)
            VALUES (?, ?, ?)
        """, (customer_id, vehicle_id, message))
        conn.commit()
        print("✅ Inquiry added.")
    except sqlite3.IntegrityError as e:
        print("Error:", e)
    finally:
        conn.close()

# ----------------- CLI -----------------

def main():
    # Delete old database for a clean start
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    # Initialize database and tables.
    init_db()
    
    # Insert initial data.
    seed_data()


    # Main CLI loop.
    while True:
        print("""
--- Vehicle Inventory Management System ---
1. List Vehicles
2. Add Vehicle
3. Update Vehicle Price
4. Delete Vehicle
5. Vehicles per Classification
6. Add Classification
7. List Inquiries
8. Add Customer
9. Add Inquiry
0. Exit
        """)
        choice = input("Enter choice: ")
        
        # Call the corresponding function based on user's choice.
        if choice == "1":
            list_vehicles()
        elif choice == "2":
            add_vehicle()
        elif choice == "3":
            update_vehicle_price()
        elif choice == "4":
            delete_vehicle()
        elif choice == "5":
            vehicles_per_classification()
        elif choice == "6":
            add_classification()
        elif choice == "7":
            list_inquiries()
        elif choice == "8":
            add_customer()
        elif choice == "9":
            add_inquiry()
        elif choice == "0":
            break
        else:
            print("❌ Invalid choice, try again.")

if __name__ == "__main__":
    main()
