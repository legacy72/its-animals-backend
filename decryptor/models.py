from django.db import models
# Create your models here.

class MD5Rainbow(models.Model):

    hash_value = models.CharField(
        'Хэш',
        max_length=255
    )

    key = models.CharField(
        'Ключ',
        max_length=255
    )

    class Meta:
        verbose_name = 'Хэш/ключ'
        verbose_name = 'Хэши/ключи'

    def __str__(self):
        return '%s %s' % (self.hash_value, self.key)