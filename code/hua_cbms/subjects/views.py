from dal import autocomplete
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from accounts.checks import is_secretariat
from core import views
from scopes.utils import get_secretariat_scope
from . import forms
from subjects.models import Subject, SubjectType, SubjectCategory

# Create your views here.

"""
Generic subjects Views
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
Subject AutoComplete forms
"""


class SecSubjectTypeAutoComplete(LoginRequiredMixin, UserPassesTestMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = SubjectType.objects.all()

        if self.q:
            qs = qs.filter(Q(title_gr__contains=self.q) | Q(title_en__contains=self.q))

        return qs[:10]

    def test_func(self):
        return is_secretariat(self.request.user)


class SecSubjectCategoryAutoComplete(SecSubjectTypeAutoComplete):
    def get_queryset(self):
        qs = SubjectCategory.objects.all()

        if self.q:
            qs = qs.filter(Q(title_gr__contains=self.q) | Q(title_en__contains=self.q))

        return qs[:10]


# class SecSubjectAutoComplete(LoginRequiredMixin, UserPassesTestMixin, autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         scopes = get_secretariat_scope(self.request.user)
#         doctoral_progs = scopes['programs'].filter(type=StudyProgram.DOCTORAL)
#         if self.q:
#             qs = PhdThesis.objects.filter(Q(subject_gr__contains=self.q) | Q(subject_en__contains=self.q) | Q(
#                 candidate__surname__contains=self.q),
#                                           candidate__program__in=doctoral_progs)
#
#         return qs[:10]
#
#     def test_func(self):
#         return is_secreteriat(self.request.user)

# class SecScopedPhDStudentAutoComplete(LoginRequiredMixin, UserPassesTestMixin, autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         from curricula.models import StudyProgram
#         scopes = get_secreteriat_scope(self.request.user)
#         doctoral_progs = scopes['programs'].filter(type=StudyProgram.DOCTORAL)
#         if self.q:
#             qs = Student.objects.filter(display_name__contains=self.q, program__in=doctoral_progs)
#         return qs[:10]
#
#     def test_func(self):
#         return is_secreteriat(self.request.user)
#
#
# class StaffMemberAutocomplete(LoginRequiredMixin, UserPassesTestMixin, autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         if self.q:
#             qs = StaffMember.objects.filter(display_name__contains=self.q) | StaffMember.objects.filter(
#                 display_name_en__contains=self.q)
#         return qs[:10]
#
#     def test_func(self):
#         return is_staff_member(self.request.user) or is_secreteriat(self.request.user) or is_student(self.request.user)
#
#
# class UserAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         User = get_user_model()
#         qs = User.objects.all()
#         if self.q:
#             qs = qs.filter(display_name__contains=self.q)
#
#         return qs[:10]
#
#
# class StudentAutocomplete(UserPassesTestMixin, LoginRequiredMixin, autocomplete.Select2QuerySetView):
#
#     def test_func(self):
#         return is_secreteriat(self.request.user) or is_staff_member(self.request.user)
#
#     def get_queryset(self):
#         if self.q:
#             q = str(self.q)
#             if len(q) >= 3:
#                 qs = Student.objects.filter(display_name__contains=q) | Student.objects.filter(reg_num__contains=q)
#                 return qs[:10]

    # def get_list(self):
    #     entries = sis.estudiesdb().filter_students(self.q)
    #     if not entries:
    #         return []
    #     else:
    #         return [ [ e['UserName'], e['SurName'] + ' ' + e['FirstName'] + ' (' + e['UserName'] + ')' ] for e in entries ]