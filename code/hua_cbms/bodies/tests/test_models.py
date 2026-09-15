from datetime import timedelta

from bodies.models import CollectiveBody
from core.testing import ProjectTestCase


class CollectiveBodyModelTests(ProjectTestCase):
    def test_active_now_returns_only_current_active_bodies(self):
        future = self.make_body(
            title_gr="Future",
            title_en="Future",
            secretariat=self.secretariat,
            president=self.president,
            start_date=self.now + timedelta(days=2),
            end_date=self.now + timedelta(days=20),
        )
        inactive = self.make_body(
            title_gr="Inactive",
            title_en="Inactive",
            secretariat=self.secretariat,
            president=self.president,
            start_date=self.now - timedelta(days=2),
            end_date=self.now + timedelta(days=20),
            active=False,
        )

        ids = set(CollectiveBody.objects.active_now().values_list("pk", flat=True))
        self.assertIn(self.body.pk, ids)
        self.assertNotIn(future.pk, ids)
        self.assertNotIn(inactive.pk, ids)

    def test_scope_filter_returns_only_secretariat_bodies(self):
        ids = set(
            CollectiveBody.objects.sc_filter(
                user=self.sec_user
            ).values_list("pk", flat=True)
        )
        self.assertIn(self.body.pk, ids)
        self.assertNotIn(self.body2.pk, ids)

    def test_active_display_uses_expected_badge(self):
        self.assertIn("bg-success", str(self.body.active_display()))
        self.body.active = False
        self.assertIn("bg-danger", str(self.body.active_display()))

    def test_build_participants_rows_contains_participant(self):
        html = self.body.build_participants_rows()
        self.assertIn(self.participant.email, html)
        self.assertIn(self.participant.display_name, html)
