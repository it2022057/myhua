from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.checks import is_secretariat
from accounts.models import StaffMember
from bodies import forms
from bodies.models import CollectiveBody
from core import views
from core.models import TitleStrMixin
from core.utils import get_order_by_title
from core.views import Table
from scopes.models import Secretariat
from scopes.utils import get_secretariat_scope
from subjects.models import Subject, Decision, SubjectType, SubjectCategory

"""
Generic CollectiveBody Views
"""


class SecCreate(views.ScopedSecCreateView):
    template_name = 'bodies/show_object.html'


class SecUpdate(views.ScopedSecUpdateView):
    template_name = 'bodies/show_object.html'


class SecList(views.ScopedSecListView):
    template_name = 'bodies/list_objects.html'


class SecMultipleList(views.SecMultipleListView):
    template_name = 'bodies/multiple_tables.html'


class SecDelete(views.ScopedDeleteView):
    template_name = 'bodies/show_object.html'


class StaffCreate(views.StaffCreateView):
    template_name = 'bodies/show_object.html'


class StaffUpdate(views.StaffUpdateView):
    template_name = 'bodies/show_object.html'


class StaffList(views.StaffListView):
    template_name = 'bodies/list_objects.html'


class StaffMultipleList(views.StaffMultipleListView):
    template_name = 'core/multiple_tables.html'


"""
Secretariat Views
"""


class SecCreateCollectiveBody(SecCreate):
    model = CollectiveBody
    form_class = forms.SecCollectiveBodyForm
    success_url = 'bodies:sec_list_collectivebodies'
    headline = _('Δημιουργία Συλλογικού Πανεπιστημιακού Οργάνου')
    back_url = ''


class SecUpdateCollectiveBody(SecUpdate):
    model = CollectiveBody
    form_class = forms.SecCollectiveBodyForm
    success_url = 'bodies:sec_list_collectivebodies'
    delete_url = 'bodies:sec_delete_collectivebody'
    confirm_modal = True


class SecListCollectiveBody(SecList):
    model = CollectiveBody
    fields = ['title_gr', 'president', 'secretariat', 'start_date', 'end_date']
    headers = {
        'title_gr': _('Τίτλος'),
        'participants': _('Συμμετέχοντες'),
        'president': _('Πρόεδρος'),
        'secretariat': _('Γραμματεία'),
        'start_date': _('Ημερομηνία Έναρξης'),
        'end_date': _('Ημερομηνία Λήξης')
    }
    table_title = _('Συλλογικά Όργανα')
    ordering = ['end_date', 'start_date', 'president', get_order_by_title()]
    create_url = 'bodies:sec_create_collectivebody'
    update_url = 'bodies:sec_update_collectivebody'
    extra_buttons = True
    extra_text = _('Συμμετέχοντες')
    extra_button_icon = 'people'
    extra_url = 'accounts:sec_list_participants'
    extra_buttons2 = True
    extra_button_icon2 = 'history'
    extra_text2 = _('Δράσεις')
    extra_url2 = 'bodies:sec_overview_collectivebody'


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

        subjects = Subject.objects.filter(collective_body=body)
        self.tables = [
            Table(
                fields=['index', 'type', 'category', 'applicant_user', 'program', 'department', 'school', 'notes'],
                table_title=_('Θέματα Συνεδριάσεων Συλλογικού Οργάνου'),
                headers={
                    'index': _('Θέση'),
                    'type': _('Τύπος'),
                    'category': _('Κατηγορία'),
                    'applicant_user': _('Αιτών'),
                    'program': _('Πρόγραμμα Σπουδών'),
                    'department': _('Τμήμα'),
                    'school': _('Σχολή'),
                    'notes': _('Σημειώσεις')
                },
                table_id='subject',
                order=[[0, 'asc']],
                update_url='subjects:sec_update_subject',
                create_url='subjects:sec_create_subject',
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
                ),
                update_text=_('Ενημέρωση λίστας'),
                create_url='accounts:sec_create_staff_member',
                objects=body.participants.all(),
                next=self.request.path
            ),
            Table(
                fields=['subject', 'title_gr'],
                table_title=_('Αποφάσεις για τα Θέματα'),
                headers={
                    'subject': _('Θέμα'),
                    'title_gr': _('Τελική Απόφαση')
                },
                table_id='decision',
                order=[[0, 'asc'], [1, 'asc']],
                update_url='subjects:sec_update_decision',
                create_url='subjects:sec_create_decision',
                objects=Decision.objects.filter(subject__in=subjects),
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
                update_url='subjects:sec_update_subject-type',
                create_url='subjects:sec_create_subject-type',
                objects=SubjectType.objects.filter(id__in=subjects.values_list("type_id", flat=True)),
                next=self.request.path
            ),
            Table(
                fields=['title_gr', 'conference_title', 'year'],
                table_title=_('Κατηγορίες Θεμάτων Συλλογικού Οργάνου'),
                headers={
                    'title_gr': _('Τίτλος')
                },
                table_id='subject_category',
                order=[[0, 'asc']],
                update_url='subjects:sec_update_subject-category',
                create_url='subjects:sec_create_subject-category',
                objects=SubjectCategory.objects.filter(id__in=subjects.values_list("category_id", flat=True)),
                next=self.request.path
            ),
        ]


class SecCollectiveBodyAutoComplete(TitleStrMixin, LoginRequiredMixin, UserPassesTestMixin,
                                    autocomplete.Select2QuerySetView):
    def get_queryset(self):
        scopes = get_secretariat_scope(self.request.user)
        qs = scopes['collective_bodies']
        if self.q:
            qs = qs.filter(Q(title_gr__icontains=self.q) | Q(title_en__icontains=self.q))

        return qs.order_by(get_order_by_title())[:10]

    def test_func(self):
        return is_secretariat(self.request.user)


"""
Staff Student Views
"""


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
    ordering = ['end_date', 'start_date', 'president', get_order_by_title()]

    def get_queryset(self, current=True):
        queryset = super().get_queryset()
        staff_member = get_object_or_404(StaffMember, user=self.request.user)
        today = timezone.now()

        queryset = CollectiveBody.objects.filter(participants=staff_member)
        if current:
            queryset = queryset.filter(end_date__gte=today)
        else:
            queryset = queryset.filter(end_date__lt=today)

        return queryset

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
                table_title=_('Παλιές Συμμετοχές'),
                headers=headers,
                table_id='old_participations',
                create_button=False,
                update_buttons=False,
                extra_buttons=True,
                extra_button_class='btn btn-secondary',
                extra_button_icon='info',
                extra_text=_('Δράσεις'),
                extra_url='bodies:staff_overview_collectivebody',
                objects=self.get_queryset(current=False),
                next=self.request.path
            ),
            Table(
                fields=fields,
                table_title=_('Τρέχουσες Συμμετοχές'),
                headers=headers,
                table_id='new_participations',
                create_button=False,
                update_buttons=False,
                extra_buttons=True,
                extra_button_class='btn btn-secondary',
                extra_button_icon='info',
                extra_text=_('Δράσεις'),
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

        subjects = Subject.objects.filter(collective_body=body)
        self.tables = [
            Table(
                fields=['index', 'type', 'category', 'program', 'department', 'school', 'notes'],
                table_title=_('Θέματα Συνεδριάσεων Συλλογικού Οργάνου'),
                headers={
                    'index': _('Θέση'),
                    'type': _('Τύπος'),
                    'category': _('Κατηγορία'),
                    'program': _('Πρόγραμμα Σπουδών'),
                    'department': _('Τμήμα'),
                    'school': _('Σχολή'),
                    'notes': _('Σημειώσεις'),
                },
                table_id='subject',
                order=[[0, 'asc']],
                create_button=False,
                update_buttons=False,
                objects=subjects,
                next=self.request.path
            ),
            Table(
                fields=['subject', 'title_gr'],
                table_title=_('Αποφάσεις για τα Θέματα'),
                headers={
                    'subject': _('Θέμα'),
                    'title_gr': _('Τελική Απόφαση')
                },
                table_id='decision',
                order=[[0, 'asc'], [1, 'asc']],
                create_button=False,
                update_buttons=False,
                objects=Decision.objects.filter(subject__in=subjects),
                next=self.request.path
            ),
        ]
