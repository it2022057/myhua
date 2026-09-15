from django import forms

from accounts.checks import is_applicant, is_external_user, is_internal_user, is_secretariat, is_staff_member, \
    validate_meeting_index, validate_password, validate_subject_index

from core.testing import ProjectTestCase


class AccountCheckTests(ProjectTestCase):
    def test_user_type_helpers(self):
        self.assertTrue(is_internal_user(self.sec_user))
        self.assertTrue(is_external_user(self.applicant))
        self.assertTrue(is_secretariat(self.sec_user))
        self.assertTrue(is_staff_member(self.participant.user))
        self.assertTrue(is_applicant(self.applicant))
        self.assertFalse(is_applicant(self.participant.user))

    def test_valid_password_is_accepted(self):
        validate_password("Valid123!!", "Valid123!!")

    def test_short_password_is_rejected(self):
        with self.assertRaises(forms.ValidationError):
            validate_password("A1!!a", "A1!!a")

    def test_mismatched_passwords_are_rejected(self):
        with self.assertRaises(forms.ValidationError):
            validate_password("Valid123!!", "Different123!!")

    def test_password_without_complexity_is_rejected(self):
        with self.assertRaises(forms.ValidationError):
            validate_password("123456789", "123456789")

    def test_duplicate_subject_index_is_rejected(self):
        with self.assertRaises(forms.ValidationError):
            validate_subject_index(1, self.body)

    def test_existing_subject_can_keep_its_own_index_when_updated(self):
        validate_subject_index(1, self.body, instance=self.subject)

    def test_duplicate_meeting_index_is_rejected(self):
        with self.assertRaises(forms.ValidationError):
            validate_meeting_index(1, self.body)

    def test_existing_meeting_can_keep_its_own_index_when_updated(self):
        validate_meeting_index(1, self.body, instance=self.meeting)
