from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.html import escape
from django.utils.translation import gettext_lazy as _

from accounts.checks import is_secretariat
from accounts.utils import get_domain_uri
from attachments.formsets import SecApplicationAttachmentFormSet, ApplicantApplicationAttachmentFormSet
from bodies.models import CollectiveBody
from bodyapplications import forms
from bodyapplications.emails import SEC_APPLICATION_NOTIFICATION_BODY, SEC_APPLICATION_NOTIFICATION_SUBJECT, \
    SEC_APPLICATION_UPDATE_NOTIFICATION_SUBJECT, SEC_APPLICATION_UPDATE_NOTIFICATION_BODY
from bodyapplications.models import Application
from core import views
from core.models import AttachmentFormSetMixin
from core.views import Table
from hua_cbms import settings
from mailer.gmail import notify
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


@login_required
@user_passes_test(is_secretariat)
def sec_show_application_via_link(request, token):
    signer = TimestampSigner()
    try:
        unsigned = signer.unsign_object(token, max_age=settings.APPLICATION_MAX_AGE_SECS)
        email = unsigned['email']
        application_pk = unsigned['application_pk']
        application = get_object_or_404(Application, pk=application_pk)
    except SignatureExpired:
        unsigned = signer.unsign_object(token)
        application_pk = unsigned['application_pk']
        application = get_object_or_404(Application, pk=application_pk)
        message = _(
            'Η προθεσμία για την απάντηση προς τον αιτούντα έχει λήξει. Η διαδικασία θα πρέπει να ξεκινήσει εκ νέου. '
            'Εάν απαιτείται, μπορείτε να επικοινωνήσετε με τον αιτούντα στο email: ') + application.applicant.email
        return render(request, 'accounts/message.html', context={'message': message})
    except BadSignature:
        message = _('O σύνδεσμος δεν είναι σωστός!')
        return render(request, 'accounts/message.html', context={'message': message})

    # A secretariat user could potentially open another secretariat’s email link if they somehow got the token
    if not request.user.is_superuser and request.user.email != email:
        raise PermissionDenied

    if application.subject is not None:
        message = _('Έχετε ήδη συνδέσει το αίτημα με ένα υπάρχον θέμα στο σύστημα.')
        return render(request, 'accounts/message.html', context={'message': message})

    return redirect('bodyapplications:sec_update_bodyapplication', pk=application.pk)


class SecUpdateApplication(SecUpdate):
    model = Application
    form_class = forms.SecApplicationForm
    success_url = 'bodyapplications:sec_list_bodyapplications'
    confirm_modal = True

    def setup(self, *args, **kwargs):
        application = get_object_or_404(Application, pk=kwargs['pk'])
        self.success_message = _(
            'Το αίτημα του αιτών, με όνομα χρήστη %s, ενημερώθηκε επιτυχώς.' % str(application.applicant.username))
        super().setup(*args, **kwargs)

    def form_valid(self, form):
        application = get_object_or_404(Application, pk=self.kwargs['pk'])

        response = super().form_valid(form)

        email = application.applicant.email
        message_body = SEC_APPLICATION_UPDATE_NOTIFICATION_BODY.format(applicant_username=escape(application.applicant.username))
        notify.delay(email, SEC_APPLICATION_UPDATE_NOTIFICATION_SUBJECT, message_body, cc=settings.ALWAYS_NOTIFY)

        return response

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
                order=[[2, 'desc'], [3, 'asc'], [0, 'asc']],
                create_button=False,
                update_url='bodyapplications:sec_update_bodyapplication',
                objects=pending_applications,
                next=self.request.path,
            ),
            Table(
                fields=['request_subject', 'description', 'updated_at', 'subject', 'applicant', 'attachments.download'],
                table_title=_('Διευθετημένες Αιτήσεις'),
                headers={
                    'request_subject': _('Θέμα Αιτήματος'),
                    'description': _('Περιγραφή'),
                    'updated_at': _('Ημ/νία Ενημέρωσης'),
                    'subject': _('Θέμα'),
                    'applicant': _('Αιτών'),
                    'attachments.download': _('Επισυναπτόμενα')
                },
                table_id='resolved_applications',
                order=[[2, 'desc'], [4, 'asc'], [3, 'asc'], [0, 'asc']],
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
        self.success_message = _(
            'Το αίτημα του αιτών, με όνομα χρήστη %s, διαγράφηκε.' % str(application.applicant.username))
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
        applicant = get_object_or_404(User, pk=self.request.user.pk)
        form.instance.applicant = applicant

        response = super().form_valid(form)

        secretariat = collective_body.secretariat
        if not secretariat or not secretariat.user or not secretariat.user.email:
            return response

        request_subject = form.cleaned_data['request_subject']
        description = form.cleaned_data['description']
        application = self.object

        signer = TimestampSigner()
        domain = get_domain_uri(self.request)
        email = secretariat.user.email
        signed_data = signer.sign_object({'email': email, 'application_pk': application.pk,})
        url = domain + reverse_lazy('bodyapplications:sec_show_bodyapplication_from_email_link', kwargs={'token': signed_data})
        message_body = SEC_APPLICATION_NOTIFICATION_BODY.format(
            first_name=escape(applicant.first_name),
            last_name=escape(applicant.last_name),
            email=escape(applicant.email),
            collective_body_title_gr=escape(collective_body.title_gr),
            collective_body_title_en=escape(collective_body.title_en),
            request_subject=escape(request_subject),
            description=escape(description),
            url=url,
        )
        attachment_paths = [attachment.file.path for attachment in application.attachments.all() if attachment.file]
        notify.delay(settings.ALWAYS_NOTIFY, SEC_APPLICATION_NOTIFICATION_SUBJECT, message_body, attachments=attachment_paths, cc=email)

        return response

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
    fields = ['request_subject', 'description', 'subject.decision', 'subject.collective_body', 'attachments.download']
    headers = {
        'request_subject': _('Θέμα Αιτήματος'),
        'description': _('Περιγραφή'),
        'subject.decision': _('Απόφαση'),
        'subject.collective_body': _('Προς'),
        'attachments.download': _('Επισυναπτόμενα')
    }
    table_title = _('Αιτήσεις')
    create_url = 'bodies:applicant_list_collectivebodies'
    create_text = _('Κάνε Αίτηση')
    update_url = 'bodyapplications:applicant_update_bodyapplication'

    def get_queryset(self):
        applicant = get_object_or_404(User, pk=self.request.user.pk)

        return applicant.bodyapplications.all().order_by('pk')
