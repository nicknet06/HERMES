# Crisis Management System

## Overview
The Crisis Management System is a web-based emergency response platform designed to facilitate communication between citizens in distress and emergency response teams. It consists of two main components: a **user side** for reporting emergencies and an **administration side** for managing and dispatching resources.

## Features

### 1. User Side
- **Chat Interface**: Citizens can describe their emergency situation through a user-friendly chat system.
- **Voice Recording**: Users can record and send a voice message describing their emergency, which will be transcribed for the administration.
- **Automated Response**: An AI-powered agent will provide an immediate response based on the user's description.
- **Location Sharing**: Users' locations are sent to the administration for precise emergency response.

### 2. Administration Side
- **Interactive Map**: Displays a map of Greece, showing the locations of emergency service departments (hospitals, police stations, fire departments).
- **Resource Management**:
  - Stores real-time data on availability, vehicles, equipment, human resources, and specialties of emergency services.
- **Emergency Assessment via AI**:
  - Determines the validity of the emergency.
  - Assesses the severity of the crisis.
  - Identifies which sector(s) (hospital, police, fire department) should respond.
  - Determines necessary personnel, equipment, and vehicles.
  - Checks availability and assigns resources based on proximity and importance.
  - Generates a response for the user.
- **Data Storage**: Stores all emergency events in a database for future reference.
- **Crisis Correlation**: Analyzes incoming emergencies and correlates them with past events to provide better crisis insights.

## 3.Youtube VIDEO
- https://youtu.be/6aUYBJImYVk


### 4.RUN
- **Download the project from github.**
- **Make sure to go in src/app.py and add your openapi key in line 185**
- **First way**:
  - run in cmd -docker-compose up --build
- **Second way**:
  - pip install --no-cache-dir -r requirements.txt
  - change in app.py line 887 to app.run(host='127.0.0.1', port=5000, debug=True)
  - access in localhost:5000
  - cd src
  - python app.py

### 5.ENJOY
- **http://localhost**
- **http://localhost/chat**:
- **http://localhost/admin/dashboard**:

