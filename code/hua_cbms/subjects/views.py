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

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


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


class SecDeleteSubject(SecDelete):
    model = Subject
    success_url = 'subjects:sec_list_subject'


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

