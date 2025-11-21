from django.contrib import admin
from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class TaskAdminForm(forms.ModelForm):
    # memo = forms.CharField(widget=CKEditorUploadingWidget)
    # decision = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Task
        fields = "__all__"


class TaskAdmin(admin.ModelAdmin):
    form = TaskAdminForm
    list_display = ('id', 'title', 'lines', 'place', 'created', 'data_complete')
    list_display_links = ('id', 'title')
    list_filter = ('lines', 'place')
    search_fields = ('title', 'lines', 'place')
    readonly_fields = ('created', 'data_complete')
    save_on_top = True


class MessageAdminForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"


class MessageAdmin(admin.ModelAdmin):
    form = MessageAdminForm
    list_display = ('sender', 'recipient', 'subject', 'created')
    list_filter = ('sender', 'recipient')


admin.site.register(Task, TaskAdmin)
admin.site.register(Lines)
admin.site.register(Place)
admin.site.register(Message, MessageAdmin)
