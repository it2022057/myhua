from dal import autocomplete
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from accounts.checks import is_secretariat
from core import views
from core.models import AttachmentFormSetMixin
from core.utils import get_order_by_title
from scopes.utils import get_secretariat_scope
from subjects.models import Subject, SubjectType, SubjectCategory, Decision
from . import forms
from attachments.formsets import SubjectAttachmentFormSet, DecisionAttachmentFormSet

"""
Secretariat CRUD Subject views
"""


class SecCreateSubject(AttachmentFormSetMixin, views.ScopedSecCreateView):
    model = Subject
    template_name = 'subjects/show_object.html'
    form_class = forms.SecSubjectForm
    success_url = 'subjects:sec_list_subjects'
    headline = _('Δημιουργία Θέματος')
    back_url = ''
    success_message = _('Το θέμα καταχωρήθηκε επιτυχώς.')
    attachment_formset_class = SubjectAttachmentFormSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the API endpoint for retrieving the next subject index
        context['nextIndexUrl'] = reverse_lazy('api:next_subject_index')

        return context

    def get_attachment_form_kwargs(self):
        return {'user': self.request.user}


class SecUpdateSubject(AttachmentFormSetMixin, views.ScopedSecUpdateView):
    model = Subject
    template_name = 'subjects/show_object.html'
    form_class = forms.SecSubjectForm
    success_url = 'subjects:sec_list_subjects'
    delete_url = 'subjects:sec_delete_subject'
    confirm_modal = True
    success_message = _('Το θέμα ενημερώθηκε επιτυχώς.')
    attachment_formset_class = SubjectAttachmentFormSet

    def get_attachment_form_kwargs(self):
        return {'user': self.request.user}


class SecListSubject(views.ScopedSecListView):
    model = Subject
    fields = ['index', 'collective_body', 'type', 'category', 'program', 'department', 'school', 'notes', 'attachments.download']
    headers = {
        'index': _('Θέση'),
        'collective_body': _('Συλλογικό Όργανο'),
        'type': _('Τύπος'),
        'category': _('Κατηγορία'),
        'program': _('Πρόγραμμα Σπουδών'),
        'department': _('Τμήμα'),
        'school': _('Σχολή'),
        'notes': _('Σημειώσεις'),
        'attachments.download': _('Επισυναπτόμενα')
    }
    table_title = _('Θέματα')
    ordering = ['type', 'category']
    create_url = 'subjects:sec_create_subject'
    update_url = 'subjects:sec_update_subject'
    back_url = reverse_lazy('bodies:sec_list_collectivebodies')

class SecDeleteSubject(views.ScopedDeleteView):
    model = Subject
    success_url = 'subjects:sec_list_subjects'
    success_message = _('Το θέμα διαγράφηκε.')


"""
Secretariat CRUD SubjectType Views
"""


class SecCreateSubjectType(views.ScopedSecCreateView):
    model = SubjectType
    form_class = forms.SecSubjectTypeForm
    success_url = 'subjects:sec_list_subject-types'
    headline = _('Δημιουργία Τύπου Θέματος')
    back_url = ''
    success_message = _('Ο τύπος θέματος καταχωρήθηκε επιτυχώς.')


class SecUpdateSubjectType(views.ScopedSecUpdateView):
    model = SubjectType
    form_class = forms.SecSubjectTypeForm
    success_url = 'subjects:sec_list_subject-types'
    delete_url = 'subjects:sec_delete_subject-type'
    confirm_modal = True
    success_message = _('Ο τύπος θέματος καταχωρήθηκε επιτυχώς.')


class SecListSubjectType(views.ScopedSecListView):
    model = SubjectType
    fields = ['title_gr']
    headers = {
        'title_gr': _('Τίτλος')
    }
    table_title = _('Τύποι Θεμάτων')
    ordering = get_order_by_title()
    create_url = 'subjects:sec_create_subject-type'
    update_url = 'subjects:sec_update_subject-type'
    back_url = reverse_lazy('bodies:sec_list_collectivebodies')
    success_message = _('Ο τύπος θέματος ενημερώθηκε επιτυχώς.')


class SecDeleteSubjectType(views.ScopedDeleteView):
    model = SubjectType
    success_url = 'subjects:sec_list_subject-types'
    success_message = _('Ο τύπος θέματος διαγράφηκε.')


"""
Secretariat CRUD SubjectCategory Views
"""


class SecCreateSubjectCategory(views.ScopedSecCreateView):
    model = SubjectCategory
    form_class = forms.SecSubjectCategoryForm
    success_url = 'subjects:sec_list_subject-categories'
    headline = _('Δημιουργία Κατηγορίας Θέματος')
    back_url = ''
    success_message = _('Η κατηγορία θέματος καταχωρήθηκε επιτυχώς.')


class SecUpdateSubjectCategory(views.ScopedSecUpdateView):
    model = SubjectCategory
    form_class = forms.SecSubjectCategoryForm
    success_url = 'subjects:sec_list_subject-categories'
    delete_url = 'subjects:sec_delete_subject-category'
    confirm_modal = True
    success_message = _('Η κατηγορία θέματος ενημερώθηκε επιτυχώς.')


class SecListSubjectCategory(views.ScopedSecListView):
    model = SubjectCategory
    fields = ['title_gr']
    headers = {
        'title_gr': _('Τίτλος')
    }
    table_title = _('Κατηγορίες Θεμάτων')
    ordering = get_order_by_title()
    create_url = 'subjects:sec_create_subject-category'
    update_url = 'subjects:sec_update_subject-category'
    back_url = reverse_lazy('bodies:sec_list_collectivebodies')


class SecDeleteSubjectCategory(views.ScopedDeleteView):
    model = SubjectCategory
    success_url = 'subjects:sec_list_subject-categories'
    success_message = _('Η κατηγορία θέματος διαγράφηκε.')


"""
Secretariat CRUD Decision Views
"""


class SecCreateDecision(AttachmentFormSetMixin, views.ScopedSecCreateView):
    model = Decision
    template_name = 'subjects/show_object.html'
    form_class = forms.SecDecisionForm
    success_url = 'subjects:sec_list_decisions'
    headline = _('Δημιουργία Απόφασης')
    back_url = ''
    success_message = _('Η απόφαση καταχωρήθηκε επιτυχώς.')
    attachment_formset_class = DecisionAttachmentFormSet

    def get_attachment_form_kwargs(self):
        return {'user': self.request.user}


class SecUpdateDecision(AttachmentFormSetMixin, views.ScopedSecUpdateView):
    model = Decision
    template_name = 'subjects/show_object.html'
    form_class = forms.SecDecisionForm
    success_url = 'subjects:sec_list_decisions'
    delete_url = 'subjects:sec_delete_decision'
    confirm_modal = True
    success_message = _('Η απόφαση ενημερώθηκε επιτυχώς.')
    attachment_formset_class = DecisionAttachmentFormSet

    def get_attachment_form_kwargs(self):
        return {'user': self.request.user}


class SecListDecision(views.ScopedSecListView):
    model = Decision
    fields = ['subject', 'title', 'attachments.download']
    headers = {
        'subject': _('Θέμα'),
        'title': _('Τελική Απόφαση'),
        'attachments.download': _('Επισυναπτόμενα')
    }
    table_title = _('Αποφάσεις')
    ordering = ['subject', 'title']
    create_url = 'subjects:sec_create_decision'
    update_url = 'subjects:sec_update_decision'
    back_url = reverse_lazy('bodies:sec_list_collectivebodies')


class SecDeleteDecision(views.ScopedDeleteView):
    model = Decision
    success_url = 'subjects:sec_list_decisions'
    success_message = _('Η απόφαση διαγράφηκε.')


"""
StaffMember Subject and Decision Views
"""


class StaffListSubject(views.StaffListView):
    model = Subject
    fields = ['collective_body', 'type', 'category', 'notes', 'attachments.download']
    headers = {
        'collective_body': _('Συλλογικό Όργανο'),
        'type': _('Τύπος'),
        'category': _('Κατηγορία'),
        'notes': _('Σημειώσεις'),
        'attachments.download': _('Επισυναπτόμενα')
    }
    table_title = _('Θέματα')
    ordering = ['collective_body', 'type', 'category']
    create_button = False
    update_buttons = False
    back_url = reverse_lazy('bodies:staff_list_collectivebodies')


class StaffListDecision(views.StaffListView):
    model = Decision
    fields = ['subject', 'title', 'attachments.download']
    headers = {
        'subject': _('Θέμα'),
        'title': _('Τελική Απόφαση'),
        'attachments.download': _('Επισυναπτόμενα')
    }
    table_title = _('Αποφάσεις')
    ordering = ['subject', 'title']
    create_button = False
    update_buttons = False
    back_url = reverse_lazy('bodies:staff_list_collectivebodies')


"""
Subject AutoComplete forms
"""


class SecSubjectAutoComplete(LoginRequiredMixin, UserPassesTestMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Get the subjects within the secretariat scope
        scopes = get_secretariat_scope(self.request.user)
        qs = Subject.objects.filter(collective_body__in=scopes['collective_bodies'])

        if self.q:
            qs = qs.filter(
                Q(type__title_gr__icontains=self.q) |
                Q(type__title_en__icontains=self.q) |
                Q(category__title_gr__icontains=self.q) |
                Q(category__title_en__icontains=self.q)
            )

        return qs.order_by('collective_body', 'index')[:10]

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
