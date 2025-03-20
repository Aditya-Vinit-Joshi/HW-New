from django import forms
from .models import Resource, Comment, Rating, Category

class ResourceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit category choices to AI and ML
        self.fields['category'].queryset = Category.objects.filter(
            name__in=['Artificial Intelligence', 'Machine Learning']
        )
        
    class Meta:
        model = Resource
        fields = ['title', 'description', 'url', 'resource_type', 'category', 'tags']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'tags': forms.TextInput(attrs={'data-role': 'tagsinput'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(attrs={'class': 'rating-input'}),
        } 