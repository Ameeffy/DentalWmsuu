from django.shortcuts import render, get_object_or_404, redirect
from . forms import CreateUserForm, LoginForm, CreateUserFormFaculty
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.models import User
from .forms import AdminLoginForm
from .models import Admin
from .forms import AppointmentForm
from .models import Appointment
from django.shortcuts import redirect
from .forms import DoctorForm, AssistantForm
from .models import Doctor, Assistant
from .models import DoctorAvailability
from .forms import DoctorAvailabilityForm
from django.utils import timezone
from django.contrib import messages
from .forms import RescheduleForm
from .models import Appointment
from django.contrib.auth.hashers import check_password




from .models import DentalSupply, DentalExtraction
from .forms import DentalSupplyForm, DentalSupplyFormquantity


from .models import DentalUser


from .forms import LoginDental
from .models import DentalUser
from .forms import ExtractionRecordForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import ForgotPasswordForm, VerifyUserForm, ResetPasswordForm
from .forms import AppointmentForm


from django.shortcuts import render, get_object_or_404, redirect
from .forms import AppointmentReportForm
from .models import Appointment, AppointmentReport

from .forms import SemesterForm

from .forms import UpdatePurposeForm
from .forms import ProfileUpdateForm

def view_profileadmin(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile = Profile.objects.get(user=user)
    doctor = Doctor.objects.filter(name=user.username).first()
    assistant = Assistant.objects.filter(name=user.username).first()
    
    form = ProfileUpdateForm(request.POST or None, instance=profile)
    if form.is_valid():
        form.save()
        return redirect('view_profileadmin', user_id=user_id)  
    
    context = {
    'user': user,
    'profile': profile,
    'doctor': doctor,
    'assistant': assistant,
    'form': form
}
    return render(request, 'WmsuClinicApp/wmsuprofileadmin.html', context)


def view_profileadminfaculty(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile = Profile.objects.get(user=user)
    doctor = Doctor.objects.filter(name=user.username).first()
    assistant = Assistant.objects.filter(name=user.username).first()
    
    form = ProfileUpdateForm(request.POST or None, instance=profile)
    if form.is_valid():
        form.save()
        return redirect('view_profileadminfaculty', user_id=user_id)  
    
    context = {
    'user': user,
    'profile': profile,
    'doctor': doctor,
    'assistant': assistant,
    'form': form
}
    return render(request, 'WmsuClinicApp/wmsuprofileadminfaculty.html', context)


def update_purpose(request, appointment_id):
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)
    
    if request.method == 'POST':
        form = UpdatePurposeForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('admin_homesite') 
    else:
        form = UpdatePurposeForm(instance=appointment)
    
    return render(request, 'WmsuClinicApp/update_purpose.html', {'form': form})
def add_semester(request):
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_doctoravailability')  
    else:
        form = SemesterForm()
    return render(request, 'WmsuClinicApp/add_semester.html', {'form': form})
def view_doctorprofile(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    return render(request, 'WmsuClinicApp/doctor_profile.html', {'doctor': doctor})

def view_assistantprofile(request, assistant_id):
    assistant = get_object_or_404(Assistant, Assistant_id=assistant_id)
    return render(request, 'WmsuClinicApp/assistant_profile.html', {'assistant': assistant})
def appointment_report(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    report = AppointmentReport.objects.filter(appointment=appointment).first() 
    if request.method == 'POST':
        form = AppointmentReportForm(request.POST, instance=report)
        if form.is_valid():
            report = form.save(commit=False)  
            report.appointment = appointment   
            report.save()  
            return redirect('admin_homesite')  
    else:
        form = AppointmentReportForm(instance=report)

    
    username = None
    if appointment.user:
        username = appointment.user.username

    return render(request, 'WmsuClinicApp/create_report.html', {'appointment': appointment, 'form': form, 'username': username})






def forgot_password(request):
    success = False
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            user = User.objects.filter(username=username, email=email).first()
            if user:
                success = True
            else:
                messages.error(request, "Invalid credentials.")
    else:
        form = ForgotPasswordForm()
    return render(request, 'WmsuClinicApp/forgotpassword.html', {'form': form,  'success': success})

def verify_user(request, username):
    user = User.objects.get(username=username)
    

    attempt_count = request.session.get('attempt_count', 0)
    
    if request.method == 'POST':
        form = VerifyUserForm(request.POST)
        if form.is_valid():
            ID_Number = form.cleaned_data['ID_Number']
            profile_ID_Number = user.profile.ID_Number
            if ID_Number == profile_ID_Number:
                request.session['attempt_count'] = 0
                request.session.save()  
                return redirect('reset_password', username=username)
            else:
                messages.error(request, "ID Number does not match.")
                attempt_count += 1
        else:
            attempt_count += 1
        
        request.session['attempt_count'] = attempt_count
        request.session.save()  
        if attempt_count >= 5:
            return redirect('forgot_password') 
    else:
       
        attempt_count = 0
        request.session['attempt_count'] = 0
        request.session.save()  
        form = VerifyUserForm()
    
    return render(request, 'WmsuClinicApp/verifyuser.html', {'form': form, 'attempt_count': attempt_count})

def reset_password(request, username):
    user = User.objects.get(username=username)
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password == confirm_password:
                user.set_password(password)
                user.save()
                messages.success(request, "Password reset successful.")
                return redirect('my_login')  
            else:
                messages.error(request, "Passwords do not match.")
        else:
            # Form is invalid, pass form with errors to the template
            return render(request, 'WmsuClinicApp/reset_password.html', {'form': form})
    else:
        form = ResetPasswordForm()
    
    return render(request, 'WmsuClinicApp/reset_password.html', {'form': form})
def dental_record(request):
    extraction_records = DentalExtraction.objects.all()
    appointment = Appointment.objects.all()
    
    return render(request, 'WmsuClinicApp/dental_record.html', {'extraction_records': extraction_records, 'appointment': appointment})

def appointmentextraction_details(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    # Retrieve all DentalExtraction records associated with the appointment
    extraction_records = DentalExtraction.objects.filter(appointment=appointment)
    
    return render(request, 'WmsuClinicApp/appointmentextraction_details.html', {'appointment': appointment, 'extraction_records': extraction_records})
def create_extraction_record(request, appointment_id):
    appointment = Appointment.objects.get(pk=appointment_id)
    extraction_records = DentalExtraction.objects.filter(appointment=appointment)
    return render(request, 'WmsuClinicApp/dental_recordview.html', {'appointment': appointment, 'extraction_records': extraction_records})

def appointment_extraction(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    if request.method == 'POST':
        form = ExtractionRecordForm(request.POST)
        if form.is_valid():
            extraction_record = form.cleaned_data['extraction_record']
            extraction_datetime = timezone.now()
            for record in extraction_record:
                DentalExtraction.objects.create(
                    appointment=appointment, 
                    extraction_record=record, 
                    extraction_datetime=extraction_datetime
                )
    else:
        form = ExtractionRecordForm()
    
    return render(request, 'WmsuClinicApp/appointmentextraction.html', {'form': form, 'appointment': appointment})

def LoginDentals(request):
    if request.method == 'POST':
        form = LoginDental(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and isinstance(user, DentalUser):
                login(request, user)
                dental_id = user.dental_id
                # Now you can use dental_id as needed
                return redirect('admin_Dashboard')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginDental()
    return render(request, 'WmsuClinicApp/LoginDental.html', {'form': form})
from .forms import ChangePasswordForm

from django.contrib import messages
def dentalchange_password(request):
   
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            dental_id = form.cleaned_data['dental_id']
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            confirm_new_password = form.cleaned_data['confirm_new_password']

            # Get the DentalUser based on dental_id
            try:
                dental_user = DentalUser.objects.get(dental_id=dental_id)
            except DentalUser.DoesNotExist:
                dental_user = None

            if dental_user:
                if dental_user.password == current_password:  # Check current password
                    if new_password == confirm_new_password:
                        dental_user.password = new_password  # Set new password
                        dental_user.save()
                        messages.success(request, "Password changed successfully!")
                        return redirect('LoginDentals')
                    else:
                        messages.error(request, "New password and confirm password do not match.")
                else:
                    messages.error(request, "Current password is incorrect.")
            else:
                messages.error(request, "User with provided dental ID does not exist.")
    else:
        form = ChangePasswordForm()
    return render(request, 'WmsuClinicApp/dentalchange_password.html', {'form': form})

def supply_list(request):
    supplies = DentalSupply.objects.all()
    return render(request, 'WmsuClinicApp/inventory_supply_list.html', {'supplies': supplies})

def supply_listhome(request):
    supplies = DentalSupply.objects.all()
    return render(request, 'WmsuClinicApp/inventory_supply_listhome.html', {'supplies': supplies})

def supply_create(request):
    if request.method == 'POST':
        form = DentalSupplyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supply_list')
    else:
        form = DentalSupplyForm()
    return render(request, 'WmsuClinicApp/inventory_supply_create.html', {'form': form})

def supply_update(request, pk):
    supply = get_object_or_404(DentalSupply, pk=pk)
    if request.method == 'POST':
        form = DentalSupplyFormquantity(request.POST, instance=supply)
        if form.is_valid():
            form.save()
            return redirect('supply_list')
    else:
        form = DentalSupplyFormquantity(instance=supply)
    return render(request, 'WmsuClinicApp/inventory_supply_update.html', {'form': form})

def supply_delete(request, pk):
    supply = get_object_or_404(DentalSupply, pk=pk)
    if request.method == 'POST':
        supply.delete()
        return redirect('supply_list')
    return render(request, 'WmsuClinicApp/inventory_supply_delete.html', {'supply': supply})

def session_done(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    appointment.status = 'Session Done'
   
    appointment.save()
    
    return redirect('admin_homesite')

def failed_to_attend(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    appointment.status = 'Failed to Attend'
    
    appointment.save()
    
    return redirect('admin_homesite')

def Decline(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    appointment.status = 'Decline'
    appointment.purpose = f"{appointment.purpose} X" if appointment.purpose else "X"
    appointment.save()
    
    return redirect('admin_homesite')
def admin_reschedule(request, appointment_id):
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)
    
    if request.method == 'POST':
        form = RescheduleForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('admin_homesite')  
    else:
        form = RescheduleForm(instance=appointment)
        
    return render(request, 'WmsuClinicApp/admin_reschedule.html', {'form': form})



    





def admin_doctoravailability(request):
    if request.method == 'POST':
        form = DoctorAvailabilityForm(request.POST)
        if form.is_valid():
           
            form.save()

            return redirect('admin_doctoravailability')  
    else:
        form = DoctorAvailabilityForm()
    
    context = {
        'form': form,
        'doctor_availabilities': DoctorAvailability.objects.all()
    }
    return render(request, 'WmsuClinicApp/admin_doctoravailability.html', context)

def view_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment.objects.order_by('-current_date'), appointment_id=appointment_id)
    user = appointment.user
    profile = Profile.objects.get(user=user)
    doctor = appointment.doctor
    assistant = appointment.assistant
    
    context = {
        'appointment': appointment,
        'user': user,
        'profile': profile,
        'doctor': doctor,
        'assistant': assistant,
    }

    return render(request, 'WmsuClinicApp/view_appointment.html', context)
def view_appointmentAdmin(request, appointment_id):
    appointment = get_object_or_404(Appointment.objects.order_by('-current_date'), appointment_id=appointment_id)
    user = appointment.user
    profile = Profile.objects.get(user=user)
    doctor = appointment.doctor
    assistant = appointment.assistant
    
    context = {
        'appointment': appointment,
        'user': user,
        'profile': profile,
        'doctor': doctor,
        'assistant': assistant,
    }

    return render(request, 'WmsuClinicApp/view_appointmentAdmin.html', context)
def view_appointmentProfile(request, appointment_id):
    appointment = get_object_or_404(Appointment.objects.order_by('-current_date'), appointment_id=appointment_id)
    user = appointment.user
    profile = Profile.objects.get(user=user)
    doctor = appointment.doctor
    assistant = appointment.assistant
    
    context = {
        'appointment': appointment,
        'user': user,
        'profile': profile,
        'doctor': doctor,
        'assistant': assistant,
    }

    return render(request, 'WmsuClinicApp/view_appointmentProfile.html', context)
def view_appointmentProfileStudent(request, appointment_id):
    appointment = get_object_or_404(Appointment.objects.order_by('-current_date'), appointment_id=appointment_id)
    user = appointment.user
    profile = Profile.objects.get(user=user)
    doctor = appointment.doctor
    assistant = appointment.assistant
    
    context = {
        'appointment': appointment,
        'user': user,
        'profile': profile,
        'doctor': doctor,
        'assistant': assistant,
    }

    return render(request, 'WmsuClinicApp/view_appointmentProfileStudent.html', context)
def view_appointmentProfileFaculty(request, appointment_id):
    appointment = get_object_or_404(Appointment.objects.order_by('-current_date'), appointment_id=appointment_id)
    user = appointment.user
    profile = Profile.objects.get(user=user)
    doctor = appointment.doctor
    assistant = appointment.assistant
    
    context = {
        'appointment': appointment,
        'user': user,
        'profile': profile,
        'doctor': doctor,
        'assistant': assistant,
    }

    return render(request, 'WmsuClinicApp/view_appointmentProfileFaculty.html', context)
def on_duty_assistant(request, assistant_id):
    assistant = get_object_or_404(Assistant, Assistant_id=assistant_id)
    assistant.status = 'On Duty'
    assistant.save()
    return redirect('admin_doctorsitelist')  

def not_on_duty_assistant(request, assistant_id):
    assistant = get_object_or_404(Assistant, Assistant_id=assistant_id)
    assistant.status = 'Not on Duty'
    assistant.save()
    return redirect('admin_doctorsitelist') 
def on_duty(request, doctor_id):
    doctor = get_object_or_404(Doctor, Doctor_id=doctor_id)
    doctor.status = 'On Duty'
    doctor.save()
    return redirect('admin_doctorsitelist')

def not_on_duty(request, doctor_id):
    doctor = get_object_or_404(Doctor, Doctor_id=doctor_id)
    doctor.status = 'Not on Duty'
    doctor.save()
    return redirect('admin_doctorsitelist')

def retire_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    doctor.status = 'Retired'
    doctor.save()
    return redirect('admin_doctorsitelist')

def resign_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    doctor.status = 'Resigned'
    doctor.save()
    return redirect('admin_doctorsitelist')
def retire_assistant(request, assistant_id):
    assistant = get_object_or_404(Assistant, pk=assistant_id)
    assistant.status = 'Retired'
    assistant.save()
    return redirect('admin_doctorsitelist')

def resign_assistant(request, assistant_id):
    assistant = get_object_or_404(Assistant, pk=assistant_id)
    assistant.status = 'Resigned'
    assistant.save()
    return redirect('admin_doctorsitelist')

def doctor(request):
    if request.method == 'POST':
        doctor_form = DoctorForm(request.POST, prefix='doctor')
    

        if doctor_form.is_valid():
            doctor_form.save()
            return redirect('admin_doctorsitelist')  
    else:
        doctor_form = DoctorForm(prefix='doctor')

    return render(request, 'WmsuClinicApp/admin_doctor.html', {'doctor_form': doctor_form})

def assistant(request):
    if request.method == 'POST':
        assistant_form = AssistantForm(request.POST, prefix='assistant')

        if assistant_form.is_valid():
            assistant_form.save()
            return redirect('admin_doctorsitelist')  
    else:

        assistant_form = AssistantForm(prefix='assistant')

    return render(request, 'WmsuClinicApp/admin_assistant.html', {'assistant_form': assistant_form})

def admin_doctorsite(request):
    doctors = Doctor.objects.all()
    assistants = Assistant.objects.all()

   

    return render(request, 'WmsuClinicApp/admin_doctorsite.html', {'doctors': doctors, 'assistants': assistants})

def admin_doctorsitelist(request):
    doctors = Doctor.objects.all()
    assistants = Assistant.objects.all()

   

    return render(request, 'WmsuClinicApp/admin_doctorsitelist.html', {'doctors': doctors, 'assistants': assistants})
def appointment_list(request):
   
    appointments = Appointment.objects.all()
    appointments_count = Appointment.objects.all()

   
    consultation_count = appointments.filter(Q(purpose='Consultation') | Q(purpose='Consultation X')).count()
    cleaning_count = appointments.filter(Q(purpose='Cleaning') | Q(purpose='Cleaning X')).count()
    extraction_count = appointments.filter(Q(purpose='Extraction') | Q(purpose='Extraction X')).count()

   
    sorted_appointments = sorted(appointments, key=lambda x: (x.preferred_date, datetime.strptime(x.preferred_time.split(' - ')[0], '%I:%M %p').time()), reverse=True)

    context = {
        'total_appointments': appointments_count,
        'appointments': sorted_appointments,  
        'consultation_count': consultation_count,
        'cleaning_count': cleaning_count,
        'extraction_count': extraction_count,
    }

    return render(request, 'WmsuClinicApp/appointment_list.html', context)
def appointment_listPending(request):
    appointments = Appointment.objects.filter(status="Pending").order_by('-preferred_date')
    consultation_count = appointments.filter(purpose='Consultation').count()
    cleaning_count = appointments.filter(purpose='Cleaning').count()
    extraction_count = appointments.filter(purpose='Extraction').count()

    context = {
        'appointments': appointments,  
        'consultation_count': consultation_count,
        'cleaning_count': cleaning_count,
        'extraction_count': extraction_count,
    }

    return render(request, 'WmsuClinicApp/appointment_listPending.html', context)
def appointment_listSuccess(request):
    appointments = Appointment.objects.filter(status="Session Done").order_by('-preferred_date')
    consultation_count = appointments.filter(purpose='Consultation').count()
    cleaning_count = appointments.filter(purpose='Cleaning').count()
    extraction_count = appointments.filter(purpose='Extraction').count()

    context = {
        'appointments': appointments,  
        'consultation_count': consultation_count,
        'cleaning_count': cleaning_count,
        'extraction_count': extraction_count,
    }

    return render(request, 'WmsuClinicApp/appointment_listSuccess.html', context)

def appointment_listFailed(request):
    appointments = Appointment.objects.filter(status="Failed to Attend").order_by('-preferred_date')
    consultation_count = appointments.filter(purpose='Consultation').count()
    cleaning_count = appointments.filter(purpose='Cleaning').count()
    extraction_count = appointments.filter(purpose='Extraction').count()

    context = {
        'appointments': appointments,  
        'consultation_count': consultation_count,
        'cleaning_count': cleaning_count,
        'extraction_count': extraction_count,
    }

    return render(request, 'WmsuClinicApp/appointment_listFailed.html', context)
def appointment_listDecline(request):
    appointments = Appointment.objects.filter(status="Decline").order_by('-preferred_date')
    consultation_count = appointments.filter(purpose='Consultation X').count()
    cleaning_count = appointments.filter(purpose='Cleaning X').count()
    extraction_count = appointments.filter(purpose='Extraction X').count()

    context = {
        'appointments': appointments,  
        'consultation_count': consultation_count,
        'cleaning_count': cleaning_count,
        'extraction_count': extraction_count,
    }

    return render(request, 'WmsuClinicApp/appointment_listDecline.html', context)

def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)

    if request.method == 'POST':
       
        appointment.delete()
        

        return redirect('WmsuDentalhomepage')

    return render(request, 'WmsuClinicApp/delete_appointment_confirm.html', {'appointment': appointment})


def appointment_details(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    user = appointment.user
    profile = Profile.objects.get(user=user)
    doctor = appointment.doctor
    assistant = appointment.assistant
    

    context = {
        'appointment': appointment,
        'user': user,
        'profile': profile,
        'doctor': doctor,
        'assistant': assistant,
    }

    return render(request, 'WmsuClinicApp/appointment_details.html', context)

def last_appointment(request):
    user_appointments = Appointment.objects.filter(user=request.user)
    if user_appointments.exists():
        last_appointment = user_appointments.latest('preferred_date')
    else:
        last_appointment = None
    return render(request, 'WmsuClinicApp/last_appointment.html', {'last_appointment': last_appointment})


def block_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.profile.status = 'Blocked'
    user.profile.save()
    
    return redirect('WMSUadmin_list')

def unblock_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.profile.status = 'Active'
    user.profile.save()
    return redirect('WMSUadmin_list')

def block_usera(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.profile.status = 'Blocked'
    user.profile.save()
    return redirect('WMSUadmin_listFaculty')

def unblock_usera(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.profile.status = 'Active'
    user.profile.save()
    return redirect('WMSUadmin_listFaculty')


def admin_list(request):
   
    users_with_profiles = User.objects.select_related('profile').all()
    

    return render(request, 'WmsuClinicApp/admin_list.html', {'users_with_profiles': users_with_profiles})

from django.db.models import Count

def WMSUadmin_list(request):
    users_with_profiles = User.objects.select_related('profile').all()

    for user in users_with_profiles:
        user.num_reports = Appointment.objects.filter(user=user).exclude(report__isnull=True).count()
        user.appointments = user.appointment_set.all()
        
       
        user.status_counts = user.appointments.values('status').annotate(count=Count('status'))

    return render(request, 'WmsuClinicApp/WMSUadmin_list.html', {
        'users_with_profiles': users_with_profiles,
    })



def WMSUadmin_listFaculty(request):
   
    users_with_profiles = User.objects.select_related('profile').all()

    for user in users_with_profiles:
        user.num_reports = Appointment.objects.filter(user=user).exclude(report__isnull=True).count()
        user.appointments = user.appointment_set.all()
        
       
        user.status_counts = user.appointments.values('status').annotate(count=Count('status'))
    return render(request, 'WmsuClinicApp/WMSUadmin_listFaculty.html', {'users_with_profiles': users_with_profiles})
def admin_listFaculty(request):
   
    users_with_profiles = User.objects.select_related('profile').all()

    return render(request, 'WmsuClinicApp/admin_listFaculty.html', {'users_with_profiles': users_with_profiles})



from django.utils import timezone
def appointment_reports(request):
    today = timezone.localtime(timezone.now()).date()
    appointment_reports = AppointmentReport.objects.filter(report_date__date=today)
    return render(request, 'WmsuClinicApp/WMSUadminreport.html', {'appointment_reports': appointment_reports})


def appointment_reportslist(request):
    appointment_reports = AppointmentReport.objects.all()
    return render(request, 'WmsuClinicApp/WMSUadminreportlist.html', {'appointment_reports': appointment_reports})


def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            admin_username = form.cleaned_data.get('username')
            admin_password = form.cleaned_data.get('password')
            user = authenticate(request, username=admin_username, password=admin_password)
            if user is not None:
                if user.is_admin:  
                    login(request, user)
                    return redirect('admin_DashboardWMSU')
                else:
                    messages.error(request, "You do not have permission to access the admin panel.")
            else:
                messages.error(request, "Invalid admin username or password.")
    else:
        form = AdminLoginForm()
    return render(request, 'WmsuClinicApp/admin_login.html', {'form': form})



from datetime import datetime
import json
from django.db.models import Count

from django.db.models.functions import ExtractMonth, ExtractYear

def admin_Dashboard(request):
    
    appointments = Appointment.objects.all()

    total_appointments_by_month = appointments.annotate(
        month=ExtractMonth('preferred_date'),
        year=ExtractYear('preferred_date')
    ).values('month', 'year').annotate(count=Count('appointment_id'))

    months = [appointment['month'] for appointment in total_appointments_by_month]
    years =  [appointment['year'] for appointment in total_appointments_by_month]
    counts = [appointment['count'] for appointment in total_appointments_by_month]

    total_appointments_data = {
        'months': months,
        'years' : years,
        'counts': counts,
    }

    pending_count = appointments.filter(status='Pending').count()
    session_done_count = appointments.filter(status='Session Done').count()
    failed_to_attend_count = appointments.filter(status='Failed to Attend').count()
    decline_count = appointments.filter(status='Decline').count()

    consultation_count = appointments.filter(purpose='Consultation').count()
    cleaning_count = appointments.filter(purpose='Cleaning').count()
    extraction_count = appointments.filter(purpose='Extraction').count()

    student_profiles_count = Profile.objects.filter(user_type='Student').count()
    faculty_profiles_count = Profile.objects.filter(user_type='FacultyandStaff').count()

    pie_chart_data = {
        'Pending': pending_count,
        'Session Done': session_done_count,
        'Failed to Attend': failed_to_attend_count,
        'Decline': decline_count,
    }

    appointment_bar_chart_json = {
        'Consultation': consultation_count,
        'Cleaning': cleaning_count,
        'Extraction': extraction_count,
    }

    profile_bar_chart_data = {
        'Student': student_profiles_count,
        'Faculty and Staff': faculty_profiles_count,
    }

    pie_chart_data_json = json.dumps(pie_chart_data)
    profile_bar_chart_json = json.dumps(profile_bar_chart_data)
    appointment_bar_chart_json = json.dumps(appointment_bar_chart_json)
    total_appointments_data_json = json.dumps(total_appointments_data)

    context = {
        'appointments': appointments,
        'total_appointments_data': total_appointments_data_json,
        'pie_chart_data': pie_chart_data_json,  
        'profile_chart_data': profile_bar_chart_json,
        'appointment_bar_chart_json': appointment_bar_chart_json,
    }

    return render(request, 'WmsuClinicApp/AdminDashboard.html', context)

def admin_DashboardWMSU(request):

    appointments = Appointment.objects.all()

    total_appointments_by_month = appointments.annotate(
        month=ExtractMonth('preferred_date'),
        year=ExtractYear('preferred_date')
    ).values('month', 'year').annotate(count=Count('appointment_id'))

    months = [appointment['month'] for appointment in total_appointments_by_month]
    years =  [appointment['year'] for appointment in total_appointments_by_month]
    counts = [appointment['count'] for appointment in total_appointments_by_month]

    total_appointments_data = {
        'months': months,
        'years' : years,
        'counts': counts,
    }

    pending_count = appointments.filter(status='Pending').count()
    session_done_count = appointments.filter(status='Session Done').count()
    failed_to_attend_count = appointments.filter(status='Failed to Attend').count()
    decline_count = appointments.filter(status='Decline').count()

    consultation_count = appointments.filter(purpose='Consultation').count()
    cleaning_count = appointments.filter(purpose='Cleaning').count()
    extraction_count = appointments.filter(purpose='Extraction').count()

    student_profiles_count = Profile.objects.filter(user_type='Student').count()
    faculty_profiles_count = Profile.objects.filter(user_type='FacultyandStaff').count()

    pie_chart_data = {
        'Pending': pending_count,
        'Session Done': session_done_count,
        'Failed to Attend': failed_to_attend_count,
        'Decline': decline_count,
    }

    appointment_bar_chart_json = {
        'Consultation': consultation_count,
        'Cleaning': cleaning_count,
        'Extraction': extraction_count,
    }

    profile_bar_chart_data = {
        'Student': student_profiles_count,
        'Faculty and Staff': faculty_profiles_count,
    }

    pie_chart_data_json = json.dumps(pie_chart_data)
    profile_bar_chart_json = json.dumps(profile_bar_chart_data)
    appointment_bar_chart_json = json.dumps(appointment_bar_chart_json)
    total_appointments_data_json = json.dumps(total_appointments_data)

    context = {
        'appointments': appointments,
        'total_appointments_data': total_appointments_data_json,
        'pie_chart_data': pie_chart_data_json,  
        'profile_chart_data': profile_bar_chart_json,
        'appointment_bar_chart_json': appointment_bar_chart_json,
    }


    return render(request, 'WmsuClinicApp/WMSUAdminDashboard.html', context)

def admin_homesite(request):
    profiles = Profile.objects.all()
    admins = Admin.objects.all()
    doctors = Doctor.objects.all()
    assistants = Assistant.objects.all()
    
    today = timezone.localtime(timezone.now()).date()
    appointments = Appointment.objects.filter(preferred_date=today)
    sorted_appointments = sorted(appointments, key=lambda x: datetime.strptime(x.preferred_time.split(' - ')[0], '%I:%M %p').time())
    
    
    context = {
        'profiles': profiles,
        'admins': admins,
        'doctors': doctors,
        'assistants': assistants,
        'appointments': sorted_appointments,
    }

    return render(request, 'WmsuClinicApp/AdminHomesite.html', context)



def update_appointment(request, appointment_id):
    appointment = Appointment.objects.get(appointment_id=appointment_id)
    
    if request.method == 'POST':
        form = RescheduleForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('admin_homesite')
    else:
        form = RescheduleForm(instance=appointment)

    context = {
        'form': form,
    }

    return render(request, 'WmsuClinicApp/UpdateAppointment.html', context)

from .models import Appointment

from django.db.models import Q


def view_profile(request):
    if not request.user.is_authenticated:
        return redirect('my-login') 

    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    appointments = Appointment.objects.filter(user=request.user).order_by('-preferred_date')
    consultation_count = appointments.filter(Q(purpose='Consultation') | Q(purpose='Consultation X')).count()
    cleaning_count = appointments.filter(Q(purpose='Cleaning') | Q(purpose='Cleaning X')).count()
    extraction_count = appointments.filter(Q(purpose='Extraction') | Q(purpose='Extraction X')).count()

    
    

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('view_profile')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
        'appointments': appointments,
        'consultation_count': consultation_count,
        'cleaning_count': cleaning_count,
        'extraction_count': extraction_count,
    }

    return render(request, 'WmsuClinicApp/profile.html', context)


def appointment_view(request):
    if not request.user.is_authenticated:
        return redirect('my-login') 

    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    appointments = Appointment.objects.filter(user=request.user).order_by('-preferred_date')
    consultation_count = appointments.filter(Q(purpose='Consultation') | Q(purpose='Consultation X')).count()
    cleaning_count = appointments.filter(Q(purpose='Cleaning') | Q(purpose='Cleaning X')).count()
    extraction_count = appointments.filter(Q(purpose='Extraction') | Q(purpose='Extraction X')).count()

    
    

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
        'appointments': appointments,
        'consultation_count': consultation_count,
        'cleaning_count': cleaning_count,
        'extraction_count': extraction_count,
    }
    return render(request, 'WmsuClinicApp/profile_appoinment.html', context) 
def see_profile(request, username):
    if not request.user.is_authenticated:
        return redirect('my-login')

    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    
    appointments = Appointment.objects.filter(user=user).order_by('-preferred_date')
    consultation_count = appointments.filter(Q(purpose='Consultation') | Q(purpose='Consultation X')).count()
    cleaning_count = appointments.filter(Q(purpose='Cleaning') | Q(purpose='Cleaning X')).count()
    extraction_count = appointments.filter(Q(purpose='Extraction') | Q(purpose='Extraction X')).count()

    context = {
        'user': user,
        'profile': profile,
        'appointments': appointments,
        'consultation_count': consultation_count,
        'cleaning_count': cleaning_count,
        'extraction_count': extraction_count,
    }

    return render(request, 'WmsuClinicApp/see_profile.html', context)

def see_profilefaculty(request, username):
    if not request.user.is_authenticated:
        return redirect('my-login')

    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    
    appointments = Appointment.objects.filter(user=user).order_by('-preferred_date')
    consultation_count = appointments.filter(Q(purpose='Consultation') | Q(purpose='Consultation X')).count()
    cleaning_count = appointments.filter(Q(purpose='Cleaning') | Q(purpose='Cleaning X')).count()
    extraction_count = appointments.filter(Q(purpose='Extraction') | Q(purpose='Extraction X')).count()

    context = {
        'user': user,
        'profile': profile,
        'appointments': appointments,
        'consultation_count': consultation_count,
        'cleaning_count': cleaning_count,
        'extraction_count': extraction_count,
    }

    return render(request, 'WmsuClinicApp/see_profilefaculty.html', context)

def select_user_type(request):
    

    return render(request, 'WmsuClinicApp/Usertype.html')


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():  # Check if the form data is valid
            form.save()  # Save the form data if it's valid
            # Redirect to a success page or do something else
        else:
            # If form data is not valid, handle the error
            # You can pass the form with errors back to the template
            context = {'registerform': form}
            return render(request, 'WmsuClinicApp/register.html', context=context)
    else:
        form = CreateUserForm()
    
    context = {'registerform': form}
    return render(request, 'WmsuClinicApp/register.html', context=context)

        
def register_faculty(request):
    if request.method == 'POST':
        form = CreateUserFormFaculty(request.POST)
        if form.is_valid():  # Check if the form data is valid
            form.save()  # Save the form data if it's valid
            # Redirect to a success page or do something else
        else:
            # If form data is not valid, handle the error
            # You can pass the form with errors back to the template
            context = {'register_form': form}
            return render(request, 'WmsuClinicApp/register_faculty.html', context=context)
    else:
        form = CreateUserFormFaculty()
    
    context = {'register_form': form}
    return render(request, 'WmsuClinicApp/register_faculty.html', context=context)



from django.contrib.auth import authenticate, login
from .forms import LoginForm  # Import your custom LoginForm

def my_login(request):
    error_message = None
    form = LoginForm()  

    if request.method == 'POST':
        form = LoginForm(data=request.POST) 

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                
            else:
                error_message = "Invalid username or password. Please try again."

    return render(request, 'WmsuClinicApp/my-login.html', {'loginform': form, 'error_message': error_message})

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import CustomPasswordChangeForm

def change_password(request):
    error_message = None
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            return redirect('WmsuDentalhomepage')  
        else:
            error_message = "Invalid form data. Please correct the errors."
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'WmsuClinicApp/change_password.html', {'form': form, 'error_message': error_message})

@login_required(login_url="my_login")
def WmsuDentalhomepage(request):
    current_user = request.user  
    today = timezone.localtime(timezone.now()).date()
    appointments = Appointment.objects.filter(preferred_date=today)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, request.FILES)
        form.user = current_user  
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = current_user
            appointment.save()
            return redirect('appointment_details', appointment_id=appointment.appointment_id)
    else:
        form = AppointmentForm()
        
    try:
        profile = current_user.profile
    except Profile.DoesNotExist:
        profile = None
    
    users = User.objects.filter(id=current_user.id)
    
    if current_user.profile.status == 'Blocked':
        error_message = "Your account is blocked. Please contact the WMSU Dental Clinic Administrator."
        return render(request, 'WmsuClinicApp/my-login.html', {'error_message': error_message})
    
    return render(request, 'WmsuClinicApp/WmsuDentalhomepage.html', {'users': users, 'form': form, 'profile': profile, 'appointments': appointments})
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('my_login')


def Homepage(request):

    return render(request, 'WmsuClinicApp/Homepage.html')






