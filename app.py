# =========================================
# IMPORTS
# =========================================
# FastAPI: to create the API
# HTTPException: to handle errors in API routes
# psycopg2: to connect to PostgreSQL / Neon
# os: to access the environment if needed
# uvicorn: to run the FastAPI app as a server
# asynccontextmanager: for lifespans (new way to startup/shutdown)

from fastapi import FastAPI, HTTPException
import psycopg2
import os
import uvicorn
from contextlib import asynccontextmanager

# =========================================
# CONFIGURATION
# =========================================
# Your Neon DB connection string
DATABASE_URL = "postgresql://neondb_owner:npg_V8W1EiYTDkFS@ep-blue-bush-ad7o4a79-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"


# =========================================
# DATABASE FUNCTIONS
# =========================================

# Function to connect to Neon DB
def get_connection():
    return psycopg2.connect(DATABASE_URL)

# Function to initialize the "team_members" table if it doesn't exist
def init_db():
    conn = get_connection() # connect
    cur = conn.cursor()  # create cursor
    cur.execute("""
        CREATE TABLE IF NOT EXISTS team_members (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            role VARCHAR(100)
        );
    """)
    conn.commit()   # confirm the changes
    cur.close()     # close cursor
    conn.close()   # close connection


# =========================================
# APP LIFESPAN (new startup/shutdown mode)
# =========================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting FastAPI app...") # message when the app starts
    try:
        init_db() # create table if it doesn't exist
        print("✅ Database initialized successfully.")
    except Exception as e:
        print("❌ Database initialization failed:")
        print(e) # show error if there is a problem with Neon
    yield
    print("🛑 Shutting down FastAPI app...") # message when the app is closed

# Create the FastAPI app with lifespan handler
app = FastAPI(lifespan=lifespan)


# =========================================
# ROUTES / API ENDPOINTS
# =========================================

# GET "/" - route for API testing
# Return message that the API is running
@app.get("/")
def read_root():
    return {"message": "Cloud Database API is running successfully!"}

# POST "/members" - add a new member to the table
# Params: name, role
@app.post("/members")
def add_member(name: str, role: str):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO team_members (name, role) VALUES (%s, %s) RETURNING id;", (name, role))
        new_id = cur.fetchone()[0]
        conn.commit()
        return {"message": "Member added successfully", "id": new_id}
    except Exception as e: 
       # If there are errors, return 500+ details
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

# GET "/members" - read all members in the table
@app.get("/members")
def get_members():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, role FROM team_members ORDER BY id;")
        rows = cur.fetchall()
        return [{"id": r[0], "name": r[1], "role": r[2]} for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

# PUT "/members/{member_id}" - update a member
# Params: member_id, name, role
@app.put("/members/{member_id}")
def update_member(member_id: int, name: str, role: str):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE team_members SET name=%s, role=%s WHERE id=%s;", (name, role, member_id))
        if cur.rowcount == 0:
              # If id does not exist, return 404
            raise HTTPException(status_code=404, detail="Member not found")
        conn.commit()
        return {"message": "Member updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

# DELETE "/members/{member_id}" - delete a member
@app.delete("/members/{member_id}")
def delete_member(member_id: int):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM team_members WHERE id=%s;", (member_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Member not found")
        conn.commit()
        return {"message": "Member deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()


# =========================================
# RUN THE APP
# =========================================
if __name__ == "__main__":
    print("💡 Launching server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
