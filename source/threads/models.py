from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.fields import PositiveIntegerField


# Create your models here.
class Thread(models.Model):
    title = models.CharField(
        max_length=300,
        null=False,
        blank=False,
        verbose_name='Название'
    )
    content = models.TextField(
        null=False,
        blank=False,
        verbose_name='Содержимое'
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='threads',
        verbose_name='Автор'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    answers_count = PositiveIntegerField(
        default=0,
        verbose_name='Количество ответов'
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'thread'
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
        ordering = ['-created_at']


class Answer(models.Model):
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Тема'
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Автор'
    )
    content = models.TextField(
        null=False,
        blank=False,
        verbose_name='Текст'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return f'Ответ {self.author.username} в {self.thread.title}'

    class Meta:
        db_table = 'answer'
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ['-created_at']