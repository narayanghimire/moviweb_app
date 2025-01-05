# MovieWeb - User and Movie Management

MovieWeb is a web application for managing users and movies. Users can add movies, update movie details, and manage movie ratings. The application fetches movie data from the OMDb API and stores the data in an SQLite database.

## Features

- Add, update, and delete movies for users.
- Fetch movie data from OMDb API.

---

## Prerequisites

Ensure you have the following installed on your system:

- Python 3.10 or later

---

## Installation

## Getting Started

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### Step 2: Installing project
```bash
pip install -r requirements.txt
```

### Step 3: Set Up the .env File
```bash
Create a .env file in the root directory of the project. Add the  values:
API_KEY='6769d9a1'
DB_NAME='moviwebapp.db'
```

### Step 4: Running Project
```bash
python3 app.py

```


### Additional Information:
- **`requirements.txt`**: This should contain all the Python dependencies that the project uses, such as Flask, Werkzeug, SQLAlchemy, and dotenv.
- **`.env`**: The `.env` file is used to securely store sensitive information like API keys and database credentials.
