# Imports
from fastapi import FastAPI, Response, Request, HTTPException
import sqlite3
from pydantic import BaseModel

app = FastAPI()

class TodoRequest(BaseModel):
    title: str

# Database Setup
def get_db():
    connection = sqlite3.connect("todos.db")
    connection.execute("""CREATE TABLE IF NOT EXISTS todos(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT,
                   completed INTEGER
                   )""")
    connection.commit()
    return connection

@app.post("/todos")
async def create_item(body: TodoRequest):
    connection = get_db()
    connection.execute("INSERT INTO todos (title, completed) VALUES (?, ?)", (body.title, 0))
    connection.commit()
    connection.close()
    return {"message": "Todo created"}

@app.get("/todos")
async def get_item():
    connection = get_db()
    rows = connection.execute("SELECT * FROM todos").fetchall()
    connection.close()
    return [{"id": row[0], "title": row[1], "completed": row[2]} for row in rows]

@app.get("/todos/{id}")
async def get_item_by_id(id: int):
    connection = get_db()
    row = connection.execute("SELECT * FROM todos WHERE id = ?", (id,)).fetchone()
    connection.close()
    if not row:
        raise HTTPException(status_code=404, detail="Todo not found")
    return [{"id": row[0], "title": row[1], "completed": row[2]}]

@app.put("/todos/{id}")
async def update_item(id: int):
    connection = get_db()
    connection.execute("UPDATE todos SET completed = 1 WHERE id = ?", (id,))
    if connection.total_changes == 0:
        connection.close()
        raise HTTPException(status_code=404, detail="Todo not found") 
    connection.commit()
    connection.close()
    return {"message": "Todo updated"}

# @app.delete("/todos/{id}")
# async def delete_item(id: int):
#     connection = 