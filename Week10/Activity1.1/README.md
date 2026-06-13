## Overview

The System is a secure web application that manages user accounts, authentication, authorization, and user administration. The system implements Role-Based Access Control with three roles: Admin, Employee, and User.

```
Main
│
├── Authentication
│   ├── Sign Up
│   ├── Login
│   ├── Logout
│   ├── Forgot Password
│   └── Reset Password
│
├── User Profile
│   ├── View Profile
│   └── Update Profile
│
├── User Management (Admin)
│   ├── Create User
│   ├── View Users
│   ├── Update User
│   └── Delete User
│
└── Role Management
    ├── Admin
    ├── Employee
    └── User
```
---

# Features

## Authentication

### Signup
The Signup feature allows new users to create an account and access the system.

**Functionality:**
- Enter Full Name
- Enter Date of Birth
- Enter Email Address
- Enter Password
- Select User Role (Admin creates Employee/User accounts)
- Validate user information
- Check for duplicate email addresses
- Encrypt password before storing
- Save user information in the database
- Redirect user to the Login page after successful registration

### Login
Users can log in using their registered email address and password.

**Functionality:**
- Validate user credentials
- Verify encrypted password
- Generate authentication token/session
- Redirect authenticated users to the dashboard

### Logout
Users can securely log out of the system.

**Functionality:**
- Invalidate active session/token
- Clear authentication data

### Forgot Password
Users can request a password reset if they forget their password.

**Functionality:**
- Enter registered email address
- Generate secure password reset token
- Send password reset link via email
- Store token information in database

### Reset Password
Users can reset their password using the password reset link.

**Functionality:**
- Validate reset token
- Verify token expiration
- Update password securely
- Mark token as used

---

## User Profile Management

Each user account contains the following information:

- Full Name
- Date of Birth
- Email Address
- Role

### Profile Features

#### View Profile
Users can view their personal information.

#### Update Profile
Users can update:
- Full Name
- Date of Birth

---

# User Roles

## Admin

The Admin role has complete access to user management features.

### Permissions

#### Create User
Admin can create:
- Admin accounts
- Employee accounts
- User accounts

#### Read Users
Admin can:
- View all users
- Search users
- View user details

#### Update Users
Admin can:
- Edit user information
- Change user roles

#### Delete Users
Admin can:
- Remove user accounts

#### Password Management
Admin can:
- Reset passwords
- Manage account access

---
# Database Table Structures

## 1. Roles Table

Stores the available user roles in the system.

| Column Name | Data Type   | Constraints      | Description            |
| ----------- | ----------- | ---------------- | ---------------------- |
| id          | INT         | Primary Key      | Unique role identifier |
| role_name   | VARCHAR(50) | UNIQUE, NOT NULL | Role name              |

### Example Data

| id | role_name |
| -- | --------- |
| 1  | Admin     |
| 2  | Employee  |
| 3  | User      |

### SQL

```sql
CREATE TABLE roles (
    id INT PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE
);
```

---

## 2. Users Table

Stores user account and profile information.

| Column Name   | Data Type    | Constraints      | Description            |
| ------------- | ------------ | ---------------- | ---------------------- |
| id            | UUID         | Primary Key      | Unique user identifier |
| full_name     | VARCHAR(255) | NOT NULL         | User full name         |
| date_of_birth | DATE         | NOT NULL         | User date of birth     |
| email         | VARCHAR(255) | UNIQUE, NOT NULL | User email             |
| password_hash | VARCHAR(255) | NOT NULL         | Encrypted password     |
| role_id       | INT          | Foreign Key      | References Roles table |
| created_at    | TIMESTAMP    | NOT NULL         | Account creation date  |
| updated_at    | TIMESTAMP    | NOT NULL         | Last update date       |

### SQL

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id)
);
```

---

## 3. Password_Resets Table

Stores password reset requests generated through the Forgot Password feature.

| Column Name | Data Type    | Constraints | Description                      |
| ----------- | ------------ | ----------- | -------------------------------- |
| id          | UUID         | Primary Key | Unique reset request identifier  |
| user_id     | UUID         | Foreign Key | References Users table           |
| reset_token | VARCHAR(255) | NOT NULL    | Password reset token             |
| expires_at  | TIMESTAMP    | NOT NULL    | Token expiration time            |
| used        | BOOLEAN      | NOT NULL    | Indicates whether token was used |
| created_at  | TIMESTAMP    | NOT NULL    | Request creation date            |

### SQL

```sql
CREATE TABLE password_resets (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    reset_token VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## Database Relationships

* One Role can be assigned to many Users.
* One User can have many Password Reset Requests.
* Each Password Reset Request belongs to one User.


