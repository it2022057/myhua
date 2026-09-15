from django.core.exceptions import PermissionDenied

from bodies.models import CollectiveBody
from core.testing import ProjectTestCase
from scopes.utils import get_scoped_object_or_exc, get_secretariat_scope
from subjects.models import Subject


class SecretariatScopeTests(ProjectTestCase):
    def test_secretariat_scope_contains_assigned_entities(self):
        scope = get_secretariat_scope(self.sec_user)

        self.assertIn(self.department, scope["departments"])
        self.assertIn(self.program, scope["programs"])
        self.assertIn(self.body, scope["collective_bodies"])
        self.assertNotIn(self.body2, scope["collective_bodies"])

    def test_non_secretariat_has_empty_scope(self):
        scope = get_secretariat_scope(self.applicant)

        self.assertFalse(scope["departments"].exists())
        self.assertFalse(scope["programs"].exists())
        self.assertFalse(scope["collective_bodies"].exists())

    def test_superuser_scope_contains_all_entities(self):
        scope = get_secretariat_scope(self.admin)

        self.assertIn(self.department, scope["departments"])
        self.assertIn(self.department2, scope["departments"])
        self.assertIn(self.body, scope["collective_bodies"])
        self.assertIn(self.body2, scope["collective_bodies"])

    def test_sc_filter_requires_user_argument(self):
        with self.assertRaises(ValueError):
            Subject.objects.sc_filter()

    def test_get_scoped_object_returns_in_scope_object(self):
        obj = get_scoped_object_or_exc(
            CollectiveBody,
            pk=self.body.pk,
            user=self.sec_user,
        )
        self.assertEqual(obj, self.body)

    def test_get_scoped_object_rejects_out_of_scope_object(self):
        with self.assertRaises(PermissionDenied):
            get_scoped_object_or_exc(
                CollectiveBody,
                pk=self.body2.pk,
                user=self.sec_user,
            )
