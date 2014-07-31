# -*- coding: utf-8 -*-
from django.db import models
from shop.fields import AutoresizeImageField, TrasliteratedAutoField
from plupload.fields import PluploadGalleryField


class Trademark(models.Model):
    title = models.CharField(max_length=255, verbose_name=u'Наименование', unique=True)
    logo = AutoresizeImageField(upload_to='trademarks/', resize_height=150, resize_width=150, verbose_name=u'Логотип')
    description = models.TextField(verbose_name=u'Описание')
    phone = models.CharField(max_length=20, verbose_name=u'Телефон')
    email = models.EmailField(verbose_name='E-mail')
    site_url = models.CharField(max_length=255, verbose_name=u'Сайт')
    url_slug = TrasliteratedAutoField(transliterate_field_name='title', verbose_name=u'Фрагмент ЧПУ', max_length=255)

    class Meta:
        ordering = ('title',)
        verbose_name = u'Торговая марка'
        verbose_name_plural = u'Торговые марки'

    def __unicode__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name=u' Наименование категории', unique=True)
    icon = AutoresizeImageField(upload_to='categories/', resize_height=100, resize_width=100,
                                verbose_name=u'Пиктограмма')
    url_slug = TrasliteratedAutoField(transliterate_field_name='title', verbose_name=u'Фрагмент ЧПУ', max_length=255)

    class Meta:
        ordering = ('title',)
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'

    def __unicode__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name=u'Наименование')
    images = PluploadGalleryField(verbose_name=u'Изображения')
    trademark = models.ForeignKey('Trademark', verbose_name=u'Торговая марка')
    #На всякий случай добавляем поле категории. Скорее всего, его забыли указать в задании
    category = models.ForeignKey('Category', verbose_name=u'Категория')
    sku = models.CharField(max_length=50, verbose_name=u'СКУ')
    description = models.TextField(verbose_name=u'Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Цена')
    in_stock_count = models.PositiveIntegerField(verbose_name=u'Количество на складе')
    url_slug = TrasliteratedAutoField(transliterate_field_name='title', verbose_name=u'Фрагмент ЧПУ', max_length=255)

    class Meta:
        ordering = ('title',)
        verbose_name = u'Товар'
        verbose_name_plural = u'Товары'

    def __unicode__(self):
        return self.title