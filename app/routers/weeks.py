from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from pydantic import BaseModel

router = APIRouter(tags=["weeks"])

class WeekToggle(BaseModel):
    week_id: int
    active: bool

@router.get("/active-weeks")
async def get_active_weeks(db: Session = Depends(get_db)):
    """Get all active week settings"""
    try:
        # Initialize default weeks if they don't exist
        default_weeks = list(range(1, 11)) + [15]  # Weeks 1-10 and Monthly (15)
        
        # Get existing sequences
        sequences = db.query(models.SequenceMapping).all()
        existing_ids = {seq.sequence_id for seq in sequences}
        
        # Add any missing sequences with default active status
        for week_id in default_weeks:
            if week_id not in existing_ids:
                try:
                    new_sequence = models.SequenceMapping(
                        sequence_id=week_id,
                        is_active=True,
                        email_body="",
                        article_link=""
                    )
                    db.add(new_sequence)
                    db.flush()
                except Exception as e:
                    print(f"Error adding sequence {week_id}: {str(e)}")
                    db.rollback()
                    continue
        
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error committing default sequences: {str(e)}")
        
        # Query all sequences and convert to dictionary
        sequences = db.query(models.SequenceMapping).all()
        return {seq.sequence_id: seq.is_active for seq in sequences}
    
    except Exception as e:
        print(f"Error in get_active_weeks: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch active weeks: {str(e)}"
        )

@router.post("/toggle-week")
async def toggle_week(week_toggle: WeekToggle, db: Session = Depends(get_db)):
    """Toggle a week's active status"""
    try:
        # Get the sequence record
        sequence = db.query(models.SequenceMapping).filter(
            models.SequenceMapping.sequence_id == week_toggle.week_id
        ).first()
        
        if not sequence:
            # Create new sequence record if it doesn't exist
            sequence = models.SequenceMapping(
                sequence_id=week_toggle.week_id,
                is_active=week_toggle.active,
                email_body="",
                article_link=""
            )
            db.add(sequence)
        else:
            # Update existing sequence record
            sequence.is_active = week_toggle.active
        
        db.commit()
        
        return {
            "sequence_id": sequence.sequence_id,
            "is_active": sequence.is_active
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to toggle week: {str(e)}"
        ) 