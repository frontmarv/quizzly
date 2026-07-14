# Quizzly - Quiz Management System

A Django REST Framework application for managing quizzes with JWT-based authentication using secure HTTP-only cookies.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)


## Features

- **Quiz Management**: Create, update, and manage quizzes
- **Quiz Questions**: Manage individual quiz questions
- **User Authentication**: JWT-based authentication with HTTP-only cookies
- **User Registration**: Secure user registration with password confirmation
- **Token Refresh**: Automatic token refresh mechanism

## Project Structure

```
quizzly/
├── core/                          # Django project settings
│   ├── settings.py               # Project configuration
│   ├── urls.py                   # Main URL routing
│   ├── asgi.py                   # ASGI configuration
│   └── wsgi.py                   # WSGI configuration
├── registration_app/              # User authentication app
│   ├── models.py                 # User model
│   ├── admin.py                  # Django admin configuration
│   ├── authentication.py         # Authentication utilities
│   ├── api/
│   │   ├── serializers.py        # DRF serializers
│   │   ├── views.py              # API views for auth endpoints
│   │   └── urls.py               # App-specific URL patterns
│   └── migrations/               # Database migrations
├── quizz_app/                     # Quiz management app
│   ├── models.py                 # Quiz and Question models
│   ├── admin.py                  # Django admin configuration
│   ├── api/
│   │   ├── serializers.py        # DRF serializers
│   │   ├── views.py              # API views for quiz endpoints
│   │   └── urls.py               # App-specific URL patterns
│   └── migrations/               # Database migrations
├── manage.py                      # Django management command
├── requirements.txt               # Python dependencies
├── db.sqlite3                     # SQLite database (development)
└── README.md                      # This file
```

## Prerequisites

- Python 3.9+
- pip (Python package manager)
- Virtual environment (recommended)

FFMPEG 
Windows per Download 
Lade ein aktuelles FFmpeg-Build herunter: https://ffmpeg.org/download.html 
Windows builds (meist von gyan.dev oder BtbN). 
Entpacke die ZIP-Datei, z. B. nach C:\ffmpeg. 
Gehe in den Ordner bin → dort liegt ffmpeg.exe. 
Füge den bin-Pfad zu den Umgebungsvariablen hinzu: 
● Rechtsklick auf "Dieser PC" → "Eigenschaften" → "Erweiterte 
Systemeinstellungen". 
● "Umgebungsvariablen…" → In Path den Eintrag C:\ffmpeg\bin 
ergänzen. 
Windows per Terminalbefehl 
winget install --id Gyan.FFmpeg -e --source winget  
macOS 
Einfachster Weg: Homebrew installieren (falls nicht vorhanden): 
/bin/bash -c "$(curl -fsSL 
https://raw.githubusercontent.com/Homebrew/install/HEAD/in
stall.sh)" 
● FFmpeg installieren: 
brew install ffmpeg 

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd quizzly
```

### 2. Create Virtual Environment

```bash
# On Windows
python -m venv .venv
.venv\Scripts\activate

# On Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### Environment Setup

Create a `.env` file in the project root (for production/sensitive settings):

```env
SECRET_KEY=your-secret-key-here
```

### Database Setup

```bash
# Apply migrations
python manage.py migrate

# Create a superuser (for admin panel access)
python manage.py createsuperuser
```

## Running the Application

### Development Server

```bash
python manage.py runserver
```

The application will be available at: `http://localhost:8000`



## API Endpoints






