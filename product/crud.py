from .models import Plans
from .schemas import PlansBase
from sqlalchemy.orm.session import Session


def create_plans(database_session: Session, request: PlansBase):

    new_plan = Plans(
        name = request.name,
        description = request.description,
        duration = request.duration,
        price  = request.price
    )
    database_session.add(new_plan)
    database_session.commit()
    database_session.refresh(new_plan)

    return new_plan

def get_all_plans(database: Session):

    return database.query(Plans).all()