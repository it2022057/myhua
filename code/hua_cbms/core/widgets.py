# widgets.py
from django import forms
from django.forms import CheckboxInput
from django.forms.widgets import FILE_INPUT_CONTRADICTION, FileInput
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
    needs_multipart_form = True
    clear_checkbox_label = _('Clear')
    initial_text = _('Currently')
    template_name = 'core/partials/image_widget.html'
    checked = False

    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'form-control',
            'accept': 'image/*'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

    def clear_checkbox_name(self, name):
        """
        Given the name of the file input, return the name of the clear checkbox
        input.
        """
        return name + "-clear"

    def clear_checkbox_id(self, name):
        """
        Given the name of the clear checkbox input, return the HTML id for it.
        """
        return name + "_id"

    def is_initial(self, value):
        """
        Return whether value is considered to be initial value.
        """
        return bool(value and getattr(value, "url", False))

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        # Sets a default pic, depending on the gender of the user, as fallback
        if self.pi.gender == self.pi.GENDER_MALE:
            default_pic = 'accounts/images/default_man.png'
        elif self.pi.gender == self.pi.GENDER_FEMALE:
            default_pic = 'accounts/images/default_woman.jpg'
        else:
            default_pic = 'accounts/images/default_other.png'

        checkbox_name = self.clear_checkbox_name(name)
        checkbox_id = self.clear_checkbox_id(checkbox_name)

        context['widget'].update(
            {
                'image': value,
                'checkbox_name': checkbox_name,
                'checkbox_id': checkbox_id,
                'is_initial': self.is_initial(value),
                'initial_text': self.initial_text,
                'clear_checkbox_label': self.clear_checkbox_label,
                'default_pic': default_pic
            }
        )
        return context

    def value_from_datadict(self, data, files, name):
        upload = FileInput().value_from_datadict(data, files, name)
        self.checked = self.clear_checkbox_name(name) in data
        if not self.is_required and CheckboxInput().value_from_datadict(
            data, files, self.clear_checkbox_name(name)
        ):
            if upload:
                # If the user contradicts themselves (uploads a new file AND
                # checks the "clear" checkbox), we return a unique marker
                # object that FileField will turn into a ValidationError.
                return FILE_INPUT_CONTRADICTION
            # False signals to clear any existing value, as opposed to just None
            return False
        return upload

    def value_omitted_from_data(self, data, files, name):
        return (
            FileInput().value_omitted_from_data(data, files, name)
            and self.clear_checkbox_name(name) not in data
        )


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
