from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add a comment...',
                'rows': 4,
            }),
        }
        labels = {
            'content': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Add a comment...',
            'rows': 4,
        })


class ShareByEmailForm(forms.Form):
    recipient_email = forms.EmailField(label='Recipient\'s Email')
    message = forms.CharField(widget=forms.Textarea, required=False, label='Message')
