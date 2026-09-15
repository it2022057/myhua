from django.utils import translation

from core.testing import ProjectTestCase
from core.utils import get_ordinal, get_order_by_title


class CoreUtilsTests(ProjectTestCase):
    def test_order_by_title_follows_language(self):
        with translation.override("el"):
            self.assertEqual(get_order_by_title(), "title_gr")

        with translation.override("en"):
            self.assertEqual(get_order_by_title(), "title_en")

    def test_greek_ordinal(self):
        with translation.override("el"):
            self.assertEqual(get_ordinal(2), "2η")

    def test_english_ordinals(self):
        with translation.override("en"):
            self.assertEqual(get_ordinal(1), "1st")
            self.assertEqual(get_ordinal(2), "2nd")
            self.assertEqual(get_ordinal(3), "3rd")
            self.assertEqual(get_ordinal(11), "11th")
