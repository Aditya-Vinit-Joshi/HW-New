from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Gemini AI API key




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

        # Interact with Gemini AI
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(user_message)

        # Extract AI response correctly
        bot_reply = response.text if hasattr(response, "text") else "Sorry, I couldn't process that."

        return JsonResponse({"status": "success", "message": bot_reply})

    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON format."}, status=400)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
