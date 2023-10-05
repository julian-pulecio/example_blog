from django import forms
from django.core.mail import send_mail
from django.urls import reverse
from taggit.models import Tag
from .models import Comment


class PostShareForm(forms.Form):
    email = forms.EmailField(
        max_length=255, widget=forms.TextInput({
            'class':'form-control'
        })
    )

    def send_email(self, post_url):
        return send_mail(
                subject='I hope you find this interesting',
                message=f'Hello I want to share this post with you {post_url}',
                from_email='your-email@mail.com',
                recipient_list=[self.cleaned_data['email']])

class PostFilterListForm(forms.Form):
    choices = [(tag.name, tag.name) for tag in Tag.objects.all()]
    choices.append(('','None'))

    tags_filter = forms.ChoiceField(
        label='Search by tags',
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        choices=choices,
        required=False
    )
    title_filter = forms.CharField(
        label='Search by title',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        required=False
    )


class CreateCommentForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=255, widget=forms.TextInput({
            'class':'form-control'   
        }),
    ),
    content = forms.CharField(
        max_length=255, widget=forms.Textarea({
            'class':'form-control',
            'rows':3   
        })
    )
    class Meta:
        model = Comment
        fields = ['email','content']