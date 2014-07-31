from django.db import models
from plupload.models import PluploadImage
from django.forms import ModelMultipleChoiceField, CheckboxSelectMultiple
from django.db.models.fields.related import RECURSIVE_RELATIONSHIP_CONSTANT, ManyToManyRel
from django.db.models.fields import Field
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.forms.util import flatatt


class PluploadWidget(CheckboxSelectMultiple):
    class Media:
        js = (
            'jquery/jquery.min.js',
            'jquery-ui/js/jquery-ui.custom.min.js',
            'plupload/js/plupload.full.js',
        )
        css = {
            'all': (settings.STATIC_URL + 'plupload/css/plupload_widget.css',),
        }
    def value_from_datadict(self, data, files, name):
        result = super(PluploadWidget, self).value_from_datadict(data, files, name)
        return result
    def render(self, name, value, attrs=None, choices=()):
        if value and len(value):
            images = PluploadImage.objects.filter(pk__in=value)
        else:
            images = False
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(render_to_string('plupload/widget.html', {
            'final_attrs': flatatt(final_attrs),
            'id': final_attrs['id'],
            'name': name,
            'images': images,
            }))

class PluploadGalleryFormField(ModelMultipleChoiceField):
    widget = PluploadWidget

class PluploadGalleryField(models.ManyToManyField):
    def __init__(self, to=None, **kwargs):
        if not to:
            to = PluploadImage
        try:
            assert not to._meta.abstract, "%s cannot define a relation with abstract class %s" % (self.__class__.__name__, to._meta.object_name)
        except AttributeError: # to._meta doesn't exist, so it must be RECURSIVE_RELATIONSHIP_CONSTANT
            assert isinstance(to, basestring), "%s(%r) is invalid. First parameter to ManyToManyField must be either a model, a model name, or the string %r" % (self.__class__.__name__, to, RECURSIVE_RELATIONSHIP_CONSTANT)
            # Python 2.6 and earlier require dictionary keys to be of str type,
            # not unicode and class names must be ASCII (in Python 2.x), so we
            # forcibly coerce it here (breaks early if there's a problem).
            to = str(to)

        kwargs['verbose_name'] = kwargs.get('verbose_name', None)
        kwargs['rel'] = ManyToManyRel(to,
            related_name=kwargs.pop('related_name', None),
            limit_choices_to=kwargs.pop('limit_choices_to', None),
            symmetrical=kwargs.pop('symmetrical', to==RECURSIVE_RELATIONSHIP_CONSTANT),
            through=kwargs.pop('through', None))

        self.db_table = kwargs.pop('db_table', None)
        if kwargs['rel'].through is not None:
            assert self.db_table is None, "Cannot specify a db_table if an intermediary model is used."

        Field.__init__(self, **kwargs)


    def formfield(self, **kwargs):
        db = kwargs.pop('using', None)
        defaults = {
            'form_class': PluploadGalleryFormField,
            'queryset': self.rel.to._default_manager.using(db).complex_filter(self.rel.limit_choices_to)
        }
        defaults.update(kwargs)
        # If initial is passed in, it's a list of related objects, but the
        # MultipleChoiceField takes a list of IDs.
        if defaults.get('initial') is not None:
            initial = defaults['initial']
            if callable(initial):
                initial = initial()
            defaults['initial'] = [i._get_pk_val() for i in initial]
        return super(models.ManyToManyField, self).formfield(**defaults)