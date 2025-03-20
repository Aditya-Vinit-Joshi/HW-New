from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()

GREETINGS = [
    'hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 
    'good evening', 'good night', 'howdy', 'hi there', 'hello there'
]

# Define AI/ML/Data Science related keywords with variations
AI_ML_KEYWORDS = [
    # Core concepts
    'ai', 'artificial intelligence', 'machine learning', 'deep learning', 'neural networks',
    'data science', 'data analysis', 'data mining', 'big data', 'statistics',
    
    # Programming and tools
    'python', 'tensorflow', 'pytorch', 'scikit-learn', 'scikit', 'pandas', 'numpy',
    'jupyter', 'notebook', 'colab', 'google colab',
    
    # Learning types
    'supervised learning', 'unsupervised learning', 'reinforcement learning',
    'classification', 'regression', 'clustering', 'dimensionality reduction',
    
    # Applications
    'natural language processing', 'nlp', 'computer vision', 'cv', 'robotics',
    'image processing', 'text processing', 'speech recognition',
    
    # Algorithms and techniques
    'random forest', 'decision tree', 'svm', 'support vector machine',
    'k-means', 'knn', 'neural network', 'cnn', 'rnn', 'lstm',
    
    # Data science concepts
    'data preprocessing', 'feature engineering', 'model training',
    'cross validation', 'hyperparameter tuning', 'model evaluation',
    
    # Ethics and applications
    'ai ethics', 'bias', 'fairness', 'responsible ai', 'ai applications'
]


def is_greeting(message):
    """Check if the message is a greeting."""
    message_lower = message.lower().strip()
    return any(greeting in message_lower for greeting in GREETINGS)

def is_ai_ml_related(message):
    """Check if the message is related to AI/ML/Data Science."""
    message_lower = message.lower()
    
    # Split message into words and check for partial matches
    words = message_lower.split()
    
    # Check for exact matches
    if any(keyword in message_lower for keyword in AI_ML_KEYWORDS):
        return True
    
    # Check for partial matches (e.g., "ml" in "machine learning")
    for word in words:
        if any(word in keyword or keyword in word for keyword in AI_ML_KEYWORDS):
            return True
    
    return False


def format_response(text):
    """Format the response text to handle markdown and HTML formatting."""
    # Replace markdown bold with HTML bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    # Replace markdown italic with HTML italic
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    
    # Replace markdown code blocks with HTML pre and code tags
    text = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', text, flags=re.DOTALL)
    
    # Replace markdown inline code with HTML code tags
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    
    # Replace markdown lists with HTML lists
    text = re.sub(r'^\s*[-*]\s+(.*)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    
    # Wrap lists in ul tags
    text = re.sub(r'(<li>.*</li>\n?)+', r'<ul>\g<0></ul>', text)
    
    return text


def get_greeting_response():
    """Generate a friendly greeting response."""
    return {
        "status": "success",
        "message": "Hello! I'm your AI/ML/Data Science assistant. I can help you with questions about:\n"
                  "- Artificial Intelligence\n"
                  "- Machine Learning\n"
                  "- Deep Learning\n"
                  "- Data Science\n"
                  "- Python Programming\n"
                  "- And more!\n\n"
                  "What would you like to know about?"
    }



def chat_view(request):
    """Render chat interface with message history."""
    chat_history = []  # Modify if using session-based messages
    return render(request, "chatbot/chat.html", {"messages": chat_history})

def chat_view(request):
    """Render chat interface with message history."""
    chat_history = []  # Modify if using session-based messages
    return render(request, "chatbot/chat.html", {"messages": chat_history})

@csrf_exempt  # Remove this for production and use proper CSRF handling
def chatbot_api(request):
    """API endpoint for chatbot communication."""
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=GEMINI_API_KEY)
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")

    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()

        if not user_message:
            return JsonResponse({"status": "error", "message": "Message cannot be empty."}, status=400)

        # Check if it's a greeting
        if is_greeting(user_message):
            return JsonResponse(get_greeting_response())

        # Check if the question is AI/ML related
        is_related = is_ai_ml_related(user_message)
        print(f"User message: {user_message}")
        print(f"Is AI/ML related: {is_related}")

        if not is_related:
            return JsonResponse({
                "status": "success",
                "message": "I'm specialized in AI, Machine Learning, and Data Science topics. "
                          "Please ask questions related to these fields. For example:\n"
                          "- What is machine learning?\n"
                          "- How does deep learning work?\n"
                          "- What are the applications of AI?\n"
                          "- How to analyze data using Python?"
            })
         # Create a focused prompt for AI/ML/Data Science
        focused_prompt = f"""You are an AI/ML/Data Science expert. Please provide a detailed and accurate answer to the following question. 
        Focus on technical accuracy and include relevant examples or code snippets when appropriate.
        
        Question: {user_message}
        
        Please provide a comprehensive answer that includes:
        1. Clear explanation of the concept
        2. Key points and important details
        3. Practical examples or use cases
        4. Related concepts or further reading suggestions
        
        Format your response using markdown:
        - Use **bold** for section headers and important terms
        - Use *italic* for emphasis
        - Use ``` for code blocks
        - Use ` for inline code
        - Use - or * for lists
        """

        # Interact with Gemini AI
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(focused_prompt)

        # Extract AI response correctly and format it
        bot_reply = response.text if hasattr(response, "text") else "Sorry, I couldn't process that."
        formatted_reply = format_response(bot_reply)

        return JsonResponse({"status": "success", "message": formatted_reply})

    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON format."}, status=400)
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Add error logging
        return JsonResponse({"status": "error", "message": str(e)}, status=500)



@csrf_exempt
def clear_chat(request):
    if request.method == "POST":
        request.session['messages'] = []  # Clear chat history in session
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)