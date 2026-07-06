from django.contrib.auth.decorators import login_required
from django.core.exceptions import ViewDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from accounts.models import StaffMember
from core import views
from . import forms
from .models import Meeting

"""
Secretariat Subject Views
"""


class SecCreateMeeting(views.ScopedSecCreateView):
    model = Meeting
    form_class = forms.SecMeetingForm
    success_url = 'meetings:sec_list_meetings'
    headline = _('Δημιουργία Συνεδρίασης')
    back_url = ''


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


class SecDeleteMeeting(views.ScopedDeleteView):
    model = Meeting
    success_url = 'meetings:sec_list_meetings'


class StaffListMeeting(views.StaffListView):
    model = Meeting
    template_name = 'meetings/list_objects.html'
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
    update_text = _('Αλλαγή απάντησης')
    extra_buttons = True
    extra_button_icon = 'check_circle'
    extra_text = _('Αποδοχή')
    extra_url = 'meetings:staff_accept_meeting'
    extra_buttons2 = True
    extra_button_icon2 = 'cancel'
    extra_button_class2 = 'btn btn-danger'
    extra_text2 = _('Άρνηση')
    extra_url2 = 'meetings:staff_refuse_meeting'
    confirm_modal_title = _('Αλλαγή απάντησης')
    confirm_modal_question = _('Παρακαλούμε επιλέξτε εκ νέου την απάντηση για τη συμμετοχή σας στη συνεδρίαση !')
    confirm_modal_cancel = _('Απών')
    confirm_modal_ok = _('Παρών')

    def get_queryset(self):
        super().get_queryset()
        staff_member = get_object_or_404(StaffMember, user=self.request.user)
        queryset = Meeting.objects.exclude(Q(present=staff_member) | Q(absent=staff_member))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_member = get_object_or_404(StaffMember, user=self.request.user)

        for meeting in context[self.context_object_name]:
            if meeting.can_respond(staff_member):
                meeting.display_invitation_buttons = True
            else:
                meeting.display_invitation_buttons = False
                # GIVE THEM AN OPTION TO CHANGE THEIR RESPONSE, IF THE DATE TIME OF THE MEETING HASN'T PASSED
                meeting.present_url = reverse_lazy('meetings:staff_accept_meeting', kwargs={'pk': meeting.pk})
                meeting.absent_url = reverse_lazy('meetings:staff_refuse_meeting', kwargs={'pk': meeting.pk})

        return context


@login_required
def accept_meeting(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    staff_member = get_object_or_404(StaffMember, user=request.user)

    # Is the staff member invited and has not already replied ?
    if not meeting.can_respond(staff_member):
        raise ViewDoesNotExist

    meeting.absent.remove(staff_member)
    meeting.present.add(staff_member)

    return redirect(request.GET.get('next') or 'meetings:staff_list_meetings')


@login_required
def refuse_meeting(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    staff_member = get_object_or_404(StaffMember, user=request.user)

    # Is the staff member invited and has not already replied ?
    if not meeting.can_respond(staff_member):
        raise ViewDoesNotExist

    meeting.present.remove(staff_member)
    meeting.absent.add(staff_member)

    return redirect(request.GET.get('next') or 'meetings:staff_list_meetings')
