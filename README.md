# AI Learning Hub

A comprehensive platform for discovering and learning about AI resources, tutorials, and research materials. The website can have some performance delays since it is hosted on a free hosting platform on render.com

## Features

- Advanced AI Resource Search Engine
- Categorized Learning Materials
- GitHub Repository Explorer
- Bookmark & Save Favorite Resources
- AI-Powered Chatbot for Assistance
- User-Contributed Resources & Community Engagement

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with:
```
DEBUG=True
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
GITHUB_TOKEN=your-github-token
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

- `ai_learning_hub/` - Main project directory
- `accounts/` - User authentication and profiles
- `resources/` - AI learning resources management
- `search/` - Advanced search functionality
- `chatbot/` - AI-powered chatbot
- `github/` - GitHub repository integration
- `templates/` - HTML templates
- `static/` - Static files (CSS, JS, images)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
