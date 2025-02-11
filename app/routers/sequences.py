from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas
from ..database import get_db
from pydantic import HttpUrl, validator

router = APIRouter(
    tags=["sequences"]
)

# Update the schema to handle nullable fields
class SequenceMapping(schemas.SequenceMapping):
    email_body: Optional[str] = ''  # Default empty string if NULL
    article_link: Optional[str] = ''  # Default empty string if NULL

@router.get("/", response_model=List[SequenceMapping])
def get_sequences(db: Session = Depends(get_db)):
    """Get all sequence mappings"""
    # Initialize default sequences if they don't exist
    default_sequences = [
        {"sequence_id": i, "email_body": "", "article_link": ""}
        for i in list(range(1, 11)) + [15]  # Weeks 1-10 and Monthly (15)
    ]
    
    # Get existing sequences
    existing_sequences = db.query(models.SequenceMapping).order_by(models.SequenceMapping.sequence_id).all()
    existing_ids = {seq.sequence_id for seq in existing_sequences}
    
    # Add any missing default sequences
    for default_seq in default_sequences:
        if default_seq["sequence_id"] not in existing_ids:
            db_sequence = models.SequenceMapping(**default_seq)
            db.add(db_sequence)
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error creating default sequences: {e}")
    
    # Return all sequences
    return db.query(models.SequenceMapping).order_by(models.SequenceMapping.sequence_id).all()

@router.get("/{sequence_id}", response_model=schemas.SequenceMapping)
def get_sequence(sequence_id: int, db: Session = Depends(get_db)):
    """Get a specific sequence mapping by ID"""
    sequence = db.query(models.SequenceMapping).filter(
        models.SequenceMapping.sequence_id == sequence_id
    ).first()
    if sequence is None:
        raise HTTPException(status_code=404, detail="Sequence not found")
    return sequence

@router.post("/", response_model=schemas.SequenceMapping)
def create_sequence(
    sequence: schemas.SequenceMappingCreate,
    db: Session = Depends(get_db)
):
    """Create a new sequence mapping"""
    db_sequence = models.SequenceMapping(**sequence.dict())
    db.add(db_sequence)
    db.commit()
    db.refresh(db_sequence)
    return db_sequence

@router.put("/{sequence_id}", response_model=schemas.SequenceMapping)
def update_sequence(
    sequence_id: int,
    sequence: schemas.SequenceMappingBase,
    db: Session = Depends(get_db)
):
    """Update a sequence mapping"""
    db_sequence = db.query(models.SequenceMapping).filter(
        models.SequenceMapping.sequence_id == sequence_id
    ).first()
    if db_sequence is None:
        raise HTTPException(status_code=404, detail="Sequence not found")
    
    # Convert the sequence dict and ensure article_link is stored as string
    update_data = sequence.dict()
    if 'article_link' in update_data:
        # Convert HttpUrl to string and handle the prefix
        article_link = str(update_data['article_link'])
        if article_link and not article_link.startswith(('http://', 'https://')):
            article_link = f'http://{article_link}'
        update_data['article_link'] = article_link
    
    for key, value in update_data.items():
        setattr(db_sequence, key, value)
    
    db.commit()
    db.refresh(db_sequence)
    return db_sequence

@router.delete("/{sequence_id}")
def delete_sequence(sequence_id: int, db: Session = Depends(get_db)):
    """Delete a sequence mapping"""
    db_sequence = db.query(models.SequenceMapping).filter(
        models.SequenceMapping.sequence_id == sequence_id
    ).first()
    if db_sequence is None:
        raise HTTPException(status_code=404, detail="Sequence not found")
    
    db.delete(db_sequence)
    db.commit()
    return {"message": "Sequence deleted successfully"}

# Remove the old /groups endpoint
# @router.get("/groups", response_model=List[schemas.EmailGroup])
# def get_email_groups(db: Session = Depends(get_db)):
#     """Get all contacts grouped by their sequence number"""
#     # ... rest of the function remains the same ... 