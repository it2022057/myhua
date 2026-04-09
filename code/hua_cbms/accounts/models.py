from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from romanize import romanize

from core.models import PersonStrMixin
from curricula.models import Department, StudyProgram
from hua_cbms import settings
from scopes.models import ScopedModelDep, ScopedQueryDep

User = get_user_model()
# Create your models here.

def create_user_if_required(email):
    email_split = email.split('@')
    username = email_split[0]
    domain = email_split[1]

    if domain == settings.INTERNAL_DOMAIN:
        if not User.objects.filter(username=username).exists():
            user = User(username=username, email=email)
            user.save()
        else:
            user = User.objects.filter(username=username).first()
    else:
        if not User.objects.filter(email=email).exists():
            user = User(username=email, email=email)
            user.save()
        else:
            user = User.objects.filter(email=email).first()
    return user


class PersonalInfo(ScopedModelDep):
    class Meta:
        verbose_name = _('Προσωπικά Στοιχεία')
        verbose_name_plural = _('Προσωπικά Στοιχεία')

    GENDER_MALE = "M"
    GENDER_FEMALE = "F"
    GENDER_OTHER = "O"

    GENDER_CHOICES = (
        (GENDER_MALE, _("Άρρεν")),
        (GENDER_FEMALE, _("Θήλυ")),
        (GENDER_OTHER, _("Άλλο")),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    given_name = models.CharField(max_length=200, null=True)
    surname = models.CharField(max_length=200, null=True)

    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)
    program = models.ForeignKey(StudyProgram, on_delete=models.SET_NULL, blank=True, null=True)
    email = models.EmailField(null=True)
    secondary_email = models.EmailField(null=True)
    fathers_name = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    tin = models.CharField(max_length=50, null=True, blank=True)
    ssn = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)

    home_address_street = models.CharField(max_length=70, null=True, blank=True)
    home_address_no = models.IntegerField(null=True, blank=True)
    home_address_po_box = models.CharField(max_length=30, null=True, blank=True)
    home_address_city = models.CharField(max_length=70, null=True, blank=True)
    home_address_country = models.CharField(max_length=70, null=True, default='Ελλάδα', blank=True)
    mobile_phone = models.CharField(max_length=30, blank=True, null=True)
    home_phone = models.CharField(max_length=30, blank=True, null=True)

    work_address_street = models.CharField(max_length=70, null=True, default='Ομήρου')
    work_address_no = models.CharField(max_length=10, null=True, default='9')
    work_address_po_box = models.CharField(max_length=30, null=True, default='17778')
    work_address_city = models.CharField(max_length=70, null=True, default='Αθήνα')
    work_address_country = models.CharField(max_length=70, null=True, default='Ελλάδα')
    work_phone = models.CharField(max_length=20, blank=True, null=True)
    pic = models.ImageField(null=True, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)

    def scope_query(self, scope):
        if self.staffmember_set.exists():
            staff_member = self.staffmember_set.first()
            return scope['departments'].filter(id=staff_member.department.id).exists()
        elif self.associate_set.exists():
            associate = self.associate_set.first()
            return scope['departments'].filter(id=associate.department.id).exists()
        elif self.student_set.exists():
            student = self.student_set.first()
            return scope['programs'].filter(id=student.program.id).exists()
        else:
            return False

    def save(self, *args, **kwargs):
        self.display_name = self.email
        user = create_user_if_required(self.email)
        if self.given_name:
            user.first_name = self.given_name

        if self.surname:
            user.last_name = self.surname

        user.save()
        self.user = user
        self.last_update = datetime.now()
        super().save(*args, **kwargs)


def create_personal_info_if_required(obj):
    email = obj.email
    pis = PersonalInfo.objects.filter(email=email)
    if not pis.exists():
        pi = PersonalInfo(email=email)
        pi.save()
    else:
        pi = pis.first()
    return pi


class ScopedStaffMemberQuery(ScopedQueryDep):
    def scope_filter(self, scope):
        return self.filter(collectivebody_participants__in=scope['collective_bodies'])


class StaffMember(PersonStrMixin, ScopedModelDep):
    """
    The basic staff member class. Stores information related to faculty members
    """
    class Meta:
        verbose_name = _('Μέλος Προσωπικού')
        verbose_name_plural = _('Μέλη Προσωπικού')

    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    email = models.EmailField(null=True)
    given_name = models.CharField(max_length=50)
    given_name_en = models.CharField(null=True, max_length=50)
    surname = models.CharField(max_length=70)
    surname_en = models.CharField(null=True, max_length=70)

    display_name = models.CharField(max_length=150, null=True, blank=True)
    display_name_en = models.CharField(max_length=150, null=True, blank=True)
    display_name_full = models.CharField(max_length=200, null=True, blank=True)

    is_internal = models.BooleanField(null=True, default=True)
    institution = models.CharField(max_length=100, blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    internal_department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200, null=True)
    personal_info = models.ForeignKey(PersonalInfo, blank=True, null=True, on_delete=models.SET_NULL)

    objects = ScopedStaffMemberQuery.as_manager()

    can_apply_for_phd = models.BooleanField(null=True, default=False)
    can_review_phd_apps = models.BooleanField(null=True, default=True)
    can_post_theses = models.BooleanField(null=True, default=True)

    def scope_query(self, scope):
        return scope['departments'].filter(id=self.internal_department.id).exists()

    def save(self, *args, **kwargs):
        self.display_name = self.given_name + ' ' + self.surname
        self.display_name_full = self.display_name + ' (' + self.title + ')'
        self.user = create_user_if_required(self.email)
        self.personal_info = create_personal_info_if_required(self)

        if not (self.given_name_en and (self.given_name_en != '')):
            self.given_name_en = romanize(self.given_name)

        if not (self.surname_en and (self.surname_en != '')):
            self.surname_en = romanize(self.surname)

        self.display_name_en = self.given_name_en + ' ' + self.surname_en

        super().save(*args, **kwargs)

class CustomUserPermissions(models.Model):
    class Meta:
        verbose_name = _('Προσαρμοσμένο Δικαίωμα Χρήστη')
        verbose_name_plural = _('Προσαρμοσμένα Δικαιώματα Χρήστη')
        permissions = (
            ("is_secretariat", "Is a secretariat user"),
        )

