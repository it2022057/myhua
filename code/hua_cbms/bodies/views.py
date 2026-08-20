from dal import autocomplete
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.checks import is_secretariat, is_staff_member
from accounts.models import StaffMember
from accounts.utils import get_domain_uri
from bodies import forms
from bodies.emails import PARTICIPANT_ADDED_NOTIFICATION_SUBJECT, PARTICIPANT_REMOVED_NOTIFICATION_SUBJECT
from bodies.models import CollectiveBody
from bodyapplications.models import Application
from core import views
from core.models import TitleStrMixin
from core.utils import get_order_by_title
from core.views import Table
from hua_cbms import settings
from mailer.gmail import notify
from meetings.models import Meeting
from scopes.models import Secretariat
from scopes.utils import get_secretariat_scope
from subjects.models import Subject, Decision, SubjectType, SubjectCategory

"""
Generic CollectiveBody Views
"""


class SecCreate(views.ScopedSecCreateView):
    template_name = 'bodies/show_object.html'
    success_message = _('Το πανεπιστημιακό όργανο καταχωρήθηκε επιτυχώς.')


class SecUpdate(views.ScopedSecUpdateView):
    template_name = 'bodies/show_object.html'
    success_message = _('Το πανεπιστημιακό όργανο ενημερώθηκε επιτυχώς.')


class SecList(views.ScopedSecListView):
    template_name = 'bodies/list_objects.html'


class SecMultipleList(views.SecMultipleListView):
    template_name = 'bodies/multiple_tables.html'


class SecDelete(views.ScopedDeleteView):
    template_name = 'bodies/show_object.html'
    success_message = _('Το πανεπιστημιακό όργανο διαγράφηκε.')


class StaffMultipleList(views.StaffMultipleListView):
    template_name = 'bodies/multiple_tables.html'


class ApplicantList(views.ApplicantListView):
    template_name = 'core/list_objects.html'


"""
Secretariat Views
"""


class SecCreateCollectiveBody(SecCreate):
    model = CollectiveBody
    form_class = forms.SecCollectiveBodyForm
    success_url = 'bodies:sec_list_collectivebodies'
    headline = _('Δημιουργία Συλλογικού Πανεπιστημιακού Οργάνου')
    back_url = ''

    # Only the admin can create a new collective body
    def test_func(self):
        return self.request.user.is_superuser


class SecUpdateCollectiveBody(SecUpdate):
    model = CollectiveBody
    form_class = forms.SecCollectiveBodyForm
    success_url = 'bodies:sec_list_collectivebodies'
    delete_url = 'bodies:sec_delete_collectivebody'
    confirm_modal = True

    def form_valid(self, form):
        # Store the old participant ids before saving the changes
        old_participant_ids = set(self.object.participants.values_list('pk', flat=True))

        # Save the collective body
        response = super().form_valid(form)

        collective_body = self.object

        # Retrieve the updated participant ids after saving the changes
        new_participant_ids = set(collective_body.participants.values_list('pk', flat=True))

        # Calculate the participants added to or removed from the collective body
        added_participant_ids = new_participant_ids - old_participant_ids
        removed_participant_ids = old_participant_ids - new_participant_ids

        # Get the actual affected, from the change, objects
        added_participants = collective_body.participants.filter(pk__in=added_participant_ids)
        removed_participants = StaffMember.objects.filter(pk__in=removed_participant_ids)

        # Notify every newly added participant
        for participant in added_participants:
            if participant.email:
                signer = TimestampSigner()
                domain = get_domain_uri(self.request)
                email = participant.email
                signed_data = signer.sign_object({'email': email, 'collective_body_pk': collective_body.pk})
                url = domain + reverse_lazy('bodies:staff_show_collectivebody_from_email_link',
                                            kwargs={'token': signed_data})
                notify.delay(
                    participant.email,
                    PARTICIPANT_ADDED_NOTIFICATION_SUBJECT,
                    collective_body.participant_added_notification_body(url)
                )

        # Notify every removed participant
        for participant in removed_participants:
            if participant.email:
                notify.delay(
                    participant.email,
                    PARTICIPANT_REMOVED_NOTIFICATION_SUBJECT,
                    collective_body.participant_removed_notification_body()
                )

        return response


class SecListCollectiveBody(SecList):
    model = CollectiveBody
    fields = ['title_gr', 'president', 'secretariat', 'start_date', 'end_date', 'active']
    headers = {
        'title_gr': _('Τίτλος'),
        'participants': _('Συμμετέχοντες'),
        'president': _('Πρόεδρος'),
        'secretariat': _('Γραμματεία'),
        'start_date': _('Ημερομηνία Έναρξης'),
        'end_date': _('Ημερομηνία Λήξης'),
        'active': _('Ενεργό')
    }
    table_title = _('Συλλογικά Όργανα')
    ordering = ['end_date', 'start_date', 'secretariat', 'president', get_order_by_title()]
    update_url = 'bodies:sec_update_collectivebody'
    extra_buttons = True
    extra_text = _('Συμμετέχοντες')
    extra_button_icon = 'groups'
    extra_url = 'accounts:sec_list_participants'
    extra_buttons2 = True
    extra_button_icon2 = 'info'
    extra_text2 = _('Πληροφορίες')
    extra_url2 = 'bodies:sec_overview_collectivebody'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        if request.user.is_superuser:
            # If the user is the admin, show the create_button and assign a create_url
            self.create_url = 'bodies:sec_create_collectivebody'
        else:
            # else hide it, because only the admin can create a new collective body
            self.create_button = False
            self.create_url = None


class SecDeleteCollectiveBody(SecDelete):
    model = CollectiveBody
    success_url = 'bodies:sec_list_collectivebodies'


class SecCollectiveBodyOverviewList(SecMultipleList):
    model = CollectiveBody
    master_headline = _('Στοιχεία Συλλογικού Οργάνου')
    master_p = _('Παρακάτω ακολουθούν κάποιες σημαντικές πληροφορίες για το συλλογικό όργανο...')
    back_url = reverse_lazy('bodies:sec_list_collectivebodies')

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        sec = Secretariat.objects.filter(user=self.request.user).first()
        body = get_object_or_404(CollectiveBody, pk=self.kwargs['pk'])

        if (body.secretariat != sec) and not self.request.user.is_superuser:
            raise PermissionDenied

        if body:
            self.master_headline = _('Στοιχεία Συλλογικού Οργάνου: ') + '%s' % str(body)

        # Allow modifications only when the CollectiveBody is active and its end_date has not passed
        can_edit = body.active and (body.end_date >= timezone.now())

        subjects = Subject.objects.filter(collective_body=body)
        self.tables = [
            Table(
                fields=['index', 'type', 'category', 'applicant_user', 'program', 'department', 'school', 'notes', 'attachments'],
                table_title=_('Θέματα Συνεδριάσεων Συλλογικού Οργάνου'),
                headers={
                    'index': _('Θέση'),
                    'type': _('Τύπος'),
                    'category': _('Κατηγορία'),
                    'applicant_user': _('Αιτών'),
                    'program': _('Πρόγραμμα Σπουδών'),
                    'department': _('Τμήμα'),
                    'school': _('Σχολή'),
                    'notes': _('Σημειώσεις'),
                    'attachments': _('Επισυναπτόμενα')
                },
                table_id='subject',
                order=[[0, 'asc']],
                update_url='subjects:sec_update_subject' if can_edit else None,
                create_url='subjects:sec_create_subject' if can_edit else None,
                update_buttons=can_edit,
                create_button=can_edit,
                objects=subjects,
                next=self.request.path
            ),
            Table(
                fields=['display_name', 'title', 'email'],
                table_title=_('Συμμετέχοντες'),
                headers={
                    'display_name': _('Ονοματεπώνυμο'),
                    'title': _('Ιδιότητα'),
                    'email': _('E-mail')
                },
                table_id='participants',
                order=[[1, 'asc'], [0, 'asc']],
                update_url_callable=lambda obj: reverse_lazy(
                    "accounts:sec_update_participants",
                    kwargs={"pk": body.pk},
                ) if can_edit else None,
                update_text=_('Ενημέρωση λίστας συμμετεχόντων'),
                create_url='accounts:sec_create_staff_member' if can_edit else None,
                update_buttons=can_edit,
                create_button=can_edit,
                objects=body.participants.all(),
                next=self.request.path
            ),
            Table(
                fields=['subject', 'title', 'attachments'],
                table_title=_('Αποφάσεις για τα Θέματα'),
                headers={
                    'subject': _('Θέμα'),
                    'title': _('Τελική Απόφαση'),
                    'attachments': _('Επισυναπτόμενα')
                },
                table_id='decision',
                order=[[0, 'asc'], [1, 'asc']],
                update_url='subjects:sec_update_decision' if can_edit else None,
                create_url='subjects:sec_create_decision' if can_edit else None,
                update_buttons=can_edit,
                create_button=can_edit,
                objects=Decision.objects.filter(subject__in=subjects),
                next=self.request.path
            ),
            Table(
                fields=['index', 'present', 'absent', 'location', 'date_and_time', 'notes'],
                table_title=_('Συνεδριάσεις Συλλογικού Οργάνου'),
                headers={
                    'index': _('Θέση'),
                    'present': _('Παρών'),
                    'absent': _('Απών'),
                    'location': _('Τοποθεσία'),
                    'date_and_time': _('Ημερομηνία & ώρα'),
                    'notes': _('Σημειώσεις')
                },
                table_id='meeting',
                order=[[0, 'asc']],
                update_url='meetings:sec_update_meeting' if can_edit else None,
                create_url='meetings:sec_create_meeting' if can_edit else None,
                update_buttons=can_edit,
                create_button=can_edit,
                objects=Meeting.objects.filter(collective_body=body),
                next=self.request.path
            ),
            Table(
                fields=['title_gr'],
                table_title=_('Τύποι Θεμάτων Συλλογικού Οργάνου'),
                headers={
                    'title_gr': _('Τίτλος')
                },
                table_id='subject_type',
                order=[[0, 'asc']],
                update_url='subjects:sec_update_subject-type' if can_edit else None,
                create_url='subjects:sec_create_subject-type' if can_edit else None,
                update_buttons=can_edit,
                create_button=can_edit,
                objects=SubjectType.objects.filter(id__in=subjects.values_list("type_id", flat=True)),
                next=self.request.path
            ),
            Table(
                fields=['title_gr'],
                table_title=_('Κατηγορίες Θεμάτων Συλλογικού Οργάνου'),
                headers={
                    'title_gr': _('Τίτλος')
                },
                table_id='subject_category',
                order=[[0, 'asc']],
                update_url='subjects:sec_update_subject-category' if can_edit else None,
                create_url='subjects:sec_create_subject-category' if can_edit else None,
                update_buttons=can_edit,
                create_button=can_edit,
                objects=SubjectCategory.objects.filter(id__in=subjects.values_list("category_id", flat=True)),
                next=self.request.path
            ),
            Table(
                fields=['request_subject', 'description', 'created_at', 'subject', 'applicant', 'subject.decision', 'attachments.download'],
                table_title=_('Αιτήσεις προς το Συλλογικό Όργανο'),
                headers={
                    'request_subject': _('Θέμα Αιτήματος'),
                    'description': _('Περιγραφή'),
                    'created_at': _('Ημ/νία Υποβολής'),
                    'subject': _('Θέμα'),
                    'applicant': _('Αιτών'),
                    'subject.decision': _('Απόφαση'),
                    'attachments.download': _('Επισυναπτόμενα')
                },
                table_id='applications',
                order=[[4, 'asc'], [3, 'asc'], [2, 'asc']],
                update_url='bodyapplications:sec_update_bodyapplication' if can_edit else None,
                update_buttons=can_edit,
                create_button=False,
                objects=Application.objects.filter(subject__in=subjects).distinct(),
                next=self.request.path
            ),
        ]


class SecCollectiveBodyAutoComplete(TitleStrMixin, LoginRequiredMixin, UserPassesTestMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Show only the active collective bodies within the secretariat scope
        scopes = get_secretariat_scope(self.request.user)
        qs = scopes['collective_bodies'].active_now()
        if self.q:
            qs = qs.filter(Q(title_gr__icontains=self.q) | Q(title_en__icontains=self.q))

        return qs.order_by(get_order_by_title())[:10]

    def test_func(self):
        return is_secretariat(self.request.user)


"""
StaffMember Views
"""


@login_required
@user_passes_test(is_staff_member)
def staff_show_collectivebody_via_link(request, token):
    signer = TimestampSigner()
    try:
        unsigned = signer.unsign_object(token, max_age=settings.INVITATION_REFERENCE_MAX_AGE_SECS)
        email = unsigned['email']
        collective_body_pk = unsigned['collective_body_pk']
    except SignatureExpired:
        message = _('Ο σύνδεσμος αυτός έχει λήξει.')
        return render(request, 'accounts/message.html', context={'message': message})
    except BadSignature:
        message = _('O σύνδεσμος δεν είναι σωστός!')
        return render(request, 'accounts/message.html', context={'message': message})

    collective_body = get_object_or_404(CollectiveBody, pk=collective_body_pk)
    staff_member = get_object_or_404(StaffMember, user=request.user)

    if not request.user.is_superuser:
        user_email = request.user.email
        staff_email = staff_member.email

        if email not in [user_email, staff_email]:
            message = _('Ο σύνδεσμος δεν αντιστοιχεί στον λογαριασμό με τον οποίο έχετε συνδεθεί. '
                        'Παρακαλούμε συνδεθείτε με τον σωστό λογαριασμό.')
            return render(request, 'accounts/message.html', context={'message': message})

        # User must be president or participant of the collective body
        is_president = collective_body.president_id == staff_member.pk
        is_participant = collective_body.participants.filter(pk=staff_member.pk).exists()

        if not is_president and not is_participant:
            message = _('Δεν έχετε δικαίωμα πρόσβασης στις πληροφορίες του συγκεκριμένου συλλογικού οργάνου.')
            return render(request, 'accounts/message.html', context={'message': message})

    return redirect('bodies:staff_overview_collectivebody', pk=collective_body_pk)


class StaffListCollectiveBody(StaffMultipleList):
    model = CollectiveBody
    fields = ['title_gr', 'president', 'start_date', 'end_date']
    headers = {
        'title_gr': _('Τίτλος'),
        'president': _('Πρόεδρος'),
        'start_date': _('Ημερομηνία Έναρξης'),
        'end_date': _('Ημερομηνία Λήξης')
    }
    master_headline = _('Συλλογικά Όργανα')
    master_p = _('Παρακάτω ακολουθούν τα συλλογικά όργανα στα οποία συμμετέχετε ή έχετε συμμετάσχει στο παρελθόν...')
    ordering = ['end_date', 'start_date', 'secretariat', 'president', get_order_by_title()]

    def get_queryset(self, current=True):
        staff_member = get_object_or_404(StaffMember, user=self.request.user)

        # Get all collective bodies where the staff member participates either as a regular participant or as president
        queryset = CollectiveBody.objects.filter(Q(participants=staff_member) | Q(president=staff_member)).distinct()
        if current:
            # Current participations: show only active collective bodies that have started and have not ended yet
            queryset = queryset.active_now()
        else:
            # Past/Inactive participations: show collective bodies that have either ended or have been marked inactive.
            # Although inactive collective bodies are more of an administrative/secretariat state
            # and not something the staff member needs to track, they keep access to their historical participation data
            queryset = queryset.inactive_now()

        return queryset.order_by(*self.ordering)

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        fields = ['title_gr', 'president', 'start_date', 'end_date']
        headers = {
            'title_gr': _('Τίτλος'),
            'president': _('Πρόεδρος'),
            'start_date': _('Ημερομηνία Έναρξης'),
            'end_date': _('Ημερομηνία Λήξης')
        }

        self.tables = [
            Table(
                fields=fields,
                table_title=_('Παλαιότερες / Ανενεργές Συμμετοχές'),
                headers=headers,
                table_id='archived_participations',
                order=[[3, 'asc']],
                create_button=False,
                update_buttons=False,
                extra_buttons=True,
                extra_button_class='btn btn-secondary',
                extra_button_icon='info',
                extra_text=_('Πληροφορίες'),
                extra_url='bodies:staff_overview_collectivebody',
                objects=self.get_queryset(current=False),
                next=self.request.path
            ),
            Table(
                fields=fields,
                table_title=_('Τρέχουσες Συμμετοχές'),
                headers=headers,
                table_id='new_participations',
                order=[[3, 'asc']],
                create_button=False,
                update_buttons=False,
                extra_buttons=True,
                extra_button_class='btn btn-secondary',
                extra_button_icon='info',
                extra_text=_('Πληροφορίες'),
                extra_url='bodies:staff_overview_collectivebody',
                objects=self.get_queryset(current=True),
                next=self.request.path
            ),
        ]


class StaffCollectiveBodyOverviewList(StaffMultipleList):
    model = CollectiveBody
    master_headline = _('Στοιχεία Συλλογικού Οργάνου')
    master_p = _('Παρακάτω ακολουθούν κάποιες σημαντικές πληροφορίες για το συλλογικό όργανο...')
    back_url = reverse_lazy('bodies:staff_list_collectivebodies')

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        staff_member = get_object_or_404(StaffMember, user=self.request.user)
        body = get_object_or_404(CollectiveBody, pk=self.kwargs['pk'])

        if (body.president != staff_member) and not (staff_member in body.participants.all()):
            raise PermissionDenied

        if body:
            self.master_headline = _('Στοιχεία Συλλογικού Οργάνου: ') + '%s' % str(body)

        subjects = Subject.objects.filter(collective_body=body).order_by('index')
        self.tables = [
            Table(
                fields=['type', 'category', 'program', 'department', 'school', 'notes', 'attachments'],
                table_title=_('Θέματα Συνεδριάσεων Συλλογικού Οργάνου'),
                headers={
                    'type': _('Τύπος'),
                    'category': _('Κατηγορία'),
                    'program': _('Πρόγραμμα Σπουδών'),
                    'department': _('Τμήμα'),
                    'school': _('Σχολή'),
                    'notes': _('Σημειώσεις'),
                    'attachments': _('Επισυναπτόμενα')
                },
                table_id='subject',
                order=[[0, 'asc']],
                create_button=False,
                update_buttons=False,
                objects=subjects,
                next=self.request.path
            ),
            Table(
                fields=['subject', 'title', 'attachments'],
                table_title=_('Αποφάσεις για τα Θέματα'),
                headers={
                    'subject': _('Θέμα'),
                    'title': _('Τελική Απόφαση'),
                    'attachments': _('Επισυναπτόμενα')
                },
                table_id='decision',
                order=[[0, 'asc'], [1, 'asc']],
                create_button=False,
                update_buttons=False,
                objects=Decision.objects.filter(subject__in=subjects),
                next=self.request.path
            ),
            Table(
                fields=['location', 'date_and_time', 'notes'],
                table_title=_('Συνεδριάσεις Συλλογικού Οργάνου'),
                headers={
                    'location': _('Τοποθεσία'),
                    'date_and_time': _('Ημερομηνία & ώρα'),
                    'notes': _('Σημειώσεις')
                },
                table_id='meeting',
                create_button=False,
                update_buttons=False,
                objects=Meeting.objects.filter(collective_body=body).order_by('index'),
                next=self.request.path
            ),
        ]


"""
Applicant view
"""


class ApplicantListCollectiveBody(ApplicantList):
    model = CollectiveBody
    fields = ['title_gr', 'secretariat']
    headers = {
        'title_gr': _('Τίτλος'),
        'secretariat': _('Γραμματεία')
    }
    table_title = _('Συλλογικά Όργανα')
    ordering = ['secretariat', get_order_by_title()]
    create_button = False
    update_buttons = False
    extra_buttons = True
    extra_text = _('Υποβολή Αιτήματος')
    extra_button_icon = 'forward_to_inbox'
    extra_url = 'bodyapplications:applicant_create_bodyapplication'
    back_url = reverse_lazy('bodyapplications:applicant_list_bodyapplications')

    def get_queryset(self):
        # Return only the currently active collective bodies, because the applicant cannot apply to inactive ones
        return CollectiveBody.objects.active_now()
