from core.testing import ProjectTestCase
from curricula.models import Department, StudyProgram


class CurriculaModelTests(ProjectTestCase):
    def test_program_level_english_translation(self):
        self.assertEqual(self.program.level_en(), "Undergraduate")

    def test_department_scope_filter(self):
        ids = set(Department.objects.sc_filter(user=self.sec_user).values_list("pk", flat=True))
        self.assertIn(self.department.pk, ids)
        self.assertNotIn(self.department2.pk, ids)

    def test_program_scope_filter(self):
        ids = set(StudyProgram.objects.sc_filter(user=self.sec_user).values_list("pk", flat=True))
        self.assertIn(self.program.pk, ids)
        self.assertNotIn(self.program2.pk, ids)
