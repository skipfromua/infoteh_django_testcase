from django.db import models


class Message(models.Model):
    user = models.CharField(verbose_name='Пользователь', max_length=150)
    message_body = models.TextField(verbose_name='Текст сообщения')
    image = models.ImageField(verbose_name='Картинка')
    pub_date = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.user
