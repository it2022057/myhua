from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse_lazy

from accounts.checks import is_secretariat
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
    success_message = _('Η συνεδρίαση καταχωρήθηκε επιτυχώς.')

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
    success_message = _('Η συνεδρίαση ενημερώθηκε επιτυχώς.')

    def form_valid(self, form):
        old_meeting = Meeting.objects.get(pk=self.object.pk)
        old_collective_body = old_meeting.collective_body

        response = super().form_valid(form)

        meeting = self.object
        new_collective_body = meeting.collective_body

        if old_collective_body != new_collective_body:
            meeting.notify_collective_body_change(
                old_collective_body=old_collective_body,
                new_collective_body=new_collective_body
            )
            meeting.present.clear()
            meeting.absent.clear()

        meeting_basic_info_change = (
                old_meeting.date_and_time != meeting.date_and_time or
                old_meeting.location != meeting.location or
                old_meeting.notes != meeting.notes
        )

        if meeting_basic_info_change:
            meeting.notify_update()

        return response


class SecListMeeting(views.ScopedSecListView):
    model = Meeting
    fields = ['index', 'present', 'absent', 'collective_body', 'location', 'date_and_time', 'notes']
    headers = {
        'index': _('Αριθμός Συνεδρίασης'),
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

    # Custom queryset that returns meetings scheduled for today or in the future, excluding past meetings
    def get_queryset(self):
        queryset = super().get_queryset()

        # If the user is a secretariat, return the scoped meetings that did not conclude
        if not self.request.user.is_superuser:

            # Use the start of today instead of the current time,
            # so today's earlier meetings are not hidden.
            start_of_today = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
            return queryset.filter(date_and_time__gte=start_of_today)

        # If the user is a superuser (admin), then use the default manager's query
        # that returns all the registered meetings without taking into account the datetime
        return queryset


class SecDeleteMeeting(views.ScopedDeleteView):
    model = Meeting
    success_url = 'meetings:sec_list_meetings'
    success_message = _('Η συνεδρίαση διαγράφηκε.')


class StaffListMeeting(views.StaffListView):
    model = Meeting
    fields = ['collective_body', 'location', 'date_and_time', 'notes']
    headers = {
        'collective_body': _('Συλλογικό Όργανο'),
        'location': _('Τοποθεσία'),
        'date_and_time': _('Ημερομηνία & ώρα'),
        'notes': _('Σημειώσεις')
    }
    table_title = _('Συνεδριάσεις')
    ordering = ['collective_body', 'date_and_time']
    create_button = False
    update_buttons = False
    back_url = reverse_lazy('bodies:staff_list_collectivebodies')

    # Custom queryset that returns meetings scheduled for today or in the future, excluding past meetings
    def get_queryset(self):
        staff_member = get_object_or_404(StaffMember, user=self.request.user)
        bodies = CollectiveBody.objects.active_now().filter(participants=staff_member)
        # Use the start of today instead of the current time,
        # so today's earlier meetings are not hidden.
        start_of_today = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)

        # The queryset includes all meetings scheduled to take place from the start of the current day onwards
        self.queryset = Meeting.objects.filter(collective_body__in=bodies, date_and_time__gte=start_of_today)

        return super().get_queryset()
