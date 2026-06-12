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