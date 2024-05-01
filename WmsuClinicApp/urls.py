from django.urls import path
from . import views
from .views import admin_list, admin_login


urlpatterns = [

   
    path('my_login', views.my_login, name="my_login"),
    path('logout/', views.logout_view, name='logout'),
    path('', views.Homepage, name=""),

    path('select_user_type/', views.select_user_type, name='select_user_type'),
    path('forgotpassword/', views.forgot_password, name='forgot_password'),
    path('verifyuser/<str:username>/', views.verify_user, name='verify_user'),
    path('resetpassword/<str:username>/', views.reset_password, name='reset_password'),
    path('register/', views.register, name="register"),
    path('change-password/', views.change_password, name='change_password'),

    path('register/faculty/', views.register_faculty, name='register_faculty'),

    path('WmsuDentalhomepage', views.WmsuDentalhomepage, name="WmsuDentalhomepage"),

    path('view_profile/', views.view_profile, name='view_profile'),
    path('see_profile/<str:username>/', views.see_profile, name='see_profile'),
    path('see_profilefaculty<str:username>/', views.see_profilefaculty, name='see_profilefaculty'),
    path('appointment/', views.appointment_view, name='appointment'),
    path('custom-admin/list/', admin_list, name='admin_list'),


    path('custom-admin/listFaculty/', views.admin_listFaculty, name='admin_listFaculty'),
    

    path('custom-admin/login/', admin_login, name='admin_login'),

    path('admin-Dashboard/', views.admin_Dashboard, name='admin_Dashboard'),
    path('admin-homesite/', views.admin_homesite, name='admin_homesite'),
    
    path('change_status/<int:appointment_id>/session_done/', views.session_done, name='session_done'),
    path('change_status/<int:appointment_id>/failed_to_attend/', views.failed_to_attend, name='failed_to_attend'),
    path('change_status/<int:appointment_id>/Decline/', views.Decline, name='Decline'),
    path('update_appointment/<int:appointment_id>/', views.update_appointment, name='update_appointment'),
   
    path('appointment/<int:appointment_id>/report/', views.appointment_report, name='appointment_report'),

    path('last_appointment/', views.last_appointment, name='last_appointment'),
    
    
    

  

    path('doctoravailability/', views.admin_doctoravailability, name='admin_doctoravailability'),
    path('semester/add/', views.add_semester, name='add_semester'),



    path('block_user/<int:user_id>/', views.block_user, name='block_user'),

    path('unblock_user/<int:user_id>/', views.unblock_user, name='unblock_user'),

    path('block_usera/<int:user_id>/', views.block_usera, name='block_usera'),

    path('unblock_usera/<int:user_id>/', views.unblock_usera, name='unblock_usera'),



    path('appointments/<int:appointment_id>/details/', views.appointment_details, name='appointment_details'),

    path('delete_appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('update_purpose/<int:appointment_id>/', views.update_purpose, name='update_purpose'),
  

    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointmentsPending/', views.appointment_listPending, name='appointment_listPending'),
    path('appointmentsSuccess/', views.appointment_listSuccess, name='appointment_listSuccess'),
    path('appointmentsFailed/', views.appointment_listFailed, name='appointment_listFailed'),
    path('appointmentsDecline/', views.appointment_listDecline, name='appointment_listDecline'),
    path('appointmentextraction/<int:appointment_id>/', views.appointment_extraction, name='appointment_extraction'),
    path('appointmentextraction_details/<int:appointment_id>/', views.appointmentextraction_details, name='appointmentextraction_details'),
    path('dental-record/', views.dental_record, name='dental_record'),
    path('extraction-record/<int:appointment_id>/', views.create_extraction_record, name='extraction_record'),

    path('Doctor/', views.doctor, name='doctor'),
    path('assistant/', views.assistant, name='assistant'),

    path('admin_doctorsite/', views.admin_doctorsite, name='admin_doctorsite'),
    path('admin_doctorsitelist/', views.admin_doctorsitelist, name='admin_doctorsitelist'),

    path('on_duty/<int:doctor_id>/', views.on_duty, name='OnDuty'),
    path('not_on_duty/<int:doctor_id>/', views.not_on_duty, name='NotOnDuty'),
    path('retire_doctor/<int:doctor_id>/', views.retire_doctor, name='retire_doctor'),
    path('resign_doctor/<int:doctor_id>/', views.resign_doctor, name='resign_doctor'),
    path('retire_assistant/<int:assistant_id>/', views.retire_assistant, name='retire_assistant'),
    path('resign_assistant/<int:assistant_id>/', views.resign_assistant, name='resign_assistant'),
    path('on_duty_assistant/<int:assistant_id>/', views.on_duty_assistant, name='OnDutyAssistant'),
    path('not_on_duty_assistant/<int:assistant_id>/', views.not_on_duty_assistant, name='NotOnDutyAssistant'),

    path('view_appointment/<int:appointment_id>/', views.view_appointment, name='view_appointment'),
    path('view_appointmentAdmin/<int:appointment_id>/', views.view_appointmentAdmin, name='view_appointmentAdmin'),
    path('view_appointmentProfile/<int:appointment_id>/', views.view_appointmentProfile, name='view_appointmentProfile'),
    path('view_appointmentProfileStudent/<int:appointment_id>/', views.view_appointmentProfileStudent, name='view_appointmentProfileStudent'),
    path('view_appointmentProfileFaculty/<int:appointment_id>/', views.view_appointmentProfileFaculty, name='view_appointmentProfileFaculty'),
    path('view_doctorprofile/<int:doctor_id>/', views.view_doctorprofile, name='view_doctorprofile'),
    path('view_assistantprofile/<int:assistant_id>/', views.view_assistantprofile, name='view_assistantprofile'),
     path('OnDuty/<int:doctor_id>/', views.on_duty, name='OnDuty'),
    path('NotOnDuty/<int:doctor_id>/', views.not_on_duty, name='NotOnDuty'),


    
    path('supply_list/', views.supply_list, name='supply_list'),
    path('supply_listhome/', views.supply_listhome, name='supply_listhome'),
    path('create/', views.supply_create, name='supply_create'),
    path('update/<int:pk>/', views.supply_update, name='supply_update'),
    path('delete/<int:pk>/', views.supply_delete, name='supply_delete'),


    
    path('loginDental/', views.LoginDentals, name='LoginDentals'),
    path('dentalchange_password/', views.dentalchange_password, name='dentalchange_password'),
    path('admin-DashboardWMSU/', views.admin_DashboardWMSU, name='admin_DashboardWMSU'),

    path('WMSUcustom-admin/list/',views.WMSUadmin_list, name='WMSUadmin_list'),


    path('WMSUcustom-admin/listFaculty/', views.WMSUadmin_listFaculty, name='WMSUadmin_listFaculty'),
    path('appointment_reports/', views.appointment_reports, name='appointment_reports'),
    path('appointment_reportslist/', views.appointment_reportslist, name='appointment_reportslist'),

    path('users/profile/<int:user_id>/', views.view_profileadmin, name='view_profileadmin'),
    path('users/profilefaculty/<int:user_id>/', views.view_profileadminfaculty, name='view_profileadminfaculty'),
    


   
]










