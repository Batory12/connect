from django import forms

from .models import Post, Topic, Entry, Comment


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ""}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols':80})}

class UserSearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))