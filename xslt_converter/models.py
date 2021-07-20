from django.db import models


class Converter(models.Model):
    file_xml = models.FileField(verbose_name='XML файл')
    file_xslt = models.FileField(verbose_name='XSLT файл')

    class Meta:
        app_label = 'xslt_converter'
        verbose_name = 'XSLT Ковертер'
        verbose_name_plural = 'XSLT Ковертер'
