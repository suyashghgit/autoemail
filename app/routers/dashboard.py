from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import case, func, extract
from typing import List
from datetime import datetime, timedelta
from .. import models, schemas
from ..database import get_db
from fastapi import HTTPException

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
    
    # Include all weeks 1-10
    for seq in range(1, 11):
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
    
    # Add monthly (sequence 15)
    stat = next((s for s in stats if s.sequence_id == 15), None)
    sequence_stats.append({
        "sequence_id": 15,
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
    """Get detailed email delivery metrics for the last 30 days"""
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    try:
        # Get base metrics with detailed delivery information
        metrics_query = db.query(
            models.EmailMetric.sequence_id,
            func.count().label('total_sent'),
            func.sum(case(
                (models.EmailMetric.status == 'delivered', 1),
                else_=0
            )).label('delivered'),
            func.sum(case(
                (models.EmailMetric.status == 'failed', 1),
                else_=0
            )).label('failed')
        ).filter(
            models.EmailMetric.sent_at >= thirty_days_ago
        ).group_by(
            models.EmailMetric.sequence_id
        ).all()

        # Get detailed delivery information for each sequence
        result = []
        for metric in metrics_query:
            # Get successful deliveries details with recipient information
            successful_deliveries = db.query(
                models.EmailMetric,
                models.Contact
            ).join(
                models.Contact,
                models.Contact.user_id == models.EmailMetric.contact_id
            ).filter(
                models.EmailMetric.sequence_id == metric.sequence_id,
                models.EmailMetric.status == 'delivered',
                models.EmailMetric.sent_at >= thirty_days_ago
            ).all()

            # Get failed deliveries details with recipient information
            failed_deliveries = db.query(
                models.EmailMetric,
                models.Contact
            ).join(
                models.Contact,
                models.Contact.user_id == models.EmailMetric.contact_id
            ).filter(
                models.EmailMetric.sequence_id == metric.sequence_id,
                models.EmailMetric.status == 'failed',
                models.EmailMetric.sent_at >= thirty_days_ago
            ).all()

            # Format the delivery details
            successful_details = [
                {
                    "recipient": delivery[1].email_address,  # Get email from Contact
                    "sent_at": delivery[0].sent_at.isoformat(),
                    "message_id": delivery[0].message_id
                }
                for delivery in successful_deliveries
            ]

            failed_details = [
                {
                    "recipient": delivery[1].email_address,  # Get email from Contact
                    "attempted_at": delivery[0].sent_at.isoformat(),
                    "error_message": "Delivery failed"  # Add actual error message if available
                }
                for delivery in failed_deliveries
            ]

            # Calculate delivery rate
            total_sent = metric.total_sent or 0
            delivered = metric.delivered or 0
            delivery_rate = (delivered / total_sent * 100) if total_sent > 0 else 0

            sequence_name = "Monthly" if metric.sequence_id == 15 else f"Week {metric.sequence_id}"
            
            result.append({
                "sequence_id": metric.sequence_id,
                "sequence_name": sequence_name,
                "total_sent": total_sent,
                "delivery_rate": round(delivery_rate, 1),
                "successful_deliveries": successful_details,
                "failed_deliveries": failed_details
            })

        # Sort by sequence_id
        result.sort(key=lambda x: x["sequence_id"])
        return result

    except Exception as e:
        print(f"Error fetching email metrics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch email metrics: {str(e)}"
        ) 