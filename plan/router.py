from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from .schemas import PlansBase, PlansListView, PlanUpdateSchema
from .crud import create_plans, get_all_plans, get_a_plan, delete_a_plan, update_a_plan
from config.database import get_db


router = APIRouter(
    prefix="/api/v1/plans",
    tags= ["plans"]
)

@router.post("/create_plan")
def create_plan(request: PlansBase, database: Session = Depends(get_db)):
    return create_plans(database, request)

@router.get("/all_plans")
def list_plans(database: Session = Depends(get_db)):
    return get_all_plans(database)

@router.get("/{id}/plans", response_model = PlansListView)
def read_plan(id: int, database: Session = Depends(get_db)):
    return get_a_plan(id, database)

@router.delete("/delete/{id}")
def delete_plan(id: int, database: Session = Depends(get_db)):
    return delete_a_plan(id, database)

@router.post("/update/{id}")
def update_plan(id: int, request: PlanUpdateSchema, database: Session = Depends(get_db)):
    return update_a_plan(id, request, database)