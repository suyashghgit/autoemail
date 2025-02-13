from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models import Contact

def test_update_sequences(client: TestClient, db: Session):
    # Create test contacts with different join dates
    contacts = [
        Contact(
            user_id=1,
            first_name="Week1",
            last_name="Test",
            email_address="week1@test.com",
            email_sequence=1,
            join_date=datetime.now() - timedelta(days=5),  # 5 days ago (week 1)
            last_email_sent_at=datetime.now()
        ),
        Contact(
            user_id=2,
            first_name="Week3",
            last_name="Test",
            email_address="week3@test.com",
            email_sequence=1,
            join_date=datetime.now() - timedelta(days=16),  # ~2.3 weeks ago (week 3)
            last_email_sent_at=datetime.now()
        ),
        Contact(
            user_id=3,
            first_name="Monthly",
            last_name="Test",
            email_address="monthly@test.com",
            email_sequence=1,
            join_date=datetime.now() - timedelta(days=50),  # >6 weeks ago (should be monthly)
            last_email_sent_at=datetime.now()
        )
    ]
    
    # Add test contacts to database
    for contact in contacts:
        db.add(contact)
    db.commit()

    # Call the update-sequences endpoint
    response = client.put("/update-sequences")
    assert response.status_code == 200
    assert response.json() == {"message": "Sequences updated successfully"}

    # Verify sequences were updated correctly
    updated_contacts = db.query(Contact).order_by(Contact.user_id).all()
    
    assert updated_contacts[0].email_sequence == 1  # Still in week 1
    assert updated_contacts[1].email_sequence == 3  # Should be in week 3
    assert updated_contacts[2].email_sequence == 9  # Should be monthly (>6 weeks)

    # Clean up - modified approach
    db.query(Contact).delete()
    db.commit() 