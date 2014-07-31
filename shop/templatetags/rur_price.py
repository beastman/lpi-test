# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def rur_sign(value):
    return mark_safe(str(value) + u' <span class="rur">p<span>уб.</span></span>')