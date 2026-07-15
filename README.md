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
├── core/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── authentication_app/
│   ├── models.py
│   ├── admin.py
│   ├── authentication.py
│   ├── api/
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   └── migrations/
├── quizz_app/
│   ├── models.py
│   ├── admin.py
│   ├── api/
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   └── migrations/
├── manage.py
├── requirements.txt
├── db.sqlite3
└── README.md
```

## Prerequisites

- Python 3.9+
- pip (Python package manager)
- Virtual environment (recommended)
- FFmpeg (for audio processing)

### FFmpeg Installation

#### Windows - Download Method

1. Download the latest FFmpeg build from https://ffmpeg.org/download.html
   - Look for Windows builds from gyan.dev or BtbN
2. Extract the ZIP file to a location like `C:\ffmpeg`
3. Navigate to the `bin` folder (contains `ffmpeg.exe`)
4. Add the bin path to your system environment variables:
   - Right-click "This PC" → "Properties" → "Advanced system settings"
   - Click "Environment Variables…" → Edit the `Path` variable
   - Add `C:\ffmpeg\bin` to the list

#### Windows - Terminal Method

```bash
winget install --id Gyan.FFmpeg -e --source winget
```

#### macOS

1. Install Homebrew (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Install FFmpeg:
   ```bash
   brew install ffmpeg
   ``` 

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

Create a `.env` file in the project root and past your Gemini API key there:

```env
GEMINI_API_KEY=your-gemini-api-key-here
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

### Authentication Endpoints

#### User Registration
- **POST** `/api/auth/register/`
  - Description: Create a new user account

#### User Login
- **POST** `/api/auth/login/`
  - Description: Authenticate user and receive JWT tokens via HTTP-only cookies

#### User Logout
- **POST** `/api/auth/logout/`
  - Description: Invalidate tokens and clear authentication cookies

#### Refresh Token
- **POST** `/api/auth/refresh/`
  - Description: Generate a new access token using refresh token from cookies

### Quiz Endpoints

#### List All Quizzes (User's Quizzes)
- **GET** `/api/quizzes/`
  - Description: Retrieve all quizzes created by the authenticated user

#### Create Quiz from YouTube Video
- **POST** `/api/quizzes/`
  - Description: Create a new quiz by providing a YouTube video URL
  - Process:
    1. Downloads audio from YouTube video
    2. Transcribes audio to text using Faster-Whisper
    3. Generates quiz with 10 questions using Gemini API

#### Get Quiz Details
- **GET** `/api/quizzes/{id}/`
  - Description: Retrieve a specific quiz with all its questions

#### Update Quiz
- **PATCH** `/api/quizzes/{id}/`
  - Description: Update quiz title and description

#### Delete Quiz
- **DELETE** `/api/quizzes/{id}/`
  - Description: Delete a quiz and all associated questions






