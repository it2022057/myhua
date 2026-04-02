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




# class SecListSubject(SecList):
#     model = Subject
#     fields = ['index', 'type', 'category', 'collective_body', 'notes']
#     headers = {
#         'index': _('Δείκτης'),
#         'type': _('Τύπος'),
#         'category': _('Κατηγορία'),
#         'collective_body': _('Συλλογικό Όργανο'),
#         'notes': _('Σημειώσεις'),
#     }
#     table_title = _('Θέματα')
#     create_url = 'subjects:sec_create_subject'
#     update_url = 'subjects:sec_update_subject'
#
#
# class SecCreate(views.ScopedSecCreateView):
#     template_name = 'subjects/show_object.html'
#
#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         form.instance.updated_by = self.request.user
#         return super().form_valid(form)
#
#
# class SecUpdate(views.ScopedSecUpdateView):
#     template_name = 'subjects/show_object.html'
#
#     def form_valid(self, form):
#         form.instance.updated_by = self.request.user
#         return super().form_valid(form)
