from django.utils.translation import gettext_lazy as _
from django.contrib import admin


# Configure the custom Django admin site
class HuaAdminSite(admin.AdminSite):
    site_header = _('Διαχείριση HUA')
    site_title = _('Ιστότοπος διαχείρισης HUA')
    index_title = _('Πίνακας Διαχείρισης HUA')