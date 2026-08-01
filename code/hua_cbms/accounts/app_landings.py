from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

APPS = {
    'secretariat' : [
        {
            'title': _('Συλλογικά Όργανα'),
            'url': reverse_lazy('bodies:sec_list_collectivebodies'),
        },
    ],
    'applicant' : [
        {
            'title': _('Οι αιτήσεις μου'),
            'url': reverse_lazy('bodyapplications:applicant_list_bodyapplications'),
        }
    ],
    'staff_member' : [
        {
            'title': _('Οι συμμετοχές μου'),
            'url': reverse_lazy('bodies:staff_list_collectivebodies'),
        },
    ],
    'change_password' : [
        {
            'title': _('Διαχείριση συνθηματικού'),
            'url': reverse_lazy('accounts:password_change'),
        }
    ]
}