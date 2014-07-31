# -*- coding: utf-8 -*-
from django import forms
from shop import models


class ProductFilterForm(forms.Form):
    trademarks = forms.ModelMultipleChoiceField(queryset=models.Trademark.objects.all(), label=u'Торговые марки',
                                                widget=forms.CheckboxSelectMultiple,
                                                initial=models.Trademark.objects.all())
    categories = forms.ModelMultipleChoiceField(queryset=models.Category.objects.all(), label=u'Категории',
                                                widget=forms.CheckboxSelectMultiple,
                                                initial=models.Category.objects.all())
    price_min = forms.IntegerField(label=u'Цена от', initial=1000)
    price_max = forms.IntegerField(label=u'Цена до', initial=16000)
    min_stock = forms.IntegerField(label=u'Минимальный остаток', initial=5)