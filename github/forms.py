from django import forms
from .models import RepositoryComment, RepositoryRating

class CommentForm(forms.ModelForm):
    class Meta:
        model = RepositoryComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = RepositoryRating
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(attrs={'class': 'rating-input'}),
        } 