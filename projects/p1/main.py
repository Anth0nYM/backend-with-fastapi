from fastapi import FastAPI, HTTPException
import pandas as pd  # type: ignore
from pydantic import BaseModel

app = FastAPI()

# Basemodels
class User(BaseModel):
    id: int
    name: str
    email: str


# The Read of "cRud", simple returns a statement
@app.get("/users", status_code=200)
def fetch_users():
    users = pd.read_csv("data.csv").to_dict(orient="records")
    return users


# The Create of "Crud", create a new contend 
@app.post("/users", status_code=201)
def append_user(user:User):
    try:
        users_db = pd.read_csv("data.csv")
    except FileNotFoundError:
        users_db = pd.DataFrame()

    new_user_df = pd.DataFrame([user.model_dump()])
    combined_users = pd.concat([users_db, new_user_df], ignore_index=True)
    combined_users.to_csv("data.csv", index=False)
    return user


'''
# The Update of "crUd", update partially a contend
@app.patch()

# The Update of "crUd", but update all the contend
@app.put()

# The Delete of "cruD", delete a contend
@app.delete()
'''