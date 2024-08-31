# InteRact Backend

Welcome to the **InteRact Backend** repository! This project is part of a full-stack application designed for real-time communication, including chat and video calling. The backend is built using Django, leveraging Django Channels for WebSocket communication to support real-time features.

## **Table of Contents**
- [Introduction](#introduction)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)

## **Introduction**
InteRact is a real-time communication platform that allows users to chat and make video calls. The backend handles user authentication, real-time messaging, and video call signaling, providing a robust and scalable infrastructure.

## **Features**
- **User Authentication**: Secure authentication using Django's custom user model and JWT.
- **Real-Time Messaging**: WebSocket-based communication using Django Channels.
- **Video Call Signaling**: WebRTC signaling for video calls.
- **Admin Panel**: A built-in admin interface to manage users and messages.

## **Architecture**
The backend is structured as a typical Django project, with the addition of Django Channels for handling real-time communication. The key components are:
- **User Authentication (user_auth)**: Manages user registration, login, and profile management.
- **Real-Time Communication (real_time)**: Manages chat messages and WebSocket connections.

## **Installation**
### **Prerequisites**
- Python 3.8+
- Django 3.2+
- Redis (for channel layers in Django Channels)


### **Steps**
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sajal-techie/InteRact-backend.git
   cd InteRact-backend
   ```
2. **Create and activate a virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3. **Install the dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4. **Set up PostgreSQL Database**
    create postgres database and add DB_NAME, DB_USER, DB_PASSWORD, DB_HOST 
    in .env file
5. **Apply the migrations:**
    ```bash
    python manage.py migrate
    ```
6. **Run the development server**
    ```bash
    python manage.py runserver
    ```