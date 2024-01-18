from django import forms

from croniter import croniter
from django.core.exceptions import ValidationError


class OwnedModelForm(forms.ModelForm):
    class Meta:
        exclude = ['user']  # Виключіть поле user з форми

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.instance.user = user

    def clean_cron_schedule(self):
        cron_schedule = self.cleaned_data['cron_schedule']
        if cron_schedule:
            # Перевіряємо чи розклад роботи коректний
            if not croniter.is_valid(cron_schedule):
                raise ValidationError('Некоректний розклад роботи, запис повинен відповідати crontab формату')
            return cron_schedule
        return None