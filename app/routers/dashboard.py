from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    tags=["dashboard"]
)

@router.get("/dashboard_stats", response_model=List[schemas.SequenceStats])
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get statistics about number of contacts in each sequence"""
    stats = db.query(
        models.Contact.email_sequence.label('sequence_id'),
        func.count().label('total_contacts')
    ).group_by(
        models.Contact.email_sequence
    ).order_by(
        models.Contact.email_sequence
    ).all()
    
    # Convert SQLAlchemy result to list of SequenceStats
    sequence_stats = []
    for seq in range(1, 7):  # Weeks 1-6
        stat = next((s for s in stats if s.sequence_id == seq), None)
        sequence_stats.append({
            "sequence_id": seq,
            "sequence_name": f"Week {seq}",
            "total_contacts": stat.total_contacts if stat else 0,
            "completed_contacts": 0,  # You can add these calculations later
            "pending_contacts": stat.total_contacts if stat else 0,
            "success_rate": 0.0  # You can add this calculation later
        })
    
    # Add monthly (sequence 9)
    stat = next((s for s in stats if s.sequence_id == 9), None)
    sequence_stats.append({
        "sequence_id": 9,
        "sequence_name": "Monthly",
        "total_contacts": stat.total_contacts if stat else 0,
        "completed_contacts": 0,
        "pending_contacts": stat.total_contacts if stat else 0,
        "success_rate": 0.0
    })
    
    return sequence_stats 