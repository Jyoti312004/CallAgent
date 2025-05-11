# CallAgent - Salon Customer Support System

CallAgent is a comprehensive system designed to provide automated customer support for salon businesses. It combines a voice assistant powered by LiveKit with a Django-based backend for knowledge management, query handling, and supervisor dashboards.
<img width="983" alt="Screenshot 2025-05-11 at 7 41 38 PM" src="https://github.com/user-attachments/assets/40596861-e19f-48fe-a4c9-04a7bc0c67d5" />

## Overview

The system consists of:

1. **Voice AI Agent**: An AI-powered voice agent that can answer customer queries about the salon's services, working hours, staff, and policies.
2. **Knowledge Base**: A structured database of salon information that the AI agent can query.
3. **Escalation System**: When the AI can't answer a question, it automatically creates a support ticket for human supervisors.
4. **Supervisor Dashboard**: A web interface for human supervisors to view and respond to customer queries.
5. **Notification System**: Sends notifications to customers when their queries are resolved.

## Features

### AI Voice Agent

- Answers common customer questions about salon services, hours, policies, etc.
- Natural voice interactions powered by LiveKit
- Automatically escalates complex queries to human supervisors

### Knowledge Management

- Structured storage of salon information
- Similarity-based query matching
- Easy knowledge base updates through the admin interface

### Query Management

- Automatic tracking of pending, resolved, and unresolved queries
- Background task to mark expired queries as unresolved
- Complete history of customer interactions

### Supervisor Dashboard

- Clean, responsive web interface for supervisors
- Tabbed navigation between pending, unresolved, and resolved queries
- Detailed view of individual queries with response form

## Technical Stack

- **Backend**: Django REST Framework
- **Database**: SQLite (can be replaced with PostgreSQL for production)
- **Task Queue**: Celery with Redis broker
- **Voice Agent**: LiveKit with OpenAI integration
- **Frontend**: HTML, CSS, JavaScript

## Setup and Installation

### Prerequisites

- Python 3.9+
- Redis server (for Celery)

### Installation Steps

1. Clone the repository:

   ```
   git clone https://github.com/Jyoti312004/CallAgent.git
   cd CallAgent
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Run database migrations:

   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser:

   ```
   python manage.py createsuperuser
   ```

6. Start the development server:

   ```
   python manage.py runserver
   ```

7. Start Celery worker (in a separate terminal):

   ```
   celery -A CallAgent worker -l info
   ```

8. Start Celery beat (in another separate terminal):
   ```
   celery -A CallAgent beat -l info
   ```
9. Start Django server :
   ```
   python manage.py runserver
   ```
10. Start LiveKit server (if applicable):
    ```
    python src/agents/livekit_server.py console
    ```

## API Endpoints

### Knowledge Base Endpoints

- `GET /api/knowledge-base/search-query/` - Search for similar entries in the knowledge base
- `POST /api/knowledge-base/add-knowledge/` - Add or update knowledge in the knowledge base
- `GET /api/knowledge-base/resolved-queries/` - Get all resolved queries

### Query Request Endpoints

- `POST /api/query-request/create-query/` - Create a new query request
- `GET /api/query-request/get-query/` - Get a specific query request
- `GET /api/query-request/get-all-queries/` - Get all query requests
- `GET /api/query-request/pending-query/` - Get all pending query requests
- `POST /api/query-request/resolve-query/` - Resolve a specific query request
- `DELETE /api/query-request/delete-query/` - Delete a specific query request
- `GET /api/query-request/get-unresolved-queries/` - Get all unresolved query requests

## Supervisor Dashboard

The supervisor dashboard is available at `src/frontend/dashboard.html`. To use it:

1. Start the Django development server
2. Open the dashboard.html file in your browser
3. Use the tabs to navigate between pending, unresolved, and resolved queries
4. Click on any query card to view details and submit a response

## Project Structure

- `CallAgent/` - Django project settings and configuration
- `src/` - Main application code
  - `agents/` - Voice agent implementation
  - `knowledge_base/` - Knowledge base query system
  - `notification/` - Customer notification system
  - `frontend/` - Supervisor dashboard interface
  - `models.py` - Database models
  - `views.py` - API endpoint implementations
  - `tasks.py` - Background tasks

## Environment Variables

For production, set the following environment variables:

- `LIVEKIT_URL` - Webhook for notifications
- `LIVEKIT_API_KEY` - Django secret key
- `LIVEKIT_API_SECRET` - Set to 'False' in production
- `OPENAI_API_KEY` - Comma-separated list of allowed hosts
- `DEEPGRAM_API_KEY` - Database connection string
- `NOTIFICATION_WEBHOOK_URL` - Allowed hosts
- `CARTESIA_API_KEY` - Allowed hosts
