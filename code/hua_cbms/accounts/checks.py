import re

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from accounts.app_landings import APPS
from accounts.models import StaffMember
from curricula.models import StudyProgram
from meetings.models import Meeting
from scopes.utils import get_secretariat_scope
from subjects.models import Subject, Decision

User = get_user_model()


def is_internal_user(user):
    return user.email.endswith(settings.INTERNAL_DOMAIN)


def is_external_user(user):
    return not is_internal_user(user)


def is_applicant(user):
    if not user or not user.is_authenticated:
        return False

    return not (is_staff_member(user) or is_secretariat(user))


def is_staff_member(user):
    s = StaffMember.objects.filter(user=user)
    return s.count() == 1


def is_internal_staff_member(user):
    s = StaffMember.objects.filter(user=user, is_internal=True)
    return s.count() == 1


def can_use_theses(user):
    s = StaffMember.objects.filter(user=user)
    if s.exists():
        return s.first().can_post_theses
    return False


def can_review_phd_apps(user):
    s = StaffMember.objects.filter(user=user)
    if s.exists():
        return s.first().can_review_phd_apps
    return False


def is_external_staff_member(user):
    s = StaffMember.objects.filter(user=user, is_internal=False)
    return s.count() == 1


def is_secretariat(user):
    scope = get_secretariat_scope(user)
    return (scope['departments'].count() > 0) | (scope['programs'].count() > 0) | (scope['collective_bodies'].count() > 0)


def is_doctoral_secretariat(user):
    scope = get_secretariat_scope(user)
    return scope['programs'].filter(type=StudyProgram.DOCTORAL)


def can_apply_for_phd(user):
    s = StaffMember.objects.filter(user=user)
    if s.exists():
        return s.first().can_apply_for_phd
    return True


def is_department_secretariat(user):
    scope = get_secretariat_scope(user)
    return scope['departments'].count() > 0


def likely_student_username(user):
    uid = user.username
    return (uid.startswith('it') or uid.startswith('csi') or uid.startswith('ap')) and not (
            (uid == 'itsec') or (uid == 'applied') or (uid == 'apresvelou'))


def get_user_roles(user):
    roles = []

    if isinstance(user, str):
        User = get_user_model()
        user = User.objects.get(username=user)

    if not user or not user.is_authenticated:
        return ['anonymous']

    # --- Secretariat scope (evaluate once) ---
    scope = get_secretariat_scope(user)

    if scope['departments'].exists():
        return ['department_secretariat']

    if scope['programs'].filter(type=StudyProgram.DOCTORAL).exists():
        return ['doctoral_secretariat']

    if scope['programs'].exists():
        return ['secretariat']

    # --- Staff ---
    staff = StaffMember.objects.filter(user=user).first()
    if staff:
        if staff.is_internal:
            roles = ['internal_staff']
        else:
            roles = ['external_staff']

    # --- Simply logged in
    roles.append('logged_in')

    return roles


# def app_urls(user):
#     roles = get_user_roles(user)
#     print(roles)
#     app_dicts = []
#     for role in roles:
#         apps = APPS[role]
#         for app in apps:
#             element = APPS[role][app]
#             print(element)
#             if element not in app_dicts:
#                 app_dicts.append(
#                     element
#                 )

#     return app_dicts

def cond_append_if_not_in(cond, l, lnew):
    if cond:
        for el in lnew:
            if el not in l:
                l.append(el)


def app_urls(user):
    # Check whether the user is a secretariat
    if is_secretariat(user):
        return APPS['secretariat']

    urls = []

    # Staff members and applicants.
    cond_append_if_not_in(is_staff_member(user), urls, APPS['staff_member'])
    cond_append_if_not_in(is_applicant(user), urls, APPS['applicant'])
    cond_append_if_not_in(is_external_user(user), urls, APPS['change_password'])
    return urls


def check_password_complexity(p):
    no_special_chars = 0
    for ch in settings.PASSWORD_SPECIAL_CHARS:
        no_special_chars += p.count(ch)

    has_uppercase = re.search(r'[A-Z]', p)
    has_lowercase = re.search(r'[a-z]', p)
    has_digit = re.search(r'\d', p)

    return has_digit, has_lowercase, has_uppercase, no_special_chars


def validate_password(password1, password2):
    if len(password1) < settings.MIN_LENGTH:
        raise forms.ValidationError(
            _('Πρέπει να χρησιμοποιήσετε τουλάχιστον %d χαρακτήρες για κωδικό') % settings.MIN_LENGTH)

    if password1 != password2:
        raise forms.ValidationError(_('Οι δύο κωδικοί δεν ταιριάζουν!'))

    no_special_chars = 0
    for ch in settings.PASSWORD_SPECIAL_CHARS:
        no_special_chars += password1.count(ch)

    has_uppercase = re.search(r'[A-Z]', password1)
    has_lowercase = re.search(r'[a-z]', password1)
    has_digit = re.search(r'\d', password1)
    has_valid_chars = all(
        ch.isupper() or ch.islower() or ch.isdigit() or ch in settings.PASSWORD_SPECIAL_CHARS
        for ch in password1
    )

    msgs = []
    if not has_valid_chars:
        msgs.append(
            _('Χρησιμοποιήστε μόνο ψηφία από 0 εώς 9, λατινικούς ή τους ειδικούς χαρακτήρες που αναφέρονται παραπάνω.'))

    if not has_digit:
        msgs.append(_('Δεν έχετε χρησιμοποιήσει τουλάχιστον ένα ψηφίο από 0 εώς 9'))

    if not has_uppercase:
        msgs.append(_('Δεν έχετε χρησιμοποιήσει τουλάχιστον ένα λατινικό κεφαλαίο γράμμα'))

    if not has_lowercase:
        msgs.append(_('Δεν έχετε χρησιμοποιήσει τουλάχιστον ένα λατινικό πεζό γράμμα'))

    if no_special_chars < 2:
        msgs.append(_('Δεν έχετε χρησιμοποιήσει τουλάχιστον δύο ειδικούς χαρακτήρες'))

    errors = ''
    for msg in msgs:
        errors += """
        <li> <p> %s </p> </li>
        """ % msg

    if errors != '':
        errors = "<ul>" + errors + "</ul>"
        raise forms.ValidationError(mark_safe(errors))


def validate_meeting_index(index, collective_body, instance=None):
    if index is None or collective_body is None:
        return

    existing_meetings = Meeting.objects.filter(collective_body=collective_body, index=index)
    # Check if another meeting has the same body and index, but ignore the current meeting updating
    if instance and instance.pk:
        existing_meetings = existing_meetings.exclude(pk=instance.pk)

    if existing_meetings.exists():
        raise forms.ValidationError(
            _('Υπάρχει ήδη συνεδρίαση με αυτόν τον αριθμό για το συγκεκριμένο συλλογικό όργανο'))


def validate_subject_index(index, collective_body, instance=None):
    if index is None or collective_body is None:
        return

    existing_subjects = Subject.objects.filter(collective_body=collective_body, index=index)

    # Check if another meeting has the same body and index, but ignore the current meeting updating
    if instance and instance.pk:
        existing_subjects = existing_subjects.exclude(pk=instance.pk)

    if existing_subjects.exists():
        raise forms.ValidationError(_('Υπάρχει ήδη θέμα με αυτόν τον αριθμό για το συγκεκριμένο συλλογικό όργανο'))


def validate_file(file):
    if not file:
        raise forms.ValidationError(_('Παρακαλώ επιλέξτε αρχείο'))


def can_download(parts, request_user):
    from attachments.models import SubjectAttachment, DecisionAttachment, ApplicationAttachment
    from bodyapplications.models import Application

    app_name = parts[0]

    # Unauthenticated users not allowed

    if app_name == 'attachments':

        if not request_user.is_authenticated:
            return False

        attachment_type = parts[1]
        object_id = parts[2]
        file_path = '/'.join(parts)

        if attachment_type == 'subjects':
            subject = get_object_or_404(Subject, pk=object_id)

            attachment_exists = SubjectAttachment.objects.filter(subject=subject, file=file_path).exists()

            if not attachment_exists:
                return False

            if subject.applicant_user == request_user:
                return True

            if is_secretariat(request_user):
                return Subject.objects.sc_filter(user=request_user).filter(pk=subject.pk).exists()
            elif is_staff_member(request_user):
                staff_member = get_object_or_404(StaffMember, user=request_user)
                if subject.collective_body:
                    return subject.collective_body.participants.filter(pk=staff_member.pk).exists()

        elif attachment_type == 'decisions':
            decision = get_object_or_404(Decision, pk=object_id)

            attachment_exists = DecisionAttachment.objects.filter(decision=decision, file=file_path).exists()

            if not attachment_exists:
                return False

            if decision.subject.applicant_user == request_user:
                return True

            if is_secretariat(request_user):
                return Decision.objects.sc_filter(user=request_user).filter(pk=decision.pk).exists()
            elif is_staff_member(request_user):
                staff_member = get_object_or_404(StaffMember, user=request_user)
                if decision.subject.collective_body:
                    return decision.subject.collective_body.participants.filter(pk=staff_member.pk).exists()

        elif attachment_type == 'bodyapplications':
            applicant_username = parts[2]

            attachment = ApplicationAttachment.objects.filter(
                application__applicant__username=applicant_username,
                file=file_path
            ).first()

            if not attachment:
                return False

            if attachment.application.applicant == request_user:
                return True

            if is_secretariat(request_user):
                return Application.objects.sc_filter(user=request_user).filter(pk=attachment.application.pk).exists()

            return False

        return False

    return False
