from dal import autocomplete
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from accounts.checks import is_secretariat
from core import views
from core.utils import get_order_by_title
from scopes.utils import get_secretariat_scope
from subjects.models import Subject, SubjectType, SubjectCategory, Decision
from . import forms

# Create your views here.

"""
Generic Subjects Views
"""

class SecCreate(views.ScopedSecCreateView):
    template_name = 'subjects/show_object.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class SecUpdate(views.ScopedSecUpdateView):
    template_name = 'subjects/show_object.html'

    # def form_valid(self, form):
    #     form.instance.updated_by = self.request.user
    #     return super().form_valid(form)


class SecList(views.ScopedSecListView):
    template_name = 'subjects/list_objects.html'


class SecMultipleList(views.SecMultipleListView):
    template_name = 'subjects/list_objects.html'


class SecDelete(views.ScopedDeleteView):
    template_name = 'subjects/show_object.html'


"""
Secretariat Subject Views
"""


class SecCreateSubject(SecCreate):
    model = Subject
    form_class = forms.SecSubjectForm
    success_url = 'subjects:sec_list_subject'
    headline = _('Δημιουργία Θέματος')
    back_url = ''


class SecUpdateSubject(SecUpdate):
    model = Subject
    form_class = forms.SecSubjectForm
    success_url = 'subjects:sec_list_subject'
    delete_url = 'subjects:sec_delete_subject'
    confirm_modal = True


class SecListSubject(SecList):
    model = Subject
    fields = ['index', 'type', 'category', 'collective_body', 'notes']
    headers = {
        'index': _('Δείκτης'),
        'type': _('Τύπος'),
        'category': _('Κατηγορία'),
        'collective_body': _('Συλλογικό Όργανο'),
        'notes': _('Σημειώσεις'),
    }
    table_title = _('Θέματα')
    create_url = 'subjects:sec_create_subject'
    update_url = 'subjects:sec_update_subject'


# class StaffStudentOverviewList(StaffMultipleList):
#     model = Student
#     template_name = 'phdstuds/multiple_tables.html'
#     master_headline = _('Στοιχεία Διδακτορικής Διατριβής')
#
#     def test_func(self):
#         return is_staff_member(self.request.user)
#
#     def setup(self, *args, **kwargs):
#         super().setup(*args, **kwargs)
#         staff_member = get_object_or_404(StaffMember, user=self.request.user)
#         phd_thesis = get_object_or_404(PhdThesis, pk=self.kwargs['pk'])
#         if (phd_thesis.supervisor != staff_member) and not (staff_member in phd_thesis.committee.all()):
#             raise PermissionDenied
#
#         create_new_recommendation = (phd_thesis.supervisor == staff_member)
#
#         student = phd_thesis.candidate
#         self.master_p = _('Υποψήφιος Διδάκτορας: ') + '%s %s' % (student.surname, student.given_name)
#         self.tables = [
#             Table(
#                 fields=['thesis', 'year'],
#                 table_title=_('Αναφορές Διδακτορικής Διατριβής'),
#                 headers={
#                     'thesis': _('Θέμα'),
#                     'year': _('Έτος'),
#                 },
#                 table_id='progress',
#                 create_button=False,
#                 update_url='phdstuds:staff_update_progress',
#                 update_button_icon='info',
#                 update_text=_('Λεπτομέρειες'),
#                 objects=ThesisProgress.objects.filter(thesis__candidate=student),
#                 next=self.request.path,
#             ),
#             Table(
#                 fields=['thesis', 'year'],
#                 table_title=_('Εισηγήσεις Επιβλέποντα'),
#                 headers={
#                     'thesis': _('Θέμα'),
#                     'year': _('Έτος'),
#                 },
#                 table_id='recommendations',
#                 update_url='phdstuds:staff_update_recommendation',
#                 update_button_icon='info',
#                 update_text=_('Λεπτομέρειες'),
#                 create_button=create_new_recommendation,
#                 create_url=reverse_lazy('phdstuds:staff_create_recommendation', kwargs={'pk': phd_thesis.pk}),
#                 create_text='Νέα εισήγηση',
#                 objects=Recommendation.objects.filter(thesis__candidate=student),
#                 next=self.request.path,
#             ),
#             Table(
#                 fields=['title', 'journal_title', 'year'],
#                 table_title=_('Δημοσιεύσεις σε Περιοδικά'),
#                 headers={
#                     'title': _('Τίτλος'),
#                     'journal_title': _('Περιοδικό'),
#                     'year': _('Έτος'),
#                 },
#                 table_id='journals',
#                 create_button=False,
#                 update_button_icon='info',
#                 update_text=_('Λεπτομέρειες'),
#                 update_url='phdstuds:staff_update_journal',
#                 objects=JournalPublication.objects.filter(thesis__candidate=student),
#                 next=self.request.path,
#             ),
#             Table(
#                 fields=['title', 'conference_title', 'year'],
#                 table_title=_('Δημοσιεύσεις σε Συνέδρια'),
#                 headers={
#                     'title': _('Τίτλος'),
#                     'conference_title': _('Συνέδριο'),
#                     'year': _('Έτος'),
#                 },
#                 table_id='conferences',
#                 create_button=False,
#                 update_url='phdstuds:staff_update_conference',
#                 update_button_icon='info',
#                 update_text=_('Λεπτομέρειες'),
#                 objects=ConferencePublication.objects.filter(thesis__candidate=student),
#                 next=self.request.path,
#             ),
#             Table(
#                 fields=['year', 'course_name', 'faculty'],
#                 headers={
#                     'year': _('Έτος'),
#                     'course_name': _('Μάθημα'),
#                     'faculty': _('Υπεύθυνος Καθηγητής'),
#                 },
#                 table_title=_('Επικουρικό Διδακτικό Έργο'),
#                 update_url='phdstuds:staff_update_teachingtask',
#                 create_button=False,
#                 objects=TeachingTask.objects.filter(thesis__candidate=student),
#                 next=self.request.path,
#             )
#         ]


class SecDeleteSubject(SecDelete):
    model = Subject
    success_url = 'subjects:sec_list_subject'


"""
Secretariat SubjectType Views
"""


class SecCreateSubjectType(SecCreate):
    model = SubjectType
    form_class = forms.SecSubjectTypeForm
    success_url = 'subjects:sec_list_subject-type'
    headline = _('Δημιουργία Τύπου Θέματος')
    back_url = ''


class SecUpdateSubjectType(SecUpdate):
    model = SubjectType
    form_class = forms.SecSubjectTypeForm
    success_url = 'subjects:sec_list_subject-type'
    delete_url = 'subjects:sec_delete_subject-type'
    confirm_modal = True


class SecListSubjectType(SecList):
    model = SubjectType
    fields = ['title_gr']
    headers = {
        'title_gr': _('Τίτλος')
    }
    table_title = _('Τύποι Θεμάτων')
    create_url = 'subjects:sec_create_subject-type'
    update_url = 'subjects:sec_update_subject-type'


class SecDeleteSubjectType(SecDelete):
    model = SubjectType
    success_url = 'subjects:sec_list_subject-type'


"""
Secretariat SubjectCategory Views
"""


class SecCreateSubjectCategory(SecCreate):
    model = SubjectCategory
    form_class = forms.SecSubjectCategoryForm
    success_url = 'subjects:sec_list_subject-category'
    headline = _('Δημιουργία Κατηγορίας Θέματος')
    back_url = ''


class SecUpdateSubjectCategory(SecUpdate):
    model = SubjectCategory
    form_class = forms.SecSubjectCategoryForm
    success_url = 'subjects:sec_list_subject-category'
    delete_url = 'subjects:sec_delete_subject-category'
    confirm_modal = True


class SecListSubjectCategory(SecList):
    model = SubjectCategory
    fields = ['title_gr']
    headers = {
        'title_gr': _('Τίτλος')
    }
    table_title = _('Κατηγορίες Θεμάτων')
    create_url = 'subjects:sec_create_subject-category'
    update_url = 'subjects:sec_update_subject-category'


class SecDeleteSubjectCategory(SecDelete):
    model = SubjectCategory
    success_url = 'subjects:sec_list_subject-category'


"""
Secretariat Decision Views
"""


class SecCreateDecision(SecCreate):
    model = Decision
    form_class = forms.SecDecisionForm
    success_url = 'subjects:sec_list_decision'
    headline = _('Δημιουργία Απόφασης')
    back_url = ''


class SecUpdateDecision(SecUpdate):
    model = Decision
    form_class = forms.SecDecisionForm
    success_url = 'subjects:sec_list_decision'
    delete_url = 'subjects:sec_delete_decision'
    confirm_modal = True


class SecListDecision(SecList):
    model = Decision
    fields = ['title_gr', 'subject']
    headers = {
        'title_gr': _('Τίτλος'),
        'subject': _('Θέμα')
    }
    table_title = _('Αποφάσεις')
    create_url = 'subjects:sec_create_decision'
    update_url = 'subjects:sec_update_decision'


class SecDeleteDecision(SecDelete):
    model = Decision
    success_url = 'subjects:sec_list_decision'


"""
Subject AutoComplete forms
"""


class SecSubjectAutoComplete(LoginRequiredMixin, UserPassesTestMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        scopes = get_secretariat_scope(self.request.user)
        qs = scopes['collective_bodies']

        if self.q:
            qs = qs.filter(Q(title_gr__icontains=self.q) | Q(title_en__icontains=self.q))

        return qs.order_by(get_order_by_title())[:10]

    def test_func(self):
        return is_secretariat(self.request.user)


class SecSubjectTypeAutoComplete(SecSubjectAutoComplete):
    def get_queryset(self):
        qs = SubjectType.objects.all()

        if self.q:
            qs = qs.filter(Q(title_gr__icontains=self.q) | Q(title_en__icontains=self.q))

        return qs.order_by(get_order_by_title())[:10]


class SecSubjectCategoryAutoComplete(SecSubjectAutoComplete):
    def get_queryset(self):
        qs = SubjectCategory.objects.all()

        if self.q:
            qs = qs.filter(Q(title_gr__icontains=self.q) | Q(title_en__icontains=self.q))

        return qs.order_by(get_order_by_title())[:10]

