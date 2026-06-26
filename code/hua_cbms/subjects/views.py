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

"""
Secretariat Subject Views
"""


class SecCreateSubject(views.ScopedSecCreateView):
    model = Subject
    form_class = forms.SecSubjectForm
    success_url = 'subjects:sec_list_subjects'
    headline = _('Δημιουργία Θέματος')
    back_url = ''


class SecUpdateSubject(views.ScopedSecUpdateView):
    model = Subject
    form_class = forms.SecSubjectForm
    success_url = 'subjects:sec_list_subjects'
    delete_url = 'subjects:sec_delete_subject'
    confirm_modal = True


class SecListSubject(views.ScopedSecListView):
    model = Subject
    fields = ['index', 'type', 'category', 'collective_body', 'notes']
    headers = {
        'index': _('Θέση'),
        'type': _('Τύπος'),
        'category': _('Κατηγορία'),
        'collective_body': _('Συλλογικό Όργανο'),
        'notes': _('Σημειώσεις'),
    }
    table_title = _('Θέματα')
    create_url = 'subjects:sec_create_subject'
    update_url = 'subjects:sec_update_subject'


class SecDeleteSubject(views.ScopedDeleteView):
    model = Subject
    success_url = 'subjects:sec_list_subjects'


"""
Secretariat SubjectType Views
"""


class SecCreateSubjectType(views.ScopedSecCreateView):
    model = SubjectType
    form_class = forms.SecSubjectTypeForm
    success_url = 'subjects:sec_list_subject-types'
    headline = _('Δημιουργία Τύπου Θέματος')
    back_url = ''


class SecUpdateSubjectType(views.ScopedSecUpdateView):
    model = SubjectType
    form_class = forms.SecSubjectTypeForm
    success_url = 'subjects:sec_list_subject-types'
    delete_url = 'subjects:sec_delete_subject-type'
    confirm_modal = True


class SecListSubjectType(views.ScopedSecListView):
    model = SubjectType
    fields = ['title_gr']
    headers = {
        'title_gr': _('Τίτλος')
    }
    table_title = _('Τύποι Θεμάτων')
    create_url = 'subjects:sec_create_subject-type'
    update_url = 'subjects:sec_update_subject-type'


class SecDeleteSubjectType(views.ScopedDeleteView):
    model = SubjectType
    success_url = 'subjects:sec_list_subject-types'


"""
Secretariat SubjectCategory Views
"""


class SecCreateSubjectCategory(views.ScopedSecCreateView):
    model = SubjectCategory
    form_class = forms.SecSubjectCategoryForm
    success_url = 'subjects:sec_list_subject-categories'
    headline = _('Δημιουργία Κατηγορίας Θέματος')
    back_url = ''


class SecUpdateSubjectCategory(views.ScopedSecUpdateView):
    model = SubjectCategory
    form_class = forms.SecSubjectCategoryForm
    success_url = 'subjects:sec_list_subject-categories'
    delete_url = 'subjects:sec_delete_subject-category'
    confirm_modal = True


class SecListSubjectCategory(views.ScopedSecListView):
    model = SubjectCategory
    fields = ['title_gr']
    headers = {
        'title_gr': _('Τίτλος')
    }
    table_title = _('Κατηγορίες Θεμάτων')
    create_url = 'subjects:sec_create_subject-category'
    update_url = 'subjects:sec_update_subject-category'


class SecDeleteSubjectCategory(views.ScopedDeleteView):
    model = SubjectCategory
    success_url = 'subjects:sec_list_subject-categories'


"""
Secretariat Decision Views
"""


class SecCreateDecision(views.ScopedSecCreateView):
    model = Decision
    form_class = forms.SecDecisionForm
    success_url = 'subjects:sec_list_decisions'
    headline = _('Δημιουργία Απόφασης')
    back_url = ''


class SecUpdateDecision(views.ScopedSecUpdateView):
    model = Decision
    form_class = forms.SecDecisionForm
    success_url = 'subjects:sec_list_decisions'
    delete_url = 'subjects:sec_delete_decision'
    confirm_modal = True


class SecListDecision(views.ScopedSecListView):
    model = Decision
    fields = ['subject', 'title_gr'],
    headers = {
        'subject': _('Θέμα'),
        'title_gr': _('Τελική Απόφαση')
    },
    table_title = _('Αποφάσεις')
    create_url = 'subjects:sec_create_decision'
    update_url = 'subjects:sec_update_decision'


class SecDeleteDecision(views.ScopedDeleteView):
    model = Decision
    success_url = 'subjects:sec_list_decisions'


"""
Staff Subject and Decision Views
"""


class StaffListSubject(views.StaffListView):
    model = Subject
    fields = ['index', 'type', 'category', 'program', 'department', 'school', 'notes']
    headers = {
        'index': _('Θέση'),
        'type': _('Τύπος'),
        'category': _('Κατηγορία'),
        'program': _('Πρόγραμμα Σπουδών'),
        'department': _('Τμήμα'),
        'school': _('Σχολή'),
        'notes': _('Σημειώσεις')
    }
    table_title = _('Θέματα')
    create_url = False
    update_url = False


class StaffListDecision(views.StaffListView):
    model = Decision
    fields = ['subject', 'title_gr'],
    headers = {
        'subject': _('Θέμα'),
        'title_gr': _('Τελική Απόφαση')
    },
    table_title = _('Αποφάσεις')
    create_url = False
    update_url = False


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
