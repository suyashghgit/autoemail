from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import case, func
from typing import List
from datetime import datetime, timedelta
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
            "completed_contacts": 0,
            "pending_contacts": stat.total_contacts if stat else 0,
            "delivery_rate": 0.0,
            "success_rate": 0.0
        })
    
    # Add monthly (sequence 9)
    stat = next((s for s in stats if s.sequence_id == 9), None)
    sequence_stats.append({
        "sequence_id": 9,
        "sequence_name": "Monthly",
        "total_contacts": stat.total_contacts if stat else 0,
        "completed_contacts": 0,
        "pending_contacts": stat.total_contacts if stat else 0,
        "delivery_rate": 0.0,
        "success_rate": 0.0
    })
    
    return sequence_stats 

@router.get("/email_metrics")
async def get_email_metrics(db: Session = Depends(get_db)):
    """Get email delivery metrics for the last 30 days"""
    # Calculate the date 30 days ago
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    metrics = db.query(
        models.EmailMetric.sequence_id,
        func.count().label('total_sent'),
        func.avg(case(
            (models.EmailMetric.status == 'delivered', 100.0),
            else_=0.0
        )).label('delivery_rate')
    ).filter(
        models.EmailMetric.sent_at >= thirty_days_ago
    ).group_by(
        models.EmailMetric.sequence_id
    ).all()
    
    # Format the results
    result = []
    for metric in metrics:
        sequence_name = "Monthly" if metric.sequence_id == 9 else f"Week {metric.sequence_id}"
        result.append({
            "sequence_id": metric.sequence_id,
            "sequence_name": sequence_name,
            "total_sent": metric.total_sent,
            "delivery_rate": round(metric.delivery_rate or 0, 1)
        })
    
    # Sort by sequence_id
    result.sort(key=lambda x: x["sequence_id"])
    
    return result 