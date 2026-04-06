from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from accounts.checks import is_secretariat
from bodies.models import CollectiveBody
from core import views
from core.models import TitleStrMixin
from core.utils import get_order_by_title
from scopes.utils import get_secretariat_scope

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


class SecCollectiveBodyAutoComplete(TitleStrMixin, LoginRequiredMixin, UserPassesTestMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        scopes = get_secretariat_scope(self.request.user)
        qs = scopes['collective_bodies']
        if self.q:
            qs = qs.filter(Q(title_gr__icontains=self.q) | Q(title_en__icontains=self.q))

        return qs.order_by(get_order_by_title())[:10]

    def test_func(self):
        return is_secretariat(self.request.user)

