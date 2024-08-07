from django import forms

from .models import Comment

# sharing post through email 
# the base Form class is used to create this form 
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
    
# Comment for a form 
# the base ModelForm is used to create this form taking advantage 
# of the existing comment model 
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        