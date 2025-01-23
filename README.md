# AI-Powered Chatbot for Supplier and Product Information

A full-stack application featuring an AI-powered chatbot that allows users to query product and supplier information using natural language.

## Features
- Natural language querying of product and supplier data
- LangGraph-based chatbot workflow
- React frontend with modern UI
- FastAPI backend
- PostgreSQL database
- LLM-powered response enhancement

## Project Structure
```
.
├── backend/               # Python FastAPI backend
│   ├── app/              # Application code
│   ├── tests/            # Backend tests
│   └── requirements.txt  # Python dependencies
├── frontend/             # React frontend
│   ├── src/             # Source code
│   ├── public/          # Static files
│   └── package.json     # Node dependencies
└── database/            # Database scripts and migrations
```

## Setup Instructions

### Backend Setup
1. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Set up the database:
```bash
# Configure your PostgreSQL connection in .env file
python database/init_db.py
```

### Frontend Setup
1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

## Environment Variables
Create a `.env` file in the backend directory with:
```
DATABASE_URL=postgresql://user:password@localhost:5432/chatbot_db
LLM_API_KEY=your_llm_api_key
```

## API Documentation
The API documentation is available at `/docs` when running the backend server.

## License
MIT 