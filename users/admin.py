from django.contrib import admin
from .models import CustomUser, Appointment
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm, CustomUserChangeForm


# Register your models here.

admin.site.unregister(Group)

@admin.register(Appointment)
class CustomAppointmentAdmin(admin.ModelAdmin):
    list_display = ("appointment_id", "scheduled_date", "is_active")
    search_fields = ["appointment_id"]
    order = "-verified_at"



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = (
        (None, {"fields": (
            "first_name", "last_name", "email", "password", "role"
        )}),
        ("Permissions", {"fields": ("is_staff", "user_permissions")}),
    )
    list_display = ("username", "email", "first_name", "last_name", "last_login")
    list_display_links = ["email"]
    search_fields = ["username", "email"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.exclude(username="admin")

        return qs
