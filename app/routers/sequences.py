from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from pydantic import HttpUrl, validator

router = APIRouter(
    prefix="",
    tags=["sequences"]
)

@router.get("/", response_model=List[schemas.SequenceMapping])
def get_sequences(db: Session = Depends(get_db)):
    """Get all sequence mappings"""
    sequences = db.query(models.SequenceMapping).order_by(models.SequenceMapping.sequence_id).all()
    return sequences

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