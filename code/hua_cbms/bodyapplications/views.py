from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from attachments.formsets import SecApplicationAttachmentFormSet, ApplicantApplicationAttachmentFormSet
from bodies.models import CollectiveBody
from bodyapplications import forms
from bodyapplications.models import Application
from core import views
from core.models import AttachmentFormSetMixin
from core.views import Table
from scopes.models import Secretariat
from scopes.utils import get_secretariat_scope

User = get_user_model()

"""
Generic Body applications Views
"""


class SecUpdate(AttachmentFormSetMixin, views.ScopedSecUpdateView):
    template_name = 'subjects/show_object.html'
    attachment_formset_class = SecApplicationAttachmentFormSet


class SecList(views.ScopedSecListView):
    template_name = 'core/list_objects.html'


class SecMultipleList(views.SecMultipleListView):
    template_name = 'core/multiple_tables.html'


class SecDelete(views.ScopedDeleteView):
    template_name = 'subjects/show_object.html'


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

    def setup(self, *args, **kwargs):
        application = get_object_or_404(Application, pk=kwargs['pk'])
        self.success_message = _('Το αίτημα του αιτών, με όνομα χρήστη %s, ενημερώθηκε επιτυχώς.' %str(application.applicant.username))
        super().setup(*args, **kwargs)

    def get_attachment_form_kwargs(self):
        return {'user': self.request.user}


class SecMultipleListApplication(SecMultipleList):
    model = Application
    master_headline = _('Αιτήσεις προς Συλλογικά Όργανα')
    master_p = _('Παρακάτω εμφανίζονται οι αιτήσεις που εκκρεμούν και οι αιτήσεις που έχουν ήδη διευθετηθεί...')
    back_url = reverse_lazy('bodies:sec_list_collectivebodies')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        sec = Secretariat.objects.filter(user=request.user).first()

        if sec is None and not request.user.is_superuser:
            raise PermissionDenied

        pending_applications = Application.objects.filter(subject__isnull=True)

        if request.user.is_superuser:
            resolved_applications = Application.objects.filter(subject__isnull=False)
        else:
            scope = get_secretariat_scope(user=request.user)

            resolved_applications = Application.objects.filter(
                subject__isnull=False,
                subject__collective_body__in=scope['collective_bodies']
            )

        self.tables = [
            Table(
                fields=['request_subject', 'description', 'created_at', 'applicant', 'attachments.download'],
                table_title=_('Εκκρεμείς Αιτήσεις'),
                headers={
                    'request_subject': _('Θέμα Αιτήματος'),
                    'description': _('Περιγραφή'),
                    'created_at': _('Ημ/νία Υποβολής'),
                    'applicant': _('Αιτών'),
                    'attachments.download': _('Επισυναπτόμενα')
                },
                table_id='pending_applications',
                order=[[2, 'asc'], [3, 'asc'], [0, 'asc']],
                create_button=False,
                update_url='bodyapplications:sec_update_bodyapplication',
                objects=pending_applications,
                next=self.request.path,
            ),
            Table(
                fields=['request_subject', 'description', 'subject', 'applicant', 'attachments.download'],
                table_title=_('Διευθετημένες Αιτήσεις'),
                headers={
                    'request_subject': _('Θέμα Αιτήματος'),
                    'description': _('Περιγραφή'),
                    'subject': _('Θέμα'),
                    'applicant': _('Αιτών'),
                    'attachments.download': _('Επισυναπτόμενα')
                },
                table_id='resolved_applications',
                order=[[2, 'asc'], [3, 'asc']],
                create_button=False,
                update_url='bodyapplications:sec_update_bodyapplication',
                objects=resolved_applications,
                next=self.request.path,
            ),
        ]


class SecDeleteApplication(SecDelete):
    model = Application
    success_url = 'bodyapplications:sec_list_bodyapplications'

    def setup(self, *args, **kwargs):
        application = get_object_or_404(Application, pk=kwargs['pk'])
        self.success_message = _('Το αίτημα του αιτών, με όνομα χρήστη %s, διαγράφηκε.' %str(application.applicant.username))
        super().setup(*args, **kwargs)


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
        collective_body = get_object_or_404(CollectiveBody.objects.active_now(), pk=self.kwargs['pk'])
        form.instance.applicant = self.request.user

        response = super().form_valid(form)

        self.send_application_email(collective_body)

        return response

    def get_attachment_form_kwargs(self):
        return {'user': self.request.user}

    # def send_application_email(self):
    #     secretariat = self.collective_body.secretariat
    #
    #     if not secretariat:
    #         return
    #
    #     if not secretariat.user or not secretariat.user.email:
    #         return
    #
    #     to = secretariat.user.email
    #
    #     subject = _('Νέο αίτημα προς συλλογικό όργανο')
    #
    #     body = """
    #         <p>Υποβλήθηκε νέο αίτημα προς το συλλογικό όργανο:</p>
    #
    #         <p><strong>{collective_body}</strong></p>
    #
    #         <p>
    #             <strong>Αιτών:</strong> {applicant}<br>
    #             <strong>Θέμα αιτήματος:</strong> {request_subject}
    #         </p>
    #
    #         <p>
    #             Παρακαλούμε συνδεθείτε στην πλατφόρμα για να το εξετάσετε.
    #         </p>
    #     """.format(
    #         collective_body=escape(str(self.collective_body)),
    #         applicant=escape(str(self.object.applicant)),
    #         request_subject=escape(str(self.object.request_subject)),
    #     )
    #
    #     notify.delay(
    #         to=to,
    #         subject=subject,
    #         body=body
    #     )


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
    create_url = 'bodies:applicant_list_collectivebodies'
    create_text = _('Κάνε Αίτηση')
    update_url = 'bodyapplications:applicant_update_bodyapplication'

    def get_queryset(self):
        applicant = get_object_or_404(User, pk=self.request.user.pk)

        return applicant.bodyapplications.all().order_by('pk')
