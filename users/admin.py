from django.contrib import admin
from .models import CustomUser, Appointment
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm


# Register your models here.

admin.site.unregister(Group)

@admin.register(Appointment)
class CustomAppointmentAdmin(admin.ModelAdmin):
    list_display = ("appointment_id", "scheduled_date", "is_active")
    search_fields = ["appointment_id"]
    order = "-verified_at"



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    # add_form = CustomUserCreationForm
    # fieldsets = (
    #     (None, {'fields': ('first_name', 'last_name', 'email', "password")}),
    #     (None, {'fields': ()}),
    # )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('first_name', 'last_name', 'email'),
    #     }),
    # )
    list_display = ("username", "email", "first_name", "last_name", "last_login")
    list_display_links = ["email"]
    search_fields = ["email"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.exclude(username="admin")

        return qs

