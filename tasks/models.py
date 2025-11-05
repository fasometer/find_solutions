from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=100, verbose_name="Задача")
    lines = models.ForeignKey('Lines', on_delete=models.CASCADE, default="", verbose_name="Линия")
    place = models.ForeignKey('Place', on_delete=models.CASCADE, default="", verbose_name="Место")
    memo = models.TextField(blank=True, verbose_name="Проблема")
    memo_images = models.ImageField(upload_to="memo/%Y/%m/%d/", blank=True, verbose_name="Фото беды")
    decision = models.TextField(blank=True, verbose_name="Решение")
    decision_images = models.ImageField(upload_to="decision/%Y/%m/%d/", blank=True, verbose_name="Фото решения")
    created = models.DateField(auto_now_add=True, verbose_name="Создано")
    data_complete = models.DateField(blank=True, null=True, verbose_name="Дата решения")
    important = models.BooleanField(default=False, verbose_name="Важность")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Ответственный")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "задача"
        verbose_name_plural = "задачи"


class Lines(models.Model):
    line = models.CharField(max_length=100, verbose_name="Линия")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.line

    class Meta:
        verbose_name = "линия"
        verbose_name_plural = "линии"


class Place(models.Model):
    place = models.CharField(max_length=100, verbose_name="Место")

    def __str__(self):
        return self.place

    class Meta:
        verbose_name = "место"
        verbose_name_plural = "места"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Отправитель")
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages",
                                  verbose_name="Получатель")
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Имя")
    email = models.EmailField(max_length=200, null=True, blank=True, verbose_name="email")
    subject = models.CharField(max_length=200, null=True, blank=True, verbose_name="Тема")
    body = models.TextField(verbose_name="Сообщение")
    is_read = models.BooleanField(default=False, null=True, verbose_name="Прочитано")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', 'created']
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"
