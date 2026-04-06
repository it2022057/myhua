from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q

from accounts.checks import is_secretariat
from core.utils import get_order_by_title
from scopes.utils import get_secretariat_scope


# Create your views here.


"""
Curricula AutoComplete forms
"""


class SecProgramAutoComplete(LoginRequiredMixin, UserPassesTestMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        from curricula.models import StudyProgram

        qs = StudyProgram.objects.all()
        if self.q:
            qs = qs.filter(Q(title_gr__icontains=self.q) | Q(title_en__icontains=self.q))

        return qs.order_by(get_order_by_title())[:10]

    def test_func(self):
        return is_secretariat(self.request.user)


class SecDepartmentAutoComplete(SecProgramAutoComplete):
    def get_queryset(self):
        from curricula.models import Department

        qs = Department.objects.all()
        if self.q:
            qs = qs.filter(Q(title_gr__icontains=self.q) | Q(title_en__icontains=self.q))

        return qs.order_by(get_order_by_title())[:10]


class SecSchoolAutoComplete(SecProgramAutoComplete):
    def get_queryset(self):
        from curricula.models import School

        qs = School.objects.all()
        if self.q:
            qs = qs.filter(Q(title_gr__icontains=self.q) | Q(title_en__icontains=self.q))

        return qs.order_by(get_order_by_title())[:10]
