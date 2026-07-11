from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET
from rest_framework.reverse import reverse_lazy

from accounts.models import StaffMember
from bodies.models import CollectiveBody
from core import views
from . import forms
from .models import Meeting

"""
Secretariat Subject Views
"""


class SecCreateMeeting(views.ScopedSecCreateView):
    model = Meeting
    template_name = 'meetings/show_object.html'
    form_class = forms.SecMeetingForm
    success_url = 'meetings:sec_list_meetings'
    headline = _('Δημιουργία Συνεδρίασης')
    back_url = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nextIndexUrl'] = reverse_lazy('api:next_meeting_index')

        return context


class SecUpdateMeeting(views.ScopedSecUpdateView):
    model = Meeting
    form_class = forms.SecMeetingForm
    success_url = 'meetings:sec_list_meetings'
    delete_url = 'meetings:sec_delete_meeting'
    confirm_modal = True


class SecListMeeting(views.ScopedSecListView):
    model = Meeting
    fields = ['index', 'present', 'absent', 'collective_body', 'location', 'date_and_time', 'notes']
    headers = {
        'index': _('Θέση'),
        'present': _('Παρών'),
        'absent': _('Απών'),
        'collective_body': _('Συλλογικό Όργανο'),
        'location': _('Τοποθεσία'),
        'date_and_time': _('Ημερομηνία & ώρα'),
        'notes': _('Σημειώσεις')
    }
    table_title = _('Συνεδριάσεις')
    ordering = ['collective_body', 'index']
    create_url = 'meetings:sec_create_meeting'
    update_url = 'meetings:sec_update_meeting'
    back_url = reverse_lazy('bodies:sec_list_collectivebodies')


class SecDeleteMeeting(views.ScopedDeleteView):
    model = Meeting
    success_url = 'meetings:sec_list_meetings'


class StaffListMeeting(views.StaffListView):
    model = Meeting
    fields = ['index', 'collective_body', 'location', 'date_and_time', 'notes']
    headers = {
        'index': _('Θέση'),
        'collective_body': _('Συλλογικό Όργανο'),
        'location': _('Τοποθεσία'),
        'date_and_time': _('Ημερομηνία & ώρα'),
        'notes': _('Σημειώσεις')
    }
    table_title = _('Συνεδριάσεις')
    ordering = ['collective_body', 'index']
    create_button = False
    update_buttons = False
    back_url = reverse_lazy('bodies:staff_list_collectivebodies')

    def get_queryset(self):
        super().get_queryset()
        staff_member = get_object_or_404(StaffMember, user=self.request.user)
        queryset = Meeting.objects.exclude(Q(present=staff_member) | Q(absent=staff_member))
        # queryset = Meeting.objects.filter(body__members=staff_member) LATER WHEN I CREATE THE BODY MODEL

        return queryset
