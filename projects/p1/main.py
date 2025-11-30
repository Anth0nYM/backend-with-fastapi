from fastapi import FastAPI 
from bcrypt import checkpw

app = FastAPI() # you can replace app with your valid Python variable name
valid_users: dict = dict() # For now, a simple in-memory dictionary will be used to store the valid users.

@app.get("/c1/index")
def index():
    return {"message":"Welcome, Nerd!"}

@app.get("/c1/login/") # NOTE: In the real world, sending a password directly through the URL using a GET request is considered a bad practice.
def login(user_name: str, user_password: str):
    if valid_users.get(user_name) is None:
        return {"message": "user doesn't exist"}
    else:
        user = valid_users.get(user_name)
        if checkpw(user_password.encode(), user.passphrase.encode()): # type: ignore
            return user
        else:
            return {"message": "invalid user"}