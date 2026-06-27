from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

APPS = {
    'secretariat' : [
        {
            'title': _('Θέματα'),
            'url': reverse_lazy('subjects:sec_list_subjects'),
        },
        {
            'title': _('Αποφάσεις'),
            'url': reverse_lazy('subjects:sec_list_decisions'),
        },
        {
            'title': _('Τύποι Θεμάτων'),
            'url': reverse_lazy('subjects:sec_list_subject-types'),
        },
        {
            'title': _('Κατηγορίες Θεμάτων'),
            'url': reverse_lazy('subjects:sec_list_subject-categories'),
        },
        {
            'title': _('Συλλογικά Όργανα'),
            'url': reverse_lazy('bodies:sec_list_collectivebodies'),
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
            'title': _('Οι αιτήσεις μου'),
            'url': reverse_lazy('accounts:forgot_password')
        },
        {
            'title': _('Ξέχασα τον κωδικό πρόσβασης'),
            'url': reverse_lazy('accounts:forgot_password')
        }
    ],
    'staff_member' : [
        {
            'title': _('Οι συμμετοχές μου'),
            'url': reverse_lazy('bodies:staff_list_collectivebodies'),
        },
        {
            'title': _('Ξέχασα τον κωδικό πρόσβασης'),
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