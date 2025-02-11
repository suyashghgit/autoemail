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
        models.Contact.email_sequence.label('sequence'),
        func.count().label('count')
    ).group_by(
        models.Contact.email_sequence
    ).order_by(
        models.Contact.email_sequence
    ).all()
    
    # Convert SQLAlchemy result to list of dicts and ensure all sequences are represented
    sequence_counts = {stat.sequence: stat.count for stat in stats}
    
    # Initialize with all possible sequences (1-6 for weeks, 9 for monthly)
    all_sequences = []
    for seq in range(1, 7):  # Weeks 1-6
        all_sequences.append({
            "sequence": seq,
            "count": sequence_counts.get(seq, 0)
        })
    # Add monthly (sequence 9)
    all_sequences.append({
        "sequence": 9,
        "count": sequence_counts.get(9, 0)
    })
    
    return all_sequences 