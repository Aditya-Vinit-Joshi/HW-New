from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q
from .models import ChatSession, Message, ChatbotKnowledge
from resources.models import Resource, Category
from openai import OpenAI
import json
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Initialize OpenAI client with error handling
try:
    if not settings.OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY is not set in environment variables")
        client = None
    else:
        # Initialize the client with the new API
        client = OpenAI(api_key=settings.OPENAI_API_KEY.strip('"').strip("'"))
        logger.info("OpenAI client initialized successfully")
except Exception as e:
    logger.error(f"Error initializing OpenAI client: {str(e)}")
    client = None

def get_relevant_resources(query):
    """Search for relevant resources based on the user's query."""
    try:
        resources = Resource.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query),
            is_approved=True
        ).distinct()[:5]
        
        return [
            {
                'title': r.title,
                'description': r.description[:200] + '...' if len(r.description) > 200 else r.description,
                'url': r.url,
                'type': r.resource_type,
                'category': r.category.name
            }
            for r in resources
        ]
    except Exception as e:
        logger.error(f"Error getting relevant resources: {str(e)}")
        return []

def get_categories_info():
    """Get information about available categories."""
    try:
        categories = Category.objects.all()
        return [
            {
                'name': cat.name,
                'description': cat.description
            }
            for cat in categories
        ]
    except Exception as e:
        logger.error(f"Error getting categories: {str(e)}")
        return []

@login_required
def chat_view(request):
    try:
        # Get or create chat session
        session, created = ChatSession.objects.get_or_create(
            user=request.user,
            defaults={'user': request.user}
        )
        
        if request.method == 'POST':
            try:
                if not client:
                    logger.error("OpenAI client is not initialized")
                    return JsonResponse({
                        'status': 'error',
                        'message': 'OpenAI API is not properly configured. Please contact the administrator.'
                    }, status=500)
                    
                data = json.loads(request.body)
                user_message = data.get('message', '').strip()
                
                if not user_message:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Message cannot be empty'
                    }, status=400)
                
                # Save user message
                Message.objects.create(
                    session=session,
                    message_type='user',
                    content=user_message
                )
                
                # Get relevant resources and categories
                relevant_resources = get_relevant_resources(user_message)
                categories_info = get_categories_info()
                
                # Prepare system message with website context
                system_message = """You are an AI learning assistant for our AI Learning Hub website. Your role is to:
                1. Help users find and understand AI/ML learning resources available on our platform
                2. Provide information about our resource categories and content
                3. Suggest relevant resources based on user queries
                4. Explain AI/ML concepts in the context of our learning materials
                5. Guide users to appropriate learning paths using our content

                When suggesting resources, use this format:
                Resource: [Title]
                URL: [URL]
                Type: [Resource Type]
                Category: [Category Name]

                Keep responses focused on our website's resources and content. If asked about topics we don't have resources for,
                suggest similar topics we do cover or recommend checking our resource categories."""

                # Get conversation history
                messages = [
                    {"role": "system", "content": system_message},
                ]
                
                if categories_info:
                    messages.append({
                        "role": "system", 
                        "content": f"Available categories: {json.dumps(categories_info, indent=2)}"
                    })
                
                if relevant_resources:
                    messages.append({
                        "role": "system",
                        "content": f"Relevant resources for this query: {json.dumps(relevant_resources, indent=2)}"
                    })
                
                # Add conversation history (last 5 messages for context)
                chat_history = Message.objects.filter(session=session).order_by('-timestamp')[:5]
                for msg in reversed(chat_history):
                    role = "user" if msg.message_type == "user" else "assistant"
                    messages.append({"role": role, "content": msg.content})
                
                try:
                    # Call OpenAI API
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        max_tokens=800,
                        temperature=0.7,
                        presence_penalty=0.6
                    )
                    
                    bot_response = response.choices[0].message.content.strip()
                    
                    # Save bot response
                    Message.objects.create(
                        session=session,
                        message_type='bot',
                        content=bot_response
                    )
                    
                    return JsonResponse({
                        'status': 'success',
                        'message': bot_response
                    })
                    
                except Exception as e:
                    logger.error(f"OpenAI API error: {str(e)}")
                    return JsonResponse({
                        'status': 'error',
                        'message': f'Error processing request: {str(e)}'
                    }, status=500)
            
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {str(e)}")
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid JSON data'
                }, status=400)
            
            except Exception as e:
                logger.error(f"Unexpected error in POST handling: {str(e)}")
                return JsonResponse({
                    'status': 'error',
                    'message': f'An unexpected error occurred: {str(e)}'
                }, status=500)
        
        # Get chat history for display
        messages = Message.objects.filter(session=session).order_by('timestamp')
        return render(request, 'chatbot/chat.html', {
            'session': session,
            'messages': messages
        })
        
    except Exception as e:
        logger.error(f"Unexpected error in chat_view: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'An unexpected error occurred. Please try again later.'
        }, status=500)

@login_required
def clear_chat(request):
    if request.method == 'POST':
        try:
            session = ChatSession.objects.filter(user=request.user).first()
            if session:
                session.messages.all().delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            logger.error(f"Error clearing chat: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f'Error clearing chat: {str(e)}'
            }, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@login_required
def get_messages(request):
    session_id = request.GET.get('session_id')
    last_timestamp = request.GET.get('last_timestamp')
    
    try:
        session = ChatSession.objects.get(id=session_id, user=request.user)
    except ChatSession.DoesNotExist:
        return JsonResponse({'error': 'Invalid session'})
    
    messages = session.messages.all()
    if last_timestamp:
        messages = messages.filter(timestamp__gt=last_timestamp)
    
    messages_data = [{
        'type': msg.message_type,
        'content': msg.content,
        'timestamp': msg.timestamp.isoformat()
    } for msg in messages]
    
    return JsonResponse({'messages': messages_data})

@login_required
def start_session(request):
    session = ChatSession.objects.create(user=request.user)
    
    # Add welcome message
    Message.objects.create(
        session=session,
        message_type='bot',
        content="Hello! I'm your AI assistant. How can I help you find AI learning resources today?"
    )
    
    return JsonResponse({
        'session_id': session.id,
        'message': "Session started successfully"
    })

@login_required
def end_session(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'})
    
    session_id = request.POST.get('session_id')
    
    try:
        session = ChatSession.objects.get(id=session_id, user=request.user)
        session.delete()
        return JsonResponse({'message': 'Session ended successfully'})
    except ChatSession.DoesNotExist:
        return JsonResponse({'error': 'Invalid session'})
