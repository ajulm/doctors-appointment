from django.urls import path
from django.contrib.auth.views import LoginView
from .views import IndexView, ConfirmationView, AppointmentView, SuccessView, AppointmentDetailView


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("appointment/", AppointmentView.as_view(), name="appointment"),
    path("confirmation/<str:slug>/", ConfirmationView.as_view(), name="confirmation"),
    path("success/<str:slug>/", SuccessView.as_view(), name="success"),
    path("appointment-detail/<str:slug>/", AppointmentDetailView.as_view(), name="appointment-detail"),


]
