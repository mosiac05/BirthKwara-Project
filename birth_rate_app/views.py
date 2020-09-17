import folium
import pandas

from django.shortcuts import render
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
    DeleteView,
)
from birth_rate_app.models import (
    Hospital,
    Birth,
)
from birth_rate_app.forms import (
    HospitalForm,
    BirthForm,
)


User = get_user_model()

# Create your views here.
class HomeView(TemplateView):
    template_name = "home.html"

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_superuser:
            birth_objects = Birth.objects.all().order_by("first_name")
            hospital_objects = Hospital.objects.all()
            context["births"] = birth_objects
            context["num_of_births"] = birth_objects.count()
            context["num_of_hospitals"] = hospital_objects.count()
        else:
            hospital_object = get_object_or_404(Hospital, user=self.request.user)
            birth_objects = Birth.objects.filter(hospital=hospital_object).order_by("first_name")
            context["births"] = birth_objects
            context["num_of_births"] = birth_objects.count()

        return context


class HospitalCreateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to create an hospital record!", extra_tags="alert-danger")
        return redirect("birth:dashboard")

    template_name = "hospital_create.html"

    def post(self, request, *args, **kwargs):
        hospital_form = HospitalForm(request.POST)

        if not hospital_form.is_valid():
            messages.error(request, "Hospital form is invalid!", extra_tags="alert-danger")
            return redirect("birth:hospital_create")

        email = hospital_form.cleaned_data["email"]
        username = hospital_form.cleaned_data["username"]

        email_check = User.objects.filter(email=email)
        username_check = User.objects.filter(username=username)

        if not (email_check or username_check):
            password = hospital_form.cleaned_data["password"]
            confirm_password = hospital_form.cleaned_data["confirm_password"]

            if password == confirm_password:
                name = hospital_form.cleaned_data["name"]
                phone_number = hospital_form.cleaned_data["phone_number"]
                cac = hospital_form.cleaned_data["cac"]
                address = hospital_form.cleaned_data["address"]
                local_government_area = hospital_form.cleaned_data["local_government_area"]

                user = User.objects.create_user(
                    email=email,
                    password=password,
                    username=username,
                )
                user.save()

                hospital = Hospital.objects.create(
                    user=user,
                    name=name,
                    phone_number=phone_number,
                    cac=cac,
                    address=address,
                    local_government_area=local_government_area
                )

                hospital.save()

                messages.success(request, "Submitted Successfully!", extra_tags="alert-success")

                return redirect("birth:hospital_create")
            else:
                messages.error(request, "Passwords do not match!", extra_tags="alert-danger")
                messages.info(request, "Please ensure your password matches.", extra_tags="alert-info")
                return redirect("birth:hospital_create")
        else:
            if email_check:
                email_message = "The email address '" + email + "' is already in use. Double check"
                messages.error(request, email_message, extra_tags="alert-danger")

            if username_check:
                user_danger_message = "The username '" + username + "' is not available!"
                messages.error(request, user_danger_message, extra_tags="alert-danger")
                messages.info(request, "The username is already in use.", extra_tags="alert-info")

            return redirect("birth:hospital_create")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            hospital_form = HospitalForm(self.request.POST)
        else:
            hospital_form = HospitalForm()

        context["hospital_form"] = hospital_form
        return context


class HospitalListView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to view the hospital records!", extra_tags="alert-danger")
        return redirect("birth:dashboard")

    model = Hospital
    template_name = "hospital_list.html"
    context_object_name = "hospitals"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .all().order_by("name")
        )


class HospitalDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to view the hospital details!", extra_tags="alert-danger")
        return redirect("birth:dashboard")

    model = Hospital
    template_name = "hospital_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hospital = get_object_or_404(Hospital, pk=self.kwargs["pk"])

        context["hospital"] = hospital
        return context


class HospitalUpdateView(LoginRequiredMixin,  UserPassesTestMixin, TemplateView):

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to update hospital records!", extra_tags="alert-danger")
        return redirect("birth:dashboard")

    template_name = "hospital_update.html"

    def post(self, request, *args, **kwargs):
        hospital_form = HospitalForm(request.POST)

        hospital_form.is_valid()
        try:
            with transaction.atomic():
                hospital_object = Hospital.objects.filter(id=kwargs["pk"])
                hospital_object.update(
                    name = hospital_form.cleaned_data["name"],
                    cac = hospital_form.cleaned_data["cac"],
                    phone_number = hospital_form.cleaned_data["phone_number"],
                    address = hospital_form.cleaned_data["address"],
                    local_government_area = hospital_form.cleaned_data["local_government_area"],
                )

                if hospital_object.count() > 0 :
                    hospital_object = hospital_object[0]

                user_object = hospital_object.user
                user_object = User.objects.filter(
                    id=user_object.id
                )

                user_check = None
                if user_object.count() > 0:
                    user_check = user_object[0]

                email = hospital_form.cleaned_data["email"]
                email_check = User.objects.filter(email=email)
                if email_check.count() > 0:
                    email_check = email_check[0]

                if email_check and (email_check != user_check):
                    email_message = "The email address '" + email + "' is already in use. Double check"
                    messages.error(request, email_message, extra_tags="alert-danger")

                    return redirect(
                        reverse_lazy(
                            "birth:hospital_update", kwargs={"pk": hospital_object.pk}
                        )
                    )

                user_object.update(
                    email=email
                )
        except:
            messages.error(
                request=self.request,
                message=_("An error occured while submitting the update"),
            )
            return redirect(
                reverse_lazy(
                    "birth:hospital_update", kwargs={"pk": hospital_object.pk}
                )
            )

        messages.success(request, "Updated Successfully!", extra_tags="alert-success")
        return redirect("birth:hospital_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            hospital_form = HospitalForm(self.request.POST)
        else:
            hospital_object = get_object_or_404(Hospital, pk=self.kwargs["pk"])
            hospital_form = HospitalForm(
                initial={
                    "name": hospital_object.name,
                    "email": hospital_object.user.email,
                    "cac": hospital_object.cac,
                    "phone_number": hospital_object.phone_number,
                    "address": hospital_object.address,
                    "local_government_area": hospital_object.local_government_area,
                }
            )

            context["hospital_pk"] = hospital_object.pk

        context["hospital_form"] = hospital_form
        return context


class HospitalDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to delete hospital records!", extra_tags="alert-danger")
        return redirect("birth:dashboard")

    def post(self, request, *args, **kwargs):
        hospital_object = get_object_or_404(Hospital, pk=kwargs["pk"])
        user_object = User.objects.get(
            id=hospital_object.user.pk
        )
        user_object.delete()
        hospital_object.delete()

        messages.info(request, "Deleted Successfully!", extra_tags="alert-info")
        return redirect("birth:hospital_list")


class BirthCreateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):

    def test_func(self):
        if self.request.user.is_superuser:
            return False
        else:
            return True

    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to create birth records!", extra_tags="alert-danger")
        return redirect("birth:dashboard")

    template_name = "birth_create.html"

    def post(self, request, *args, **kwargs):
        birth_form = BirthForm(request.POST)

        if not birth_form.is_valid():
            messages.error(request, "Birth form is invalid!", extra_tags="alert-danger")
            return redirect("birth:birth_create")

        if self.request.user.is_superuser:
            messages.info(request, "Superadmins cannot add birth records!", extra_tags="alert-info")
            return redirect("birth:hospital_list")

        user = User.objects.get(
            id=self.request.user.pk
        )

        hospital_object = Hospital.objects.get(
            user=user
        )

        first_name=birth_form.cleaned_data["first_name"]
        last_name=birth_form.cleaned_data["last_name"]
        other_name=birth_form.cleaned_data["other_name"]
        gender=birth_form.cleaned_data["gender"]
        weight=birth_form.cleaned_data["weight"]
        father_name=birth_form.cleaned_data["father_name"]
        mother_name=birth_form.cleaned_data["mother_name"]
        doctor_name=birth_form.cleaned_data["doctor_name"]
        mobile_number=birth_form.cleaned_data["mobile_number"]
        email=birth_form.cleaned_data["email"]
        time_of_birth=birth_form.cleaned_data["time_of_birth"]
        date_of_birth=birth_form.cleaned_data["date_of_birth"]


        birth_record = Birth.objects.create(
            hospital=hospital_object,
            first_name=first_name,
            last_name=last_name,
            other_name=other_name,
            gender=gender,
            weight=weight,
            father_name=father_name,
            mother_name=mother_name,
            doctor_name=doctor_name,
            mobile_number=mobile_number,
            email=email,
            time_of_birth=time_of_birth,
            date_of_birth=date_of_birth,
        )

        birth_record.save()

        messages.success(request, "Birth record added successfully!", extra_tags="alert-success")
        return redirect("birth:birth_create")



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            birth_form = BirthForm(self.request.POST)
        else:
            birth_form = BirthForm()

        context["birth_form"] = birth_form
        return context


class BirthListView(LoginRequiredMixin, ListView):
    model = Birth
    template_name = "birth_list.html"
    context_object_name = "births"

    def get_queryset(self):
        if not self.request.user.is_superuser:
            hospital_object = get_object_or_404(Hospital, user=self.request.user)

            return (
                super()
                .get_queryset()
                .filter(hospital=hospital_object).order_by("first_name")
            )
        else:
            return (
                super()
                .get_queryset()
                .all().order_by("first_name")
            )


class BirthDetailView(LoginRequiredMixin, DetailView):
    model = Birth
    template_name = "birth_details.html"

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            birth_object = get_object_or_404(Birth, pk=self.kwargs["pk"])
            hospital_object = get_object_or_404(Hospital, user=self.request.user)

            if birth_object.hospital != hospital_object:
                messages.error(self.request, "You are not authorized to view that record!", extra_tags="alert-danger")
                return redirect("birth:dashboard")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        birth_object = get_object_or_404(Birth, pk=self.kwargs["pk"])

        context["birth_object"] = birth_object
        return context


class BirthUpdateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):

    def test_func(self):
        if self.request.user.is_superuser:
            return False
        else:
            return True

    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to update birth records!", extra_tags="alert-danger")
        return redirect("birth:dashboard")

    template_name = "birth_update.html"

    def post(self, request, *args, **kwargs):
        birth_form = BirthForm(request.POST)

        birth_form.is_valid()
        try:
            with transaction.atomic():
                birth_object = Birth.objects.filter(id=kwargs["pk"])
                birth_object.update(
                    first_name = birth_form.cleaned_data["first_name"],
                    last_name = birth_form.cleaned_data["last_name"],
                    other_name = birth_form.cleaned_data["other_name"],
                    gender = birth_form.cleaned_data["gender"],
                    weight = birth_form.cleaned_data["weight"],
                    father_name = birth_form.cleaned_data["father_name"],
                    mother_name = birth_form.cleaned_data["mother_name"],
                    mobile_number = birth_form.cleaned_data["mobile_number"],
                    email = birth_form.cleaned_data["email"],
                    doctor_name = birth_form.cleaned_data["doctor_name"],
                    time_of_birth = birth_form.cleaned_data["time_of_birth"],
                    date_of_birth = birth_form.cleaned_data["date_of_birth"],
                )
        except:
            messages.error(
                request=self.request,
                message=_("An error occured while submitting the update"),
            )
            return redirect(
                reverse_lazy(
                    "birth:birth_update", kwargs={"pk": birth_object.pk}
                )
            )

        messages.success(request, "Updated Successfully!", extra_tags="alert-success")
        return redirect("birth:birth_list")

    def get(self, request, *args, **kwargs):
        birth_object = get_object_or_404(Birth, pk=self.kwargs["pk"])
        hospital_object = get_object_or_404(Hospital, user=self.request.user)

        if birth_object.hospital != hospital_object:
            messages.error(self.request, "You are not authorized to update that record!", extra_tags="alert-danger")
            return redirect(
                        reverse_lazy("birth:dashboard")
                        )

        return super().get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            birth_form = BirthForm(self.request.POST)
        else:
            birth_object = get_object_or_404(Birth, pk=self.kwargs["pk"])

            birth_form = BirthForm(
                initial={
                    "first_name": birth_object.first_name,
                    "last_name": birth_object.last_name,
                    "other_name": birth_object.other_name,
                    "gender": birth_object.gender,
                    "weight": birth_object.weight,
                    "father_name": birth_object.father_name,
                    "mother_name": birth_object.mother_name,
                    "mobile_number": birth_object.mobile_number,
                    "email": birth_object.email,
                    "doctor_name": birth_object.doctor_name,
                    "time_of_birth": birth_object.time_of_birth,
                    "date_of_birth": birth_object.date_of_birth,
                }
            )

            context["birth_pk"] = birth_object.pk

        context["birth_form"] = birth_form
        return context


class BirthDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    def test_func(self):
        if self.request.user.is_superuser:
            return False
        else:
            return True

    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to delete birth records!", extra_tags="alert-danger")
        return redirect("birth:dashboard")

    def post(self, request, *args, **kwargs):
        birth_object = get_object_or_404(Birth, pk=kwargs["pk"])
        hospital_object = get_object_or_404(Hospital, user=self.request.user)

        if birth_object.hospital != hospital_object:
            messages.error(self.request, "You are not authorized to delete that record!", extra_tags="alert-danger")
            return redirect("birth:dashboard")

        birth_object.delete()

        messages.info(request, "Deleted Birth Record Successfully!", extra_tags="alert-info")
        return redirect("birth:birth_list")


def color_setter(number):
    if number <= 50:
        return "green"
    elif number <= 100:
        return "orange"
    else:
        return "red"


def map_create():
    try:
        data = pandas.read_csv("./static/Kwara State Coordinates.txt")
        lat = list(data["LAT"])
        lon = list(data["LON"])
        lga_name = list(data["NAME"])

        html = """<h4>%s</h4>
        Births: %s
        """

        map = folium.Map(location=[8.634559,4.7525483], zoom_start=10, tiles="Stamen Terrain")

        fg = folium.FeatureGroup(name="Births")

        for lt, ln, name in zip(lat, lon, lga_name):
            lga_coordinates = str(lt) + "," + str(ln)
            hospitals = Hospital.objects.filter(
                local_government_area=lga_coordinates
            )

            birth_count = 0
            for hospital_object in hospitals:
                births = Birth.objects.filter(
                    hospital=hospital_object
                )
                birth_count += births.count()

            iframe = folium.IFrame(html=html % (name, str(birth_count)), width=100, height=100)
            fg.add_child(folium.CircleMarker(location=[lt, ln],
                                            radius=10,
                                            popup=folium.Popup(iframe),
                                            fill_color=color_setter(birth_count),
                                            color='grey',
                                            fill_opacity=0.7
                                        )
                                    )

        map.add_child(fg)
        map.add_child(folium.LayerControl())
        map.save("./templates/map.html")
        print("done")
    except:
        return

class MapView(TemplateView):
    template_name = "map.html"
    def get(self, request, *args, **kwargs):
        map_create()
        return super().get(request, *args, **kwargs)


class BirthCertificateView(LoginRequiredMixin, DetailView):
    model = Birth
    template_name = 'certificate/birth_certificate.html'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            birth_object = get_object_or_404(Birth, pk=self.kwargs["pk"])
            hospital_object = get_object_or_404(Hospital, user=self.request.user)

            if birth_object.hospital != hospital_object:
                messages.error(self.request, "You are not authorized to print this certificate!", extra_tags="alert-danger")
                return redirect("birth:dashboard")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        birth_object = get_object_or_404(Birth, pk=self.kwargs["pk"])

        context["birth_object"] = birth_object
        return context
