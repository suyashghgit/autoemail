from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="",
    tags=["sequences"]
)

@router.get("/", response_model=List[schemas.SequenceMapping])
def get_sequences(db: Session = Depends(get_db)):
    """Get all sequence mappings"""
    sequences = db.query(models.SequenceMapping).all()
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
    
    for key, value in sequence.dict().items():
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