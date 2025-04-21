# Secure Access Insights Platform (SAIP)

A comprehensive platform for monitoring, analyzing, and securing access patterns across your organization.

## Overview

SAIP provides real-time monitoring, anomaly detection, and alerting for access patterns across your organization. It helps security teams identify potential security threats, analyze access patterns, and respond to incidents quickly.

## Features

- **Real-time Access Monitoring**: Track all access attempts across your organization
- **Anomaly Detection**: Identify suspicious access patterns using machine learning
- **Alert Management**: Create, assign, and track security alerts
- **Role-Based Access Control**: Secure access to sensitive information
- **Analytics Dashboard**: Visualize access patterns and security metrics
- **API Integration**: Connect with existing security tools and systems

## Architecture

The platform consists of three main components:

1. **Frontend**: Next.js application with React, TypeScript, and Tailwind CSS
2. **Backend**: FastAPI application with PostgreSQL database
3. **ML Service**: Python service for anomaly detection and pattern analysis

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/saip.git
   cd saip
   ```

2. Set up environment variables:
   ```
   cp frontend/.env.example frontend/.env.local
   cp backend/.env.example backend/.env
   ```

3. Start the application using Docker Compose:
   ```
   docker-compose up -d
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api
   - API Documentation: http://localhost:8000/docs

### Local Development

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API Documentation

The API documentation is available at http://localhost:8000/docs when running the backend service.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FastAPI for the backend framework
- Next.js for the frontend framework
- PostgreSQL for the database
- scikit-learn for machine learning capabilities 