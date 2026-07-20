from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from romanize import romanize

from core.utils import get_lang
from scopes.models import ScopedModelDep, ScopedModelPrg

User = get_user_model()


# Create your models here.

class TitleStrMixin:

    def __str__(self):
        lang = get_lang()
        if lang == 'en':
            if hasattr(self, 'title_en'):
                if self.title_en and (self.title_en != ''):
                    return self.title_en
        return self.title_gr


class PersonStrMixin:

    def __str__(self):
        lang = get_lang()
        if lang == 'en':
            if hasattr(self, 'surname_en') and hasattr(self, 'given_name_en'):
                if self.surname_en and (self.surname_en != '') and self.given_name_en and (self.given_name_en != ''):
                    return self.given_name_en + ' ' + self.surname_en
            return romanize(self.given_name) + ' ' + romanize(self.surname)

        return self.given_name + ' ' + self.surname


class AttachmentFormSetMixin:
    attachment_formset_class = None
    attachment_context_name = 'attachment_formset'
    attachment_prefix = 'attachments'
    # By default, do not pass extra kwargs to the attachment forms
    attachment_form_kwargs = None

    def get_attachment_form_kwargs(self):
        """
        Returns extra kwargs for each form inside the formset.
        Override this only when the attachment form needs something extra,
        for example the current user.
        """
        return self.attachment_form_kwargs or {}

    def get_attachment_formset(self):
        """
        Creates the attachment formset for GET or POST requests
        """

        formset_kwargs = {
            'instance': self.object,
            'prefix': self.attachment_prefix
        }

        # Add form_kwargs only it exists
        form_kwargs = self.get_attachment_form_kwargs()

        if form_kwargs:
            formset_kwargs['form_kwargs'] = form_kwargs

        if self.request.method == 'POST':
            formset_kwargs['data'] = self.request.POST
            formset_kwargs['files'] = self.request.FILES

        return self.attachment_formset_class(**formset_kwargs)

    def get_context_data(self, **kwargs):
        """
        Adds the attachment formset to the template context
        """
        context = super().get_context_data(**kwargs)

        attachment_formset = self.get_attachment_formset()
        context[self.attachment_context_name] = attachment_formset

        if attachment_formset.can_delete:
            for attachment_form in attachment_formset.forms:
                if 'DELETE' in attachment_form.fields:
                    attachment_form.fields['DELETE'].help_text = (
                        _('Πατήστε για να σημειώσετε το συνημμένο προς διαγραφή. Η διαγραφή ολοκληρώνεται με την αποθήκευση !'))

        return context

    def form_valid(self, form):
        """
        Saves the parent model first, then saves its attachments
        """

        context = self.get_context_data(form=form)
        attachment_formset = context[self.attachment_context_name]

        if not attachment_formset.is_valid():
            return self.form_invalid(context)

        response = super().form_valid(form)

        attachment_formset.instance = self.object
        attachment_formset.save()

        return response

    def form_invalid(self, context):
        return self.render_to_response(context)


class TrackedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="%(app_label)s_%(class)s_created")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="%(app_label)s_%(class)s_updated")

    def save(self, *args, update_user=None, **kwargs):

        # Allow passing either a User object or a username
        if isinstance(update_user, str):
            update_user = User.objects.get(username=update_user)

        now = timezone.now()

        self.updated_at = now
        self.updated_by = update_user

        # Only set create information when the object is actually created
        if not self.id:
            self.created_at = now
            self.created_by = update_user

        super().save(*args, **kwargs)


class TrackedScopedProgramModel(ScopedModelPrg, TrackedModel):
    class Meta:
        abstract = True


class TrackedScopedDepartmentModel(ScopedModelDep, TrackedModel):
    class Meta:
        abstract = True


def get_or_create_object(model_class, update_user=None, **kwargs):
    objects = model_class.objects.filter(**kwargs)
    if objects.exists():
        object = objects.first()
    else:
        object = model_class(**kwargs)
        object.save(update_user=update_user)
    return object


def get_latest_or_create(model_class, update_user=None, **kwargs):
    objects = model_class.objects.filter(**kwargs).order_by('-updated_at')
    if objects.exists():
        object = objects.first()
    else:
        object = model_class(**kwargs)
        object.save(update_user=update_user)
    return object
