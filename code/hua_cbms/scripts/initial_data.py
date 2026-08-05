from pathlib import Path

from django.contrib.auth.models import Permission
from django.core.files import File

from curricula.models import StudyProgram, School, Department, Institution
from accounts.models import StaffMember
from hua_cbms import settings
from scopes.models import Secretariat
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

PICS_DIR = Path(settings.BASE_DIR) / 'scripts' / 'initial_pi_pics'

DEFAULT_DUMMY_PASS = 'test1234'

INSTITUTION = {
    'HUA': {
        'title_gr': 'Χαροκόπειο Πανεπιστήμιο',
        'title_en': 'Harokopio University',
        'short_gr': 'ΧΠΑ',
        'short_en': 'HUA',
        'class_type': Institution,
    }
}

SCHOOLS = {
    'DT': {
        'title_gr': 'Ψηφιακής Τεχνολογίας',
        'title_en': 'Digital Technology',
        'short_gr': 'ΨΤ',
        'short_en': 'DT',
        'class_type': School,
        'institution': 'HUA',
    },
    'EG': {
        'title_gr': 'Περιβάλλοντος, Γεωγραφίας και Εφαρμοσμένων Οικονομικών',
        'title_en': 'Environment, Geography and Applied Economics',
        'short_gr': 'ΠΓ',
        'short_en': 'EG',
        'class_type': School,
        'institution': 'HUA',
    },
    'HS': {
        'title_gr': 'Σχολή Επιστημών Υγείας και Αγωγής',
        'title_en': 'School of Health and Education Sciences',
        'short_gr': 'ΕΥ',
        'short_en': 'HS',
        'class_type': School,
        'institution': 'HUA',
    }
}

DEPARTMENTS = {
    'IT': {
        'title_gr': 'Πληροφορικής και Τηλεματικής',
        'title_en': 'Informatics and Telematics',
        'short_gr': 'ΠΤ',
        'short_en': 'IT',
        'school': 'DT',
        'class_type': Department,
    },
    'GEO': {
        'title_gr': 'Γεωγραφίας',
        'title_en': 'Geography',
        'short_gr': 'ΓΕΩ',
        'short_en': 'GEO',
        'school': 'EG',
        'class_type': Department,
    },
    'ESD': {
        'title_gr': 'Οικονομίας και Βιώσιμης Ανάπτυξης',
        'title_en': 'Economics and Sustainable Development',
        'short_gr': 'ΟΒΑ',
        'short_en': 'ESD',
        'school': 'EG',
        'class_type': Department,
    },
    'ND': {
        'title_gr': 'Επιστήμης Διαιτολογίας - Διατροφής',
        'title_en': 'Nutrition and Dietetics',
        'short_gr': 'ΔΔ',
        'short_en': 'ND',
        'school': 'HS',
        'class_type': Department,
    }
}

PROGRAMS = {
    'UND': {
        'title_gr': 'Προπτυχιακό Πρόγραμμα Σπουδών',
        'title_en': 'Undergraduate Program',
        'short_gr': 'ΠΠΣ',
        'short_en': 'UND',
        'code_gr': '7',
        'code_en': '7',
        'type': StudyProgram.UNDERGRADUATE,
        'sis_code': StudyProgram.SIS_UNDERGRADUATE,
        'department': 'IT',
        'active': True,
        'has_thesis': True,
        'thesis_semesters': 2,
        'thesis_report_semesters': 1,
        'thesis_has_report': False,
        'class_type': StudyProgram,
    },
    'CSI': {
        'title_gr': 'Προηγμένες Τεχνολογίες Πληροφορικής και Εφαρμογές',
        'title_en': 'Advances in Computer Science and Information Systems',
        'short_gr': 'ΤΠΕ',
        'short_en': 'CSI',
        'code_gr': '5',
        'code_en': '5',
        'type': StudyProgram.POSTGRADUATE,
        'sis_code': StudyProgram.SIS_MSC_DIT,
        'department': 'IT',
        'active': True,
        'has_thesis': True,
        'thesis_semesters': 1,
        'thesis_report_semesters': 1,
        'thesis_has_report': False,
        'class_type': StudyProgram,
    },
    'APPLIED': {
        'title_gr': 'ΠΜΣ Εφαρμοσμένη Πληροφορική',
        'title_en': 'MSc Applied Informatics',
        'short_gr': 'ΕΦ. ΠΛ.',
        'short_en': 'APPLIED',
        'code_gr': '3',
        'code_en': '3',
        'type': StudyProgram.POSTGRADUATE,
        'sis_code': StudyProgram.SIS_APPLIED,
        'department': 'IT',
        'active': True,
        'has_thesis': True,
        'thesis_semesters': 1,
        'thesis_report_semesters': 1,
        'thesis_has_report': False,
        'class_type': StudyProgram,
    },
    'MPHIL': {
        'title_gr': 'ΠΜΣ Επιστήμη των Υπολογιστών και Πληροφορική',
        'title_en': 'MPhil in Computer Science and Informatics',
        'short_gr': 'ΕΥΠΛ',
        'short_en': 'MPHIL',
        'code_gr': '4',
        'code_en': '4',
        'type': StudyProgram.POSTGRADUATE,
        'sis_code': StudyProgram.SIS_MPHIL,
        'department': 'IT',
        'active': True,
        'has_thesis': True,
        'thesis_semesters': 1,
        'thesis_report_semesters': 1,
        'thesis_has_report': False,
        'class_type': StudyProgram,
    },
    'I&T': {
        'title_gr': 'ΠΜΣ Πληροφορική και Τηλεματική',
        'title_en': 'MSc in Informatics and Telematics',
        'short_gr': 'Π&Τ',
        'short_en': 'I&T',
        'code_gr': '2',
        'code_en': '2',
        'type': StudyProgram.POSTGRADUATE,
        'sis_code': StudyProgram.SIS_MSC_DIT,
        'department': 'IT',
        'active': True,
        'has_thesis': True,
        'thesis_semesters': 1,
        'thesis_report_semesters': 1,
        'thesis_has_report': False,
        'class_type': StudyProgram,
    }
}

STAFF_MEMBERS = {
    'michalak': {
        'username': 'michalak',
        'email': 'michalak@hua.gr',
        'given_name': 'Χρήστος',
        'surname': 'Μιχαλακέλης',
        'is_internal': True,
        'title': 'Καθηγητής',
        'institution': 'Χαροκόπειο Πανεπιστήμιο',
        'school': 'Ψηφιακής Τεχνολογίας',
        'department': 'Πληροφορικής και Τηλεματικής',
        'internal_department': 'IT',
        'class_type': StaffMember,
    },
    'cdiou': {
        'username': 'cdiou',
        'email': 'cdiou@hua.gr',
        'given_name': 'Χρήστος',
        'surname': 'Δίου',
        'is_internal': True,
        'title': 'Αναπληρωτής Καθηγητής',
        'institution': 'Χαροκόπειο Πανεπιστήμιο',
        'school': 'Ψηφιακής Τεχνολογίας',
        'department': 'Πληροφορικής και Τηλεματικής',
        'internal_department': 'IT',
        'class_type': StaffMember,
    },
    'gfragi': {
        'username': 'gfragi',
        'email': 'gfragi@hua.gr',
        'given_name': 'Γιώργος',
        'surname': 'Φραγκιαδάκης',
        'is_internal': True,
        'title': 'Εξωτερικός Διδάσκων',
        'institution': 'Χαροκόπειο Πανεπιστήμιο',
        'school': 'Ψηφιακής Τεχνολογίας',
        'department': 'Πληροφορικής και Τηλεματικής',
        'internal_department': 'IT',
        'class_type': StaffMember,
    },
    'mara': {
        'username': 'mara',
        'email': 'mara@hua.gr',
        'given_name': 'Μάρα',
        'surname': 'Νικολαΐδου',
        'is_internal': True,
        'title': 'Καθηγήτρια',
        'institution': 'Χαροκόπειο Πανεπιστήμιο',
        'school': 'Ψηφιακής Τεχνολογίας',
        'department': 'Πληροφορικής και Τηλεματικής',
        'internal_department': 'IT',
        'class_type': StaffMember,
    },
    'gdede': {
        'username': 'gdede',
        'email': 'gdede@hua.gr',
        'given_name': 'Γεωργία',
        'surname': 'Δέδε',
        'is_internal': True,
        'title': 'Επίκουρη Καθηγήτρια',
        'institution': 'Χαροκόπειο Πανεπιστήμιο',
        'school': 'Ψηφιακής Τεχνολογίας',
        'department': 'Πληροφορικής και Τηλεματικής',
        'internal_department': 'IT',
        'class_type': StaffMember,
    },
    'gdimitra': {
        'username': 'gdimitra',
        'email': 'gdimitra@hua.gr',
        'given_name': 'Γεώργιος',
        'surname': 'Δημητρακόπουλος',
        'is_internal': True,
        'title': 'Καθηγητής',
        'institution': 'Χαροκόπειο Πανεπιστήμιο',
        'school': 'Ψηφιακής Τεχνολογίας',
        'department': 'Πληροφορικής και Τηλεματικής',
        'internal_department': 'IT',
        'class_type': StaffMember,
    },
    'thkam': {
        'username': 'thkam',
        'email': 'thkam@hua.gr',
        'given_name': 'Θωμάς',
        'surname': 'Καμαλάκης',
        'is_internal': True,
        'title': 'Καθηγητής',
        'institution': 'Χαροκόπειο Πανεπιστήμιο',
        'school': 'Ψηφιακής Τεχνολογίας',
        'department': 'Πληροφορικής και Τηλεματικής',
        'internal_department': 'IT',
        'class_type': StaffMember,
    },
    'prizomil': {
        'username': 'prizomil',
        'email': 'prizomil@hua.gr',
        'given_name': 'Παναγιώτης',
        'surname': 'Ριζομυλιώτης',
        'is_internal': True,
        'title': 'Αναπληρωτής Καθηγητής',
        'institution': 'Χαροκόπειο Πανεπιστήμιο',
        'school': 'Ψηφιακής Τεχνολογίας',
        'department': 'Πληροφορικής και Τηλεματικής',
        'internal_department': 'IT',
        'class_type': StaffMember,
    },
    'evangelf': {
        'username': 'evangelf',
        'email': 'evangelf@hua.gr',
        'given_name': 'Ευαγγελία',
        'surname': 'Φιλιοπούλου',
        'is_internal': True,
        'title': 'Διδάσκων (με απόσπαση)',
        'institution': 'Χαροκόπειο Πανεπιστήμιο',
        'school': 'Ψηφιακής Τεχνολογίας',
        'department': 'Πληροφορικής και Τηλεματικής',
        'internal_department': 'IT',
        'class_type': StaffMember,
    },
    'president': {
        'username': 'president',
        'email': 'president@gmail.com',
        'given_name': 'Ντέμης',
        'surname': 'Νικολαΐδης',
        'is_internal': False,
        'title': 'Πρόεδρος Πανεπιστημιακού Οργάνου',
        'institution': 'ΑΕΚ',
        'department': 'Διοίκησης Επιχειρήσεων και Οργανισμών',
        'class_type': StaffMember,
    },
    'staff': {
        'username': 'staff',
        'email': 'staff@gmail.com',
        'given_name': 'Πέτρος',
        'surname': 'Μάνταλος',
        'is_internal': False,
        'title': 'Καθηγητής',
        'institution': 'Χαροκόπειο Πανεπιστήμιο',
        'school': 'Ψηφιακής Τεχνολογίας',
        'department': 'Πληροφορικής και Τηλεματικής',
        'internal_department': 'IT',
        'class_type': StaffMember,
    },
    'ng': {
        'username': 'ng',
        'email': 'ng@gmail.com',
        'given_name': 'Νίκος',
        'surname': 'Γκάλης',
        'is_internal': True,
        'title': 'Καθηγητής',
        'institution': 'Χαροκόπειο Πανεπιστήμιο',
        'school': 'Ψηφιακής Τεχνολογίας',
        'department': 'Πληροφορικής και Τηλεματικής',
        'internal_department': 'IT',
        'class_type': StaffMember,
    },
    'pg': {
        'username': 'pg',
        'email': 'pg@gmail.com',
        'given_name': 'Παναγιώτης',
        'surname': 'Γιαννάκης',
        'is_internal': True,
        'title': 'Καθηγητής',
        'institution': 'Χαροκόπειο Πανεπιστήμιο',
        'school': 'Ψηφιακής Τεχνολογίας',
        'department': 'Πληροφορικής και Τηλεματικής',
        'internal_department': 'IT',
        'class_type': StaffMember,
    },
    'mj': {
        'username': 'mj',
        'email': 'mj@nba.com',
        'given_name': 'Michael',
        'surname': 'Jordan',
        'is_internal': False,
        'title': 'Πρόεδρος Πανεπιστημιακού Οργάνου',
        'institution': 'Jordan',
        'department': 'Διοίκησης Επιχειρήσεων και Οργανισμών',
        'class_type': StaffMember,
    }
}

APPLICANTS = {
    'smanolas': {
        'username': 'smanolas',
        'email': 'smanolas@gmail.com',
        'first_name': 'Στέλιος',
        'last_name': 'Μανωλάς',
    },
    'louki': {
        'username': 'louki',
        'email': 'byronlouki21@gmail.com',
        'first_name': 'Louki',
        'last_name': 'Louk',
    },
    'it2022057': {
        'username': 'it2022057',
        'email': 'it2022057@hua.gr',
        'first_name': 'Βύρωνας',
        'last_name': 'Λουκιδέλης',
    },
    'it2022029': {
        'username': 'it2022029',
        'email': 'it2022029@hua.gr',
        'first_name': 'Αριάδνη',
        'last_name': 'Καρακατσανίδη',
    },
    'applicant': {
        'username': 'applicant',
        'email': 'applicant@gmail.com',
        'first_name': 'Applicant',
        'last_name': 'Applicantakios',
    },
}

SECRETARIATS = {
    'UND': {
        'email': 'itsec@hua.gr',
        'first_name': 'Γραμματεία',
        'last_name': 'Τμήματος Πληροφορικής και Τηλεματικής (ΠΠΣ)',
        'programs': ['UND'],
        'departments': None,
        'class_type': Secretariat,
    },
    'CSI + I&T': {
        'email': 'itpsec@hua.gr',
        'first_name': 'Γραμματεία',
        'last_name': 'ΠΜΣ Πληροφορικής και Τηλεματικής',
        'programs': ['CSI', 'I&T'],
        'departments': None,
        'class_type': Secretariat,
    },
    'MPHIL': {
        'email': 'mphilsec@hua.gr',
        'first_name': 'Γραμματεία',
        'last_name': 'MPhil in Computer Science and Informatics',
        'programs': ['MPHIL'],
        'departments': None,
        'class_type': Secretariat,
    },
    'APPLIED': {
        'email': 'applied@hua.gr',
        'first_name': 'Applied',
        'last_name': 'Informatics',
        'programs': ['APPLIED'],
        'departments': None,
        'class_type': Secretariat,
    },
    'apresvelou': {
        'email': 'apresvelou@hua.gr',
        'first_name': 'ANGELIKI - NIKI',
        'last_name': 'PRESVELOU',
        'programs': None,
        'departments': ['IT'],
        'class_type': Secretariat,
    },
    'mysec': {
        'email': 'mysec@hua.gr',
        'first_name': 'Γραμματεία',
        'last_name': 'mysec',
        'programs': None,
        'departments': None,
        'class_type': Secretariat,
    }
}


def get_key(class_type):
    if class_type in [StaffMember]:
        return 'email'
    elif class_type in [Secretariat]:
        return 'programs'
    else:
        return 'short_en'


def queries(class_type, field_name, value):
    if value:
        if class_type == School:
            if field_name == 'institution':
                return Institution.objects.get(short_en=value)
        elif class_type == Department:
            if field_name == 'school':
                return School.objects.get(short_en=value)
        elif class_type == StudyProgram:
            if field_name == 'department':
                return Department.objects.get(short_en=value)
        elif class_type == StaffMember:
            if field_name == 'internal_department':
                return Department.objects.get(short_en=value)
        elif class_type == Secretariat:
            if field_name == 'programs':
                return StudyProgram.objects.filter(short_en__in=value)
            if field_name == 'departments':
                return Department.objects.filter(short_en__in=value)
    return None


def get_or_create_user(username, email, password=DEFAULT_DUMMY_PASS):
    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        user = User()

    user.username = username
    user.set_password(password)
    user.email = email

    user.save()
    return user


def create_or_update_object(field_dict={}):
    class_type = field_dict['class_type']
    key = get_key(class_type)
    print(field_dict)
    try:
        query = {key: field_dict[key]}
        obj = class_type.objects.get(**query)
    except ObjectDoesNotExist:
        obj = class_type()

    if 'email' in field_dict:
        email = field_dict['email']
        username = field_dict['username']
        user = get_or_create_user(username, email)

    if hasattr(class_type, 'user'):
        obj.user = user

    for k, v in field_dict.items():
        if hasattr(class_type, k):
            q = queries(class_type, k, v)
            if q:
                setattr(obj, k, q)
            else:
                setattr(obj, k, v)

    obj.save()

    if hasattr(class_type, 'personal_info'):
        department = None
        for dep in DEPARTMENTS.values():
            if obj.department in (dep['title_gr'], dep['title_en']):
                department = Department.objects.get(short_en=dep['short_en'])
                break

        pi = obj.personal_info
        if not pi.department:
            pi.department = department
        if not pi.pic:
            pic_name = field_dict['username'] + '.jpeg'
            pic_path = PICS_DIR / pic_name
            if pic_path.exists():
                with pic_path.open('rb') as f:
                    pi.pic.save(pic_name, File(f), save=False, )
        pi.save()


def run():
    DICTS = [INSTITUTION, SCHOOLS, DEPARTMENTS, PROGRAMS, STAFF_MEMBERS]

    # Create default superuser if one does not already exist
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser('admin', 'admin@gmail.com', DEFAULT_DUMMY_PASS)

    for dicts in DICTS:
        for key, obj in dicts.items():
            print(obj)
            create_or_update_object(obj)

    for key, applicant in APPLICANTS.items():
        print(applicant)
        user = get_or_create_user(applicant['username'], applicant['email'])

        user.first_name = applicant.get('first_name', '')
        user.last_name = applicant.get('last_name', '')
        user.save(update_fields=['first_name', 'last_name'])

    for key, sec in SECRETARIATS.items():
        print(sec)
        email = sec['email']
        username = email.split('@')[0]
        user = get_or_create_user(username, email)

        user.first_name = sec.get('first_name', '')
        user.last_name = sec.get('last_name', '')
        user.save(update_fields=['first_name', 'last_name'])

        is_secretariat = Permission.objects.get(codename='is_secretariat')
        if is_secretariat not in user.user_permissions.all():
            user.user_permissions.add(is_secretariat)

        try:
            obj = Secretariat.objects.get(user=user)
        except ObjectDoesNotExist:
            obj = Secretariat(user=user)

        obj.save()

        if sec['programs']:
            obj.programs.set(StudyProgram.objects.filter(short_en__in=sec['programs']))
        if sec['departments']:
            obj.departments.set(Department.objects.filter(short_en__in=sec['departments']))

        obj.save()
