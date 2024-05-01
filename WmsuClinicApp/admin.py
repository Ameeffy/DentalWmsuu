# admin.py

from django.contrib import admin
from .models import Profile

from .models import Admin

from .models import Appointment
from .models import Doctor, Assistant, DoctorAvailability
from .models import DentalSupply
from .models import DentalUser
from .models import DentalExtraction


from .models import AppointmentReport
from .models import Semester

class SemesterAdmin(admin.ModelAdmin):
    list_display = ('semester_id', 'start_date', 'end_date', 'current_date')
    search_fields = ('semester_id', 'start_date', 'end_date', 'current_date')
    list_filter = ('start_date', 'end_date')

admin.site.register(Semester, SemesterAdmin)
class AppointmentReportAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'report_date')
    search_fields = ['appointment__purpose', 'report_date']
    list_filter = ['report_date']

admin.site.register(AppointmentReport, AppointmentReportAdmin)   
    
    
@admin.register(DentalExtraction)
class DentalExtractionAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'extraction_record']
    search_fields = ['appointment__purpose', 'extraction_record']  # Add fields you want to search
    list_filter = ['extraction_record']

    
admin.site.register(DentalUser)
@admin.register(DentalSupply)
class DentalSupplyAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'quantity']
    
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('Doctor_id', 'name', 'specialization', 'status')
    search_fields = ('name', 'specialization')

@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date' ,'time', 'Text')
    search_fields = ('doctor__name',)
    list_filter = ('date', 'Text')

@admin.register(Assistant)
class AssistantAdmin(admin.ModelAdmin):
    list_display = ('Assistant_id', 'name', 'role', 'status')
    search_fields = ('name', 'role')

    
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'user', 'preferred_date', 'preferred_time','purpose', 'reference_number')
    search_fields = ('user__username', 'purpose')
    list_filter = ('preferred_date',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'course', 'user_type', 'status']

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'admin_username', 'first_name', 'last_name')
    search_fields = ('admin_username', 'first_name', 'last_name')



