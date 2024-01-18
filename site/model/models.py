# from django.db import models

# # Create your models here.

# class Bot(models.Model):
#     label = models.CharField(max_length=100)
#     token = models.CharField(max_length=255)
#     chat_id = models.CharField(max_length=255)
#     message_pattern = models.CharField(max_length=255)
#     is_active = models.BooleanField(default=False)

# class Site(models.Model):
#     label = models.CharField(max_length=100)
#     url = models.URLField()
#     description = models.TextField(default='', blank=True, null=True)
#     expected_response_code = models.CharField(max_length=255)
#     expected_response_body_pattern = models.CharField(max_length=255, default='', blank=True, null=True)
#     checking_active = models.BooleanField(default=False)
#     bot = models.ForeignKey(Bot, on_delete=models.CASCADE,  related_name='model_site')


from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class BaseOwnedModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def is_user_owner(self, user):
        return self.user == user

    class Meta:
        abstract = True 

class Bot(BaseOwnedModel):
    label = models.CharField(max_length=100, verbose_name="Назва")
    token = models.CharField(max_length=255, verbose_name="Токен telegram бота")
    # chat_id = models.CharField(max_length=255, verbose_name="ID чату(вписати 0)")
    message_pattern = models.TextField(max_length=255, verbose_name="Шаблон повідомлення")
    is_active = models.BooleanField(default=False, verbose_name="Активниа")
    contacts = models.ManyToManyField('Contact',  related_name='model_site', verbose_name="Контакти")

    def __str__(self):
        return self.label
    
    class Meta:
        verbose_name = 'Розсилка'
        verbose_name_plural = 'розсилки'


class Site(BaseOwnedModel):
    label = models.CharField(max_length=100, verbose_name="Назва")
    url = models.URLField(verbose_name="URL сайту/сторінки")
    description = models.TextField(default='', blank=True, null=True, verbose_name="Опис")
    expected_response_code = models.CharField(max_length=255, verbose_name="Очікувані коди відповіді")
    expected_response_body_pattern = models.CharField(max_length=255, default='', blank=True, null=True, verbose_name="Шаблон тексту відповіді")
    cron_schedule = models.CharField(max_length=255, default='', blank=True, null=True, verbose_name="Розклад запуску", help_text="Рядок у форматі crontab(<a href=\"https://en.wikipedia.org/wiki/Cron\" target=\"_blank\">help</a>)")
    checking_active = models.BooleanField(default=False, verbose_name="Активний")
    inverse_conditions = models.BooleanField(default=False, verbose_name="Інверсія умов")
    bot = models.ManyToManyField(Bot,  related_name='model_site', verbose_name="Розсилки")

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = 'Сайт'
        verbose_name_plural = 'Сайти'

class Contact(BaseOwnedModel):
    label = models.CharField(max_length=100, verbose_name="Назва")
    contact_string = models.CharField(max_length=255, verbose_name="ID чату")
    is_active = models.BooleanField(default=False, verbose_name="Активний")

    def __str__(self):
        return self.label
    
    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакти'