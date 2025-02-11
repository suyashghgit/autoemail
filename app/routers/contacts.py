from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from datetime import datetime

router = APIRouter()

@router.get("/contacts")
def get_contacts(db: Session = Depends(get_db)):
    contacts = db.query(models.Contact).order_by(models.Contact.user_id.asc()).all()
    return contacts 