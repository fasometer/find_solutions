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
    list_display = ('id', 'title', 'lines', 'created', 'data_complete')
    list_display_links = ('id', 'title')
    readonly_fields = ('created', 'data_complete')
    save_on_top = True


admin.site.register(Task, TaskAdmin)
admin.site.register(Lines)
admin.site.register(Place)
admin.site.register(Message)
