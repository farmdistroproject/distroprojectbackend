from .models import Plans
from .schemas import PlansBase
from sqlalchemy.orm.session import Session
from fastapi import HTTPException,status

def create_plans(db: Session, request: PlansBase):

    new_plan = Plans(
        name = request.name,
        description = request.description,
        duration = request.duration,
        price  = request.price
    )
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)

    return new_plan

def get_all_plans(database: Session):

    return database.query(Plans).all()

def get_a_plan(id: int, database: Session):
    plan = database.query(Plans).filter(Plans.pkid == id).first()
    if not plan:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail=f"Plan with id: {id} not found")
    return plan

def delete_a_plan(id: int, db: Session):
    plan = db.query(Plans).filter(Plans.pkid == id).first()
    db.delete(plan)
    db.commit()
    return "Deleted Successfully"