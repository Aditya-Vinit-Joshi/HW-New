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
- Category-based search


## Technical Stack

### Backend
- Python 3.10
- Django 5.0.2
- PostgreSQL

### Frontend
- Bootstrap 5
- Custom CSS/JS

### AI Integration
- Google Gemini API

## Database Schema

<img src = "https://github.com/Aditya-Vinit-Joshi/SeekAI/blob/main/database_schema">

## Data Sourcing

1. Research papers:
- Extracted top-rated research papers in the field of AI/ML and ran migrations script

2. Github Projects:
- Sourced trending GitHub public repos and ran migrations script

3. Blogs
- Extracted medium and towards data science articles and ran migrations script

4. Video Resources
- Extracted YouTube, Coursera, EDX, and Udemy data science articles and ran migrations script

These are extracted dataset and proves that the system can scale when real-time data is added in the future.

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
GITHUB_TOKEN=your-github-token
GEMINI_API_KEY=your-gemini-api-key
DATABASE_URL=database_url
ALLOWED_MIGRATION="*"
```

4. **Database Setup**
```bash

This is to only be done, if you want to replicate the database on your local machine. Otherwise this step can be skipped.

python manage.py makemigrations
python manage.py migrate
python manage.py load_json_data
python manage.py generate_video_resources
python manage.py load_video_resources

python manage.py import_medium_csv
```

5. **Create Admin User**
```bash

This can only be done if the you are using your local database.
In case of using the database the application is using, the user cannot create the superuser.
For creation of any super user, please contact the GitHub Repository owner.

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
   - Gemini: Chat bot curated to answer queries on AI/ML

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Submit a pull request

## Development Guidelines

1. **Code Style**
   - Use Django best practices
   - Document functions and classes

2. **Testing**
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
