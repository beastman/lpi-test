# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class PluploadImage(models.Model):
    image = models.ImageField(upload_to='uploads/', verbose_name='Изображение')
    sort_order = models.IntegerField(blank=True, null=True, verbose_name='Порядок при сортировке')
    class Meta:
        ordering = ('sort_order',)