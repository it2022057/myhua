from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from romanize import romanize

from core.models import PersonStrMixin, TrackedScopedProgramModel
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


class PersonalInfo(TrackedScopedProgramModel):
    class Meta:
        verbose_name = _('Προσωπικά Στοιχεία')
        verbose_name_plural = _('Προσωπικά Στοιχεία')
        ordering = ['pk']

    GENDER_MALE = "M"
    GENDER_FEMALE = "F"
    GENDER_OTHER = "O"

    GENDER_CHOICES = (
        (GENDER_MALE, _("Άρρεν")),
        (GENDER_FEMALE, _("Θήλυ")),
        (GENDER_OTHER, _("Άλλο")),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Χρήστης'))
    given_name = models.CharField(max_length=200, null=True, verbose_name=_('Όνομα'))
    surname = models.CharField(max_length=200, null=True, verbose_name=_('Επώνυμο'))

    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True,
                                   verbose_name=_('Τμήμα'))
    program = models.ForeignKey(StudyProgram, on_delete=models.SET_NULL, blank=True, null=True,
                                verbose_name=_('Πρόγραμμα Σπουδών'))
    email = models.EmailField(null=True, verbose_name=_('Email'))
    secondary_email = models.EmailField(null=True, verbose_name=_('Δεύτερο Email'))
    fathers_name = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Όνομα Πατέρα'))
    date_of_birth = models.DateField(blank=True, null=True, verbose_name=_('Ημ/νία Γέννησης'))
    tin = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('ΑΦΜ'))
    ssn = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('ΑΜΚΑ'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, verbose_name=_('Φύλο'))

    home_address_street = models.CharField(max_length=70, null=True, blank=True, verbose_name=_('Οδός Κατοικίας'))
    home_address_no = models.IntegerField(null=True, blank=True, verbose_name=_('Αριθμός Κατοικίας'))
    home_address_po_box = models.CharField(max_length=30, null=True, blank=True, verbose_name=_('Τ.Κ. Κατοικίας'))
    home_address_city = models.CharField(max_length=70, null=True, blank=True, verbose_name=_('Πόλη Κατοικίας'))
    home_address_country = models.CharField(max_length=70, null=True, default='Ελλάδα', blank=True,
                                            verbose_name=_('Χώρα Κατοικίας'))
    mobile_phone = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('Κινητό Τηλέφωνο'))
    home_phone = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('Τηλέφωνο Κατοικίας'))

    work_address_street = models.CharField(max_length=70, null=True, default='Ομήρου', verbose_name=_('Οδός Εργασίας'))
    work_address_no = models.CharField(max_length=10, null=True, default='9', verbose_name=_('Αριθμός Εργασίας'))
    work_address_po_box = models.CharField(max_length=30, null=True, default='17778', verbose_name=_('Τ.Κ. Εργασίας'))
    work_address_city = models.CharField(max_length=70, null=True, default='Αθήνα', verbose_name=_('Πόλη Εργασίας'))
    work_address_country = models.CharField(max_length=70, null=True, default='Ελλάδα', verbose_name=_('Χώρα Εργασίας'))
    work_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Τηλέφωνο Εργασίας'))
    pic = models.ImageField(null=True, blank=True, upload_to='images/', verbose_name=_('Εικόνα'))

    def __str__(self):
        return _('Προσωπικά στοιχεία χρήστη: ') + self.given_name + ' ' + self.surname

    def scope_query(self, scope):
        if self.staffmember_set.exists():
            staff_member = self.staffmember_set.first()
            return scope['collective_bodies'].filter(Q(participants=staff_member) |
                                                     Q(president=staff_member)).exists()
        else:
            return False

    def save(self, *args, **kwargs):
        user = create_user_if_required(self.email)
        if self.given_name:
            user.first_name = self.given_name

        if self.surname:
            user.last_name = self.surname

        user.save()
        super().save(*args, update_user=self.updated_by, **kwargs)


def create_personal_info_if_required(obj):
    email = obj.email
    given_name = obj.given_name
    surname = obj.surname
    pis = PersonalInfo.objects.filter(email=email)
    if not pis.exists():
        pi = PersonalInfo(email=email, given_name=given_name, surname=surname)
        pi.save()
    else:
        pi = pis.first()
    return pi


class ScopedStaffMemberQuery(ScopedQueryDep):
    def scope_filter(self, scope):
        return self.filter(collectivebody_participants__in=scope['collective_bodies']).distinct()


class StaffMember(PersonStrMixin, ScopedModelDep):
    """
    The basic staff member class. Stores information related to faculty members
    """

    class Meta:
        verbose_name = _('Μέλος Προσωπικού')
        verbose_name_plural = _('Μέλη Προσωπικού')
        ordering = ['pk']

    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Χρήστης'))
    email = models.EmailField(null=True, verbose_name=_('Email'))
    given_name = models.CharField(max_length=50, verbose_name=_('Όνομα'))
    given_name_en = models.CharField(null=True, max_length=50, verbose_name=_('Όνομα (Αγγλικά)'))
    surname = models.CharField(max_length=70, verbose_name=_('Επώνυμο'))
    surname_en = models.CharField(null=True, max_length=70, verbose_name=_('Επώνυμο (Αγγλικά)'))

    display_name = models.CharField(max_length=150, null=True, blank=True, verbose_name=_('Ονοματεπώνυμο'))
    display_name_en = models.CharField(max_length=150, null=True, blank=True, verbose_name=_('Ονοματεπώνυμο (Αγγλικά)'))
    display_name_full = models.CharField(max_length=200, null=True, blank=True,
                                         verbose_name=_('Ονοματεπώνυμο και Ιδιότητα'))

    is_internal = models.BooleanField(null=True, default=True, verbose_name=_('Εσωτερικός Χρήστης'))
    institution = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Ίδρυμα'))
    school = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Σχολή'))
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Τμήμα'))
    internal_department = models.ForeignKey(Department, blank=True, null=True, on_delete=models.SET_NULL,
                                            verbose_name=_('Εσωτερικό Τμήμα'))
    title = models.CharField(max_length=200, null=True, verbose_name=_('Ιδιότητα'))
    personal_info = models.ForeignKey(PersonalInfo, blank=True, null=True, on_delete=models.SET_NULL,
                                      verbose_name=_('Προσωπικά Στοιχεία'))

    objects = ScopedStaffMemberQuery.as_manager()

    can_apply_for_phd = models.BooleanField(null=True, default=False,
                                            verbose_name=_('Δυνατότητα υποβολής αίτησης για διδακτορικό'))
    can_review_phd_apps = models.BooleanField(null=True, default=True,
                                              verbose_name=_('Δυνατότητα αξιολόγησης αιτήσεων για διδακτορικό'))
    can_post_theses = models.BooleanField(null=True, default=True, verbose_name=_('Δυνατότητα δημοσίευσης διατριβών'))

    def scope_query(self, scope):
        return scope['collective_bodies'].filter(id__in=self.collectivebody_participants.values('id')).exists()

    def save(self, *args, **kwargs):
        self.display_name = self.given_name + ' ' + self.surname
        self.display_name_full = self.display_name + ' (' + self.title + ')'
        self.user = create_user_if_required(self.email)
        self.personal_info = create_personal_info_if_required(self)

        if not (self.given_name_en and (self.given_name_en != '')):
            self.given_name_en = romanize(self.given_name)

        if not (self.surname_en and (self.surname_en != '')):
            self.surname_en = romanize(self.surname)

        if not self.is_internal:
            self.internal_department = None

        self.display_name_en = self.given_name_en + ' ' + self.surname_en

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        When deleting a staff member, makes sure his/her personal info does too
        """
        personal_info = self.personal_info
        super().delete(*args, **kwargs)

        if personal_info:
            personal_info.delete()


class CustomUserPermissions(models.Model):
    class Meta:
        verbose_name = _('Προσαρμοσμένο Δικαίωμα Χρήστη')
        verbose_name_plural = _('Προσαρμοσμένα Δικαιώματα Χρήστη')
        permissions = (
            ("is_secretariat", "Is a secretariat user"),
        )
