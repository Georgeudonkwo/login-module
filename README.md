# login-module
A user authentication module
# Flask JWT Authentication API

A secure Flask REST API with:
## Features
- User registration and login
- Password hashing with Werkzeug
- JWT-based authentication via `flask-jwt-extended`
- SQLite database with SQLAlchemy ORM
- `.env` environment configuration
- Swagger UI interactive docs via `flasgger`

---
## Requirements
Install all dependencies from the `requirements.txt` file:
pip install -r requirements.txt
## Test Endpoints using Swagger
** http://localhost:5000/apidocs/**
## Endpoints Descriptions:
Register a new user using: http://localhost:5000/register
*login and authenticate a user using: http://localhost:5000/login*
*Access a protected route using: http://localhost:5000/protected*

## Environment Configuration

Create a `.env` file in your root directory:

env
# .env
JWT_SECRET_KEY=your-secret-key


