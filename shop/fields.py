from django.db.models import ImageField, CharField
from PIL import Image
from django.conf import settings
import os
from django import forms
from django.core import validators
from django.utils.safestring import mark_safe


class AutoresizeImageField(ImageField):
    def __init__(self, *args, **kwargs):
        if 'resize_width' in kwargs.keys():
            self.resize_width = kwargs['resize_width']
            del(kwargs['resize_width'])
        else:
            raise Exception('resize_width is required')
        if 'resize_height' in kwargs.keys():
            self.resize_height = kwargs['resize_height']
            del(kwargs['resize_height'])
        else:
            raise Exception('resize_height is required')
        super(AutoresizeImageField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        file = super(AutoresizeImageField, self).pre_save(model_instance, add)
        file_path = os.path.join(settings.MEDIA_ROOT, file.name)
        image = Image.open(file_path)
        image = image.resize((self.resize_width, self.resize_height))
        image.save(file_path)
        image.close()
        return file


class TransliteratedAutoFieldWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        transliterate_field_name = self.attrs['transliterate_field_name']
        prefix = self.attrs['prefix']
        result = super(TransliteratedAutoFieldWidget, self).render(name, value, attrs)
        if not value:
            script = """<script type="text/javascript">
            $(function() {{
                $('#id_{field_name}').keyup(function() {{
                    field_value = $('#id_{field_name}').val();
                    if(field_value.length > 30) {{
                        field_value = field_value.substr(0, field_value.indexOf(' ', 30));
                    }}
                    $('#{this_id}').val('{prefix}' + transliterate(field_value))
                }});
            }});
            </script>""".format(field_name=transliterate_field_name, this_id=attrs['id'], prefix=prefix)
            result += script
        return mark_safe(result)

    class Media:
        js = ('jquery/jquery.min.js', 'js/transliterate.js',)


class TransliteratedAutoFormField(forms.CharField):
    widget = TransliteratedAutoFieldWidget

    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
        self.transliterate_field_name = kwargs['transliterate_field_name']
        self.prefix = kwargs['prefix']
        del(kwargs['transliterate_field_name'])
        del(kwargs['prefix'])
        super(TransliteratedAutoFormField, self).__init__(max_length, min_length, *args, **kwargs)

    def widget_attrs(self, widget):
        result = super(TransliteratedAutoFormField, self).widget_attrs(widget)
        result['transliterate_field_name'] = self.transliterate_field_name
        result['prefix'] = self.prefix
        return result


class TrasliteratedAutoField(CharField):
    def __init__(self, *args, **kwargs):
        self.transliterate_field_name = kwargs['transliterate_field_name']
        self.prefix = kwargs.get('prefix', '')
        del(kwargs['transliterate_field_name'])
        if 'prefix' in kwargs.keys():
            del(kwargs['prefix'])
        super(CharField, self).__init__(*args, **kwargs)
        self.validators.append(validators.MaxLengthValidator(self.max_length))

    def formfield(self, **kwargs):
        if 'widget' in kwargs.keys():
            del(kwargs['widget'])
        defaults = {
            'max_length': self.max_length,
            'transliterate_field_name': self.transliterate_field_name,
            'prefix': self.prefix,
            'form_class': TransliteratedAutoFormField,
        }
        defaults.update(kwargs)
        return super(CharField, self).formfield(**defaults)