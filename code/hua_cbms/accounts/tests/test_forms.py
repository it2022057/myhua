from accounts.forms import SecStaffForm, SignUpForm
from core.testing import ProjectTestCase


class AccountFormTests(ProjectTestCase):
    def test_internal_staff_requires_internal_department(self):
        data = {
            "email": "staff2@hua.gr",
            "given_name": "Staff",
            "surname": "Two",
            "institution": "Harokopio University",
            "school": "Digital Technology",
            "department": "Informatics and Telematics",
            "title": "Professor",
            "is_internal": "True",
            "internal_department": "",
        }
        form = SecStaffForm(data=data, user=self.sec_user)
        self.assertFalse(form.is_valid())
        self.assertIn("internal_department", form.errors)

    def test_external_staff_does_not_need_internal_department(self):
        data = {
            "email": "external2@example.com",
            "given_name": "External",
            "surname": "Two",
            "institution": "Other",
            "school": "Other",
            "department": "Other",
            "title": "Member",
            "is_internal": "",
            "internal_department": "",
        }
        form = SecStaffForm(data=data, user=self.sec_user)
        self.assertTrue(form.is_valid(), form.errors)

    def test_signup_rejects_internal_hua_email(self):
        form = SignUpForm(
            data={
                "email": "internal@hua.gr",
                "name": "Name",
                "surname": "Surname",
                "password1": "Valid123!!",
                "password2": "Valid123!!",
            }
        )
        self.assertFalse(form.is_valid())

    def test_signup_rejects_existing_email(self):
        form = SignUpForm(
            data={
                "email": self.applicant.email,
                "name": "Name",
                "surname": "Surname",
                "password1": "Valid123!!",
                "password2": "Valid123!!",
            }
        )
        self.assertFalse(form.is_valid())
