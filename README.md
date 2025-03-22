# SeekAI Platform

SeekAI is an intelligent learning platform that aggregates and organizes AI/ML resources while providing interactive learning experiences through AI-powered features.

## Quick Setup

1. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
Create a `.env` file in the root directory:
```env
DEBUG=True
DJANGO_SECRET_KEY=your-secret-key
GEMINI_API_KEY=your-gemini-api-key
```

4. **Run migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py load_json_data
python manage.py generate_youtube_resources
python manage.py load_video_resources
python manage.py import_medium_csv
```

5. **Create a superuser:**
```bash
python manage.py createsuperuser
```

6. **Run the development server:**
```bash
python manage.py runserver
```

## Project Structure

- `ai_learning_hub/` - Main project directory
- `accounts/` - User authentication and profiles
- `resources/` - AI learning resources management
- `search/` - Advanced search functionality
- `chatbot/` - AI-powered chatbot
- `github/` - GitHub trending repository 
- `templates/` - HTML templates
- `static/` - Static files (CSS, JS, images)

## Table of Contents
- [Database Schema](#database-schema)
- [User Guide](#user-guide)
- [AI Features](#ai-features)
- [Contributing](#contributing)

## Database Schema

### Resource Management
```sql
Resource:
- id (UUID): Primary key
- title (varchar): Resource title
- description (text): Detailed description
- url (varchar): Link to resource
- resource_type (enum): [research, github, blog, other]
- category (enum): [AI, ML]
- created_at (timestamp)
- author (FK -> User)
- tags (M2M -> Tag)
```

### User Interactions
```sql
UserBookmark:
- id (UUID): Primary key
- user (FK -> User)
- resource (FK -> Resource)
- created_at (timestamp)

UserProgress:
- id (UUID): Primary key
- user (FK -> User)
- resource (FK -> Resource)
- status (enum): [not_started, in_progress, completed]
- last_accessed (timestamp)
- completion_date (timestamp, nullable)

ResourceRating:
- id (UUID): Primary key
- user (FK -> User)
- resource (FK -> Resource)
- rating (integer): 1-5 scale
- review (text, nullable)
- created_at (timestamp)
```

### AI Chat & Contributions
```sql
ChatSession:
- id (UUID): Primary key
- user (FK -> User)
- created_at (timestamp)
- last_active (timestamp)
- context (jsonb): Session context

ChatMessage:
- id (UUID): Primary key
- session (FK -> ChatSession)
- content (text): Message content
- role (enum): [user, assistant]
- created_at (timestamp)
- metadata (jsonb): Additional message data

UserContribution:
- id (UUID): Primary key
- user (FK -> User)
- resource (FK -> Resource)
- contribution_type (enum): [suggestion, correction, addition]
- content (text): Contribution details
- status (enum): [pending, approved, rejected]
- created_at (timestamp)
- reviewed_at (timestamp, nullable)
- reviewed_by (FK -> User, nullable)
```

## User Guide

### Getting Started

1. **Account Creation & Login**
   - Sign up using email and password

2. **Resource Discovery**
   - Browse curated AI/ML resources by category
   - Filter by type (research papers, GitHub repos, blog posts)
   - Sort by views, last updated, alphabetical order and forks(for github repos).
   - Use advanced search with tags and keywords

3. **Learning Management**
   - Bookmark interesting resources for later

4. **AI Assistant Integration**
   - Access the AI chatbot for learning support
   - Ask questions about specific topics
   - Receive explanations and clarifications
   - Curated only for AI/ML related queries

### Resource Types

1. **Research Papers**
   - Latest AI/ML research publications
   - Summarized key findings
   - Implementation details and code links
   - Related works and references

2. **GitHub Repositories**
   - Curated list of AI/ML projects
   - Implementation examples
   - Training datasets
   - Model architectures

3. **Blog Posts & Tutorials**
   - Step-by-step guides
   - Best practices
   - Industry insights
   - Case studies

## AI Features

### Intelligent Chatbot

The platform includes an AI-powered chatbot that provides:

1. **Learning Support**
   - Concept explanations
   - Resource recommendations

2. **Interactive Features**
   - Context-aware responses
   - Multi-turn conversations

3. **Personalization**
   - Remembers previous interactions
   - Provides tailored recommendations

## Deployment

The application is configured for deployment on Render:
- PostgreSQL database
- WhiteNoise for static files
- Gunicorn web server
- Environment variable configuration
- Health check endpoint

## User Contributions

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

This platform is continuously evolving with new features and improvements. User feedback and contributions are welcome to enhance the learning experience for everyone. 

---

This platform is continuously evolving with new features and improvements. User feedback and contributions are welcome to enhance the learning experience for everyone. 



# SeekAI Platform

SeekAI is an intelligent learning platform that aggregates and organizes AI/ML resources, featuring GitHub repository integration and AI-powered search capabilities.

## Features

### 1. Resource Management
- Browse AI and Machine Learning resources
- Resource types: Research Papers, GitHub Repositories, Blog Posts
- View tracking and like system
- Tag-based organization using django-taggit
- Admin approval workflow for new submissions

### 2. GitHub Integration
- Curated AI/ML trending repository listing
- Topic-based filtering
- Repository comments and ratings
- Sort repos based on 
- Save favorite repositories

### 3. Search Capabilities
- Full-text search across resources
- Filter by resource type and category
- Sort by various criteria (views, date, rating)
- Advanced search with multiple filters

### 4. User Features
- Custom user profiles
- Resource bookmarking
- Category-based interests
- Social interactions (likes, comments, ratings)

## Technical Stack

### Backend
- Python 3.12+
- Django 4.2
- PostgreSQL
- Redis (optional)

### Frontend
- Bootstrap 5
- Font Awesome
- Custom CSS/JS

### AI Integration
- OpenAI API
- Google Gemini API

## Database Schema



## Setup Instructions

1. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Environment Configuration**
Create `.env` file:
```env
DEBUG=True
DJANGO_SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
GITHUB_TOKEN=your-github-token
GEMINI_API_KEY=your-gemini-api-key
```

4. **Database Setup**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py load_json_data  # Load initial AI resources
```

5. **Create Admin User**
```bash
python manage.py createsuperuser
```

6. **Run Development Server**
```bash
python manage.py runserver
```

## Project Structure

```
SeekAI/
├── ai_learning_hub/     # Project settings
├── accounts/           # User authentication
│   ├── models.py       # CustomUser model
│   └── views.py        # Auth views
├── resources/          # Core resource management
│   ├── models.py       # Resource models
│   └── views.py        # Resource views
├── github/            # GitHub integration
│   ├── models.py      # Repository models
│   └── views.py       # GitHub views
├── search/            # Search functionality
├── static/            # Static files
└── templates/         # HTML templates
```

## Key URLs

- `/` - Home page with featured resources
- `/resources/` - Resource listing
- `/github/` - GitHub repositories
- `/search/` - Search interface
- `/accounts/profile/` - User profile
- `/admin/` - Admin interface

## Deployment

The application is configured for deployment on Render:

1. **Database**
   - PostgreSQL database service
   - Connection via DATABASE_URL

2. **Web Service**
   - Python runtime
   - Build command: `./build.sh`
   - Start command: `gunicorn ai_learning_hub.wsgi:application`

3. **Static Files**
   - Served via WhiteNoise
   - Collected to `staticfiles/`

4. **Environment Variables**
   - Configure in Render dashboard
   - Include all API keys and secrets

## API Integrations

1. **GitHub API**
   - Repository data fetching
   - Star and fork counts
   - Topic information

2. **AI Services**
   - OpenAI: Resource recommendations
   - Gemini: Code analysis

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Submit a pull request

## Development Guidelines

1. **Code Style**
   - Follow PEP 8
   - Use Django best practices
   - Document functions and classes

2. **Testing**
   - Write unit tests
   - Test database migrations
   - Check API integrations

3. **Security**
   - Keep API keys secure
   - Validate user input
   - Use HTTPS in production

## Support

- GitHub Issues
- Documentation
- Admin Contact

---

This platform is actively maintained and improved. Contributions and feedback are welcome. 
