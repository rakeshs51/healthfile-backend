
# HealthFile

A platform to store and access medical reports.

## Tech Stack 
1. FastAPI
2. PostgreSQL for database
3. SQLAlchemy for ORM
4. SWAGGER UI for API docs

## Running Locally

 1. Set up a virtual env
        
        $ python -m venv env
        
    "env" is the virtual environment

    2. Make sure your terminal is running inside this env

    3. Install dependencies (Install pip and python3)
        
            $ pip install -r requirements.txt
            $ pip install FastAPI

    4. Running the app 
        
            $ uvicorn app.main:app --reload


## API Reference

#### Base URL
The base URL for all endpoints is http://localhost:8000/api/.

#### Authentication
Authentication is not required for the endpoints documented below.

#### Error Handling
All endpoints will return appropriate HTTP status codes and JSON responses in case of errors.


#### API Docs
        URL: localhost:8000/docs 


