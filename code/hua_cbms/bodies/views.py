from multiprocessing import context

from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from accounts.checks import is_secretariat
from accounts.models import StaffMember
from bodies.models import CollectiveBody
from core import views
from core.models import TitleStrMixin
from core.utils import get_order_by_title
from bodies import forms
from scopes.utils import get_secretariat_scope

# Create your views here.


class SecCreateCollectiveBody(views.ScopedSecCreateView):
    model = CollectiveBody
    form_class = forms.SecCollectiveBodyForm
    success_url = 'bodies:sec_list_collectivebody'
    headline = _('Δημιουργία Συλλογικού Πανεπιστημιακού Οργάνου')
    back_url = ''


class SecUpdateCollectiveBody(views.ScopedSecUpdateView):
    model = CollectiveBody
    form_class = forms.SecCollectiveBodyForm
    success_url = 'bodies:sec_list_collectivebody'
    delete_url = 'bodies:sec_delete_collectivebody'
    confirm_modal = True


class SecListCollectiveBody(views.ScopedSecListView):
    model = CollectiveBody
    fields = ['title_gr', 'president', 'secretariat', 'start_date', 'end_date']
    headers = {
        'title_gr': _('Τίτλος'),
        'participants': _('Συμμετέχοντες'),
        'president': _('Πρόεδρος'),
        'secretariat': _('Γραμματεία'),
        'start_date': _('Ημερομηνία Έναρξης'),
        'end_date': _('Ημερομηνία Λήξης')
    }
    table_title = _('Συλλογικά Όργανα')
    create_url = 'bodies:sec_create_collectivebody'
    update_url = 'bodies:sec_update_collectivebody'
    extra_buttons = True
    extra_text = _('Συμμετέχοντες')
    extra_button_icon = 'people'
    extra_url = 'accounts:sec_list_staff_member'

    def get_extra_url(self, obj):
        return reverse_lazy(self.extra_url)


class SecDeleteCollectiveBody(views.ScopedDeleteView):
    model = CollectiveBody
    success_url = 'bodies:sec_list_collectivebody'


class SecCollectiveBodyAutoComplete(TitleStrMixin, LoginRequiredMixin, UserPassesTestMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        scopes = get_secretariat_scope(self.request.user)
        qs = scopes['collective_bodies']
        if self.q:
            qs = qs.filter(Q(title_gr__icontains=self.q) | Q(title_en__icontains=self.q))

        return qs.order_by(get_order_by_title())[:10]

    def test_func(self):
        return is_secretariat(self.request.user)

