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
OPENAI_API_KEY=your-openai-api-key
GITHUB_TOKEN=your-github-token
GEMINI_API_KEY=your-gemini-api-key
```

4. **Run migrations:**
```bash
python manage.py migrate
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
- `github/` - GitHub repository integration
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
- difficulty_level (enum): [beginner, intermediate, advanced]
- created_at (timestamp)
- updated_at (timestamp)
- author (FK -> User)
- tags (M2M -> Tag)
- avg_rating (float): Computed field
```

### User Interactions
```sql
UserBookmark:
- id (UUID): Primary key
- user (FK -> User)
- resource (FK -> Resource)
- created_at (timestamp)
- notes (text): Optional user notes

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
   - Sign up using email or GitHub account
   - Complete your profile with interests and expertise level
   - Set learning preferences and goals

2. **Resource Discovery**
   - Browse curated AI/ML resources by category
   - Filter by type (research papers, GitHub repos, blog posts)
   - Sort by difficulty level, rating, or popularity
   - Use advanced search with tags and keywords

3. **Learning Management**
   - Bookmark interesting resources for later
   - Track progress on resources you're studying
   - Rate and review completed resources
   - Add personal notes to bookmarked items

4. **AI Assistant Integration**
   - Access the AI chatbot for learning support
   - Get personalized resource recommendations
   - Ask questions about specific topics
   - Receive explanations and clarifications

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
   - Code debugging help
   - Implementation guidance
   - Resource recommendations

2. **Interactive Features**
   - Context-aware responses
   - Code completion suggestions
   - Natural language processing
   - Multi-turn conversations

3. **Personalization**
   - Adapts to user's skill level
   - Remembers previous interactions
   - Provides tailored recommendations
   - Tracks learning progress

### User Contributions

Community members can enhance the platform through:

1. **Resource Submissions**
   - Submit new AI/ML resources
   - Provide descriptions and metadata
   - Tag with relevant topics
   - Set difficulty levels

2. **Quality Control**
   - Community voting system
   - Expert review process
   - Content moderation
   - Version tracking

3. **Collaborative Features**
   - Discussion threads
   - Resource annotations
   - Error reporting
   - Content improvements

## Best Practices

1. **Resource Organization**
   - Use clear, descriptive titles
   - Add relevant tags
   - Provide comprehensive descriptions
   - Include prerequisites

2. **Learning Path**
   - Start with foundational resources
   - Progress systematically
   - Complete hands-on exercises
   - Participate in discussions

3. **Contribution Guidelines**
   - Follow submission templates
   - Provide accurate metadata
   - Include source references
   - Maintain quality standards

## Technical Requirements

- Modern web browser
- GitHub account (optional)
- Basic understanding of AI/ML concepts
- Internet connection for AI features

## Support

For technical support or questions:
- Use the AI chatbot
- Contact platform administrators
- Check documentation
- Join community discussions

---

This platform is continuously evolving with new features and improvements. User feedback and contributions are welcome to enhance the learning experience for everyone. 