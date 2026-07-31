from django.contrib.admin.apps import AdminConfig


# Register the custom admin site as the default Django admin
class HuaAdminSiteConfig(AdminConfig):
    # Specify the custom AdminSite implementation
    default_site = 'hua_cbms.admin_site.HuaAdminSite'
