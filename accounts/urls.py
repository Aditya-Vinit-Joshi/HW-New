from django.urls import path
from .views import CustomLoginView, CustomSignupView, CustomLogoutView, CustomPasswordResetView
from django.views.generic import TemplateView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='account_login'),
    path('signup/', CustomSignupView.as_view(), name='account_signup'),
    path('logout/', CustomLogoutView.as_view(), name='account_logout'),
    path('password/reset/', CustomPasswordResetView.as_view(), name='account_reset_password'),
    path('test-reset-links/', TemplateView.as_view(template_name='test_reset_links.html'), name='test_reset_links'),
] 