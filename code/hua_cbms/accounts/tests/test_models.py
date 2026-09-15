from django.contrib.auth import get_user_model

from accounts.models import PersonalInfo, StaffMember, create_user_if_required
from core.testing import ProjectTestCase

User = get_user_model()


class AccountModelTests(ProjectTestCase):
    def test_internal_user_uses_first_part_as_username(self):
        user = create_user_if_required("newmember@hua.gr")
        self.assertEqual(user.username, "newmember")
        self.assertEqual(user.email, "newmember@hua.gr")

    def test_external_user_uses_email_as_username(self):
        user = create_user_if_required("external@example.com")
        self.assertEqual(user.username, "external@example.com")

    def test_create_user_if_required_does_not_duplicate_user(self):
        first = create_user_if_required("same@hua.gr")
        second = create_user_if_required("same@hua.gr")
        self.assertEqual(first.pk, second.pk)
        self.assertEqual(User.objects.filter(email="same@hua.gr").count(), 1)

    def test_staff_member_save_populates_names_user_and_personal_info(self):
        staff = StaffMember.objects.create(
            email="generated@hua.gr",
            given_name="Local",
            surname="Tester",
            title="Researcher",
            is_internal=True,
            internal_department=self.department,
        )

        self.assertEqual(staff.display_name, "Local Tester")
        self.assertEqual(staff.display_name_full, "Local Tester (Researcher)")
        self.assertIsNotNone(staff.user)
        self.assertIsNotNone(staff.personal_info)
        self.assertEqual(staff.personal_info.email, staff.email)
        self.assertTrue(staff.given_name_en)
        self.assertTrue(staff.surname_en)

    def test_external_staff_member_clears_internal_department(self):
        staff = StaffMember.objects.create(
            email="externalstaff@example.com",
            given_name="External",
            surname="Staff",
            title="External Staff",
            is_internal=False,
            internal_department=self.department,
        )
        self.assertIsNone(staff.internal_department)

    def test_staff_delete_also_deletes_personal_info(self):
        staff = StaffMember.objects.create(
            email="delete-me@hua.gr",
            given_name="Delete",
            surname="Me",
            title="Professor",
            is_internal=True,
            internal_department=self.department,
        )
        personal_info_pk = staff.personal_info_id

        staff.delete()

        self.assertFalse(PersonalInfo.objects.filter(pk=personal_info_pk).exists())
