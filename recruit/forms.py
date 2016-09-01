from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content', 'recruit_count', 'recruit_status')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content', )
        
    def __init__(self, content, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.instance.content = content
