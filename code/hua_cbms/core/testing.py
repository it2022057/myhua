from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from accounts.models import StaffMember
from bodies.models import CollectiveBody
from bodyapplications.models import Application
from curricula.models import Department, Institution, School, StudyProgram
from meetings.models import Meeting
from scopes.models import Secretariat
from subjects.models import Decision, Subject, SubjectCategory, SubjectType

User = get_user_model()


class ProjectTestCase(TestCase):
    """
    Shared test data for the project.

    The objects are deliberately small and controlled. They are not loaded from
    scripts/initial_data.py so that unit tests do not depend on demo/seed data.
    """

    @classmethod
    def setUpTestData(cls):
        cls.now = timezone.now()

        cls.admin = User.objects.create_superuser(
            username="admin",
            email="admin@hua.gr",
            password="Admin123!!",
        )
        cls.sec_user = User.objects.create_user(
            username="sec",
            email="sec@hua.gr",
            password="Secret123!!",
        )
        cls.sec2_user = User.objects.create_user(
            username="sec2",
            email="sec2@hua.gr",
            password="Secret123!!",
        )
        cls.applicant = User.objects.create_user(
            username="applicant@example.com",
            email="applicant@example.com",
            password="Applicant123!!",
        )
        cls.applicant2 = User.objects.create_user(
            username="applicant2@example.com",
            email="applicant2@example.com",
            password="Applicant123!!",
        )

        cls.institution = Institution.objects.create(
            title_gr="Χαροκόπειο Πανεπιστήμιο",
            title_en="Harokopio University",
            short_gr="ΧΠΑ",
            short_en="HUA",
        )
        cls.school = School.objects.create(
            title_gr="Ψηφιακής Τεχνολογίας",
            title_en="Digital Technology",
            short_gr="ΨΤ",
            short_en="DT",
            institution=cls.institution,
        )
        cls.school2 = School.objects.create(
            title_gr="Σχολή Επιστημών Υγείας και Αγωγής",
            title_en="School of Health and Education Sciences",
            short_gr="ΕΥ",
            short_en="HS",
            institution=cls.institution,
        )
        cls.department = Department.objects.create(
            title_gr="Πληροφορικής και Τηλεματικής",
            title_en="Informatics and Telematics",
            short_gr="ΠΤ",
            short_en="IT",
            school=cls.school,
        )
        cls.department2 = Department.objects.create(
            title_gr="Επιστήμης Διαιτολογίας - Διατροφής",
            title_en="Nutrition and Dietetics",
            short_gr="ΔΔ",
            short_en="ND",
            school=cls.school2,
        )

        cls.program = StudyProgram.objects.create(
            title_gr="Προπτυχιακό Πρόγραμμα",
            title_en="Undergraduate Program",
            short_gr="ΠΠΣ",
            short_en="UND",
            department=cls.department,
            type=StudyProgram.UNDERGRADUATE,
        )
        cls.program2 = StudyProgram.objects.create(
            title_gr="Δεύτερο Πρόγραμμα",
            title_en="Second Program",
            short_gr="Π2",
            short_en="P2",
            department=cls.department2,
            type=StudyProgram.POSTGRADUATE,
        )

        cls.secretariat = Secretariat.objects.create(user=cls.sec_user)
        cls.secretariat.departments.add(cls.department)
        cls.secretariat.programs.add(cls.program)

        cls.secretariat2 = Secretariat.objects.create(user=cls.sec2_user)
        cls.secretariat2.departments.add(cls.department2)
        cls.secretariat2.programs.add(cls.program2)

        cls.president = StaffMember.objects.create(
            email="president@hua.gr",
            given_name="President",
            surname="One",
            title="Head Professor",
            is_internal=True,
            internal_department=cls.department,
        )
        cls.participant = StaffMember.objects.create(
            email="participant@hua.gr",
            given_name="Participant",
            surname="One",
            title="Associate Professor",
            is_internal=True,
            internal_department=cls.department,
        )
        cls.other_staff = StaffMember.objects.create(
            email="other@hua.gr",
            given_name="Other",
            surname="Staff",
            title="Professor",
            is_internal=True,
            internal_department=cls.department2,
        )

        cls.body = cls.make_body(
            title_gr="Συνέλευση Τμήματος",
            title_en="Department Assembly",
            secretariat=cls.secretariat,
            president=cls.president,
            start_date=cls.now - timedelta(days=5),
            end_date=cls.now + timedelta(days=30),
            participant=cls.participant,
        )
        cls.body2 = cls.make_body(
            title_gr="Δεύτερο Όργανο",
            title_en="Second Body",
            secretariat=cls.secretariat2,
            president=cls.other_staff,
            start_date=cls.now - timedelta(days=5),
            end_date=cls.now + timedelta(days=30),
            participant=cls.other_staff,
        )

        cls.subject_type = SubjectType.objects.create(
            title_gr="Ακαδημαϊκό",
            title_en="Academic",
        )
        cls.subject_category = SubjectCategory.objects.create(
            title_gr="Έγκριση",
            title_en="Approval",
        )

        cls.subject = Subject.objects.create(
            index=1,
            type=cls.subject_type,
            category=cls.subject_category,
            applicant_user=cls.applicant,
            program=cls.program,
            department=cls.department,
            school=cls.school,
            collective_body=cls.body,
            notes="Test subject",
        )
        cls.subject2 = Subject.objects.create(
            index=1,
            type=cls.subject_type,
            category=cls.subject_category,
            applicant_user=cls.applicant2,
            program=cls.program2,
            department=cls.department2,
            school=cls.school2,
            collective_body=cls.body2,
            notes="Out of scope subject",
        )

        cls.decision = Decision.objects.create(
            title=Decision.TITLE_APPROVAL,
            subject=cls.subject,
        )
        cls.decision2 = Decision.objects.create(
            title=Decision.TITLE_REJECTION,
            subject=cls.subject2,
        )

        cls.pending_application = Application.objects.create(
            applicant=cls.applicant,
            request_subject="Pending request",
            description="Pending application",
        )
        cls.resolved_application = Application.objects.create(
            applicant=cls.applicant,
            request_subject="Resolved request",
            description="Resolved application",
            subject=cls.subject,
        )
        cls.other_resolved_application = Application.objects.create(
            applicant=cls.applicant2,
            request_subject="Other resolved request",
            description="Other resolved application",
            subject=cls.subject2,
        )

        cls.meeting = cls.make_meeting(
            collective_body=cls.body,
            index=1,
            date_and_time=cls.now + timedelta(days=2),
        )
        cls.meeting2 = cls.make_meeting(
            collective_body=cls.body2,
            index=1,
            date_and_time=cls.now + timedelta(days=2),
        )

    @classmethod
    def make_body(
            cls,
            *,
            title_gr,
            title_en,
            secretariat,
            president,
            start_date,
            end_date,
            active=True,
            participant=None,
    ):
        with patch("bodies.models.notify.delay"):
            body = CollectiveBody.objects.create(
                title_gr=title_gr,
                title_en=title_en,
                secretariat=secretariat,
                president=president,
                start_date=start_date,
                end_date=end_date,
                active=active,
            )

        if participant is not None:
            body.participants.add(participant)
        return body

    @classmethod
    def make_meeting(cls, *, collective_body, index, date_and_time, **kwargs):
        with patch("meetings.models.notify.delay"):
            return Meeting.objects.create(
                index=index,
                collective_body=collective_body,
                date_and_time=date_and_time,
                location=kwargs.pop("location", "Room A"),
                notes=kwargs.pop("notes", "Test meeting"),
                **kwargs,
            )
