# Email Management System

A full-stack application for managing email sequences and contacts, built with FastAPI (backend) and React (frontend).

## Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL database
- Gmail API credentials

## Backend Setup

1. Create and activate a virtual environment:

bash
python -m venv venv
source venv/bin/activate # On Windows use: venv\Scripts\activate


2. Install backend dependencies:
bash
pip install -r requirements.txt


3. Set up environment variables:
   - Create a `.env` file in the `app` directory
   - Use this template:

env
CLIENT_SECRETS_FILE=path/to/your/client_secrets.json
ENABLE_GOOGLE_CONTACTS=false
REDIRECT_URI=http://localhost:8000/auth/callback
CLIENT_ID=your_google_client_id
CLIENT_SECRET=your_google_client_secret
CORS_ORIGINS=http://localhost:3000
EMAIL_REPLY_TO=your@email.com
BACKEND_URL=http://localhost:8000
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
USERNAME=admin_username
PASSWORD=admin_password


4. Run database migrations:
bash
alembic upgrade head

5. Start the backend server:

bash
uvicorn app.main:app --reload --port 8000

The backend API will be available at `http://localhost:8000`

## Frontend Setup

1. Install frontend dependencies:

bash
cd frontend
npm install

2. Create a `.env` file in the `frontend` directory:
env
REACT_APP_API_URL=http://localhost:8000

3. Start the frontend development server:

bash
npm start


The frontend application will be available at `http://localhost:3000`

## Google API Setup

1. Create a Google Cloud Project
2. Enable Gmail API and Google People API (if using contacts feature)
3. Configure OAuth 2.0 credentials
4. Download client secrets JSON file and save it as specified in your `.env`

## Features

- Gmail authentication
- Contact management
- Email sequence management
- Email templates
- Dashboard with delivery metrics
- Weekly email scheduling
- Contact notes and tracking

## Project Structure

.
├── app/ # Backend application
│ ├── routers/ # API route handlers
│ ├── templates/ # Email templates
│ ├── models.py # Database models
│ ├── schemas.py # Pydantic schemas
│ └── services.py # Business logic
└── frontend/ # Frontend application
├── public/ # Static files
└── src/
├── components/ # React components
└── services/ # API services

## Security Notes

- Never commit `.env` files or Google API credentials
- Keep your `CLIENT_SECRET` and database credentials secure
- Use HTTPS in production
- Regularly update dependencies

## License

This project is proprietary and confidential.