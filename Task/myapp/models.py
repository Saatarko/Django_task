from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


# Create your models here.


class Task(models.Model):
    name_task = models.CharField('Название задачи', max_length=30)
    description = models.TextField('Описание задачи', max_length=500)
    date_start = models.DateTimeField('Дата начала', auto_now_add=True)
    date_end = models.DateTimeField('Дата окончания', null=True, blank=True)

    NEW = 'Новая'
    IN_PROGRESS = 'В процессе'
    COMPLETED = 'Завершена'

    STATUS_CHOICES = [
        (NEW, 'Новая'),
        (IN_PROGRESS, 'В процессе'),
        (COMPLETED, 'Завершена'),
    ]

    status = models.CharField('Статус', max_length=50, choices=STATUS_CHOICES, default=NEW)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.status == self.COMPLETED and self.date_end is None:
            self.date_end = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_task

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'