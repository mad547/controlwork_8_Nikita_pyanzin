from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    avatar = models.ImageField(
        upload_to='avatars',
        null=False,
        blank=False,
        verbose_name='Аватар'
    )
    messages_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество сообщений'
    )

    def __str__(self):
        return f'Профиль {self.user.username}'

    class Meta:
        db_table = 'profile'
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'