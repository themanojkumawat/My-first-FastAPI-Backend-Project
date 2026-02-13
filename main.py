from fastapi import FastAPI
from routers import users, todos
from database import engine
from models import Base
from routers import users, students
from routers import logs


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="My First API",
    description="This is my first FastAPI project",
)

#### THEN include routers
app.include_router(users.router)
app.include_router(todos.router)
app.include_router(students.router)
app.include_router(logs.router)


@app.get("/")
def home():
    return {"msg": "My Frist API is running"}
