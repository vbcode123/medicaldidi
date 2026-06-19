"""
URL configuration for medicaldidi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    
    path('', views.home, name='home'),           # Home page
    path('admin-login/', views.admin_login, name='admin_login'),  # Admin Login
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin Dashboard
    path('admin-logout/', views.admin_logout, name='admin_logout'),

    # Sub Admin
    path('add-sub-admin/', views.add_sub_admin, name='add_sub_admin'),
    path('sub-admin-list/', views.sub_admin_list, name='sub_admin_list'),
    path('sub-admin-view/<int:id>/', views.sub_admin_view, name='sub_admin_view'),
    path('sub-admin-edit/<int:id>/', views.sub_admin_edit, name='sub_admin_edit'),
    path('sub-admin-delete/<int:id>/', views.sub_admin_delete, name='sub_admin_delete'),

#======================================
    path('sub-admin-login/', views.sub_admin_login, name='sub_admin_login'),
    path('sub-admin-dashboard/', views.sub_admin_dashboard, name='sub_admin_dashboard'),
    path('sub-admin-logout/', views.sub_admin_logout, name='sub_admin_logout'),
#ADD NURSE=====================
    path('subadmin/add-nurse/', views.subadmin_add_nurse, name='subadmin_add_nurse'),
    path('subadmin/nurse-list/', views.subadmin_nurse_list, name='subadmin_nurse_list'),
    path('subadmin/nurse-edit/<int:id>/', views.nurse_edit, name='subadmin_nurse_edit'),
    path('subadmin/nurse-delete/<int:id>/', views.nurse_delete, name='subadmin_nurse_delete'),
    path('subadmin/nurse-approve/<int:id>/', views.approve_nurse, name='approve_nurse'),
    path('subadmin/nurse-reject/<int:id>/', views.reject_nurse, name='reject_nurse'),
    path("nurse-view/<int:id>/", views.nurse_view, name="nurse_view"),
#ADMIN SEEN NURSE LIST======================================
    path('admin/nurse-list/', views.admin_nurse_list, name='admin_nurse_list'),
    path('admin/nurse-view/<int:id>/', views.admin_nurse_view, name='admin_nurse_view'),
    path('admin/nurse-edit/<int:id>/', views.nurse_edit, name='admin_nurse_edit'),
    path('admin/nurse-delete/<int:id>/', views.nurse_delete, name='admin_nurse_delete'),
#===========Customer Inquirey=================================
    path('inquiry-form/', views.inquiry_form, name='inquiry_form'),
    path('inquiry-list/', views.inquiry_list, name='inquiry_list'),
    path('admin-inquiry-list/', views.admin_inquiry_list, name='admin_inquiry_list'),   #admin seen
#NURSE LOGIN & DASHBOARD=================================
    path('nurse-login/', views.nurse_login, name='nurse_login'),
    path('nurse-dashboard/', views.nurse_dashboard, name='nurse_dashboard'),
    path('nurse-logout/', views.nurse_logout, name='nurse_logout'),
#PUBLIC NURSE APPLICATION=================================
    path('join-as-nurse/', views.public_add_nurse, name='public_add_nurse'),
#PUBLIC PATIENT REGISTRATION=================================
    path('book-now/', views.public_add_patient, name='public_add_patient'),
#PATIENT APPROVAL/REJECTION=================================
    path('patient-approve/<int:id>/', views.approve_patient, name='approve_patient'),
    path('patient-reject/<int:id>/', views.reject_patient, name='reject_patient'),
#PATIENT MANAGEMENT=================================
    path('admin/add-patient/', views.admin_add_patient, name='admin_add_patient'),
    path('admin/patient-list/', views.admin_patient_list, name='admin_patient_list'),
    path('admin/patient-view/<int:id>/', views.admin_patient_view, name='admin_patient_view'),
    path('admin/patient-edit/<int:id>/', views.admin_patient_edit, name='admin_patient_edit'),
    path('admin/patient-delete/<int:id>/', views.admin_patient_delete, name='admin_patient_delete'),
    path('subadmin/add-patient/', views.subadmin_add_patient, name='subadmin_add_patient'),
    path('subadmin/patient-list/', views.subadmin_patient_list, name='subadmin_patient_list'),
    path('subadmin/patient-view/<int:id>/', views.subadmin_patient_view, name='subadmin_patient_view'),
    path('subadmin/patient-edit/<int:id>/', views.subadmin_patient_edit, name='subadmin_patient_edit'),
    path('subadmin/patient-delete/<int:id>/', views.subadmin_patient_delete, name='subadmin_patient_delete'),
#CUSTOMER (PATIENT) LOGIN & DASHBOARD=================================
    path('customer-login/', views.customer_login, name='customer_login'),
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('customer-logout/', views.customer_logout, name='customer_logout'),
#NURSE ASSIGNMENT=================================
    path('subadmin/assign-nurse/<int:patient_id>/', views.subadmin_assign_nurse_page, name='subadmin_assign_nurse_page'),
    path('subadmin/submit-nurse-assignment/<int:patient_id>/', views.subadmin_submit_nurse_assignment, name='subadmin_submit_nurse_assignment'),
    path('nurse/approve-assignment/<int:assignment_id>/', views.approve_assignment, name='approve_assignment'),
        path('nurse/reject-assignment/<int:assignment_id>/', views.reject_assignment, name='reject_assignment'),
        path('nurse/approve-temp-assignment/<int:temp_assignment_id>/', views.approve_temp_assignment, name='approve_temp_assignment'),
        path('nurse/reject-temp-assignment/<int:temp_assignment_id>/', views.reject_temp_assignment, name='reject_temp_assignment'),
    path('nurse/view-patient/<int:patient_id>/', views.nurse_view_patient, name='nurse_view_patient'),
    
    # ATTENDANCE MANAGEMENT
    path('nurse/check-in/<int:assignment_id>/', views.nurse_check_in, name='nurse_check_in'),
    path('nurse/temp-check-in/<int:temp_assignment_id>/', views.nurse_temp_check_in, name='nurse_temp_check_in'),
    path('nurse/check-out/<int:attendance_id>/', views.nurse_check_out, name='nurse_check_out'),
    path('patient/approve-check-in/<int:attendance_id>/', views.patient_approve_check_in, name='patient_approve_check_in'),
    path('patient/reject-check-in/<int:attendance_id>/', views.patient_reject_check_in, name='patient_reject_check_in'),
    path('patient/approve-check-out/<int:attendance_id>/', views.patient_approve_check_out, name='patient_approve_check_out'),
    path('patient/reject-check-out/<int:attendance_id>/', views.patient_reject_check_out, name='patient_reject_check_out'),
    path('admin/attendance-list/', views.admin_attendance_list, name='admin_attendance_list'),
    path('subadmin/attendance-list/', views.subadmin_attendance_list, name='subadmin_attendance_list'),

    # LEAVE MANAGEMENT
    path('nurse/apply-leave/', views.nurse_apply_leave, name='nurse_apply_leave'),
    path('admin/leave-list/', views.admin_leave_list, name='admin_leave_list'),
    path('subadmin/leave-list/', views.subadmin_leave_list, name='subadmin_leave_list'),
    path('approve-leave/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('reject-leave/<int:leave_id>/', views.reject_leave, name='reject_leave'),
    path('assign-replacement/<int:leave_id>/', views.assign_replacement_nurse, name='assign_replacement_nurse'),
    
    # MONTHLY STATISTICS
    path('admin/monthly-stats/', views.admin_monthly_stats, name='admin_monthly_stats'),
    path('subadmin/monthly-stats/', views.subadmin_monthly_stats, name='subadmin_monthly_stats'),

    path('admin/', admin.site.urls),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
