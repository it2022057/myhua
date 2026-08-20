from urllib import response

from dal import autocomplete
from django.contrib.auth import get_user_model, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from bodies.models import CollectiveBody
from core import views
from core.utils import get_order_by_display_name
from core.views import Section
from hua_cbms import settings
from mailer.gmail import notify
from scopes.models import Secretariat
from .checks import app_urls, is_secretariat, is_staff_member, is_applicant
from .forms import SignUpForm, RegisterForm, PasswordForm, ForgotPasswordForm, SecStaffForm, SecPersonalInfoForm, SecParticipantsForm
from .models import StaffMember, PersonalInfo
from .utils import complexity_message, get_domain_uri, send_password_link


# Create your views here.

def render_unauthorized_staff(request):
    msg1 = _('Δεν είστε δηλωμένος στο σύστημα ως μέλος του ιδρύματος.')
    return render(request, 'accounts/message.html',
                  context={'message': msg1})


"""
Secretary CRUD views
"""


class SecCreateStaffMember(views.ScopedSecCreateView):
    model = StaffMember
    template_name = 'accounts/show_object.html'
    form_class = SecStaffForm
    success_url = 'accounts:sec_list_staff_members'
    headline = _('Δημιουργία Μέλους Προσωπικού')
    back_url = ''
    success_message = _('Το μέλος του προσωπικού καταχωρήθηκε επιτυχώς.')

    # If the create_button, located at the participants table, is pressed in bodies:sec_overview_collectivebody and the
    # staff member is created, it is important to also automatically add him/her to the participants list of the body
    def form_valid(self, form):
        response = super().form_valid(form)

        next_url = self.request.GET.get('next')

        if 'sec/collectivebody/' in next_url:
            body_id = next_url.split('collectivebody/')[1].split('/')[0]
            body = get_object_or_404(CollectiveBody, pk=body_id)
            body.participants.add(self.object)
            self.success_url = reverse_lazy('bodies:sec_overview_collectivebody')

        return response


class SecUpdateStaffMember(views.ScopedSecUpdateView):
    model = StaffMember
    template_name = 'accounts/show_object.html'
    form_class = SecStaffForm
    success_url = 'accounts:sec_list_staff_members'
    delete_url = 'accounts:sec_delete_staff_member'
    confirm_modal = True
    success_message = _('Το μέλος του προσωπικού ενημερώθηκε επιτυχώς.')


class SecListStaffMember(views.ScopedSecListView):
    model = StaffMember
    fields = ['display_name', 'title', 'email']
    headers = {
        'display_name': _('Ονοματεπώνυμο'),
        'title': _('Ιδιότητα'),
        'email': _('E-mail')
    }
    table_title = _('Μέλη Προσωπικού')
    ordering = ['title', get_order_by_display_name()]
    create_url = 'accounts:sec_create_staff_member'
    update_url = 'accounts:sec_update_staff_member'
    back_url = reverse_lazy('bodies:sec_list_collectivebodies')
    extra_buttons = True
    extra_text = _('Προφίλ')
    extra_button_icon = 'person'
    extra_url = 'accounts:sec_personal_info_overview'


class SecDeleteStaffMember(views.ScopedDeleteView):
    model = StaffMember
    success_url = 'subjects:sec_list_staff_members'
    success_message = _('Το μέλος του προσωπικού διαγράφηκε.')


"""
Participant's Update and List views
"""


class SecUpdateParticipants(views.ScopedSecUpdateView):
    model = CollectiveBody
    form_class = SecParticipantsForm
    success_url = 'bodies:sec_overview_collectivebody'
    confirm_modal = True
    success_message = _('Η λίστα με τους συμμετέχοντες ενημερώθηκε επιτυχώς.')


class SecListParticipants(views.ScopedSecListView):
    model = StaffMember
    fields = ['display_name', 'title', 'email']
    headers = {
        'display_name': _('Ονοματεπώνυμο'),
        'title': _('Ιδιότητα'),
        'email': _('E-mail')
    }
    table_title = _('Συμμετέχοντες')
    ordering = ['title', get_order_by_display_name()]
    create_url = 'accounts:sec_create_staff_member'
    update_url = 'accounts:sec_update_staff_member'
    back_url = reverse_lazy('bodies:sec_list_collectivebodies')
    extra_buttons = True
    extra_text = _('Προφίλ')
    extra_button_icon = 'person'
    extra_url = 'accounts:sec_personal_info_overview'

    def get_queryset(self):
        body = get_object_or_404(CollectiveBody, pk=self.kwargs['pk'])

        return body.participants.all().order_by(*self.ordering)


"""
Secretariat views for viewing, updating and deleting a staff member's personal information

The overview page displays the PersonalInfo object in multiple sections
"""


class SecUpdatePersonalInfo(views.ScopedSecUpdateView):
    model = PersonalInfo
    form_class = SecPersonalInfoForm
    success_url = 'accounts:sec_personal_info_overview'
    delete_url = 'accounts:sec_delete_personal_info'
    confirm_modal = True
    success_message = _('Τα προσωπικά στοιχεία του μέλους ενημερώθηκαν επιτυχώς.')

    def get_object(self, *args, **kwargs):
        pi = get_object_or_404(PersonalInfo, pk=self.kwargs['pi_pk'])

        return pi

    def get_delete_url(self, obj):
        if isinstance(self.delete_url, str):
            return reverse_lazy(
                self.delete_url,
                kwargs={
                    'pi_pk': obj.pk,
                    'pk': obj.staffmember_set.first().pk
                }
            )
        else:
            return self.delete_url


class SecDeletePersonalInfo(views.ScopedDeleteView):
    model = PersonalInfo
    pk_url_kwarg = 'pi_pk'
    success_url = 'accounts:sec_list_staff_members'
    success_message = _('Τα προσωπικά στοιχεία του μέλους διαγράφηκαν.')


class SecPersonalInfoOverviewList(views.SecMultipleSectionView):
    model = StaffMember
    template_name = 'core/multiple_sections.html'
    master_headline = _('Προσωπικά Στοιχεία')
    master_p = _('Παρακάτω ακολουθούν τα προσωπικά στοιχεία του χρήστη, χωρισμένα σε κατηγορίες...')
    update_url = 'accounts:sec_update_personal_info'

    def get_update_url(self, obj):
        if self.update_url:
            return reverse_lazy(
                self.update_url,
                kwargs={
                    'pi_pk': obj.personal_info.pk,
                    'pk': obj.pk
                }
            )
        return None

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        staff_member = get_object_or_404(StaffMember, pk=self.kwargs['pk'])
        obj = get_object_or_404(PersonalInfo, id=staff_member.personal_info_id)

        if staff_member:
            self.master_headline = _('Προσωπικά Στοιχεία: ') + '%s' % str(staff_member)

        self.sections = [
            Section(
                section_title=_('Βασικά Στοιχεία'),
                section_id='section-1',
                fields=['pic', 'given_name', 'surname', 'email', 'secondary_email'],
                headers={
                    'pic': _('Εικόνα'),
                    'given_name': _('Όνομα'),
                    'surname': _('Επώνυμο'),
                    'email': _('E-mail'),
                    'secondary_email': _('2ο E-mail')
                },
                object=obj,
            ),
            Section(
                section_title=_('Προσωπικά Στοιχεία'),
                section_id='section-2',
                fields=['fathers_name', 'date_of_birth', 'gender', 'mobile_phone', 'tin', 'ssn'],
                headers={
                    'fathers_name': _('Όνομα Πατέρα'),
                    'date_of_birth': _('Ημ/νία Γέννησης'),
                    'gender': _('Φύλο'),
                    'mobile_phone': _('Κινητό Τηλέφωνο'),
                    'tin': _('ΑΦΜ'),
                    'ssn': _('ΑΜΚΑ')
                },
                object=obj,
            ),
            Section(
                section_title=_('Στοιχεία Κατοικίας'),
                section_id='section-3',
                fields=[
                    'home_address_street',
                    'home_address_no',
                    'home_address_po_box',
                    'home_address_city',
                    'home_address_country',
                    'home_phone'
                ],
                headers={
                    'home_address_street': _('Οδός Κατοικίας'),
                    'home_address_no': _('Αριθμός Κατοικίας'),
                    'home_address_po_box': _('Τ.Κ. Κατοικίας'),
                    'home_address_city': _('Πόλη Κατοικίας'),
                    'home_address_country': _('Χώρα Κατοικίας'),
                    'home_phone': _('Τηλέφωνο Κατοικίας')
                },
                object=obj,
            ),
            Section(
                section_title=_('Στοιχεία Εργασίας'),
                section_id='section-4',
                fields=[
                    'work_address_street',
                    'work_address_no',
                    'work_address_po_box',
                    'work_address_city',
                    'work_address_country',
                    'work_phone'
                ],
                headers={
                    'work_address_street': _('Οδός Εργασίας'),
                    'work_address_no': _('Αριθμός Εργασίας'),
                    'work_address_po_box': _('Τ.Κ. Εργασίας'),
                    'work_address_city': _('Πόλη Εργασίας'),
                    'work_address_country': _('Χώρα Εργασίας'),
                    'work_phone': _('Τηλέφωνο Εργασίας')
                },
                object=obj,
            ),
        ]


@login_required
def index(request):
    if is_secretariat(request.user):
        return redirect('accounts:dashboard')
    elif is_staff_member(request.user):
        return redirect('accounts:dashboard')

    return redirect('accounts:dashboard')


@login_required
def logout_view(request):
    logout(request)
    msg1 = _('Αποσυνδεθήκατε από το σύστημα. Ευχαριστούμε που χρησιμοποιήσατε την υπηρεσία μας. ')
    msg2 = _('Συνδεθείτε ξανά')
    here = _('εδώ')
    return render(request,
                  'accounts/message.html',
                  context={'message':
                               """
                                 %s </br> </br>
                                 %s <a href="%s"> %s </a>
                                 """ % (msg1, msg2, reverse_lazy('accounts:index'), here)})


def signup(request, token):
    logout(request)
    signer = TimestampSigner()
    try:
        unsigned = signer.unsign_object(token, max_age=settings.INVITATION_REFERENCE_MAX_AGE_SECS)
        email = unsigned['email']
    except SignatureExpired:
        message = _('H πρόσκληση να εγγραφείτε έχει λήξει. Θα πρέπει να επαναλάβετε την διαδικασία.')
        return render(request, 'accounts/message.html', context={'message': message})
    except BadSignature:
        message = _('O σύνδεσμος δεν είναι σωστός!')
        return render(request, 'accounts/message.html', context={'message': message})

    UserModel = get_user_model()

    if UserModel.objects.filter(username=email).count() > 0:
        message = _('Έχετε ήδη εγγραφεί στο σύστημα!')
        return render(request, 'accounts/message.html', context={'message': message})

    if request.method == "POST":

        form = SignUpForm(request.POST, email=email)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            email = cleaned_data['email']
            name = cleaned_data['name']
            surname = cleaned_data['surname']
            password = cleaned_data['password1']
            user = UserModel.objects.create_user(email, email=email, password=password, first_name=name,
                                                 last_name=surname)
            user.save()
            return redirect('accounts:signup_success')
        else:
            alertclass = "alert alert-info"

    else:
        form = SignUpForm(email=email)
        alertclass = "alert alert-info"

    return render(request, "accounts/signup.html",
                  {"form": form, "password_policy": mark_safe(complexity_message()), "alertclass": alertclass})


def signup_success(request):
    msg1 = _('Εγγραφήκατε επιτυχώς στο σύστημα!')
    msg2 = _('Συνδεθείτε ξανά')
    msg3 = _('εδώ')
    return render(request,
                  'accounts/message.html',
                  context={'message':
                               """
                                 %s </br></br>
                                 %s <a href="%s"> %s </a>
                                 """ % (msg1, msg2, reverse_lazy('accounts:index'), msg3)})


def register(request):
    back_url = reverse_lazy('accounts:index')
    domain = get_domain_uri(request)
    if request.method == "POST":

        form = RegisterForm(request.POST)
        if form.is_valid():
            signer = TimestampSigner()
            email = form.cleaned_data['email1']
            signed_data = signer.sign_object({'email': email})
            url = domain + reverse_lazy('accounts:signup', kwargs={'token': signed_data})
            message_body = settings.REGISTRATION_MESSAGE.format(url=url)
            notify.delay(email, settings.REGISTRATION_SUBJECT, message_body)
            return redirect('accounts:register_success')
        else:
            return render(request, "accounts/register.html", {"form": form, "back_url": back_url})
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form, "back_url": back_url})


def register_success(request):
    return render(request,
                  'accounts/message.html',
                  context={'message': _(
                      'Έχει αποσταλλεί e-mail στην διεύθυνση που δηλώσατε για να ενεργοποιήσετε το λογαριασμό σας')})


# Landing page for apps destined for the general public (after registration)
@login_required
def dashboard(request):
    user = request.user
    apps = app_urls(user)
    return render(request,
                  'accounts/landing.html',
                  context={'apps': apps}
                  )


@login_required
def password_change(request):
    user = request.user
    success_url = reverse_lazy('accounts:dashboard')

    if settings.INTERNAL_DOMAIN in user.email:
        msg1 = _(
            'Είστε ιδρυματικός χρήστης. Θα πρέπει να αλλάξετε τον κωδικό χρησιμοποιώντας τα κεντρικά συστήματα του ιδρύματος')
        msg2 = _('Επιστροφή')
        message = """
                <p> %s </p>
                <a href="%s" class="alert-link"> %s </a>
                """ % (msg1, success_url, msg2)
        return render(request, 'accounts/message.html', context={'message': mark_safe(message)})

    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)
            msg1 = _('Ο κωδικός σας έχει αλλάξει.')
            msg2 = _('Επιστροφή')
            message = """
                <p> %s </p>
                </br>
                <a href="%s" class="alert-link"> %s </a>
                """ % (msg1, success_url, msg2)
            return render(request, 'accounts/message.html',
                          context={
                              'message': mark_safe(message),
                              'back_url': success_url})
    else:
        form = PasswordForm()

    return render(request, "accounts/changepassword.html",
                  context={"form": form, "password_policy": mark_safe(complexity_message()),
                           "alertclass": "alert alert-info",
                           "back_url": success_url})


def forgot_password(request):
    back_url = reverse_lazy('accounts:index')
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email1']
            send_password_link(request, email)
            msg = _('Παρακαλούμε ελέγξτε την διεύθυνση ηλεκτρονικού ταχυδρομείου που καταχωρήσατε για την συνέχεια.')
            message = """
                <p> %s </p>
            """ % msg
            return render(request, 'accounts/message.html',
                          context={'message': mark_safe(message), "back_url": back_url})
        else:
            return render(request, "accounts/forgotpassword.html", {"form": form, "back_url": back_url})
    else:
        form = ForgotPasswordForm()
        return render(request, "accounts/forgotpassword.html", {"form": form, "back_url": back_url})


def password_reset_choice(request):
    return render(request, 'accounts/password_reset_choice.html')


def password_token(request, token):
    signer = TimestampSigner()
    try:
        invitation = signer.unsign_object(token, max_age=settings.PASSWORD_RESET_LINK_AGE)
    except SignatureExpired:
        message = _('Ο σύνδεσμος αυτός έχει λήξει.')
        return render(request, 'accounts/message.html', context={'message': message})
    except BadSignature:
        message = _('O σύνδεσμος δεν είναι σωστός!')
        return render(request, 'accounts/message.html', context={'message': message})
    email = invitation['email']
    UserModel = get_user_model()
    user = get_object_or_404(UserModel, email=email)
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            success_url = reverse_lazy('accounts:dashboard')
            msg1 = _('Ο κωδικός σας έχει αλλάξει.')
            msg2 = _('Επιστροφή')
            message = """
                <p> %s </p>
                </br>
                <a href="%s" class="alert-link">%s</a>
                """ % (msg1, success_url, msg2)
            return render(request, 'accounts/message.html', context={'message': mark_safe(message)})
    else:
        form = PasswordForm()

    return render(request, "accounts/changepassword.html",
                  {"form": form, "password_policy": mark_safe(complexity_message()), "alertclass": "alert alert-info"})


class ApplicantAutocomplete(LoginRequiredMixin, UserPassesTestMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        User = get_user_model()

        applicant_ids = []
        for user in User.objects.all():
            if is_applicant(user):
                applicant_ids.append(user.pk)

        qs = User.objects.filter(id__in=applicant_ids)
        if self.q:
            qs = qs.filter(username__icontains=self.q)

        return qs.order_by('username')[:10]

    def test_func(self):
        return is_secretariat(self.request.user)


class ParticipantAutocomplete(ApplicantAutocomplete):
    def get_queryset(self):
        # Get selected collective body
        collective_body_id = self.forwarded.get('collective_body')

        if not collective_body_id:
            return StaffMember.objects.none()


        collective_body = CollectiveBody.objects.get(pk=collective_body_id)

        # Start from the participants of this collective body only
        qs = collective_body.participants.all()

        if collective_body.president:
            # Also include the president, since he/she is not stored in the participants list
            qs = qs | StaffMember.objects.filter(pk=collective_body.president.pk)

        # Get the staff members that are already selected as present or absent
        present_ids = self.get_forwarded_ids('present')
        absent_ids = self.get_forwarded_ids('absent')

        # Exclude already selected present members from the results (prevents choosing the same person again)
        if present_ids:
            qs = qs.exclude(pk__in=present_ids)

        # Exclude already selected absent members from the results (prevents a person from being both present and absent)
        if absent_ids:
            qs = qs.exclude(pk__in=absent_ids)

        if self.q:
            qs = qs.filter(Q(display_name__icontains=self.q) | Q(display_name_en__icontains=self.q))

        return qs.order_by(get_order_by_display_name())[:10]

    def get_forwarded_ids(self, field_name):
        value = self.forwarded.get(field_name)

        if not value:
            return []

        if isinstance(value, list):
            return value

        return [value]


class StaffMemberAutocomplete(ParticipantAutocomplete):
    def get_queryset(self):
        qs = StaffMember.objects.all()

        participant_ids = self.get_forwarded_ids('participants')
        if participant_ids:
            # When selecting a president, exclude staff members already selected as participants
            qs = qs.exclude(pk__in=participant_ids)

        president_id = self.forwarded.get('president')
        if president_id:
            # When selecting participants, exclude the staff member already selected as president
            qs = qs.exclude(pk=president_id)

        if self.q:
            qs = qs.filter(Q(display_name__icontains=self.q) | Q(display_name_en__icontains=self.q))

        return qs.order_by(get_order_by_display_name())[:10]

    def test_func(self):
        return self.request.user.is_superuser or is_secretariat(self.request.user)


class SecretariatAutocomplete(ApplicantAutocomplete):
    def get_queryset(self):
        qs = Secretariat.objects.all()
        if self.q:
            qs = qs.filter(user__username__icontains=self.q)

        return qs.order_by('user')[:10]

    def test_func(self):
        return self.request.user.is_superuser
