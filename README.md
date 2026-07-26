# Flask SQLAlchemy Workout App

## Project Description

The Flask SQLAlchemy Workout App is a RESTful API built with Flask and SQLAlchemy for managing workout routines. The application allows users to create,read and retrieve workout records stored in a database. 
## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- SQLAlchemy
- Pipenv
- SQLite
- Pytest

## Installation Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Cheplel/flask-sqlalchemy-workout-app.git
```

### 2. Navigate into the project

```bash
cd flask-sqlalchemy-workout-app
```

### 3. Install dependencies

```bash
pipenv install
```

### 4. Activate the virtual environment

```bash
pipenv shell
```

### 5. Initialize the database

```bash
flask db init
```

### 6. Create migrations

```bash
flask db migrate -m "Initial migration"
```

### 7. Apply migrations

```bash
flask db upgrade
```

### 8. Seed the database (if applicable)

```bash
python seed.py
```

## Running the Application

Start the Flask server:

```bash
flask run
```

The API will run at:

```
http://127.0.0.1:5000
```

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /workouts | Retrieve all workouts |
| GET | /workouts/<id> | Retrieve a specific workout |
| POST | /workouts | Create a new workout |
| GET | /exercises | Retrieve all exercises |
| GET | /exercises/<id> | Retrieve a specific exercise |
| POST | /exercises | Create a new exercise |
| POST | /workouts/<workout_id>/exercises/<exercise_id>/workout_exercies | Create an association between workout and exercise |



## Example Workout JSON

```json
{
    "name": "Morning Cardio",
    "duration": 30,
    "category": "Cardio"
}
```

## Project Structure

```
flask-sqlalchemy-workout-app/
│
├── server/
│   ├── app.py
│   ├── models.py
│   ├── seed.py
│   └── ...
│

├── Pipfile
├── Pipfile.lock
├── README.md
└── .gitignore
```

## Testing


After starting the Flask server:

bash
flask run


Use Thunder Client (VS Code extension) or Postman to test the API endpoints.

Example:

GET http://127.0.0.1:5000/workouts
POST http://127.0.0.1:5000/exercises

## Author
Jean Koech