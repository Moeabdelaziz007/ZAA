# Zentix AI Backend

This is the backend service for the Zentix AI recommendation system. It provides a RESTful API for user management, item management, and personalized recommendations.

## Features

- User authentication and authorization
- Item management
- User interactions tracking
- Personalized recommendations
- User preferences management
- Caching and performance optimization

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- Alembic
- Pydantic
- JWT Authentication

## Prerequisites

- Python 3.8+
- PostgreSQL
- Redis

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/zentix-ai.git
cd zentix-ai/backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your configuration:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Initialize the database:
```bash
alembic upgrade head
```

## Running the Application

1. Start the development server:
```bash
uvicorn main:app --reload
```

2. Access the API documentation:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## API Endpoints

### Authentication
- POST `/api/v1/auth/login` - User login
- POST `/api/v1/auth/register` - User registration
- POST `/api/v1/auth/verify-email/{token}` - Email verification
- POST `/api/v1/auth/reset-password` - Password reset
- POST `/api/v1/auth/change-password` - Change password

### Users
- GET `/api/v1/users/me` - Get current user
- PUT `/api/v1/users/me` - Update current user
- GET `/api/v1/users/{user_id}` - Get user by ID
- GET `/api/v1/users/` - List users
- POST `/api/v1/users/` - Create user
- PUT `/api/v1/users/{user_id}` - Update user
- DELETE `/api/v1/users/{user_id}` - Delete user

### Items
- GET `/api/v1/items/` - List items
- POST `/api/v1/items/` - Create item
- GET `/api/v1/items/{item_id}` - Get item by ID
- PUT `/api/v1/items/{item_id}` - Update item
- DELETE `/api/v1/items/{item_id}` - Delete item

### Recommendations
- GET `/api/v1/recommendations/` - Get personalized recommendations
- GET `/api/v1/recommendations/similar/{item_id}` - Get similar items
- GET `/api/v1/recommendations/trending` - Get trending items
- GET `/api/v1/recommendations/category/{category}` - Get category recommendations

### Interactions
- POST `/api/v1/interactions/` - Create interaction
- GET `/api/v1/interactions/` - List user interactions
- GET `/api/v1/interactions/{interaction_id}` - Get interaction by ID
- DELETE `/api/v1/interactions/{interaction_id}` - Delete interaction

### Preferences
- GET `/api/v1/preferences/` - List user preferences
- POST `/api/v1/preferences/` - Create preference
- PUT `/api/v1/preferences/{category}` - Update preference
- DELETE `/api/v1/preferences/{category}` - Delete preference
- GET `/api/v1/preferences/categories` - Get user categories
- GET `/api/v1/preferences/tags` - Get user tags

## Development

### Running Tests
```bash
pytest
```

### Database Migrations
```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Code Style
```bash
# Format code
black .

# Sort imports
isort .
```

## Deployment

1. Set up a production database
2. Configure environment variables
3. Run migrations
4. Start the server with gunicorn:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 