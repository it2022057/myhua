# widgets.py
from django import forms
from django.utils.translation import gettext_lazy as _


class DatePickerInput(forms.DateInput):
    input_type = 'date'

    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'datepicker',
            'placeholder': _('Επιλέξτε')
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class ImageInput(forms.widgets.Input):
    input_type = 'file'
    initial_text = _("Currently")
    input_text = _("Change")
    template_name = 'core/partials/image_widget.html'

    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'form-control d-flex h-auto',
            'accept': 'image/*'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

    def is_initial(self, value):
        """
        Return whether value is considered to be initial value.
        """
        return bool(value and getattr(value, "url", False))

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        context['widget'].update(
            {
                'image': value,
                'is_initial': self.is_initial(value),
                'input_text': self.input_text,
                'initial_text': self.initial_text,
            }
        )
        return context


class CustomFileInput(forms.FileInput):
    template_name = 'core/partials/file_input.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        # Extract just the filename from the value
        if value:
            # value is typically a FieldFile object or string path
            filename = str(value).split('/')[-1]  # Gets last part after final /
            context['widget']['filename'] = filename
            context['widget']['has_file'] = True
        else:
            context['widget']['has_file'] = False

        return context
