from fastapi import APIRouter

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.get("/")
def get_todos():
    return {"msg": "todos working"}
