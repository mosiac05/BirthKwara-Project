from django.urls import path
from birth_rate_app import views

app_name = "birth"
urlpatterns = [
    path('',views.HomeView.as_view(),name='home',),
    path('dashboard',views.DashboardView.as_view(),name='dashboard',),
    path('hospital/create',views.HospitalCreateView.as_view(),name='hospital_create',),
    path('hospitals',views.HospitalListView.as_view(),name='hospital_list',),
    path('hospital/<int:pk>/details',views.HospitalDetailView.as_view(),name='hospital_details',),
    path('hospital/<int:pk>/update',views.HospitalUpdateView.as_view(),name='hospital_update',),
    path('hospital/<int:pk>/delete',views.HospitalDeleteView.as_view(),name='hospital_delete',),
    path('birth/create',views.BirthCreateView.as_view(),name='birth_create',),
    path('births',views.BirthListView.as_view(),name='birth_list',),
    path('birth/<int:pk>/detail',views.BirthDetailView.as_view(),name='birth_details',),
    path('birth/<int:pk>/update',views.BirthUpdateView.as_view(),name='birth_update',),
    path('birth/<int:pk>/delete',views.BirthDeleteView.as_view(),name='birth_delete',),
    path('map',views.MapView.as_view(),name='map',),
    path('birth/<int:pk>/certificate',views.BirthCertificateView.as_view(),name='birth_certificate',),
]
