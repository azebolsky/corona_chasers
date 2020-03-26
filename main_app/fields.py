from django import forms
from django.template.defaultfilters import filesizeformat


class RestrictedImageField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        self.max_file_size = kwargs.pop('max_file_size', None)
        super(RestrictedImageField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(RestrictedImageField, self).clean(*args, **kwargs)
        try:
            if data.size > self.max_file_size:
                raise forms.ValidationError(('File size limit is %s, attempted file size was %s') % (filesizeformat(self.max_file_size), filesizeformat(data.size)))
        except AttributeError:
            pass
        return data
