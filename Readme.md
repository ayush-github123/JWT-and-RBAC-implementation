# 🚀 Scalable JWT Authentication & RBAC API

A production-ready REST API built with **FastAPI + PostgreSQL**, implementing secure authentication, role-based access control, refresh token rotation, and modular scalable architecture.  

This project was developed as part of a Backend Developer assignment to demonstrate secure system design, API best practices, and scalability awareness.

---

## 🏗️ Architecture Overview

**Tech Stack**
- FastAPI (Async)
- PostgreSQL
- SQLAlchemy 2.0 (Typed ORM)
- JWT (Access + Refresh Tokens)
- bcrypt (Password hashing)

**Architecture Pattern**
- Layered architecture
  - Routers (HTTP layer)
  - Services (Business logic)
  - Models (Database layer)
  - Dependencies (Auth & RBAC)
- Stateless access tokens
- Database-backed refresh token rotation
- Role-based authorization via dependency injection

---

## 🔐 Authentication Design

### Token Strategy
- Short-lived **Access Token**
- Long-lived **Refresh Token**
- Refresh token rotation
- Refresh tokens stored **hashed** in database
- Token type enforcement (`access` vs `refresh`)
- JWT includes:
  - `sub` (user_id)
  - `role`
  - `exp`
  - `iat`
  - `jti`

### Password Security
- bcrypt hashing via passlib
- No plain-text password storage
- Secure verification

---

## 👥 Role-Based Access Control (RBAC)

Roles:
- `USER`
- `ADMIN`

Authorization Rules:
- Users can manage only their own tasks
- Admins can view and delete all tasks
- Role checks enforced via dependency layer
- Self role assignment during registration for assignment ease
---

## 📦 Features Implemented

### Backend

- User Registration
- User Login
- Access & Refresh Token System
- Token Rotation
- Logout with Refresh Token Revocation
- Task CRUD APIs
- Ownership Enforcement
- Admin Override
- Centralized Exception Handling
- Structured Logging
- UUID Primary Keys

---

## 📚 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and receive tokens |
| POST | `/auth/refresh` | Rotate tokens |
| POST | `/auth/logout` | Revoke refresh token |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks/` | Create task |
| GET | `/tasks/` | List tasks (paginated) |
| PUT | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |

---

## 🗄️ Database Schema

### Users Table
- id (UUID, PK)
- username (unique)
- email (unique)
- password_hash
- role
- is_active
- created_at
- updated_at

### Refresh Tokens Table
- id (UUID)
- user_id (FK)
- token_hash (indexed)
- expires_at
- revoked
- created_at

### Tasks Table
- id (UUID)
- title
- description
- is_completed
- owner_id (FK)
- created_at
- updated_at

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```bash
git clone <your_repo_url>
cd backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate     # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
Create a .env file in the root directory:

DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
SECRET_KEY=your_super_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

```
⚠️ Never commit .env file to version control.

### 5. Initialize Database

If using auto table creation (development mode):
```bash
uvicorn app.main:app --reload
```

### 6. Start the Server
```bash
uvicorn app.main:app --reload
```

Server runs at:

- http://127.0.0.1:8000


### Swagger documentation available at:

- http://127.0.0.1:8000/docs

### API Testing

You can test endpoints using:

- Swagger UI (/docs)
- Postman
- VS Code REST Client (test.rest file included)

Test scenarios covered:

- User registration
- Login

- Accessing protected routes
- Token refresh
- Logout & token revocation
- Role-based restrictions
- Unauthorized access handling

### Security Practices

- Password hashing using bcrypt
- Refresh tokens stored hashed (SHA-256)
- Access token expiration enforced