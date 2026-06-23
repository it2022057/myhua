from dal import autocomplete
from django.contrib.auth import get_user_model, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from core import views
from core.utils import get_order_by_display_name
from core.views import Section
from hua_cbms import settings
from scopes.models import Secretariat
from .checks import app_urls, is_secretariat, is_staff_member
from .forms import SignUpForm, RegisterForm, PasswordForm, ForgotPasswordForm, StaffForm, PersonalInfoForm
from .models import StaffMember, PersonalInfo
from .utils import complexity_message, get_domain_uri, send_password_link


# Create your views here.

def render_unauthorized_staff(request):
    msg1 = _('Δεν είστε δηλωμένος στο σύστημα ως μέλος του ιδρύματος.')
    return render(request, 'accounts/message.html',
                  context={'message': msg1})


"""
Faculty CRUD views
"""


class SecCreateStaffMember(views.ScopedSecCreateView):
    model = StaffMember
    template_name = 'accounts/show_object.html'
    form_class = StaffForm
    success_url = 'accounts:sec_list_staff_member'
    headline = _('Δημιουργία Μέλους Προσωπικού')
    back_url = ''


class SecUpdateStaffMember(views.ScopedSecUpdateView):
    model = StaffMember
    template_name = 'accounts/show_object.html'
    form_class = StaffForm
    success_url = 'accounts:sec_list_staff_member'
    delete_url = 'accounts:sec_delete_staff_member'
    confirm_modal = True


class SecListStaffMember(views.ScopedSecListView):
    model = StaffMember
    fields = ['display_name', 'title', 'email']
    headers = {
        'display_name': _('Ονοματεπώνυμο'),
        'title': _('Ιδιότητα'),
        'email': _('E-mail'),
    }
    table_title = _('Μέλη Προσωπικού')
    create_url = 'accounts:sec_create_staff_member'
    update_url = 'accounts:sec_update_staff_member'
    extra_buttons = True
    extra_text = _('Προφίλ')
    extra_button_icon = 'person'
    extra_url = 'accounts:sec_personal_info_overview'


class SecDeleteStaffMember(views.ScopedDeleteView):
    model = StaffMember
    success_url = 'subjects:sec_list_staff_member'


class SecUpdatePersonalInfo(views.ScopedSecUpdateView):
    model = PersonalInfo
    form_class = PersonalInfoForm
    success_url = 'accounts:sec_personal_info_overview'
    delete_url = 'accounts:sec_delete_personal_info'
    confirm_modal = True

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
    success_url = 'accounts:sec_personal_info_overview'


class SecPersonalInfoOverviewList(views.SecMultipleSectionView):
    model = StaffMember
    template_name = 'core/multiple_sections.html'
    master_headline = _('Προσωπικά Στοιχεία')
    master_p = _('Παρακάτω ακολουθούν τα προσωπικά στοιχεία του χρήστη, χωρισμένα σε κατηγορίες...')
    update_url = 'accounts:sec_update_personal_info'
    back_url = reverse_lazy('accounts:sec_list_staff_member')

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
        staff_member = StaffMember.objects.get(pk=self.kwargs['pk'])
        obj = PersonalInfo.objects.get(id=staff_member.personal_info_id)

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
        message = _('H πρόκληση να εγγραφείτε έχει λήξει. Θα πρέπει να επαναλάβετε την διαδικασία.')
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
            # message_body = settings.REGISTRATION_MESSAGE.format(url=url)
            # notify.delay(email, settings.REGISTRATION_SUBJECT, message_body)
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


class ApplicantAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        User = get_user_model()
        qs = User.objects.all()
        if self.q:
            qs = qs.filter(username__icontains=self.q)

        return qs.order_by('username')[:10]


class StaffMemberAutocomplete(LoginRequiredMixin, UserPassesTestMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = StaffMember.objects.all()
        if self.q:
            qs = qs.filter(display_name__icontains=self.q) | qs.filter(display_name_en__icontains=self.q)

        return qs.order_by(get_order_by_display_name())[:10]

    def test_func(self):
        return is_staff_member(self.request.user) or is_secretariat(self.request.user)


class SecretariatAutocomplete(LoginRequiredMixin, UserPassesTestMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Secretariat.objects.all()
        if self.q:
            qs = qs.filter(user__username__icontains=self.q)

        return qs.order_by('user')[:10]

    def test_func(self):
        return is_secretariat(self.request.user)
