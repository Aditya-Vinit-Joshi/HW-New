from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login as auth_login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from allauth.account.views import LoginView, SignupView, LogoutView, PasswordResetView
from django.contrib import messages

User = get_user_model()

class CustomLoginView(LoginView):
    """Custom login view that ensures proper redirection"""
    
    def get_success_url(self):
        # First check for a 'next' parameter
        redirect_to = self.request.GET.get('next', None)
        
        # If no 'next' parameter, use the default redirect
        if not redirect_to:
            redirect_to = reverse('resources:home')
        
        return redirect_to
        
    def form_valid(self, form):
        # Add a success message
        messages.success(self.request, "You have successfully logged in!")
        return super().form_valid(form)

class CustomSignupView(SignupView):
    """Custom signup view with a welcome message"""
    
    def get_success_url(self):
        redirect_to = reverse('resources:home')
        return redirect_to
        
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Welcome to AI Learning Hub! Your account has been created successfully.")
        return response

class CustomLogoutView(LogoutView):
    """Custom logout view that redirects to home"""
    
    def get_redirect_url(self):
        messages.success(self.request, "You have been logged out successfully.")
        return reverse('resources:home')

class CustomPasswordResetView(PasswordResetView):
    """Custom password reset view with improved success message"""
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, 
            "Password reset email sent! Please check your inbox."
        )
        return response
