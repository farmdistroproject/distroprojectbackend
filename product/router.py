from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from .schemas import PlansBase, PlansListView
from .crud import create_plans, get_all_plans, get_a_plan
from config.database import get_db


router = APIRouter(
    prefix="/plans",
    tags= ["plans"]
)

@router.post("/create_plan")
def create_plan(request: PlansBase, database: Session = Depends(get_db)):
    return create_plans(database, request)

@router.get("/all_plans")
def create_plan(database: Session = Depends(get_db)):
    return get_all_plans(database)

@router.get("/{id}/plans", response_model = PlansListView)
def create_plan(id: int, database: Session = Depends(get_db)):
    return get_a_plan(id, database)