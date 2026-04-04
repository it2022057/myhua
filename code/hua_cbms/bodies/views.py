from django.utils.translation import gettext_lazy as _

from bodies.models import CollectiveBody
from core import views

# Create your views here.

"""
Generic subjects Views
"""

class SecListCollectiveBody(views.ScopedSecListView):
    template_name = 'core/list_objects.html'
    model = CollectiveBody
    fields = ['title_gr', 'start_date', 'end_date']
    headers = {
        'title_gr': _('Τίτλος'),
        'start_date': _('Ημερομηνία Έναρξης'),
        'end_date': _('Ημερομηνία Λήξης')
    }
    table_title = _('Συλλογικά Όργανα')
    #     create_url = 'bodies:sec_create_collective_body'
    #     update_url = 'bodies:sec_update_collective_body'


# class SecCreateCollectiveBody(views.ScopedSecCreateView):
#     model = CollectiveBody
#     form_class = forms.SecSubjectForm
#     success_url = 'subjects:sec_list_subject'
#     headline = _('Δημιουργία Θέματος')
#     back_url = ''

