from datetime import datetime

from django.utils import timezone

from bodies.models import CollectiveBody
from bodyapplications.models import Application
from curricula.models import StudyProgram, School, Department, Institution
from accounts.models import StaffMember
from hua_cbms import settings
from meetings.models import Meeting
from scopes.models import Secretariat
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from subjects.models import Decision, Subject, SubjectType, SubjectCategory

User = get_user_model()

COLLECTIVE_BODY = {
    'Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής': {
        'title_gr': 'Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής',
        'title_en': 'Department Assembly of Informatics and Telematics',
        'participants': ['michalak@hua.gr', 'cdiou@hua.gr', 'mj@nba.com', 'gdede@hua.gr', 'gfragi@hua.gr',
                         'mara@hua.gr'],
        'president': 'thkam@hua.gr',
        'secretariat': 'apresvelou@hua.gr',
        'start_date': '01/09/2026 09:00',
        'end_date': '01/09/2027 09:00',
        'class_type': CollectiveBody,
    },
    'Σύγκλητος': {
        'title_gr': 'Σύγκλητος',
        'title_en': 'Senate',
        'participants': ['mj@nba.com', 'evangelf@hua.gr', 'mara@hua.gr', 'gfragi@hua.gr', 'prizomil@hua.gr'],
        'president': 'president@gmail.com',
        'secretariat': 'mysec@hua.gr',
        'start_date': '01/01/2012 08:00',
        'end_date': '01/01/2030 08:00',
        'class_type': CollectiveBody,
    },
    'Όργανο Αξιολόγησης Υποψηφίων Μεταπτυχιακών': {
        'title_gr': 'Όργανο Αξιολόγησης Υποψηφίων Μεταπτυχιακών',
        'title_en': 'Postgraduate Candidate Evaluation Body',
        'participants': ['pg@gmail.com', 'cdiou@hua.gr', 'ng@gmail.com', 'gdimitra@hua.gr', 'staff@gmail.com'],
        'president': 'mj@nba.com',
        'secretariat': 'itpsec@hua.gr',
        'start_date': '15/08/2026 14:00',
        'end_date': '15/08/2028 14:00',
        'class_type': CollectiveBody,
    },
    'Γενική Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής': {
        'title_gr': 'Γενική Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής',
        'title_en': 'General Assembly of the Department of Informatics and Telematics',
        'participants': ['michalak@hua.gr', 'cdiou@hua.gr', 'mara@hua.gr', 'gdede@hua.gr', 'gfragi@hua.gr',
                         'staff@gmail.com'],
        'president': 'thkam@hua.gr',
        'secretariat': 'apresvelou@hua.gr',
        'start_date': '01/09/2026 09:00',
        'end_date': '01/09/2027 09:00',
        'class_type': CollectiveBody,
    },
    'Όργανο Διοίκησης': {
        'title_gr': 'Όργανο Διοίκησης',
        'title_en': 'Governing Body',
        'participants': ['thkam@hua.gr', 'ng@gmail.com', 'pg@gmail.com', 'gdimitra@hua.gr', 'prizomil@hua.gr',
                         'mj@nba.com'],
        'president': 'president@gmail.com',
        'secretariat': 'mysec@hua.gr',
        'start_date': '30/05/2015 23:59',
        'end_date': '01/01/2027 06:00',
        'class_type': CollectiveBody,
    },
    '(Παλιό) Όργανο Διοίκησης': {
        'title_gr': '(Παλιό) Όργανο Διοίκησης',
        'title_en': '(Old) Governing Body',
        'participants': ['thkam@hua.gr', 'ng@gmail.com', 'pg@gmail.com', 'gfragi@hua.gr', 'prizomil@hua.gr',
                         'evangelf@hua.gr', 'cdiou@hua.gr', 'gdimitra@hua.gr', 'mara@hua.gr', 'michalak@hua.gr'],
        'president': 'president@gmail.com',
        'secretariat': 'mysec@hua.gr',
        'start_date': '01/01/2009 10:00',
        'end_date': '01/05/2015 23:59',
        'active': False,
        'class_type': CollectiveBody,
    },
    'Πρυτανικό Όργανο': {
        'title_gr': 'Πρυτανικό Όργανο',
        'title_en': 'Rector Body',
        'participants': ['thkam@hua.gr', 'gdede@hua.gr', 'mara@hua.gr', 'gdimitra@hua.gr', 'ng@gmail.com',
                         'pg@gmail.com'],
        'president': 'president@gmail.com',
        'secretariat': 'mysec@hua.gr',
        'start_date': '01/01/2025 09:00',
        'end_date': '01/08/2026 09:00',
        'class_type': CollectiveBody,
    },
    'Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών': {
        'title_gr': 'Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών',
        'title_en': 'Electoral Body for the Promotion of Professors',
        'participants': ['thkam@hua.gr', 'gdede@hua.gr', 'mara@hua.gr', 'gdimitra@hua.gr', 'gfragi@hua.gr',
                         'cdiou@hua.gr', 'michalak@hua.gr', 'evangelf@hua.gr', 'prizomil@hua.gr'],
        'president': 'president@gmail.com',
        'secretariat': 'mysec@hua.gr',
        'start_date': '02/01/2026 09:00',
        'end_date': '01/01/2027 09:00',
        'class_type': CollectiveBody,
    },
    '(Παλιό) Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών': {
        'title_gr': '(Παλιό) Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών',
        'title_en': '(Old) Electoral Body for the Promotion of Professors',
        'participants': ['thkam@hua.gr', 'gdede@hua.gr', 'mara@hua.gr', 'gdimitra@hua.gr', 'ng@gmail.com',
                         'pg@gmail.com', 'mj@nba.com', 'gfragi@hua.gr', 'cdiou@hua.gr', 'staff@gmail.com',
                         'michalak@hua.gr', 'evangelf@hua.gr', 'prizomil@hua.gr'],
        'president': 'president@gmail.com',
        'secretariat': 'mysec@hua.gr',
        'start_date': '01/01/2024 09:00',
        'end_date': '01/01/2026 09:00',
        'class_type': CollectiveBody,
    },
}

MEETINGS = {
    '1 - Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής': {
        'index': 1,
        'collective_body': 'Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής',
        'present': ['thkam@hua.gr', 'michalak@hua.gr', 'cdiou@hua.gr', 'mara@hua.gr', 'gdede@hua.gr'],
        'absent': ['mj@nba.com', 'gfragi@hua.gr'],
        'date_and_time': '30/09/2026 10:00',
        'notes': 'Έγκριση θεμάτων έναρξης του ακαδημαϊκού έτους.',
        'class_type': Meeting,
    },
    '2 - Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής': {
        'index': 2,
        'collective_body': 'Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής',
        'present': ['thkam@hua.gr', 'michalak@hua.gr', 'cdiou@hua.gr', 'mj@nba.com', 'mara@hua.gr', 'gfragi@hua.gr'],
        'absent': ['gdede@hua.gr'],
        'location': 'Αίθουσα Τηλεδιάσκεψης',
        'date_and_time': '5/10/2026 12:00',
        'notes': 'Συζήτηση θεμάτων προγράμματος σπουδών και διδασκαλίας.',
        'class_type': Meeting,
    },
    '1 - Σύγκλητος': {
        'index': 1,
        'collective_body': 'Σύγκλητος',
        'present': ['president@gmail.com', 'mj@nba.com', 'evangelf@hua.gr', 'mara@hua.gr', 'prizomil@hua.gr'],
        'absent': ['gfragi@hua.gr'],
        'location': 'Θησέως 70, 17676, Καλλιθέα',
        'date_and_time': '10/02/2026 11:00',
        'notes': 'Έγκριση ακαδημαϊκού προγραμματισμού του Πανεπιστημίου.',
        'class_type': Meeting,
    },
    '2 - Σύγκλητος': {
        'index': 2,
        'collective_body': 'Σύγκλητος',
        'present': ['president@gmail.com', 'mj@nba.com', 'mara@hua.gr', 'gfragi@hua.gr', 'prizomil@hua.gr'],
        'absent': ['evangelf@hua.gr'],
        'location': 'Θησέως 70, 17676, Καλλιθέα',
        'date_and_time': '18/06/2026 10:30',
        'notes': 'Έγκριση οικονομικού και διοικητικού απολογισμού.',
        'class_type': Meeting,
    },
    '1 - Όργανο Αξιολόγησης Υποψηφίων Μεταπτυχιακών': {
        'index': 1,
        'collective_body': 'Όργανο Αξιολόγησης Υποψηφίων Μεταπτυχιακών',
        'present': ['mj@nba.com', 'pg@gmail.com', 'cdiou@hua.gr', 'gdimitra@hua.gr'],
        'absent': ['ng@gmail.com', 'staff@gmail.com'],
        'location': 'Ομήρου 9, 17778, Αίθουσα 2.4',
        'date_and_time': '20/09/2026 14:30',
        'notes': 'Αρχική αξιολόγηση αιτήσεων υποψηφίων μεταπτυχιακών φοιτητών.',
        'class_type': Meeting,
    },
    '2 - Όργανο Αξιολόγησης Υποψηφίων Μεταπτυχιακών': {
        'index': 2,
        'collective_body': 'Όργανο Αξιολόγησης Υποψηφίων Μεταπτυχιακών',
        'present': ['mj@nba.com', 'pg@gmail.com', 'ng@gmail.com', 'cdiou@hua.gr', 'staff@gmail.com'],
        'absent': ['gdimitra@hua.gr'],
        'location': 'Ομήρου 9, 17778, Αίθουσα 2.2',
        'date_and_time': '05/10/2026 16:00',
        'notes': 'Οριστικοποίηση πίνακα κατάταξης υποψηφίων.',
        'class_type': Meeting,
    },
    '1 - Γενική Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής': {
        'index': 1,
        'collective_body': 'Γενική Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής',
        'present': ['thkam@hua.gr', 'michalak@hua.gr', 'cdiou@hua.gr', 'mara@hua.gr', 'staff@gmail.com'],
        'absent': ['gdede@hua.gr', 'gfragi@hua.gr'],
        'location': 'Ομήρου 9, 17778, Αίθουσα 1',
        'date_and_time': '25/09/2026 09:30',
        'notes': 'Κατανομή διδακτικού έργου του ακαδημαϊκού έτους.',
        'class_type': Meeting,
    },
    '2 - Γενική Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής': {
        'index': 2,
        'collective_body': 'Γενική Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής',
        'present': ['thkam@hua.gr', 'michalak@hua.gr', 'cdiou@hua.gr', 'gdede@hua.gr', 'gfragi@hua.gr'],
        'absent': ['mara@hua.gr', 'staff@gmail.com'],
        'location': 'Ομήρου 9, 17778, Αίθουσα 1',
        'date_and_time': '12/11/2026 13:00',
        'notes': 'Συζήτηση προτάσεων αναμόρφωσης του προγράμματος σπουδών.',
        'class_type': Meeting,
    },
    '1 - Όργανο Διοίκησης': {
        'index': 1,
        'collective_body': 'Όργανο Διοίκησης',
        'present': ['president@gmail.com', 'thkam@hua.gr', 'ng@gmail.com', 'gdimitra@hua.gr', 'prizomil@hua.gr'],
        'absent': ['pg@gmail.com', 'mj@nba.com'],
        'location': 'Θησέως 70, 17676, Καλλιθέα',
        'date_and_time': '15/03/2026 11:00',
        'notes': 'Έγκριση ετήσιου διοικητικού προγραμματισμού.',
        'class_type': Meeting,
    },
    '2 - Όργανο Διοίκησης': {
        'index': 2,
        'collective_body': 'Όργανο Διοίκησης',
        'present': ['president@gmail.com', 'thkam@hua.gr', 'ng@gmail.com', 'pg@gmail.com', 'prizomil@hua.gr',
                    'mj@nba.com'],
        'absent': ['gdimitra@hua.gr'],
        'location': 'Θησέως 70, 17676, Καλλιθέα',
        'date_and_time': '15/07/2026 10:00',
        'notes': 'Παρακολούθηση προϋπολογισμού και διοικητικών ενεργειών.',
        'class_type': Meeting,
    },
    '1 - (Παλιό) Όργανο Διοίκησης': {
        'index': 1,
        'collective_body': '(Παλιό) Όργανο Διοίκησης',
        'present': ['president@gmail.com', 'thkam@hua.gr', 'pg@gmail.com', 'gdimitra@hua.gr', 'mara@hua.gr',
                    'michalak@hua.gr'],
        'absent': ['ng@gmail.com', 'gfragi@hua.gr', 'prizomil@hua.gr', 'evangelf@hua.gr', 'cdiou@hua.gr'],
        'location': 'Θησέως 70, 176 76, Καλλιθέα',
        'date_and_time': '15/04/2015 12:00',
        'notes': 'Τελικός απολογισμός της θητείας του οργάνου.',
        'class_type': Meeting,
    },
    '1 - Πρυτανικό Όργανο': {
        'index': 1,
        'collective_body': 'Πρυτανικό Όργανο',
        'present': ['president@gmail.com', 'thkam@hua.gr', 'gdede@hua.gr', 'mara@hua.gr', 'ng@gmail.com', ],
        'absent': ['gdimitra@hua.gr', 'pg@gmail.com'],
        'location': 'Θησέως 70, 17676, Καλλιθέα',
        'date_and_time': '12/01/2026 09:30',
        'notes': 'Προγραμματισμός διοικητικών και ακαδημαϊκών ενεργειών.',
        'class_type': Meeting,
    },
    '2 - Πρυτανικό Όργανο': {
        'index': 2,
        'collective_body': 'Πρυτανικό Όργανο',
        'present': ['president@gmail.com', 'thkam@hua.gr', 'gdede@hua.gr', 'mara@hua.gr', 'gdimitra@hua.gr',
                    'ng@gmail.com'],
        'absent': ['pg@gmail.com'],
        'location': 'Θησέως 70, 17676, Καλλιθέα',
        'date_and_time': '20/07/2026 10:00',
        'notes': 'Απολογισμός ενεργειών πριν από τη λήξη της θητείας.',
        'class_type': Meeting,
    },
    '1 - Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών': {
        'index': 1,
        'collective_body': 'Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών',
        'present': ['president@gmail.com', 'thkam@hua.gr', 'gdede@hua.gr', 'mara@hua.gr', 'gdimitra@hua.gr',
                    'cdiou@hua.gr', 'michalak@hua.gr'],
        'absent': ['gfragi@hua.gr', 'evangelf@hua.gr', 'prizomil@hua.gr'],
        'location': 'Μέσω τηλεδιάσκεψης',
        'date_and_time': '10/09/2026 12:00',
        'notes': 'Εξέταση φακέλου υποψηφίου για εξέλιξη σε ανώτερη βαθμίδα.',
        'class_type': Meeting,
    },
    '2 - Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών': {
        'index': 2,
        'collective_body': 'Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών',
        'present': ['president@gmail.com', 'thkam@hua.gr', 'gdede@hua.gr', 'mara@hua.gr', 'gfragi@hua.gr',
                    'cdiou@hua.gr', 'michalak@hua.gr', 'evangelf@hua.gr', 'prizomil@hua.gr'],
        'absent': ['gdimitra@hua.gr'],
        'location': 'Μέσω τηλεδιάσκεψης',
        'date_and_time': '30/09/2026 13:00',
        'notes': 'Παρουσίαση υποψηφίου και διεξαγωγή ψηφοφορίας.',
        'class_type': Meeting,
    },
    '1 - (Παλιό) Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών': {
        'index': 1,
        'collective_body': '(Παλιό) Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών',
        'present': ['president@gmail.com', 'thkam@hua.gr', 'gdede@hua.gr', 'mara@hua.gr', 'gdimitra@hua.gr',
                    'ng@gmail.com', 'mj@nba.com', 'cdiou@hua.gr'],
        'absent': ['pg@gmail.com', 'gfragi@hua.gr', 'staff@gmail.com', 'michalak@hua.gr', 'evangelf@hua.gr',
                   'prizomil@hua.gr'],
        'location': 'Μέσω τηλεδιάσκεψης',
        'date_and_time': '15/04/2024 11:00',
        'notes': 'Πρώτη συνεδρίαση για την εξέταση φακέλου υποψηφίου.',
        'class_type': Meeting,
    },
    '2 - (Παλιό) Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών': {
        'index': 2,
        'collective_body': '(Παλιό) Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών',
        'present': ['president@gmail.com', 'thkam@hua.gr', 'gdede@hua.gr', 'mara@hua.gr', 'ng@gmail.com',
                    'pg@gmail.com', 'mj@nba.com', 'gfragi@hua.gr', 'cdiou@hua.gr', 'michalak@hua.gr',
                    'prizomil@hua.gr'],
        'absent': ['gdimitra@hua.gr', 'staff@gmail.com', 'evangelf@hua.gr'],
        'location': 'Μέσω τηλεδιάσκεψης',
        'date_and_time': '10/12/2025 12:30',
        'notes': 'Τελική αξιολόγηση και έκδοση απόφασης εξέλιξης.',
        'class_type': Meeting,
    },
}

SUBJECT_TYPES = {
    'Ακαδημαϊκό': {
        'title_gr': 'Ακαδημαϊκό',
        'title_en': 'Academic ',
        'created_by': 'apresvelou@hua.gr',
	'updated_by': 'apresvelou@hua.gr',
        'class_type': SubjectType,
    },
    'Διοικητικό': {
        'title_gr': 'Διοικητικό',
        'title_en': 'Administrative',
        'created_by': 'apresvelou@hua.gr',
	'updated_by': 'apresvelou@hua.gr',
        'class_type': SubjectType,
    },
    'Οικονομικό': {
        'title_gr': 'Οικονομικό',
        'title_en': 'Financial',
        'created_by': 'mysec@hua.gr',
	'updated_by': 'mysec@hua.gr',
        'class_type': SubjectType,
    },
    'Προσωπικού': {
        'title_gr': 'Προσωπικού',
        'title_en': 'Personnel',
        'created_by': 'apresvelou@hua.gr',
	'updated_by': 'apresvelou@hua.gr',
        'class_type': SubjectType,
    },
    'Φοιτητικό': {
        'title_gr': 'Φοιτητικό',
        'title_en': 'Student',
        'created_by': 'apresvelou@hua.gr',
	'updated_by': 'apresvelou@hua.gr',
        'class_type': SubjectType,
    },
    'Μεταπτυχιακών Σπουδών': {
        'title_gr': 'Μεταπτυχιακών Σπουδών',
        'title_en': 'Postgraduate Studies',
        'created_by': 'itpsec@hua.gr',
	'updated_by': 'itpsec@hua.gr',
        'class_type': SubjectType,
    },
    'Εξέλιξης Καθηγητή': {
        'title_gr': 'Εξέλιξης Καθηγητή',
        'title_en': 'Professor Promotion',
        'created_by': 'mysec@hua.gr',
	'updated_by': 'mysec@hua.gr',
        'class_type': SubjectType,
    },
    'Θεσμικό': {
        'title_gr': 'Θεσμικό',
        'title_en': 'Institutional',
        'created_by': 'mysec@hua.gr',
	'updated_by': 'mysec@hua.gr',
        'class_type': SubjectType,
    },
}

SUBJECT_CATEGORIES = {
    'Πρόγραμμα Σπουδών': {
        'title_gr': 'Πρόγραμμα Σπουδών',
        'title_en': 'Curriculum',
        'created_by': 'apresvelou@hua.gr',
	'updated_by': 'apresvelou@hua.gr',
        'class_type': SubjectCategory,
    },
    'Αναθέσεις Διδακτικού Έργου': {
        'title_gr': 'Αναθέσεις Διδακτικού Έργου',
        'title_en': 'Teaching Assignments',
        'created_by': 'apresvelou@hua.gr',
	'updated_by': 'apresvelou@hua.gr',
        'class_type': SubjectCategory,
    },
    'Αιτήματα Φοιτητών': {
        'title_gr': 'Αιτήματα Φοιτητών',
        'title_en': 'Student Requests',
        'created_by': 'apresvelou@hua.gr',
	'updated_by': 'apresvelou@hua.gr',
        'class_type': SubjectCategory,
    },
    'Εισαγωγή Μεταπτυχιακών Φοιτητών': {
        'title_gr': 'Εισαγωγή Μεταπτυχιακών Φοιτητών',
        'title_en': 'Postgraduate Admissions',
        'created_by': 'itpsec@hua.gr',
	'updated_by': 'itpsec@hua.gr',
        'class_type': SubjectCategory,
    },
    'Αξιολόγηση Υποψηφίων Μεταπτυχιακών': {
        'title_gr': 'Αξιολόγηση Υποψηφίων Μεταπτυχιακών',
        'title_en': 'Postgraduate Candidate Evaluation',
        'created_by': 'itpsec@hua.gr',
	'updated_by': 'itpsec@hua.gr',
        'class_type': SubjectCategory,
    },
    'Πρόσληψη Προσωπικού': {
        'title_gr': 'Πρόσληψη Προσωπικού',
        'title_en': 'Personnel Recruitment',
        'created_by': 'apresvelou@hua.gr',
	'updated_by': 'apresvelou@hua.gr',
        'class_type': SubjectCategory,
    },
    'Εξέλιξη Καθηγητών': {
        'title_gr': 'Εξέλιξη Καθηγητών',
        'title_en': 'Professor Promotion',
        'created_by': 'mysec@hua.gr',
	'updated_by': 'mysec@hua.gr',
        'class_type': SubjectCategory,
    },
    'Εκλεκτορική Διαδικασία': {
        'title_gr': 'Εκλεκτορική Διαδικασία',
        'title_en': 'Electoral Procedure',
        'created_by': 'mysec@hua.gr',
	'updated_by': 'mysec@hua.gr',
        'class_type': SubjectCategory,
    },
    'Προϋπολογισμός': {
        'title_gr': 'Προϋπολογισμός',
        'title_en': 'Budget',
        'created_by': 'mysec@hua.gr',
	'updated_by': 'mysec@hua.gr',
        'class_type': SubjectCategory,
    },
    'Προμήθειες': {
        'title_gr': 'Προμήθειες',
        'title_en': 'Procurement',
        'created_by': 'mysec@hua.gr',
	'updated_by': 'mysec@hua.gr',
        'class_type': SubjectCategory,
    },
    'Υποδομές και Εξοπλισμός': {
        'title_gr': 'Υποδομές και Εξοπλισμός',
        'title_en': 'Infrastructure and Equipment',
        'created_by': 'mysec@hua.gr',
	'updated_by': 'mysec@hua.gr',
        'class_type': SubjectCategory,
    },
    'Στρατηγικός Σχεδιασμός Πανεπιστημίου': {
        'title_gr': 'Στρατηγικός Σχεδιασμός Πανεπιστημίου',
        'title_en': 'University Strategic Planning',
        'created_by': 'mysec@hua.gr',
	'updated_by': 'mysec@hua.gr',
        'class_type': SubjectCategory,
    },
    'Κανονισμοί και Θεσμικό Πλαίσιο': {
        'title_gr': 'Κανονισμοί και Θεσμικό Πλαίσιο',
        'title_en': 'Regulations and Institutional Framework',
        'created_by': 'mysec@hua.gr',
	'updated_by': 'mysec@hua.gr',
        'class_type': SubjectCategory,
    },
    'Διοικητικός Προγραμματισμός': {
        'title_gr': 'Διοικητικός Προγραμματισμός',
        'title_en': 'Administrative Planning',
        'created_by': 'mysec@hua.gr',
	'updated_by': 'mysec@hua.gr',
        'class_type': SubjectCategory,
    },
    'Έγκριση Πρακτικών': {
        'title_gr': 'Έγκριση Πρακτικών',
        'title_en': 'Approval of Minutes',
        'created_by': 'apresvelou@hua.gr',
	'updated_by': 'apresvelou@hua.gr',
        'class_type': SubjectCategory,
    },
    'Γενικά Θέματα': {
        'title_gr': 'Γενικά Θέματα',
        'title_en': 'General Subjects',
        'created_by': 'mysec@hua.gr',
	'updated_by': 'mysec@hua.gr',
        'class_type': SubjectCategory,
    },
}

SUBJECTS = {
    '1 - Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής': {
        'index': 1,
        'type': 'Ακαδημαϊκό',
        'category': 'Πρόγραμμα Σπουδών',
        'applicant_user': 'it2022057@hua.gr',
        'program': 'UND',
        'department': 'IT',
        'school': 'DT',
        'collective_body': 'Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής',
        'notes': 'Έγκριση τροποποιήσεων στο προπτυχιακό πρόγραμμα σπουδών.',
        'class_type': Subject,
    },
    '2 - Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής': {
        'index': 2,
        'type': 'Ακαδημαϊκό',
        'category': 'Αναθέσεις Διδακτικού Έργου',
        'applicant_user': 'it2022057@hua.gr',
        'program': 'UND',
        'department': 'IT',
        'school': 'DT',
        'collective_body': 'Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής',
        'notes': 'Κατανομή διδακτικού έργου για το νέο ακαδημαϊκό έτος.',
        'class_type': Subject,
    },
    '3 - Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής': {
        'index': 3,
        'type': 'Φοιτητικό',
        'category': 'Αιτήματα Φοιτητών',
        'applicant_user': 'it2022057@hua.gr',
        'program': 'UND',
        'department': 'IT',
        'school': 'DT',
        'collective_body': 'Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής',
        'notes': 'Εξέταση αιτήματος αναγνώρισης μαθημάτων φοιτητή.',
        'class_type': Subject,
    },
    '1 - Σύγκλητος': {
        'index': 1,
        'type': 'Θεσμικό',
        'category': 'Κανονισμοί και Θεσμικό Πλαίσιο',
        'applicant_user': 'smanolas@gmail.com',
        'collective_body': 'Σύγκλητος',
        'notes': 'Έγκριση τροποποίησης του εσωτερικού κανονισμού του Πανεπιστημίου.',
        'class_type': Subject,
    },
    '2 - Σύγκλητος': {
        'index': 2,
        'type': 'Οικονομικό',
        'category': 'Προϋπολογισμός',
        'applicant_user': 'smanolas@gmail.com',
        'collective_body': 'Σύγκλητος',
        'notes': 'Έγκριση του ετήσιου προϋπολογισμού του Πανεπιστημίου.',
        'class_type': Subject,
    },
    '3 - Σύγκλητος': {
        'index': 3,
        'type': 'Θεσμικό',
        'category': 'Στρατηγικός Σχεδιασμός Πανεπιστημίου',
        'applicant_user': 'smanolas@gmail.com',
        'collective_body': 'Σύγκλητος',
        'notes': 'Έγκριση του στρατηγικού σχεδιασμού για την επόμενη τετραετία.',
        'class_type': Subject,
    },
    '1 - Όργανο Αξιολόγησης Υποψηφίων Μεταπτυχιακών': {
        'index': 1,
        'type': 'Μεταπτυχιακών Σπουδών',
        'category': 'Αξιολόγηση Υποψηφίων Μεταπτυχιακών',
        'applicant_user': 'it2022029@hua.gr',
        'program': 'CSI',
        'department': 'IT',
        'school': 'DT',
        'collective_body': 'Όργανο Αξιολόγησης Υποψηφίων Μεταπτυχιακών',
        'notes': 'Αξιολόγηση αιτήσεων και δικαιολογητικών των υποψηφίων.',
        'class_type': Subject,
    },
    '2 - Όργανο Αξιολόγησης Υποψηφίων Μεταπτυχιακών': {
        'index': 2,
        'type': 'Μεταπτυχιακών Σπουδών',
        'category': 'Εισαγωγή Μεταπτυχιακών Φοιτητών',
        'applicant_user': 'it2022029@hua.gr',
        'program': 'CSI',
        'department': 'IT',
        'school': 'DT',
        'collective_body': 'Όργανο Αξιολόγησης Υποψηφίων Μεταπτυχιακών',
        'notes': 'Κατάρτιση και έγκριση του τελικού πίνακα εισακτέων.',
        'class_type': Subject,
    },
    '1 - Γενική Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής': {
        'index': 1,
        'type': 'Προσωπικού',
        'category': 'Πρόσληψη Προσωπικού',
        'applicant_user': 'byronlouki21@gmail.com',
        'department': 'IT',
        'school': 'DT',
        'collective_body': 'Γενική Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής',
        'notes': 'Έγκριση προκήρυξης θέσης έκτακτου διδακτικού προσωπικού.',
        'class_type': Subject,
    },
    '2 - Γενική Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής': {
        'index': 2,
        'type': 'Διοικητικό',
        'category': 'Έγκριση Πρακτικών',
        'applicant_user': 'byronlouki21@gmail.com',
        'department': 'IT',
        'school': 'DT',
        'collective_body': 'Γενική Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής',
        'notes': 'Έγκριση των πρακτικών της προηγούμενης συνεδρίασης.',
        'class_type': Subject,
    },
    '1 - Όργανο Διοίκησης': {
        'index': 1,
        'type': 'Διοικητικό',
        'category': 'Διοικητικός Προγραμματισμός',
        'applicant_user': 'smanolas@gmail.com',
        'collective_body': 'Όργανο Διοίκησης',
        'notes': 'Έγκριση του ετήσιου διοικητικού προγραμματισμού.',
        'class_type': Subject,
    },
    '2 - Όργανο Διοίκησης': {
        'index': 2,
        'type': 'Οικονομικό',
        'category': 'Προμήθειες',
        'applicant_user': 'smanolas@gmail.com',
        'collective_body': 'Όργανο Διοίκησης',
        'notes': 'Έγκριση προμήθειας νέου πληροφοριακού εξοπλισμού.',
        'class_type': Subject,
    },
    '1 - (Παλιό) Όργανο Διοίκησης': {
        'index': 1,
        'type': 'Οικονομικό',
        'category': 'Υποδομές και Εξοπλισμός',
        'applicant_user': 'byronlouki21@gmail.com',
        'collective_body': '(Παλιό) Όργανο Διοίκησης',
        'notes': 'Έγκριση αναβάθμισης εργαστηριακού εξοπλισμού.',
        'class_type': Subject,
    },
    '1 - Πρυτανικό Όργανο': {
        'index': 1,
        'type': 'Διοικητικό',
        'category': 'Διοικητικός Προγραμματισμός',
        'applicant_user': 'applicant@gmail.com',
        'collective_body': 'Πρυτανικό Όργανο',
        'notes': 'Προγραμματισμός διοικητικών ενεργειών της Πρυτανείας.',
        'class_type': Subject,
    },
    '2 - Πρυτανικό Όργανο': {
        'index': 2,
        'type': 'Θεσμικό',
        'category': 'Γενικά Θέματα',
        'applicant_user': 'applicant@gmail.com',
        'collective_body': 'Πρυτανικό Όργανο',
        'notes': 'Συζήτηση θεμάτων γενικής λειτουργίας του Πανεπιστημίου.',
        'class_type': Subject,
    },
    '1 - Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών': {
        'index': 1,
        'type': 'Εξέλιξης Καθηγητή',
        'category': 'Εκλεκτορική Διαδικασία',
        'applicant_user': 'applicant@gmail.com',
        'department': 'IT',
        'school': 'DT',
        'collective_body': 'Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών',
        'notes': 'Έλεγχος πληρότητας του φακέλου του υποψηφίου.',
        'class_type': Subject,
    },
    '2 - Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών': {
        'index': 2,
        'type': 'Εξέλιξης Καθηγητή',
        'category': 'Εξέλιξη Καθηγητών',
        'applicant_user': 'applicant@gmail.com',
        'department': 'IT',
        'school': 'DT',
        'collective_body': 'Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών',
        'notes': 'Αξιολόγηση και τελική κρίση για την εξέλιξη του υποψηφίου.',
        'class_type': Subject,
    },
    '1 - (Παλιό) Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών': {
        'index': 1,
        'type': 'Εξέλιξης Καθηγητή',
        'category': 'Εξέλιξη Καθηγητών',
        'applicant_user': 'smanolas@gmail.com',
        'department': 'IT',
        'school': 'DT',
        'collective_body': '(Παλιό) Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών',
        'notes': 'Ιστορική απόφαση εξέλιξης μέλους ΔΕΠ.',
        'class_type': Subject,
    },
}

DECISIONS = {
    '1 - Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής': {
        'title': Decision.TITLE_APPROVAL,
        'subject': ('Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής', 1),
        'class_type': Decision,
    },
    '2 - Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής': {
        'title': Decision.TITLE_APPROVAL,
        'subject': ('Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής', 2),
        'class_type': Decision,
    },
    '3 - Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής': {
        'title': Decision.TITLE_REJECTION,
        'subject': ('Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής', 3),
        'class_type': Decision,
    },
    '1 - Σύγκλητος': {
        'title': Decision.TITLE_APPROVAL,
        'subject': ('Σύγκλητος', 1),
        'class_type': Decision,
    },
    '2 - Σύγκλητος': {
        'title': Decision.TITLE_PENDING,
        'subject': ('Σύγκλητος', 2),
        'class_type': Decision,
    },
    '3 - Σύγκλητος': {
        'title': Decision.TITLE_APPROVAL,
        'subject': ('Σύγκλητος', 3),
        'class_type': Decision,
    },
    '1 - Όργανο Αξιολόγησης Υποψηφίων Μεταπτυχιακών': {
        'title': Decision.TITLE_APPROVAL,
        'subject': ('Όργανο Αξιολόγησης Υποψηφίων Μεταπτυχιακών', 1),
        'class_type': Decision,
    },
    '2 - Όργανο Αξιολόγησης Υποψηφίων Μεταπτυχιακών': {
        'title': Decision.TITLE_APPROVAL,
        'subject': ('Όργανο Αξιολόγησης Υποψηφίων Μεταπτυχιακών', 2),
        'class_type': Decision,
    },
    '1 - Γενική Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής': {
        'title': Decision.TITLE_PENDING,
        'subject': ('Γενική Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής', 1),
        'class_type': Decision,
    },
    '2 - Γενική Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής': {
        'title': Decision.TITLE_APPROVAL,
        'subject': ('Γενική Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής', 2),
        'class_type': Decision,
    },
    '1 - Όργανο Διοίκησης': {
        'title': Decision.TITLE_APPROVAL,
        'subject': ('Όργανο Διοίκησης', 1),
        'class_type': Decision,
    },
    '2 - Όργανο Διοίκησης': {
        'title': Decision.TITLE_REJECTION,
        'subject': ('Όργανο Διοίκησης', 2),
        'class_type': Decision,
    },
    '1 - (Παλιό) Όργανο Διοίκησης': {
        'title': Decision.TITLE_APPROVAL,
        'subject': ('(Παλιό) Όργανο Διοίκησης', 1),
        'class_type': Decision,
    },
    '1 - Πρυτανικό Όργανο': {
        'title': Decision.TITLE_APPROVAL,
        'subject': ('Πρυτανικό Όργανο', 1),
        'class_type': Decision,
    },
    '2 - Πρυτανικό Όργανο': {
        'title': Decision.TITLE_PENDING,
        'subject': ('Πρυτανικό Όργανο', 2),
        'class_type': Decision,
    },
    '1 - Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών': {
        'title': Decision.TITLE_APPROVAL,
        'subject': ('Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών', 1),
        'class_type': Decision,
    },
    '2 - Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών': {
        'title': Decision.TITLE_APPROVAL,
        'subject': ('Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών', 2),
        'class_type': Decision,
    },
    '1 - (Παλιό) Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών': {
        'title': Decision.TITLE_APPROVAL,
        'subject': ('(Παλιό) Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών', 1),
        'class_type': Decision,
    },
}

APPLICATIONS = {
    'Αίτημα τροποποίησης προγράμματος σπουδών': {
        'applicant': 'it2022057@hua.gr',
        'request_subject': 'Αίτημα τροποποίησης προγράμματος σπουδών',
        'description': 'Παρακαλώ να εξεταστούν οι προτεινόμενες αλλαγές στο προπτυχιακό πρόγραμμα σπουδών.',
        'subject': ('Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής', 1),
        'class_type': Application,
    },
    'Αίτημα εξέτασης ανάθεσης διδακτικού έργου': {
        'applicant': 'it2022057@hua.gr',
        'request_subject': 'Αίτημα εξέτασης ανάθεσης διδακτικού έργου',
        'description': 'Υποβάλλεται αίτημα για εξέταση της κατανομής του διδακτικού έργου του νέου ακαδημαϊκού έτους.',
        'subject': ('Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής', 2),
        'class_type': Application,
    },
    'Αίτημα αναγνώρισης μαθημάτων': {
        'applicant': 'it2022057@hua.gr',
        'request_subject': 'Αίτημα αναγνώρισης μαθημάτων',
        'description': 'Παρακαλώ να εξεταστεί η αναγνώριση μαθημάτων που έχουν ολοκληρωθεί σε άλλο πρόγραμμα σπουδών.',
        'subject': ('Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής', 3),
        'class_type': Application,
    },
    'Αίτημα τροποποίησης εσωτερικού κανονισμού': {
        'applicant': 'smanolas@gmail.com',
        'request_subject': 'Αίτημα τροποποίησης εσωτερικού κανονισμού',
        'description': 'Υποβάλλεται πρόταση τροποποίησης επιλεγμένων άρθρων του εσωτερικού κανονισμού του Πανεπιστημίου.',
        'subject': ('Σύγκλητος', 1),
        'class_type': Application,
    },
    'Αίτημα έγκρισης ετήσιου προϋπολογισμού': {
        'applicant': 'smanolas@gmail.com',
        'request_subject': 'Αίτημα έγκρισης ετήσιου προϋπολογισμού',
        'description': 'Παρακαλώ να εξεταστεί και να εγκριθεί ο ετήσιος προϋπολογισμός του Πανεπιστημίου.',
        'subject': ('Σύγκλητος', 2),
        'class_type': Application,
    },
    'Αίτημα έγκρισης στρατηγικού σχεδιασμού': {
        'applicant': 'smanolas@gmail.com',
        'request_subject': 'Αίτημα έγκρισης στρατηγικού σχεδιασμού',
        'description': 'Υποβάλλεται προς εξέταση το σχέδιο στρατηγικής ανάπτυξης του Πανεπιστημίου για την επόμενη τετραετία.',
        'subject': ('Σύγκλητος', 3),
        'class_type': Application,
    },
    'Αίτηση αξιολόγησης υποψηφιότητας ΠΜΣ': {
        'applicant': 'it2022029@hua.gr',
        'request_subject': 'Αίτηση αξιολόγησης υποψηφιότητας ΠΜΣ',
        'description': 'Υποβάλλεται αίτηση και τα απαραίτητα δικαιολογητικά για την αξιολόγηση της υποψηφιότητας στο ΠΜΣ.',
        'subject': ('Όργανο Αξιολόγησης Υποψηφίων Μεταπτυχιακών', 1),
        'class_type': Application,
    },
    'Αίτημα εισαγωγής σε μεταπτυχιακό πρόγραμμα': {
        'applicant': 'it2022029@hua.gr',
        'request_subject': 'Αίτημα εισαγωγής σε μεταπτυχιακό πρόγραμμα',
        'description': 'Παρακαλώ να εξεταστεί η ένταξή μου στον τελικό πίνακα εισακτέων του μεταπτυχιακού προγράμματος.',
        'subject': ('Όργανο Αξιολόγησης Υποψηφίων Μεταπτυχιακών', 2),
        'class_type': Application,
    },
    'Αίτημα προκήρυξης θέσης διδάσκοντα': {
        'applicant': 'byronlouki21@gmail.com',
        'request_subject': 'Αίτημα προκήρυξης θέσης διδάσκοντα',
        'description': 'Υποβάλλεται αίτημα για την προκήρυξη θέσης έκτακτου διδακτικού προσωπικού.',
        'subject': ('Γενική Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής', 1),
        'class_type': Application,
    },
    'Αίτημα έγκρισης πρακτικών': {
        'applicant': 'byronlouki21@gmail.com',
        'request_subject': 'Αίτημα έγκρισης πρακτικών',
        'description': 'Παρακαλώ να εγκριθούν τα πρακτικά της προηγούμενης συνεδρίασης της Γενικής Συνέλευσης.',
        'subject': ('Γενική Συνέλευση Τμήματος Πληροφορικής και Τηλεματικής', 2),
        'class_type': Application,
    },
    'Αίτημα έγκρισης διοικητικού προγραμματισμού': {
        'applicant': 'smanolas@gmail.com',
        'request_subject': 'Αίτημα έγκρισης διοικητικού προγραμματισμού',
        'description': 'Υποβάλλεται προς έγκριση ο ετήσιος διοικητικός προγραμματισμός του Πανεπιστημίου.',
        'subject': ('Όργανο Διοίκησης', 1),
        'class_type': Application,
    },
    'Αίτημα προμήθειας πληροφοριακού εξοπλισμού': {
        'applicant': 'smanolas@gmail.com',
        'request_subject': 'Αίτημα προμήθειας πληροφοριακού εξοπλισμού',
        'description': 'Παρακαλώ να εγκριθεί η προμήθεια νέων υπολογιστών και περιφερειακού εξοπλισμού.',
        'subject': ('Όργανο Διοίκησης', 2),
        'class_type': Application,
    },
    'Αίτημα αναβάθμισης εργαστηριακού εξοπλισμού': {
        'applicant': 'byronlouki21@gmail.com',
        'request_subject': 'Αίτημα αναβάθμισης εργαστηριακού εξοπλισμού',
        'description': 'Υποβάλλεται αίτημα αντικατάστασης και αναβάθμισης του εργαστηριακού εξοπλισμού.',
        'subject': ('(Παλιό) Όργανο Διοίκησης', 1),
        'class_type': Application,
    },
    'Αίτημα προγραμματισμού ενεργειών Πρυτανείας': {
        'applicant': 'applicant@gmail.com',
        'request_subject': 'Αίτημα προγραμματισμού ενεργειών Πρυτανείας',
        'description': 'Παρακαλώ να εξεταστεί ο προγραμματισμός των διοικητικών ενεργειών της Πρυτανείας.',
        'subject': ('Πρυτανικό Όργανο', 1),
        'class_type': Application,
    },
    'Αίτημα εξέτασης θέματος λειτουργίας': {
        'applicant': 'applicant@gmail.com',
        'request_subject': 'Αίτημα εξέτασης θέματος λειτουργίας',
        'description': 'Υποβάλλεται αίτημα συζήτησης θέματος που αφορά τη γενική λειτουργία του Πανεπιστημίου.',
        'subject': ('Πρυτανικό Όργανο', 2),
        'class_type': Application,
    },
    'Αίτημα ελέγχου φακέλου εξέλιξης': {
        'applicant': 'applicant@gmail.com',
        'request_subject': 'Αίτημα ελέγχου φακέλου εξέλιξης',
        'description': 'Παρακαλώ να πραγματοποιηθεί έλεγχος πληρότητας του φακέλου υποψηφιότητας για εξέλιξη.',
        'subject': ('Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών', 1),
        'class_type': Application,
    },
    'Αίτηση εξέλιξης σε ανώτερη βαθμίδα': {
        'applicant': 'applicant@gmail.com',
        'request_subject': 'Αίτηση εξέλιξης σε ανώτερη βαθμίδα',
        'description': 'Υποβάλλεται αίτηση αξιολόγησης για εξέλιξη σε ανώτερη ακαδημαϊκή βαθμίδα.',
        'subject': ('Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών', 2),
        'class_type': Application,
    },
    'Ιστορική αίτηση εξέλιξης καθηγητή': {
        'applicant': 'smanolas@gmail.com',
        'request_subject': 'Ιστορική αίτηση εξέλιξης καθηγητή',
        'description': 'Αρχειοθετημένη αίτηση εξέλιξης μέλους ΔΕΠ από προηγούμενη εκλεκτορική διαδικασία.',
        'subject': ('(Παλιό) Εκλεκτορικό Όργανο για την Εξέλιξη Καθηγητών', 1),
        'class_type': Application,
    },
}


def get_keys(class_type):
    if class_type in [Meeting]:
        return ['collective_body', 'index']
    elif class_type in [Subject]:
        return ['collective_body', 'index']
    elif class_type in [Decision]:
        return ['subject']
    elif class_type == Application:
        return ['applicant', 'request_subject']
    else:
        return ['title_gr']


def queries(class_type, field_name, value):
    if value:
        if class_type == CollectiveBody:
            if field_name == 'participants':
                return StaffMember.objects.filter(email__in=value)
            if field_name == 'president':
                return StaffMember.objects.get(email=value)
            if field_name == 'secretariat':
                return Secretariat.objects.get(user__email=value)
            if field_name in ['start_date', 'end_date']:
                parsed_datetime = datetime.strptime(value, settings.DATETIME_FORMAT)
                return timezone.make_aware(parsed_datetime, timezone.get_current_timezone())
        elif class_type == Meeting:
            if field_name == 'collective_body':
                return CollectiveBody.objects.get(title_gr=value)
            if field_name in ['present', 'absent']:
                return StaffMember.objects.filter(email__in=value)
            if field_name == 'date_and_time':
                parsed_datetime = datetime.strptime(value, settings.DATETIME_FORMAT)
                return timezone.make_aware(parsed_datetime, timezone.get_current_timezone())
        elif class_type == Subject:
            if field_name == 'type':
                return SubjectType.objects.get(title_gr=value)
            if field_name == 'category':
                return SubjectCategory.objects.get(title_gr=value)
            if field_name == 'applicant_user':
                return User.objects.get(email=value)
            if field_name == 'program':
                return StudyProgram.objects.get(short_en=value)
            if field_name == 'department':
                return Department.objects.get(short_en=value)
            if field_name == 'school':
                return School.objects.get(short_en=value)
            if field_name == 'collective_body':
                return CollectiveBody.objects.get(title_gr=value)
        elif class_type in [SubjectType, SubjectCategory]:
            if field_name in ['created_by', 'updated_by']:
                return User.objects.get(email=value)
        elif class_type == Decision:
            if field_name == 'subject':
                collective_body_title, subject_index = value
                return Subject.objects.get(collective_body__title_gr=collective_body_title, index=subject_index)
        elif class_type == Application:
            if field_name == 'applicant':
                return User.objects.get(email=value)
            if field_name == 'subject':
                collective_body_title, subject_index = value
                return Subject.objects.get(collective_body__title_gr=collective_body_title, index=subject_index)
    return None


def create_or_update_object(field_dict={}):
    class_type = field_dict['class_type']
    keys = get_keys(class_type)
    print(field_dict)
    try:
        query = {}
        for key in keys:
            value = field_dict[key]
            q = queries(class_type, key, value)
            query[key] = (q if q is not None else value)
        obj = class_type.objects.get(**query)
    except ObjectDoesNotExist:
        obj = class_type()

    m2m_fields = ['participants', 'present', 'absent']
    m2m_values = {}

    for k, v in field_dict.items():
        if hasattr(class_type, k):
            q = queries(class_type, k, v)
            if q:
                if k in m2m_fields:
                    m2m_values[k] = q
                else:
                    setattr(obj, k, q)
            else:
                setattr(obj, k, v)
    
    # Select who should appear in the created_by/updated_by fields
    if class_type == Application:
        update_user = obj.applicant
    elif class_type == Subject:
        update_user = obj.collective_body.secretariat.user
    elif class_type == Decision:
        update_user = obj.subject.collective_body.secretariat.user
    elif class_type == CollectiveBody:
        update_user = User.objects.get(email='admin@gmail.com', is_superuser=True)
    else:
        update_user = None

    if update_user:
        if not obj.created_by_id:
            obj.created_by = update_user
        obj.updated_by = update_user

    obj.save()

    for field, queryset in m2m_values.items():
        getattr(obj, field).set(queryset)
        obj.save()


def run():
    DICTS = [COLLECTIVE_BODY, MEETINGS, SUBJECT_TYPES, SUBJECT_CATEGORIES, SUBJECTS, DECISIONS, APPLICATIONS]

    for dicts in DICTS:
        for key, obj in dicts.items():
            print(obj)
            create_or_update_object(obj)
