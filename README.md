# About
This is a simple project using JWT with FastAPI for user authentication and authorization for learning purposes. User data is saved on a mocked database lost everytime the server restarts.

## Usage

1. Make sure you have python installed in your environment.

2. Create a virtual environment and access it using the following commands (PowerShell):
```
python -m venv .venv
.\.venv\Scripts\Activate
```

3. Install the project requirements using:
```
pip install -r requirements.txt
```

4. Create a .env file on root directory containing:
```env
JWT_SECRET="YOUR_SECRET_KEY"
JWT_COOKIE_EXPIRE_MINUTES= # Optional (Defaults to 60)
ENVIRONMENT= # Optional (Defaults to development)
```

5. Run server using:
```
uvicorn app:app
```

6. Access the Swagger and make tests on your local machine at:
```
localhost:8000/docs
```

## Structure
```
root/
├── .venv/             # Virtual environment files
├── dependencies/      # Custom functions used as dependencies from routes and another functions
├── models/            # Project models such as enums, dataclasses and pydantic models
├── utils/             # Files for specifics purposes, such as auth functions and environment variables validation
├── app.py             # Server initialization and routes
└── requirements.txt   # Project dependencies
```

## Endpoints

1. ```/```: Returns server message
2. ```/login```: Makes login and save httpOnly cookie
3. ```/logout```: Makes logout removing httpOnly cookie
4. ```/protected```: Protected route only available for logged users
5. ```/admin_only```: Protected route only available for logged users with admin role
6. ```/register```: Creates a new user on mocked database, enabling login. Available roles: "admin" and "user", see at ```/models/user.py```
