from core.testing import ProjectTestCase


class SecretariatModelTests(ProjectTestCase):
    def test_program_scope_returns_assigned_programs(self):
        self.assertIn(self.program, self.secretariat.program_scope())
        self.assertNotIn(self.program2, self.secretariat.program_scope())

    def test_department_scope_returns_assigned_departments(self):
        self.assertIn(self.department, self.secretariat.department_scope())
        self.assertNotIn(self.department2, self.secretariat.department_scope())

    def test_string_representation_contains_username(self):
        self.assertIn(self.sec_user.username, str(self.secretariat))
