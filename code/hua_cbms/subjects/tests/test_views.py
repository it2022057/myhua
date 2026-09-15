from django.urls import reverse

from core.testing import ProjectTestCase
from subjects.models import Subject
from subjects.views import SecListSubject


class SubjectViewTests(ProjectTestCase):
    def test_existing_decision_opens_update_url(self):
        view = SecListSubject()
        url = str(view.get_extra_url(self.subject))

        self.assertEqual(url, reverse("subjects:sec_update_decision", kwargs={"pk": self.decision.pk}))

    def test_subject_without_decision_opens_create_url(self):
        subject = Subject.objects.create(
            index=2,
            type=self.subject_type,
            category=self.subject_category,
            collective_body=self.body,
        )

        view = SecListSubject()
        url = str(view.get_extra_url(subject))

        self.assertEqual(url,f"{reverse('subjects:sec_create_decision')}?subject_id={subject.pk}")

    def test_staff_subject_list_includes_participating_body(self):
        self.client.force_login(self.participant.user)
        response = self.client.get(
            reverse("subjects:staff_list_subjects")
        )

        ids = set(response.context["objects"].values_list("pk", flat=True))
        self.assertIn(self.subject.pk, ids)
        self.assertNotIn(self.subject2.pk, ids)

    def test_president_can_see_body_subjects(self):
        self.client.force_login(self.president.user)
        response = self.client.get(
            reverse("subjects:staff_list_subjects")
        )

        ids = set(response.context["objects"].values_list("pk", flat=True))
        self.assertIn(self.subject.pk, ids)

    def test_secretariat_subject_list_is_scoped(self):
        self.client.force_login(self.sec_user)
        response = self.client.get(
            reverse("subjects:sec_list_subjects")
        )

        ids = set(response.context["objects"].values_list("pk", flat=True))
        self.assertIn(self.subject.pk, ids)
        self.assertNotIn(self.subject2.pk, ids)
