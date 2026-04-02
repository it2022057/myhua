from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

APPS = {
    'secretariat' : [
        {
            'title': _('Θέματα'),
            'url': reverse_lazy('subjects:sec_list_subject'),
        },
        # {
        #     'title': _('Αποφάσεις'),
        #     'url': reverse_lazy('subjects:missing'),
        # },
        {
            'title': _('Συλλογικά Όργανα'),
            'url': reverse_lazy('bodies:sec_list_collective_body'),
        },
    ],
    # 'participant': [
    #     {
    #         'title': 'Participant',
    #         'url': reverse_lazy('accounts:forgot_password')
    #     },
    # ],
    # 'president': [
    #     {
    #         'title': 'President',
    #         'url': reverse_lazy('accounts:forgot_password')
    #     },
    # ],
    'applicant' : [
        {
            'title': 'Applicant',
            'url': reverse_lazy('accounts:forgot_password')
        }
    ],
    'staff_member' : [
        {
            'title': 'Staff Member',
            'url': reverse_lazy('accounts:forgot_password')
        }
    ],
    'change_password' : [
        {
            'title': _('Διαχείριση συνθηματικού'),
            'url': reverse_lazy('accounts:password_change'),
        }
    ]
}