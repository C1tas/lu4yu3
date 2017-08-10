from django import forms
from django.forms import Textarea, TextInput, Select
from django.utils.translation import ugettext_lazy as _

from .models import Article


class ArticlePublishApiForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            'content_md',
        )
        labels = {
            'title': _('Title'),
        }
        widgets = {
            'title': TextInput(),
            'content_md': Textarea(),
            'tags': TextInput(),
        }


class ArticlePublishWebForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            'content_md',
        )
        labels = {
            'title': _('Title'),
        }
        widgets = {
            'title': TextInput(),
            'content_md': Textarea(),
            'tags': TextInput(),
        }
