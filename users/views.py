from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView
from users.models import Appointment
from django.http import JsonResponse
import uuid
from django.utils import timezone
from users.models import APPOINTMENT_CHOICES_DICT

class IndexView(TemplateView):
    template_name = 'pages/index.html'


class AppointmentDetailView(DetailView):
    template_name = 'pages/appointment-detail.html'
    model = Appointment
    slug_field = 'appointment_id'


class AppointmentView(TemplateView):
    template_name = 'pages/appointment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = APPOINTMENT_CHOICES_DICT
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST

        doctor = data.get('doctor')
        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')
        date = data.get('date')

        appointment = Appointment.objects.create(
            type=doctor,
            name=name,
            phone=phone,
            customer_email=email,
            scheduled_date=date
        )

        appointment.refresh_from_db()
        url = reverse_lazy("confirmation", args=[appointment.appointment_id])

        return  JsonResponse({"data": url}, status=200)


class ConfirmationView(DetailView):
    template_name = 'pages/confirmation.html'
    model = Appointment
    slug_field = 'appointment_id'

    def post(self, request, *args, **kwargs):
        data = request.POST
        code = data.get('otp')

        appointment = self.get_object()
        if appointment.code == code:
            appointment.verified_at = timezone.datetime.now()
            appointment.save()
            url = reverse_lazy("success", args=[appointment.appointment_id])
            return redirect(url)
        return redirect(request.path_info) 
    

class SuccessView(DetailView):
    model = Appointment
    slug_field = 'appointment_id'
    template_name = 'pages/success.html'