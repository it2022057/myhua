from django.test import RequestFactory

from api.permissions import IsSecretariatUser
from core.testing import ProjectTestCase


class ApiPermissionTests(ProjectTestCase):
    def test_secretariat_is_allowed(self):
        request = RequestFactory().get("/")
        request.user = self.sec_user
        self.assertTrue(IsSecretariatUser().has_permission(request, None))

    def test_applicant_is_denied(self):
        request = RequestFactory().get("/")
        request.user = self.applicant
        self.assertFalse(IsSecretariatUser().has_permission(request, None))
