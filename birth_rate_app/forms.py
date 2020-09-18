from django import forms
from birth_rate_app.choices import (
    LGA,
    GENDER,
)

class HospitalForm(forms.Form):
    name = forms.CharField(max_length=100,
                            required=True,
                            widget=forms.TextInput(
                                attrs={
                                    "placeholder": u"Enter hospital name...",
                                    "class": u"form-control",
                                }
                            )
                        )
    username = forms.CharField(max_length=100,
                            required=True,
                            widget=forms.TextInput(
                                attrs={
                                    "placeholder": u"Enter a login access username...",
                                    "class": u"form-control",
                                }
                            )
                        )
    email = forms.EmailField(required=True,
                            widget=forms.EmailInput(
                                attrs={
                                    "placeholder": u"Enter hospital valid email address...",
                                    "class": u"form-control",
                                }
                            )
                        )
    password = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.PasswordInput(
                                    attrs={
                                        "placeholder": u"Choose a safe one...",
                                        "class": u"form-control",
                                    }
                                )
                            )
    confirm_password = forms.CharField(max_length=100,
                                        required=True,
                                        widget=forms.PasswordInput(
                                            attrs={
                                                "placeholder": u"...type it again to confirm",
                                                "class": u"form-control",
                                            }
                                        )
                                    )
    phone_number = forms.CharField(max_length=15,
                                    required=True,
                                    widget=forms.TextInput(
                                        attrs={
                                            "placeholder": u"Enter hospital phone number...",
                                            "class": u"form-control",
                                        }
                                    )
                                )
    cac = forms.CharField(max_length=100,
                            required=True,
                            widget=forms.TextInput(
                                attrs={
                                    "placeholder": u"Enter hospital CAC...",
                                    "class": u"form-control",
                                }
                            )
                        )
    address = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(
                                    attrs={
                                        "placeholder": u"Enter hospital address...",
                                        "class": u"form-control",
                                    }
                                )
                            )
    local_government_area = forms.ChoiceField(choices=LGA,
                                                required=True,
                                                widget=forms.Select(
                                                    attrs={
                                                        "placeholder": u"Select hospital LGA...",
                                                        "class": u"form-control",
                                                    }
                                                )
                                            )


class BirthForm(forms.Form):
    first_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(
                                    attrs={
                                        "placeholder": u"Enter child's first name...",
                                        "class": u"form-control",
                                    }
                                )
                            )

    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(
                                    attrs={
                                        "placeholder": u"Enter child's last name...",
                                        "class": u"form-control",
                                    }
                                )
                            )

    other_name = forms.CharField(required=False,
                                max_length=100,
                                widget=forms.TextInput(
                                    attrs={
                                        "placeholder": u"Enter child's other name...",
                                        "class": u"form-control",
                                    }
                                )
                            )
    gender = forms.ChoiceField(choices=GENDER,
                                required=True,
                                widget=forms.Select(
                                    attrs={
                                        "placeholder": u"Select baby's gender...",
                                        "class": u"form-control",
                                    }
                                )
                            )
    weight = forms.CharField(max_length=15,
                            required=True,
                            widget=forms.TextInput(
                                attrs={
                                    "placeholder": u"Enter child's weight...",
                                    "class": u"form-control",
                                }
                            )
                        )
    father_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(
                                    attrs={
                                        "placeholder": u"Enter child's father's name...",
                                        "class": u"form-control",
                                    }
                                )
                            )

    mother_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(
                                    attrs={
                                        "placeholder": u"Enter child's mother's name...",
                                        "class": u"form-control",
                                    }
                                )
                            )
    email = forms.EmailField(required=False,
                            max_length=100,
                            widget=forms.EmailInput(
                                attrs={
                                    "placeholder": u"Enter home email address...",
                                    "class": u"form-control",
                                }
                            )
                        )
    mobile_number = forms.CharField(max_length=15,
                                    required=True,
                                    widget=forms.TextInput(
                                        attrs={
                                            "placeholder": u"Enter home mobile number...",
                                            "class": u"form-control",
                                        }
                                    )
                                )
    doctor_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(
                                    attrs={
                                        "placeholder": u"Enter delivery doctor's name...",
                                        "type": u"text",
                                        "class": u"form-control",
                                    }
                                )
                            )
    time_of_birth = forms.TimeField(required=True,
                                    widget=forms.TimeInput(
                                        attrs={
                                            "placeholder": u"Enter child's time of birth...",
                                            "class": u"form-control",
                                            "id": u"timepicker",
                                        }
                                    )
                                )
    date_of_birth = forms.DateField(required=True,
                                    widget=forms.DateInput(
                                        attrs={
                                            "placeholder": u"Enter child's date of birth...",
                                            "class": u"form-control",
                                            "id": u"mdate",
                                        }
                                    )
                                )
