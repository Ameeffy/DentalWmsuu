
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

from django.forms.widgets import PasswordInput, TextInput

from .models import Profile

from django import forms
from .models import DentalUser
from .models import DentalExtraction
from datetime import date
from .models import Profile
from .models import Admin
from .models import Appointment
from .models import Doctor, Assistant
from .models import DoctorAvailability
from datetime import datetime
import datetime
from django.utils import timezone
from .models import DentalSupply
from .models import Profile

from django import forms
from django.contrib.auth.models import User
from .models import Profile

from .models import AppointmentReport
from .models import Semester

from django import forms
from .models import Semester

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
class UpdatePurposeForm(forms.ModelForm):
    PURPOSE_CHOICES = [
        ('', 'Select Purpose'),
        ('Consultation', 'Consultation'),
        ('Cleaning', 'Cleaning'),
        ('Extraction', 'Extraction'),
    ]
    
    purpose = forms.ChoiceField(choices=PURPOSE_CHOICES, label='New Purpose')

    class Meta:
        model = Appointment
        fields = ['purpose']
class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['start_date', 'end_date', 'semester_choice']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'})
        }


class AppointmentReportForm(forms.ModelForm):
    REPORT_CHOICES = [
        ('Malicious content', 'Malicious content'),
        ('ID Number is not matched', 'ID Number is not matched'),
         ('False information', 'False information'),
        ('Malicious content', 'Malicious content'),
        ('Inappropriate behavior', 'Inappropriate behavior'),
        ('Spam', 'Spam'),
        ('Violence', 'Violence'),
        ('Other', 'Other'),
    ]

    report_content = forms.ChoiceField(choices=REPORT_CHOICES, widget=forms.RadioSelect, required=True)
    report_description = forms.CharField(label='Report Description', required=False, widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}))

    class Meta:
        model = AppointmentReport
        fields = ['report_content', 'report_description']

    
class ForgotPasswordForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if not username or not email:
            raise ValidationError("Please enter both username and email.")
        
        if not User.objects.filter(username=username, email=email).exists():
            raise ValidationError("Invalid credentials.")

        return cleaned_data

class VerifyUserForm(forms.Form):
    ID_Number = forms.CharField(label='ID Number', max_length=100)



class ResetPasswordForm(forms.Form):
    password = forms.CharField(label='New Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")


class ExtractionRecordForm(forms.ModelForm):
    UPPER_RIGHT_QUADRANT_CHOICES = (
        ('Right Third Molar (Wisdom Tooth)', 'Right Third Molar (Wisdom Tooth) - #1'),
        ('Right Second Molar', 'Right Second Molar - #2'),
        ('Right First Molar', 'Right First Molar - #3'),
        ('Right Second Premolar (Bicuspid)', 'Right Second Premolar (Bicuspid) - #4'),
        ('Right First Premolar (Bicuspid)', 'Right First Premolar (Bicuspid) - #5'),
        ('Right Canine (Cuspid)', 'Right Canine (Cuspid) - #6'),
        ('Right Lateral Incisor', 'Right Lateral Incisor - #7'),
        ('Right Central Incisor', 'Right Central Incisor - #8'),
    )

    UPPER_LEFT_QUADRANT_CHOICES = (
        ('Left Central Incisor', 'Left Central Incisor - #9'),
        ('Left Lateral Incisor', 'Left Lateral Incisor - #10'),
        ('Left Canine (Cuspid)', 'Left Canine (Cuspid) - #11'),
        ('Left First Premolar (Bicuspid)', 'Left First Premolar (Bicuspid) - #12'),
        ('Left Second Premolar (Bicuspid)', 'Left Second Premolar (Bicuspid) - #13'),
        ('Left First Molar', 'Left First Molar - #14'),
        ('Left Second Molar', 'Left Second Molar - #15'),
        ('Left Third Molar (Wisdom Tooth)', 'Left Third Molar (Wisdom Tooth) - #16'),
    )

    LOWER_LEFT_QUADRANT_CHOICES = (
        ('Left Third Molar (Wisdom Tooth)', 'Left Third Molar (Wisdom Tooth) - #17'),
        ('Left Second Molar', 'Left Second Molar - #18'),
        ('Left First Molar', 'Left First Molar - #19'),
        ('Left Second Premolar (Bicuspid)', 'Left Second Premolar (Bicuspid) - #20'),
        ('Left First Premolar (Bicuspid)', 'Left First Premolar (Bicuspid) - #21'),
        ('Left Canine (Cuspid)', 'Left Canine (Cuspid) - #22'),
        ('Left Lateral Incisor', 'Left Lateral Incisor - #23'),
        ('Left Central Incisor', 'Left Central Incisor - #24'),
    )

    LOWER_RIGHT_QUADRANT_CHOICES = (
        ('Right Central Incisor', 'Right Central Incisor - #25'),
        ('Right Lateral Incisor', 'Right Lateral Incisor - #26'),
        ('Right Canine (Cuspid)', 'Right Canine (Cuspid) - #27'),
        ('Right First Premolar (Bicuspid)', 'Right First Premolar (Bicuspid) - #28'),
        ('Right Second Premolar (Bicuspid)', 'Right Second Premolar (Bicuspid) - #29'),
        ('Right First Molar', 'Right First Molar - #30'),
        ('Right Second Molar', 'Right Second Molar - #31'),
        ('Right Third Molar (Wisdom Tooth)', 'Right Third Molar (Wisdom Tooth) - #32'),
    )

    
    
    extraction_record = forms.MultipleChoiceField(
        required=False,  # Set required to False
        choices=(
            UPPER_RIGHT_QUADRANT_CHOICES +
            UPPER_LEFT_QUADRANT_CHOICES +
            LOWER_LEFT_QUADRANT_CHOICES +
            LOWER_RIGHT_QUADRANT_CHOICES
        ),
        widget=forms.CheckboxSelectMultiple(),
    )

    def clean_extraction_record(self):
        data = self.cleaned_data['extraction_record']
        if not data:
            raise forms.ValidationError("Please select at least one option.")
        return data

    class Meta:
        model = DentalExtraction
        fields = ['extraction_record', 'extraction_datetime']


        


class LoginDental(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                user = DentalUser.objects.get(username=username)
                if user.password != password:
                    self.add_error('password', "Incorrect password. Please try again.")
            except DentalUser.DoesNotExist:
                self.add_error('username', "Username does not exist. Please try again.")

        return cleaned_data
    
    
    
class ChangePasswordForm(forms.Form):
    dental_id = forms.CharField(max_length=100, initial="1", widget=forms.HiddenInput)
    current_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    new_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if new_password and confirm_new_password and new_password != confirm_new_password:
            raise ValidationError("The new passwords do not match.")

        if new_password:
            if len(new_password) < 8:
                raise ValidationError("The new password must be at least 8 characters long.")
            if not new_password[0].isupper():
                raise ValidationError("The new password must start with a capital letter.")
            
        

        


    

class DentalSupplyForm(forms.ModelForm):
    class Meta:
        model = DentalSupply
        fields = ['name', 'description', 'quantity']

class DentalSupplyFormquantity(forms.ModelForm):
    class Meta:
        model = DentalSupply
        fields = ['quantity']

TIME_CHOICES = [
    ('8:00 AM - 8:30 AM', '8:00 AM - 8:30 AM'),
    ('8:30 AM - 9:00 AM', '8:30 AM - 9:00 AM'),
    ('9:00 AM - 9:30 AM', '9:00 AM - 9:30 AM'),
    ('9:30 AM - 10:00 AM', '9:30 AM - 10:00 AM'),
    ('10:00 AM - 10:30 AM', '10:00 AM - 10:30 AM'),
    ('10:30 AM - 11:00 AM', '10:30 AM - 11:00 AM'),
    ('11:00 AM - 11:30 AM', '11:00 AM - 11:30 AM'),
    ('11:30 AM - 12:00 NOON', '11:30 AM - 12:00 PM'),
   
    ('1:00 PM - 1:30 PM', '1:00 PM - 1:30 PM'),
    ('1:30 PM - 2:00 PM', '1:30 PM - 2:00 PM'),
    ('2:00 PM - 2:30 PM', '2:00 PM - 2:30 PM'),
    ('2:30 PM - 3:00 PM', '2:30 PM - 3:00 PM'),
    ('3:00 PM - 3:30 PM', '3:00 PM - 3:30 PM'),
    ('3:30 PM - 4:00 PM', '3:30 PM - 4:00 PM'),
    
]
class RescheduleForm(forms.ModelForm):
    preferred_date = forms.DateField(label='Preferred Date', widget=forms.TextInput(attrs={'type': 'date'}))
    preferred_time = forms.ChoiceField(choices=TIME_CHOICES, label='Preferred Time')

    class Meta:
        model = Appointment
        fields = ['preferred_date', 'preferred_time', 'resched_status']
        widgets = {
            'resched_status': forms.HiddenInput(),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.resched_status = "Rescheduled"
        if commit:
            instance.save()
        return instance





class DoctorAvailabilityForm(forms.ModelForm):
    TIME_CHOICES = [
        ('', 'You only once select this'),
        ('Whole day', 'Doctor is not available for today '),
        ('AM', 'Doctor is not available Morning '),
        ('PM', 'Doctor is not available Afternoon '),
    ]
    
    date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),required=False)
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), to_field_name='name')
    time = forms.ChoiceField(choices=TIME_CHOICES, required=False)

    class Meta:
        model = DoctorAvailability
        fields = ['doctor', 'date', 'start_date', 'end_date', 'time', 'Text']
   

class DoctorForm(forms.ModelForm):
    CIVIL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Separated', 'Separated'),
        ('Widowed', 'Widowed'),
    ]

    civil_status = forms.ChoiceField(choices=CIVIL_STATUS_CHOICES)

    class Meta:
        model = Doctor
        fields = ['name', 'specialization', 'birthday', 'address', 'civil_status', 'secondary_high_school', 'college', 'pre_med']

        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'name': forms.TextInput(attrs={'placeholder': 'First Name, Middle Name, Last Name'}),
        }

        labels = {
            'name': 'Full Name',
        }

class AssistantForm(forms.ModelForm):
    CIVIL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Separated', 'Separated'),
        ('Widowed', 'Widowed'),
    ]

    civil_status = forms.ChoiceField(choices=CIVIL_STATUS_CHOICES)

    class Meta:
        model = Assistant
        fields = ['name', 'role', 'birthday', 'address', 'civil_status', 'secondary_high_school', 'college']

        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'name': forms.TextInput(attrs={'placeholder': 'First Name, Middle Name, Last Name'}),
        }

        labels = {
            'name': 'Full Name',
        }

class AppointmentForm(forms.ModelForm):

    PURPOSE_CHOICES = [
        ('', 'Select Purpose'),
        ('Consultation', 'Consultation'),
        ('Cleaning', 'Cleaning'),
        ('Extraction', 'Extraction'),
]

    purpose = forms.ChoiceField(choices=PURPOSE_CHOICES, label='Purpose')

    
    TIME_CHOICES = [
    ('8:00 AM - 8:30 AM', '8:00 AM - 8:30 AM'),
    ('8:30 AM - 9:00 AM', '8:30 AM - 9:00 AM'),
    ('9:00 AM - 9:30 AM', '9:00 AM - 9:30 AM'),
    ('9:30 AM - 10:00 AM', '9:30 AM - 10:00 AM'),
    ('10:00 AM - 10:30 AM', '10:00 AM - 10:30 AM'),
    ('10:30 AM - 11:00 AM', '10:30 AM - 11:00 AM'),
    ('11:00 AM - 11:30 AM', '11:00 AM - 11:30 AM'),
   ('11:30 AM - 12:00 NOON', '11:30 AM - 12:00 PM'),
   
    ('1:00 PM - 1:30 PM', '1:00 PM - 1:30 PM'),
    ('1:30 PM - 2:00 PM', '1:30 PM - 2:00 PM'),
    ('2:00 PM - 2:30 PM', '2:00 PM - 2:30 PM'),
    ('2:30 PM - 3:00 PM', '2:30 PM - 3:00 PM'),
    ('3:00 PM - 3:30 PM', '3:00 PM - 3:30 PM'),
    ('3:30 PM - 4:00 PM', '3:30 PM - 4:00 PM'),
    
]


    
    preferred_date = forms.DateField(label='Preferred Date', widget=forms.TextInput(attrs={'type': 'date'}))
    
    preferred_time = forms.ChoiceField(choices=TIME_CHOICES, label='Preferred Time')
    comments = forms.CharField(label='Comments', required= False, widget=forms.Textarea(attrs={'placeholder': 'Please indicate, if any..', 'class': 'large-text-input'}))
    cor_upload = forms.FileField(label='Cor Upload', required=True)

    class Meta:
        model = Appointment
        fields = ['preferred_date','preferred_time', 'purpose', 'comments', 'cor_upload', 'reference_number', 'doctor', 'assistant']
        ordering = ['preferred_time']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        instance = super(AppointmentForm, self).save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance
    

    def clean(self):
       
        cleaned_data = super().clean()
        preferred_date = cleaned_data.get('preferred_date')
        preferred_time = cleaned_data.get('preferred_time')
        purpose = cleaned_data.get('purpose')
        user = self.user
       
        if not Semester.objects.filter(start_date__lte=preferred_date, end_date__gte=preferred_date).exists():
                raise forms.ValidationError("Semester is not yet set you cannot make appointments outside the range. Please choose another date.")


        if purpose == 'Extraction' and preferred_date:
            if 1 <= preferred_date.month <= 5:
                semester = 'first_semester'
            else:
                semester = 'second_semester'

        if purpose == 'Extraction':
            if preferred_date:
                semester = self.get_semester(preferred_date)
                existing_extraction = Appointment.objects.filter(user=self.user, purpose='Extraction', preferred_date__range=(semester.start_date, semester.end_date)).exists()
                if existing_extraction:
                    raise forms.ValidationError("You have already selected 'Extraction' for this semester.")
     
        
        if preferred_date and preferred_time:
            existing_appointment = Appointment.objects.filter(
                preferred_date=preferred_date,
                preferred_time=preferred_time
            ).exists()

            if existing_appointment:
                
                self.add_error(None, forms.ValidationError("This date and time slot is already booked. Please choose another date and time."))

        if Appointment.objects.filter(user=self.user, preferred_date=preferred_date).exists():
           raise forms.ValidationError("You already have an appointment scheduled for this day. Please choose another date.")
        
        if preferred_date and Appointment.objects.filter(user=user, status='Pending').exists():
            raise forms.ValidationError("You already have a pending appointment. You cannot set another appointment until the pending one is resolved.")


      
        if preferred_date:
            
                doctor_availability_exists = DoctorAvailability.objects.filter(
                    date=preferred_date,
                    time='Whole day'
        ).exists()
                if doctor_availability_exists:
                    raise forms.ValidationError(
                         "The Dentist is not available for the whole day on the selected date. Please choose another date or time."
            )      

        if preferred_date and preferred_time:
            doctor_availability_exists = DoctorAvailability.objects.filter(    
                date=preferred_date,
                time__contains="AM"
            ).exists()

            if doctor_availability_exists and "AM" in preferred_time:
                 self.add_error(
            None,
            forms.ValidationError("The Dentist is not available in the morning. Please choose another date and time.")
        )
                 
        if preferred_date and preferred_time:
            doctor_availability_exists = DoctorAvailability.objects.filter(  
                date=preferred_date,
                time__contains="PM"
            ).exists()
            if doctor_availability_exists and "PM" in preferred_time:
                 self.add_error(
            None,
            forms.ValidationError("The Dentist is not available in the afternoon. Please choose another date and time.")

                 )

                
        if preferred_date:
        
           if preferred_date.weekday() in [5, 6]:
            raise forms.ValidationError("The clinic is closed on Saturdays and Sundays. Please choose another date.")
           
        if preferred_date and preferred_date < date.today():
            raise forms.ValidationError("Preferred date cannot be in the past. Please choose a date from today onwards.")
        
    
        doctor_leave = DoctorAvailability.objects.filter(start_date__lte=preferred_date, end_date__gte=preferred_date)
        
        if doctor_leave.exists():
            raise forms.ValidationError("The doctor is on leave on the selected date. Please choose another date.")
           
      
        


        return cleaned_data
    
    def get_semester(self, date):
        try:
            semester = Semester.objects.get(start_date__lte=date, end_date__gte=date)
            return semester
        except Semester.DoesNotExist:
            raise forms.ValidationError("There is no semester for the selected date.")

                
    


    def save(self, commit=True):
        instance = super(AppointmentForm, self).save(commit=False)

        instance.reference_number = self.generate_unique_reference_number()

        
        available_doctor = Doctor.objects.filter(status='On Duty').first()
        available_assistant = Assistant.objects.filter(status='On Duty').first()

        if available_doctor:
            instance.doctor = available_doctor

        if available_assistant:
            instance.assistant = available_assistant

        if commit:
            instance.save()

        return instance
    def generate_unique_reference_number(self):
        
        import time
        import random

        timestamp_str = str(int(time.time()))
        random_str = str(random.randint(10000, 99999))

        return f"WMSU-{timestamp_str}-{random_str}"
    


    

class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['admin_username', 'admin_password', 'first_name', 'last_name']

class AdminLoginForm(forms.Form):
    admin_username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})
    )
    admin_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        admin_username = cleaned_data.get('admin_username')
        admin_password = cleaned_data.get('admin_password')

        if admin_username and admin_password:
            try:
                user = Admin.objects.get(admin_username=admin_username)
                if user.admin_password != admin_password:
                    self.add_error('admin_password', "Incorrect password. Please try again.")
            except Admin.DoesNotExist:
                self.add_error('admin_username', "Username does not exist. Please try again.")

        return cleaned_data



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'height_Centimeters', 'weight_Kilogram']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['profile_picture'].widget.attrs.update({'class': 'form-control-file'})

   




COURSE_CHOICES = [
    ('', 'Select your Course'),
    ('Bachelor of Science in Accountancy', 'Bachelor of Science in Accountancy'),
    ('Bachelor of Science in Biology', 'Bachelor of Science in Biology'),
    ('Bachelor of Science in Business Administration', 'Bachelor of Science in Business Administration'),
    ('Bachelor of Science in Chemistry', 'Bachelor of Science in Chemistry'),
    ('Bachelor of Science in Civil Engineering', 'Bachelor of Science in Civil Engineering'),
    ('Bachelor of Science in Computer Science', 'Bachelor of Science in Computer Science'),
    ('Bachelor of Science in Electrical Engineering', 'Bachelor of Science in Electrical Engineering'),
    ('Bachelor of Science in Environmental Engineering', 'Bachelor of Science in Environmental Engineering'),
    ('Bachelor of Science in Information Technology', 'Bachelor of Science in Information Technology'),
    ('Bachelor of Science in Mathematics', 'Bachelor of Science in Mathematics'),
    ('Bachelor of Science in Mechanical Engineering', 'Bachelor of Science in Mechanical Engineering'),
    ('Bachelor of Science in Nursing', 'Bachelor of Science in Nursing'),
    ('Bachelor of Science in Nutrition and Dietetics', 'Bachelor of Science in Nutrition and Dietetics'),
    ('Bachelor of Science in Physics', 'Bachelor of Science in Physics'),
    ('Bachelor of Science in Psychology', 'Bachelor of Science in Psychology'),
    
]
DEPARTMENT_CHOICES = [
    ('', 'Select your College Department'),
    ('Computer Computing Studies', 'Computer Computing Studies'),
    ('College of Engineering', 'College of Engineering'),
    ('College of Nursing', 'College of Nursing'),
    
    
]
USER_TYPE_CHOICES = [
        ('Student', 'Student'),
        
    ]
STATUS_IN_LIFE_CHOICES = [
        ('', 'Select your status'),
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
    ]
RELATIONSHIP_CHOICES = [
    ('', 'Relationship with the Contact Person'),
    ('Wife', 'Wife'),
    ('Husband', 'Husband'),
    ('Mother', 'Mother'),
    ('Father', 'Father'),
    ('Sister', 'Sister'),
    ('Brother', 'Brother'),
    ('Guardian', 'Guardian'),
]
class CreateUserForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'required': True}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'required': True}))
    email = forms.EmailField(
        label='Email Address',
        validators=[EmailValidator('@wmsu.edu.ph')], 
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address'})
    )
    course = forms.ChoiceField(label='Course', choices=COURSE_CHOICES, widget=forms.Select(attrs={'placeholder': 'Course'}))
    department = forms.ChoiceField(label='department', choices=DEPARTMENT_CHOICES, widget=forms.Select(attrs={'placeholder': 'Department'}))
    gender = forms.CharField(
    label='Gender',
    required=True,
    widget=forms.TextInput(attrs={'placeholder': 'Gender'})
)

    contact_number = forms.IntegerField(
        label='Contact Number',
        min_value=0,
        max_value=99999999999,  # Maximum 11 digits
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Contact Number', 'oninput': 'this.value = this.value.replace(/[^0-9]/g, "").slice(0, 11)'})
    )
    first_name = forms.CharField(label='First Name', max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label='Last Name', max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    middle_name = forms.CharField(label='Last Name', max_length=30, required=False, widget=forms.TextInput(attrs={'placeholder': 'Middle Name (Optional Only)'}))
    user_type = forms.ChoiceField(label='User Type', choices=USER_TYPE_CHOICES, widget=forms.Select(attrs={'placeholder': 'User Type'}))
    ID_Number = forms.IntegerField(
        label='ID Number',
        min_value=0,
        max_value=999999999999999,  # Maximum 15 digits
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'ID Number', 'oninput': 'this.value = this.value.replace(/[^0-9]/g, "").slice(0, 15)'})
    )
    status_in_life = forms.ChoiceField(label='Status in Life', choices=STATUS_IN_LIFE_CHOICES, required=True, widget=forms.Select(attrs={'placeholder': 'Status in Life'}))
    home_address = forms.CharField(label='Home Address', max_length=70, required=True, widget=forms.TextInput(attrs={'placeholder': 'Block, Lot, Barangay, City, Province, Country'}))
    religion = forms.CharField(label='Religion', max_length=15, required=True, widget=forms.TextInput(attrs={'placeholder': 'Religion'}))
    height_Centimeters = forms.DecimalField(label='Height in Centimeters', max_digits=5, decimal_places=2, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Height in Centimeters'}))  
    weight_Kilogram = forms.DecimalField(label='Weight in Kilograms', max_digits=5, decimal_places=2, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Weight in Kilograms'}))
    date_of_birth = forms.DateField(label='Date of Birth', widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Date of Birth'}), required=True)
    place_of_birth = forms.CharField(label='Place of Birth', max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Place of Birth'}))
    parent_name = forms.CharField(label='Guardian Name', max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    parent_address = forms.CharField(label='Guardian Address', max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder': 'Block, Lot, Barangay, City, Province, Country'}))
    parent_telephone_number = forms.IntegerField(
        label='Guardian Telephone Number',
        min_value=0,
        max_value=99999999999,  # Maximum 11 digits
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Telephone Number', 'oninput': 'this.value = this.value.replace(/[^0-9]/g, "").slice(0, 11)'})
    )
    
    relationship = forms.ChoiceField(label='Relationship with Guardian', choices=RELATIONSHIP_CHOICES, required=True, widget=forms.Select(attrs={'placeholder': 'Relationship with Guardian'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'ID_Number', 'password1', 'password2', 'first_name', 'last_name', 'middle_name', 'department', 'user_type', 'course', 'gender', 'contact_number','date_of_birth', 'place_of_birth', 'status_in_life', 'home_address', 'religion', 'height_Centimeters', 'weight_Kilogram', 'parent_name', 'parent_address', 'parent_telephone_number', 'relationship']

    
    
    
    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if not contact_number.isdigit() or len(contact_number) != 11:
            raise ValidationError("Contact number must be 11 digits.")
        return contact_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@wmsu.edu.ph'):
            raise ValidationError("Only email addresses with '@wmsu.edu.ph' are allowed.")
        
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")

        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
    
   
        if User.objects.filter(username=username).exists():
           raise ValidationError("This username is already in use.")
    
    
        if not username.isalpha():
           raise ValidationError("Username should only contain letters.")
    
    
        if len(username) < 5 or len(username) > 15:
           raise ValidationError("Username length should be between 5 to 15 characters.")
    
        return username
    
    def clean_ID_Number(self):
        ID_Number = self.cleaned_data.get('ID_Number')  

        
        if Profile.objects.filter(ID_Number=ID_Number).exists():  
            raise ValidationError("This ID Number is already in use.")

        return ID_Number
    
   
    
    
    
    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
           user.save()

        profile = Profile.objects.create(user=user,
                                         middle_name=self.cleaned_data['middle_name'],
                                         gender=self.cleaned_data['gender'],
                                         contact_number=self.cleaned_data['contact_number'],
                                         user_type=self.cleaned_data['user_type'],
                                         ID_Number=self.cleaned_data['ID_Number'],
                                         status_in_life=self.cleaned_data['status_in_life'],
                                         home_address=self.cleaned_data['home_address'],
                                         religion=self.cleaned_data['religion'],
                                         height_Centimeters=self.cleaned_data['height_Centimeters'],
                                         weight_Kilogram=self.cleaned_data['weight_Kilogram'],
                                         date_of_birth=self.cleaned_data['date_of_birth'],
                                         place_of_birth=self.cleaned_data['place_of_birth'],
                                         parent_name=self.cleaned_data['parent_name'],
                                         parent_address=self.cleaned_data['parent_address'],
                                         parent_telephone_number=self.cleaned_data['parent_telephone_number'],
                                         relationship=self.cleaned_data['relationship'],
                                         department=self.cleaned_data['department'],
                                         course=self.cleaned_data['course'])
        return user

COURSE_CHOICES_FACULTY = [
    ('', 'Please Select'),
    ('Teacher', 'Teacher'),
    ('Nurse', 'Nurse'),   
]

USER_TYPE_CHOICES_FACULTY = [
    ('FacultyandStaff', 'Faculty and Staff'),
   
        
    ]
class CreateUserFormFaculty(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'required': True}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'required': True}))
    email = forms.EmailField(
        label='Email Address', required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address'})
    )
    position = forms.ChoiceField(choices=COURSE_CHOICES_FACULTY)  
    gender = forms.CharField(
    label='Gender',
    required=True,
    widget=forms.TextInput(attrs={'placeholder': 'Gender'})
)

    contact_number = forms.IntegerField(
        label='Contact Number',
        min_value=0,
        max_value=99999999999,  # Maximum 11 digits
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Contact Number', 'oninput': 'this.value = this.value.replace(/[^0-9]/g, "").slice(0, 11)'})
    )
    first_name = forms.CharField(label='First Name', max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label='Last Name', max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    middle_name = forms.CharField(label='Last Name', max_length=30, required=False, widget=forms.TextInput(attrs={'placeholder': 'Middle Name (Optional Only)'}))
    user_type = forms.ChoiceField(label='User Type', choices=USER_TYPE_CHOICES_FACULTY, widget=forms.Select(attrs={'placeholder': 'User Type'}))
    ID_Number = forms.IntegerField(
        label='ID Number',
        min_value=0,
        max_value=999999999999999,  # Maximum 15 digits
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'ID Number', 'oninput': 'this.value = this.value.replace(/[^0-9]/g, "").slice(0, 15)'})
    )
    status_in_life = forms.ChoiceField(label='Status in Life', choices=STATUS_IN_LIFE_CHOICES, required=True, widget=forms.Select(attrs={'placeholder': 'Status in Life'}))
    home_address = forms.CharField(label='Home Address', max_length=70, required=True, widget=forms.TextInput(attrs={'placeholder': 'Block, Lot, Barangay, City, Province, Country'}))
    religion = forms.CharField(label='Religion', max_length=15, required=True, widget=forms.TextInput(attrs={'placeholder': 'Religion'}))
    height_Centimeters = forms.DecimalField(label='Height in Centimeters', max_digits=5, decimal_places=2, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Height in Centimeters'}))  
    weight_Kilogram = forms.DecimalField(label='Weight in Kilograms', max_digits=5, decimal_places=2, required=True, widget=forms.NumberInput(attrs={'placeholder': 'Weight in Kilograms'}))
    date_of_birth = forms.DateField(label='Date of Birth', widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Date of Birth'}), required=True)
    place_of_birth = forms.CharField(label='Place of Birth', max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Place of Birth'}))
    parent_name = forms.CharField(label='Guardian Name', max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    parent_address = forms.CharField(label='Guardian Address', max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder': 'Block, Lot, Barangay, City, Province, Country'}))
    parent_telephone_number = forms.IntegerField(
        label='Telephone Number',
        min_value=0,
        max_value=99999999999,  # Maximum 11 digits
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Contact Number', 'oninput': 'this.value = this.value.replace(/[^0-9]/g, "").slice(0, 11)'})
    )
    relationship = forms.ChoiceField(label='Relationship with Guardian', choices=RELATIONSHIP_CHOICES, required=True, widget=forms.Select(attrs={'placeholder': 'Relationship with Guardian'}))
    

    class Meta:
        model = User
        fields = ['username', 'email', 'ID_Number', 'password1', 'password2', 'first_name', 'last_name','user_type','position', 'gender', 'contact_number','date_of_birth', 'place_of_birth', 'status_in_life', 'home_address', 'religion', 'height_Centimeters', 'weight_Kilogram', 'parent_name', 'parent_address', 'parent_telephone_number', 'relationship']

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if not contact_number.isdigit() or len(contact_number) != 11:
            raise ValidationError("Contact number must be 11 digits.")
        return contact_number
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@gmail.com'):
            raise ValidationError("Only email addresses with '@gmail.com' are allowed.")
        
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")

        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
    
   
        if User.objects.filter(username=username).exists():
           raise ValidationError("This username is already in use.")
    
    
        if not username.isalpha():
           raise ValidationError("Username should only contain letters.")
    
    
        if len(username) < 5 or len(username) > 15:
           raise ValidationError("Username length should be between 5 to 15 characters.")
    
        return username
    
    def clean_ID_Number(self):
        ID_Number = self.cleaned_data.get('ID_Number')  

        
        if Profile.objects.filter(ID_Number=ID_Number).exists():  
            raise ValidationError("This ID Number is already in use.")

        return ID_Number

           
    

    def save(self, commit=True):
        user = super(CreateUserFormFaculty, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        
        user.save()

        profile = Profile.objects.create(user=user,
                                         gender=self.cleaned_data['gender'],
                                         contact_number=self.cleaned_data['contact_number'],
                                         user_type=self.cleaned_data['user_type'],
                                         ID_Number=self.cleaned_data['ID_Number'],
                                         status_in_life=self.cleaned_data['status_in_life'],
                                         home_address=self.cleaned_data['home_address'],
                                         religion=self.cleaned_data['religion'],
                                         height_Centimeters=self.cleaned_data['height_Centimeters'],
                                         weight_Kilogram=self.cleaned_data['weight_Kilogram'],
                                         date_of_birth=self.cleaned_data['date_of_birth'],
                                         place_of_birth=self.cleaned_data['place_of_birth'],
                                         parent_name=self.cleaned_data['parent_name'],
                                         parent_address=self.cleaned_data['parent_address'],
                                         parent_telephone_number=self.cleaned_data['parent_telephone_number'],
                                         relationship=self.cleaned_data['relationship'],
                                         position=self.cleaned_data['position'])
                                         
        
                                           
        if commit:
            user.save()
            profile.save()

        return user


from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            
            if not User.objects.filter(username=username).exists():
                self.add_error('username', "Username does not exist. Please try again.")
                return cleaned_data  

            
            user = authenticate(username=username, password=password)
            if user is None:
                self.add_error('password', "Incorrect password. Please try again.")

        return cleaned_data
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.password_validation import validate_password

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Old Password', widget=forms.PasswordInput(attrs={'autofocus': True})
    )
    new_password1 = forms.CharField(
        label='New Password', widget=forms.PasswordInput
    )
    new_password2 = forms.CharField(
        label='Confirm New Password', widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password1 != new_password2:
            raise ValidationError("The two password fields didn't match.")

        if old_password == new_password1:
            raise ValidationError("New password must be different from the old password.")

        validate_password(new_password1, self.user)

        # Check if new passwords match first name and last name
        user = self.user
        first_name = user.first_name.lower()
        last_name = user.last_name.lower()

        if new_password1.lower() == first_name or new_password1.lower() == last_name:
            raise ValidationError("New password must not match your first name or last name.")

        # Check length of new passwords
        if len(new_password1) != 8:
            raise ValidationError("New password must be 8 characters long.")

        return cleaned_data
