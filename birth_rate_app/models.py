from django.db import models
from django.contrib.auth import get_user_model
from model_utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from birth_rate_app.choices import (
    LGA,
    GENDER,
)
# Create your models here.

class Hospital(TimeStampedModel):
    user = models.ForeignKey(
        get_user_model(),
        verbose_name=_("User Detail"),
        on_delete=models.CASCADE,
    )
    name = models.CharField(_("Hospital Name"), max_length=100)
    cac = models.CharField(_("CAC"), max_length=100)
    phone_number = models.CharField(_("Hospital Phone Number"), max_length=15)
    address = models.CharField(_("Hospital Address"), max_length=100)
    local_government_area = models.CharField(_("LGA"), choices=LGA, max_length=100)

    def __str__(self):
        return self.name


class Birth(TimeStampedModel):
    hospital = models.ForeignKey(
        Hospital,
        verbose_name=_("Child's Birth Hospital"),
        on_delete=models.CASCADE,
    )

    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100)
    other_name = models.CharField(
        _("Other Name"), max_length=100, null=True, blank=True
    )
    father_name = models.CharField(_("Father's Name"), max_length=100)
    mother_name = models.CharField(_("Mother's Name"), max_length=100)
    doctor_name = models.CharField(_("Doctor's Name"), max_length=100)
    mobile_number = models.CharField(_("Mobile Number"), max_length=15)
    email = models.EmailField(_("Email Address"), max_length=100, null=True, blank=True)
    gender = models.CharField(_("Gender"), choices=GENDER, max_length=15)
    weight = models.CharField(_("Child Weight"), max_length=15)
    time_of_birth = models.TimeField(
        _("Time of Birth"), auto_now=False, auto_now_add=False
    )
    date_of_birth = models.DateField(
        _("Date of Birth"), auto_now=False, auto_now_add=False
    )

    def __str__(self):
        return "{}, {}".format(self.first_name, self.last_name)
