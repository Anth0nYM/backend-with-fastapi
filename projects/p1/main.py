from typing import Optional
from fastapi import FastAPI, HTTPException
import pandas as pd
from pydantic import BaseModel

app = FastAPI()

# --- Models ---
class User(BaseModel):
    id: int
    name: str
    email: str
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

# --- Helpers---
def get_db():
    try:
        return pd.read_csv("data.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["id", "name", "email"])

# --- Rotas ---

# The Read of "cRud"
@app.get("/users", status_code=200)
def fetch_users():
    users_df = get_db()
    # orient='records' transforma o DataFrame em uma lista de dicionários (JSON array)
    return users_df.to_dict(orient="records")


# The Create of "Crud"
@app.post("/users", status_code=201)
def append_user(user: User):
    users_db = get_db()

    if not users_db.empty and user.id in users_db["id"].values:
        raise HTTPException(status_code=409, detail="User ID already exists")

    new_user_df = pd.DataFrame([user.model_dump()])
    combined_users = pd.concat([users_db, new_user_df], ignore_index=True)
    combined_users.to_csv("data.csv", index=False)
    return user


# The Update of "crUd" (Partial Update)
@app.patch("/users/{user_id}", status_code=200)
def update_user_partial(user_id: int, user_update: UserUpdate):
    users_db = get_db()

    if users_db.empty or user_id not in users_db["id"].values:
        raise HTTPException(status_code=404, detail="User not found")

    user_index = users_db.index[users_db["id"] == user_id].tolist()[0]
    update_data = user_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        users_db.at[user_index, key] = value

    users_db.to_csv("data.csv", index=False)
    
    return users_db.iloc[user_index].to_dict()


# The Update of "crUd" (Full Replace)
@app.put("/users/{user_id}", status_code=200)
def update_user_full(user_id: int, user: User):
    users_db = get_db()

    if users_db.empty or user_id not in users_db["id"].values:
        raise HTTPException(status_code=404, detail="User not found")

    # Same body id same url id (boas práticas)
    if user.id != user_id:
        raise HTTPException(status_code=400, detail="ID in path and body must match")

    # Hole row
    user_index = users_db.index[users_db["id"] == user_id].tolist()[0]
    
    users_db.at[user_index, "name"] = user.name
    users_db.at[user_index, "email"] = user.email
    
    users_db.to_csv("data.csv", index=False)
    return user


# The Delete of "cruD"
@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    users_db = get_db()

    if users_db.empty or user_id not in users_db["id"].values:
        raise HTTPException(status_code=404, detail="User not found")

    users_db = users_db[users_db["id"] != user_id]
    
    users_db.to_csv("data.csv", index=False)
    
    # 204 No Content
    return None