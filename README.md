# Secure Access Insights Platform (SAIP)

A modern platform for monitoring and analyzing user access behavior in Zero Trust networks.

## Features

- Real-time access behavior monitoring
- ML-based anomaly detection
- Interactive dashboard with visualizations
- Alert management system
- Webhook integrations

## Tech Stack

- Frontend: Next.js with TypeScript
- Backend: Python FastAPI
- Database: PostgreSQL
- ML: scikit-learn, pandas
- Visualization: Chart.js

## Project Structure

```
saip/
├── frontend/           # Next.js frontend application
├── backend/           # FastAPI backend service
├── ml/               # ML models and data processing
└── docs/             # Documentation
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.9+ (for local development)
- PostgreSQL (for local development)

### Running with Docker Compose

The easiest way to run the application is using Docker Compose:

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Local Development

If you prefer to run the application locally without Docker:

1. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
4. Start the frontend development server:
   ```bash
   cd frontend
   npm run dev
   ```

## Development

- Frontend runs on http://localhost:3000
- Backend API runs on http://localhost:8000
- API documentation available at http://localhost:8000/docs

## License

MIT 