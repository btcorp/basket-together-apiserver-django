from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content', 'recruit_count', 'meeting_date', 'latlng', 'address1', 'address2')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content', )
