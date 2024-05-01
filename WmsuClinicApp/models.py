
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def user_profile_picture_path(instance, filename):
    
    return f'profile_pictures/{instance.user.first_name}_{instance.user.last_name}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name  = models.CharField(max_length=100, blank=True, null=True)
    ID_Number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10)
    department = models.CharField(max_length=100, blank=True, null=True)
    course = models.CharField(max_length=100, blank=True, null=True)
    contact_number = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path , blank=True, null=True)
    STATUS_IN_LIFE_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
    ]
    status_in_life = models.CharField(max_length=20, choices=STATUS_IN_LIFE_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=10, default='Active')
    USER_TYPE_CHOICES = [
        ('Student', 'Student'),
        ('FacultyandStaff', 'Faculty and Staff'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES,blank=True, null=True)

    position = models.CharField(max_length=100, blank=True, null=True)
    home_address = models.TextField(blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)
    height_Centimeters= models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight_Kilogram = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True) 
    date_of_birth = models.DateField(blank=True, null=True)
    place_of_birth = models.CharField(max_length=100, blank=True, null=True)
    parent_name = models.CharField(max_length=100, blank=True, null=True)
    parent_address = models.TextField(blank=True, null=True)
    parent_telephone_number = models.CharField(max_length=15, blank=True, null=True)
    relationship = models.CharField(max_length=50, blank=True, null=True)

class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin_username = models.CharField(max_length=50, unique=True)
    admin_password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=30, blank=True, null=True)




class DentalUser(models.Model):
    dental_id = models.CharField(max_length=100, unique=True,blank=True, null=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    

    
class Doctor(models.Model):
    Doctor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,null=True, blank=True)
    specialization = models.CharField(max_length=100,null=True, blank=True)
    status = models.CharField(max_length=50, default='Not on Duty')
    birthday = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    civil_status = models.CharField(max_length=50, null=True, blank=True)
    secondary_high_school = models.CharField(max_length=100, null=True, blank=True)
    college = models.CharField(max_length=100, null=True, blank=True)
    pre_med = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return ""
    

class Assistant(models.Model):
    Assistant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,null=True, blank=True)
    role = models.CharField(max_length=50,null=True, blank=True)
    status = models.CharField(max_length=50, default='Not on Duty')
    birthday = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    civil_status = models.CharField(max_length=50, null=True, blank=True)
    secondary_high_school = models.CharField(max_length=100, null=True, blank=True)
    college = models.CharField(max_length=100, null=True, blank=True)

    

class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    preferred_date = models.DateField(null=True, blank=True)
    preferred_time = models.CharField(max_length=70,null=True, blank=True)
    purpose = models.CharField(max_length=100)
    comments = models.TextField(blank=True, null=True)
    cor_upload = models.FileField(upload_to='cor_uploads/', null=True, blank=True)
    reference_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    current_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    status = models.CharField(max_length=20, default='Pending')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE, null=True, blank=True)
    resched_status = models.CharField(max_length=20, null=True, blank=True)
    


    
    def __str__(self):
        return f"Appointment {self.appointment_id} - {self.user.username}"
    
class AppointmentReport(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='report')
    report_date = models.DateTimeField(default=timezone.now)
    report_content = models.TextField()
    report_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Report for {self.appointment}"
    
class DentalExtraction(models.Model):
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE)
    extraction_record = models.CharField(max_length=100)
    extraction_datetime = models.DateTimeField(null=True, blank=True)
    
class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    time = models.CharField(max_length=500, null=True, blank=True)
    Text = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.doctor.name} - {self.date} - {self.time}"

    
class DentalSupply(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    
    
    def __str__(self):
        return self.name   
    
class Semester(models.Model):
    SEMESTER_CHOICES = (
        (1, 'Semester 1'),
        (2, 'Semester 2'),
    )

    semester_id = models.AutoField(primary_key=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    current_date = models.DateField(default=timezone.now,null=True, blank=True)
    semester_choice = models.IntegerField(choices=SEMESTER_CHOICES,null=True, blank=True)



