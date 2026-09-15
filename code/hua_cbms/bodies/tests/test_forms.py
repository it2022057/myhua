from datetime import timedelta

from django.utils import timezone

from accounts.models import StaffMember
from bodies.forms import SecCollectiveBodyForm
from core.testing import ProjectTestCase
from hua_cbms import settings


class CollectiveBodyFormTests(ProjectTestCase):
    def _base_data(self):
        return {
            "title_gr": "Νέο Όργανο",
            "title_en": "New Body",
            "participants": [str(self.participant.pk)],
            "president": str(self.president.pk),
            "secretariat": str(self.secretariat.pk),
            "start_date": timezone.localtime(self.now).strftime("%Y-%m-%d %H:%M"),
            "end_date": timezone.localtime(self.now + timedelta(days=10)).strftime("%Y-%m-%d %H:%M"),
            "active": "True",
        }

    def _admin_form(self, data):
        all_staff = StaffMember.objects.all()
        return SecCollectiveBodyForm(
            data=data,
            user=self.admin,
            querysets={
                "participants": all_staff,
                "president": all_staff,
            },
        )

    def test_president_cannot_also_be_participant(self):
        data = self._base_data()
        data["participants"] = [str(self.president.pk)]
        form = self._admin_form(data)

        self.assertFalse(form.is_valid())
        self.assertIn("participants", form.errors)

    def test_start_after_end_is_rejected(self):
        data = self._base_data()
        data["start_date"] = timezone.localtime(self.now + timedelta(days=20)).strftime("%Y-%m-%d %H:%M")
        data["end_date"] = timezone.localtime(self.now + timedelta(days=10)).strftime("%Y-%m-%d %H:%M")

        form = self._admin_form(data)
        self.assertFalse(form.is_valid())
        self.assertIn("start_date", form.errors)

    def test_secretariat_cannot_edit_admin_only_fields(self):
        form = SecCollectiveBodyForm(
            instance=self.body,
            user=self.sec_user,
        )
        for field in [
            "secretariat",
            "president",
            "start_date",
            "end_date",
            "active",
        ]:
            self.assertTrue(form.fields[field].disabled)
