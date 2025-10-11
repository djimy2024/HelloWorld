Project Title:

Cloud Database API with FastAPI and Neon PostgreSQL

Author:

Djimy Francillon

Course:

CSE 310 – Applied Programming
Module 3: Cloud Databases
Date: October 11, 2025

Project Description

This project demonstrates how to create a FastAPI backend that connects to a Neon PostgreSQL cloud database.
It implements full CRUD (Create, Read, Update, Delete) operations for a simple table of team members, showing how cloud-based data can be managed through RESTful API endpoints.

The app automatically initializes the database table on startup using FastAPI’s lifespan events.
All interactions are handled through psycopg2 for secure SQL execution.

Technologies Used

Python 3.12
FastAPI (Web framework)
PostgreSQL via Neon Cloud
psycopg2 (Database driver)
Uvicorn (ASGI server)
Render / Localhost deployment

Project Features

Connects securely to a Neon PostgreSQL cloud database
Creates table automatically on app startup
CRUD API endpoints for managing team_members
Error handling using HTTPException
Clean code structure with function comments
Simple and modular database management

API Endpoints Overview
HTTP Method	Endpoint	Description	Parameters
GET	/	Test route, confirms API is running	None
POST	/members	Add a new member	name, role
GET	/members	Retrieve all members	None
PUT	/members/{member_id}	Update member info by ID	member_id, name, role
DELETE	/members/{member_id}	Delete a member by ID	member_id
How to Run Locally
1. Clone the repository
git clone https://github.com/djimy2024/HelloWorld.git
cd helloworld

2. Install dependencies
pip install fastapi psycopg2 uvicorn

3. Run the server
python app.py


The app will start at:

http://127.0.0.1:8000

4. Test Endpoints

Use Postman or your browser to test:

GET / → Check API status

POST /members?name=John&role=Developer → Add new member

GET /members → View all members

PUT /members/1?name=Jane&role=Manager → Update member

DELETE /members/1 → Delete member

Database Schema
CREATE TABLE IF NOT EXISTS team_members (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    role VARCHAR(100)
);

Example JSON Output
[
  {
    "id": 1,
    "name": "John Doe",
    "role": "Developer"
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "role": "Manager"
  }
]

Video Demonstration

🎥 Watch my full project demo here:
https://youtu.be/HKhsZ1ZJeQc?si=A-tR1h6sbq5PH_k_



GitHub Repository
https://github.com/djimy2024/HelloWorld.git

Reflection

This project taught me how to integrate FastAPI with a cloud database (Neon) and handle connection issues, SSL configurations, and structured CRUD design.
The biggest challenge was getting the Neon SSL connection right, but understanding the database connection flow improved my overall backend development skills.