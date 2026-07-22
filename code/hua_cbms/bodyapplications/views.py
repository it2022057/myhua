from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from attachments.formsets import SecApplicationAttachmentFormSet, ApplicantApplicationAttachmentFormSet
from bodyapplications import forms
from bodyapplications.models import Application
from core import views
from core.models import AttachmentFormSetMixin

User = get_user_model()

"""
Generic Body applications Views
"""


class SecUpdate(AttachmentFormSetMixin, views.ScopedSecUpdateView):
    template_name = 'subjects/show_object.html'
    success_message = _('Το αίτημα σας ενημερώθηκε επιτυχώς.')
    attachment_formset_class = SecApplicationAttachmentFormSet


class SecList(views.ScopedSecListView):
    template_name = 'core/list_objects.html'


class SecMultipleList(views.SecMultipleListView):
    template_name = 'core/multiple_tables.html'


class SecDelete(views.ScopedDeleteView):
    template_name = 'subjects/show_object.html'
    success_message = _('Το αίτημα σας διαγράφηκε.')


class ApplicantCreate(AttachmentFormSetMixin, views.ApplicantCreateView):
    template_name = 'subjects/show_object.html'
    success_message = _('Το αίτημα σας καταχωρήθηκε επιτυχώς.')
    attachment_formset_class = ApplicantApplicationAttachmentFormSet


class ApplicantUpdate(AttachmentFormSetMixin, views.ApplicantUpdateView):
    template_name = 'subjects/show_object.html'
    success_message = _('Το αίτημα σας ενημερώθηκε επιτυχώς.')
    attachment_formset_class = ApplicantApplicationAttachmentFormSet


class ApplicantList(views.ApplicantListView):
    template_name = 'core/list_objects.html'


class ApplicantMultipleList(views.ApplicantMultipleListView):
    template_name = 'core/multiple_tables.html'


"""
Secretariat Views
"""


class SecUpdateApplication(SecUpdate):
    model = Application
    form_class = forms.SecApplicationForm
    success_url = 'bodyapplications:sec_list_bodyapplications'
    confirm_modal = True

    def get_attachment_form_kwargs(self):
        return {'user': self.request.user}


class SecListApplication(SecList):
    model = Application
    fields = ['request_subject', 'description', 'subject', 'applicant', 'attachments.download']
    headers = {
        'request_subject': _('Θέμα Αιτήματος'),
        'description': _('Περιγραφή'),
        'subject': _('Θέμα'),
        'applicant': _('Αιτών'),
        'attachments.download': _('Επισυναπτόμενα')
    }
    table_title = _('Αιτήσεις')
    create_button = False
    update_url = 'bodyapplications:sec_update_bodyapplication'
    back_url = reverse_lazy('bodies:sec_list_collectivebodies')


class SecDeleteApplication(SecDelete):
    model = Application
    success_url = 'bodyapplications:sec_list_bodyapplications'


"""
Applicant Views
"""


class ApplicantCreateApplication(ApplicantCreate):
    model = Application
    form_class = forms.ApplicationForm
    success_url = 'bodyapplications:applicant_list_bodyapplications'
    headline = _('Δημιουργία Αιτήματος')
    back_url = ''

    def form_valid(self, form):
        form.instance.applicant = self.request.user

        return super().form_valid(form)

    def get_attachment_form_kwargs(self):
        return {'user': self.request.user}


class ApplicantUpdateApplication(ApplicantUpdate):
    model = Application
    form_class = forms.ApplicationForm
    success_url = 'bodyapplications:applicant_list_bodyapplications'
    confirm_modal = True

    def get_attachment_form_kwargs(self):
        return {'user': self.request.user}


class ApplicantListApplication(ApplicantList):
    model = Application
    fields = ['request_subject', 'description', 'attachments.download']
    headers = {
        'request_subject': _('Θέμα Αιτήματος'),
        'description': _('Περιγραφή'),
        'attachments.download': _('Επισυναπτόμενα')
    }
    table_title = _('Αιτήσεις')
    update_url = 'bodyapplications:applicant_update_bodyapplication'
    create_url = 'bodyapplications:applicant_create_bodyapplication'

    def get_queryset(self):
        applicant = get_object_or_404(User, pk=self.request.user.pk)

        return applicant.bodyapplications.all().order_by('pk')
