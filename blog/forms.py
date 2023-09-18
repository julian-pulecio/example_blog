from django import forms
from .models import Post
from django.core.mail import send_mail

class PostShareForm(forms.Form):
    email = forms.CharField(max_length=255)

    def send_email(self, post_url):
        return send_mail(
                subject='I hope you find this interesting',
                message=f'Hello I want to share this post with you {post_url}',
                from_email='your-email@mail.com',
                recipient_list=[self.cleaned_data['email']])