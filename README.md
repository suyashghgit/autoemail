# autoemail

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Create a real .env file based on the .env.example template and fill in your actual email credentials.
To test the basic setup, run the FastAPI application:

uvicorn app.main:app --reload
