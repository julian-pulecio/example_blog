from django import forms
from django.core.mail import send_mail
from django.urls import reverse
from .models import Comment


class PostShareForm(forms.Form):
    email = forms.EmailField(max_length=255, widget=forms.TextInput())

    def send_email(self, post_url):
        return send_mail(
                subject='I hope you find this interesting',
                message=f'Hello I want to share this post with you {post_url}',
                from_email='your-email@mail.com',
                recipient_list=[self.cleaned_data['email']])

class PostFilterListForm(forms.Form):
    
    filter_value = forms.CharField(
        label='Search by title',
        max_length=255,
        widget=forms.TextInput(attrs={
            'hx-trigger': 'keyup changed delay:500ms',
            'hx-swap':'outerHTML',
            'hx-target': '#search-results'
        })
    )

class CreateCommentForm(forms.ModelForm):
    email = forms.EmailField(max_length=255, widget=forms.TextInput())
    class Meta:
        model = Comment
        fields = ['email','content']