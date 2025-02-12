# autoemail

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Create a real .env file based on the .env.example template and fill in your actual email credentials.
To test the basic setup, run the FastAPI application:

uvicorn app.main:app --reload


sendgrid - 9f397ee582e82daa96fd4cc90085b2cb-1654a412-3ec4901e