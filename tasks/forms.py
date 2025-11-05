from django.forms import ModelForm
from .models import Task, Message
from django import forms


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'user', 'data_complete', 'lines', 'place', 'memo', 'memo_images', 'decision',
                  'decision_images', 'important']
        widgets = {
            'lines': forms.Select(attrs={'class': 'form-input'}),
            'place': forms.Select(attrs={'class': 'form-input'}),
            'memo': forms.Textarea(attrs={'rows': 4}),
            'decision': forms.Textarea(attrs={'rows': 4}),
        }


class MessageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fields in self.fields.values():
            fields.widget.attrs.update({'class': 'input'})

    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body', 'recipient']

