from django.contrib import admin, messages
from django.templatetags.static import static
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _, ngettext

from accounts.models import StaffMember, PersonalInfo, CustomUserPermissions
from core.admin import DisplayFieldAdminMixin, AuditModelAdmin
from hua_cbms import settings
from .forms import StaffMemberAdminForm


# Register your models here.


@admin.register(StaffMember)
class StaffMemberAdmin(DisplayFieldAdminMixin, admin.ModelAdmin):
    form = StaffMemberAdminForm
    list_per_page = 20
    exclude = ['display_name', 'display_name_en', 'display_name_full']
    list_display = ['id', 'current_display_name', 'email', 'title', 'is_internal', 'can_apply_for_phd', 'can_review_phd_apps',
                    'can_post_theses']
    list_display_links = ['current_display_name']
    list_editable = ['is_internal', 'can_apply_for_phd', 'can_review_phd_apps', 'can_post_theses']
    search_fields = ['display_name', 'display_name_en', 'email']
    list_filter = ['title', 'institution', 'school', 'department', 'is_internal', 'can_apply_for_phd',
                   'can_review_phd_apps', 'can_post_theses']
    autocomplete_fields = ['user', 'personal_info', 'internal_department']
    list_select_related = ['user', 'personal_info', 'internal_department']
    fieldsets = [
        (_('Λογαριασμός Χρήστη'), {
            'fields': ('user', 'personal_info', 'email')
        }),
        (_('Ονοματεπώνυμο'), {
            'fields': (('given_name', 'given_name_en'), ('surname', 'surname_en'))
        }),
        (_('Στοιχεία Ιδρύματος'), {
            'fields': ('title', 'is_internal', 'internal_department', 'institution', 'school', 'department')
        }),
        (_('Δικαιώματα'), {
            'fields': ('can_apply_for_phd', 'can_review_phd_apps', 'can_post_theses'),
        }),
    ]
    actions = ['make_internal_user', 'remove_internal_user', 'allow_phd_applications',
               'disallow_phd_applications', 'allow_phd_reviews', 'disallow_phd_reviews', 'allow_thesis_posting',
               'disallow_thesis_posting']

    class Media:
        js = ('admin/js/jquery.init.js', 'accounts/admin/js/staffmember_internal_department.js')

    @admin.action(description=_('Ορισμός ως εσωτερικοί χρήστες'))
    def make_internal_user(self, request, queryset):
        updated = queryset.update(is_internal=True)
        self.message_user(
            request,
            ngettext(
                '%d Μέλος Προσωπικού ορίστηκε ως εσωτερικός χρήστης ιδρύματος.',
                '%d Μέλη Προσωπικού ορίστηκαν ως εσωτερικοί χρήστες ιδρύματος.',
                updated,
            ) % updated,
            messages.SUCCESS,
        )

    @admin.action(description=_('Κατάργηση κατάστασης εσωτερικού χρήστη'))
    def remove_internal_user(self, request, queryset):
        updated = queryset.update(is_internal=False)
        self.message_user(
            request,
            ngettext(
                '%d Μέλος Προσωπικού έπαψε να είναι εσωτερικός χρήστης ιδρύματος.',
                '%d Μέλη Προσωπικού έπαψαν να είναι εσωτερικοί χρήστες ιδρύματος.',
                updated,
            ) % updated,
            messages.SUCCESS,
        )

    @admin.action(description=_('Προσθήκη δικαιώματος υποβολής διδακτορικής αίτησης'))
    def allow_phd_applications(self, request, queryset):
        updated = queryset.update(can_apply_for_phd=True)
        self.message_user(
            request,
            ngettext(
                'Δόθηκε δικαίωμα υποβολής διδακτορικής αίτησης σε %d Μέλος Προσωπικού.',
                'Δόθηκε δικαίωμα υποβολής διδακτορικής αίτησης σε %d Μέλη Προσωπικού.',
                updated,
            ) % updated,
            messages.SUCCESS,
        )

    @admin.action(description=_('Αφαίρεση δικαιώματος υποβολής διδακτορικής αίτησης'))
    def disallow_phd_applications(self, request, queryset):
        updated = queryset.update(can_apply_for_phd=False)
        self.message_user(
            request,
            ngettext(
                'Αφαιρέθηκε το δικαίωμα υποβολής διδακτορικής αίτησης από %d Μέλος Προσωπικού.',
                'Αφαιρέθηκε το δικαίωμα υποβολής διδακτορικής αίτησης από %d Μέλη Προσωπικού.',
                updated,
            ) % updated,
            messages.SUCCESS,
        )

    @admin.action(description=_('Προσθήκη δικαιώματος αξιολόγησης διδακτορικών αιτήσεων'))
    def allow_phd_reviews(self, request, queryset):
        updated = queryset.update(can_review_phd_apps=True)
        self.message_user(
            request,
            ngettext(
                'Δόθηκε δικαίωμα αξιολόγησης διδακτορικών αιτήσεων σε %d Μέλος Προσωπικού.',
                'Δόθηκε δικαίωμα αξιολόγησης διδακτορικών αιτήσεων σε %d Μέλη Προσωπικού.',
                updated,
            ) % updated,
            messages.SUCCESS,
        )

    @admin.action(description=_('Αφαίρεση δικαιώματος αξιολόγησης διδακτορικών αιτήσεων'))
    def disallow_phd_reviews(self, request, queryset):
        updated = queryset.update(can_review_phd_apps=False)
        self.message_user(
            request,
            ngettext(
                'Αφαιρέθηκε το δικαίωμα αξιολόγησης διδακτορικών αιτήσεων από %d Μέλος Προσωπικού.',
                'Αφαιρέθηκε το δικαίωμα αξιολόγησης διδακτορικών αιτήσεων από %d Μέλη Προσωπικού.',
                updated,
            ) % updated,
            messages.SUCCESS,
        )

    @admin.action(description=_('Προσθήκη δικαιώματος ανάρτησης διπλωματικών εργασιών'))
    def allow_thesis_posting(self, request, queryset):
        updated = queryset.update(can_post_theses=True)
        self.message_user(
            request,
            ngettext(
                'Δόθηκε δικαίωμα ανάρτησης διπλωματικών εργασιών σε %d Μέλος Προσωπικού.',
                'Δόθηκε δικαίωμα ανάρτησης διπλωματικών εργασιών σε %d Μέλη Προσωπικού.',
                updated,
            ) % updated,
            messages.SUCCESS,
        )

    @admin.action(description=_('Αφαίρεση δικαιώματος ανάρτησης διπλωματικών εργασιών'))
    def disallow_thesis_posting(self, request, queryset):
        updated = queryset.update(can_post_theses=False)
        self.message_user(
            request,
            ngettext(
                'Αφαιρέθηκε το δικαίωμα ανάρτησης διπλωματικών εργασιών από %d Μέλος Προσωπικού.',
                'Αφαιρέθηκε το δικαίωμα ανάρτησης διπλωματικών εργασιών από %d Μέλη Προσωπικού.',
                updated,
            ) % updated,
            messages.SUCCESS,
        )


@admin.register(CustomUserPermissions)
class CustomUserPermissionsAdmin(admin.ModelAdmin):
    pass


@admin.register(PersonalInfo)
class PersonalInfoAdmin(AuditModelAdmin):
    readonly_fields = ['pic_preview', 'created_at', 'updated_at', 'created_by', 'updated_by']
    list_display = ['id', 'pic_thumbnail', 'full_name', 'gender', 'email', 'birthday', 'mobile_phone']
    date_hierarchy = 'date_of_birth'
    list_display_links = ['full_name']
    list_editable = ['gender']
    search_fields = ['given_name', 'surname', 'email', 'tin', 'ssn', 'mobile_phone']
    list_filter = ['gender', 'department', 'program', 'home_address_country', 'work_address_country']
    autocomplete_fields = ['user', 'department', 'program']
    list_select_related = ['user', 'department', 'program', 'created_by', 'updated_by']
    fieldsets = [
        (_('Βασικά Στοιχεία'), {
            'fields': ('user', ('given_name', 'surname'), ('department', 'program'))
        }),
        (_('Ευαίσθητα Στοιχεία'), {
            'fields': ('fathers_name', 'date_of_birth', ('tin', 'ssn'), 'gender', 'pic_preview', 'pic')
        }),
        (_('Στοιχεία Επικοινωνίας'), {
            'fields': (('email', 'secondary_email'), ('mobile_phone', 'home_phone', 'work_phone'))
        }),
        (_('Διεύθυνση Κατοικίας'), {
            'fields': (('home_address_street', 'home_address_no'), ('home_address_po_box', 'home_address_city',
                                                                    'home_address_country'))
        }),
        (_('Διεύθυνση Εργασίας'), {
            'fields': (('work_address_street', 'work_address_no'), ('work_address_po_box', 'work_address_city',
                                                                    'work_address_country'))
        }),
        (_('Σημαντικές Ημερομηνίες'), {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by')
        }),
    ]

    class Media:
        js = ('accounts/admin/js/pic_preview.js',)

    @admin.display(description=_('Προεπισκόπηση Εικόνας'))
    def pic_preview(self, obj):
        if obj and obj.pic:
            return mark_safe(
                '<img id="pic-preview-img" src="{}" style="width: 120px; height: 120px; object-fit: cover; '
                ' border-radius: 50%; border: 1px solid #dee2e6; background-color: #fff; padding: .25rem;" />'
                .format(escape(obj.pic.url))
            )
        else:
            return _('Δεν έχει επιλεχθεί εικόνα...')

    @admin.display(description=_('Εικόνα'))
    def pic_thumbnail(self, obj):
        if obj.pic:
            return mark_safe(
                '<img src="{}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 50%; padding: .2rem;" />'
                .format(escape(obj.pic.url))
            )
        elif obj.gender == 'M':
            return mark_safe(
                '<img src="{}" style="width: 70px; height: 70px; object-fit: cover; border-radius: 50%;'
                ' padding: .2rem; border: 1px solid #dee2e6; background-color: #fff;" />'
                .format(static('accounts/images/default_man.png'))
            )
        elif obj.gender == 'F':
            return mark_safe(
                '<img src="{}" style="width: 70px; height: 70px; object-fit: cover; border-radius: 50%;'
                ' padding: .2rem; border: 1px solid #dee2e6; background-color: #fff;" />'
                .format(static('accounts/images/default_woman.png'))
            )
        elif obj.gender == 'O':
            return mark_safe(
                '<img src="{}" style="width: 70px; height: 70px; object-fit: cover; border-radius: 50%;'
                ' padding: .2rem; border: 1px solid #dee2e6; background-color: #fff;" />'
                .format(static('accounts/images/default_other.png'))
            )
        else:
            return mark_safe(
                '<img src="{}" style="width: 70px; height: 70px; object-fit: cover; border-radius: 50%;'
                ' padding: .2rem; border: 1px solid #dee2e6; background-color: #fff;" />'
                .format(static('accounts/images/no_pic2.png'))
            )

    @admin.display(description=_('Ημ/νία Γέννησης'), ordering='date_of_birth')
    def birthday(self, obj):
        if obj.date_of_birth:
            return obj.date_of_birth.strftime(settings.DATE_FORMAT)
        else:
            return '-'

    @admin.display(description=_('Ονοματεπώνυμο'), ordering='given_name')
    def full_name(self, obj):
        return obj.given_name + ' ' + obj.surname
