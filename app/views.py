from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import (
    SubAdmin,
    Patient,
    Nurse,
    NurseAssignment,
    Attendance,
    NurseLeave,
    TemporaryAssignment,
    Inquiry
)



def home(request):
    return render(request, 'home.html')


def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Email se user fetch kar rahe hain
            user_obj = User.objects.get(email=email)

            # Ab authenticate username(pass as email's corresponding username)
            user = authenticate(username=user_obj.username, password=password)

        except User.DoesNotExist:
            user = None

        if user:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin/admin_login.html', {
                'error': 'Invalid Email or Password'
            })

    return render(request, 'admin/admin_login.html')


@login_required
def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')

@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')


# ---------------- SUB ADMIN ADD ----------------
@login_required
def add_sub_admin(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        aadhaar_image = request.FILES.get('aadhaar_image')
        profile_photo = request.FILES.get('profile_photo')
        joining_date = request.POST.get('joining_date')
        password = request.POST.get('password')
        
        if SubAdmin.objects.filter(phone=phone).exists():
            messages.error(request, "This mobile number is already registered. Please use a different mobile number.")
            return render(request, 'admin/add_sub_admin.html')
        
        try:
            SubAdmin.objects.create(
                name=name,
                phone=phone,
                address=address,
                aadhaar_image=aadhaar_image,
                profile_photo=profile_photo,
                joining_date=joining_date,
                password=password
            )
            return redirect('admin_dashboard')
        except Exception as e:
            messages.error(request, "This mobile number is already registered. Please use a different mobile number.")
            return render(request, 'admin/add_sub_admin.html')

    return render(request, 'admin/add_sub_admin.html')


# ---------------- SUB ADMIN LOGIN ----------------
def sub_admin_login(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        try:
            sub_admin = SubAdmin.objects.get(phone=phone, password=password)
            request.session['sub_admin_id'] = sub_admin.id
            return redirect('sub_admin_dashboard')
        except SubAdmin.DoesNotExist:
            return render(request, 'subadmin/sub_admin_login.html', {
                'error': 'Invalid Phone or Password'
            })

    return render(request, 'subadmin/sub_admin_login.html')


# ---------------- SUB ADMIN DASHBOARD ----------------
def sub_admin_dashboard(request):
    if not request.session.get('sub_admin_id'):
        return redirect('sub_admin_login')
    return render(request, 'subadmin/sub_admin_dashboard.html')

def sub_admin_logout(request):
    if 'sub_admin_id' in request.session:
        del request.session['sub_admin_id']
    return redirect('sub_admin_login')




from django.shortcuts import render, redirect, get_object_or_404
from .models import SubAdmin, Nurse, Patient, NurseAssignment, Attendance
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
import json

def sub_admin_list(request):
    subadmins = SubAdmin.objects.all()
    return render(request, 'admin/subadmin_list.html', {'subadmins': subadmins})


def sub_admin_view(request, id):
    subadmin = get_object_or_404(SubAdmin, id=id)
    return render(request, 'admin/subadmin_view.html', {'subadmin': subadmin})


def sub_admin_edit(request, id):
    subadmin = get_object_or_404(SubAdmin, id=id)

    if request.method == 'POST':
        subadmin.name = request.POST.get('name')
        subadmin.phone = request.POST.get('phone')
        subadmin.address = request.POST.get('address')
        subadmin.joining_date = request.POST.get('joining_date')

        # Aadhaar Image Update
        if request.FILES.get('aadhaar_image'):
            subadmin.aadhaar_image = request.FILES.get('aadhaar_image')

        # Profile Photo Update
        if request.FILES.get('profile_photo'):
            subadmin.profile_photo = request.FILES.get('profile_photo')

        subadmin.save()
        messages.success(request, "Sub Admin updated successfully!")
        return redirect('sub_admin_list')

    return render(request, 'admin/subadmin_edit.html', {'subadmin': subadmin})



def sub_admin_delete(request, id):
    subadmin = get_object_or_404(SubAdmin, id=id)
    subadmin.delete()
    messages.success(request, "Sub Admin deleted successfully!")
    return redirect('sub_admin_list')

#ADD NURSE=====================
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Nurse


def subadmin_add_nurse(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'subadmin/add_nurse.html')
        
        phone = request.POST.get('phone')
        if Nurse.objects.filter(phone=phone).exists():
            messages.error(request, "This mobile number is already registered. Please use a different mobile number.")
            return render(request, 'subadmin/add_nurse.html')
        
        try:
            Nurse.objects.create(
                full_name=request.POST.get('full_name'),
                gender=request.POST.get('gender'),
                dob=request.POST.get('dob'),
                profile_image=request.FILES.get('profile_image'),
                aadhaar_image=request.FILES.get('aadhaar_image'),
                email=request.POST.get('email'),
                phone=phone,
                address=request.POST.get('address'),
                pin_code=request.POST.get('pin_code'),
                certificate_image=request.FILES.get('certificate_image'),
                experience=request.POST.get('experience'),
                joining_date=request.POST.get('joining_date'),
                password=password,

                # NEW FIELDS
                parents_name=request.POST.get('parents_name'),
                parents_aadhaar_image=request.FILES.get('parents_aadhaar_image'),
                parents_contact_number=request.POST.get('parents_contact_number'),
            )
            messages.success(request, "Nurse Added Successfully!")
            return redirect('subadmin_nurse_list')
        except Exception as e:
            messages.error(request, "This mobile number is already registered. Please use a different mobile number.")
            return render(request, 'subadmin/add_nurse.html')

    return render(request, 'subadmin/add_nurse.html')


def public_add_nurse(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'public_add_nurse.html')
        
        phone = request.POST.get('phone')
        if Nurse.objects.filter(phone=phone).exists():
            messages.error(request, "This mobile number is already registered. Please use a different mobile number.")
            return render(request, 'public_add_nurse.html')
        
        try:
            Nurse.objects.create(
                full_name=request.POST.get('full_name'),
                gender=request.POST.get('gender'),
                dob=request.POST.get('dob'),
                profile_image=request.FILES.get('profile_image'),
                aadhaar_image=request.FILES.get('aadhaar_image'),
                email=request.POST.get('email'),
                phone=phone,
                address=request.POST.get('address'),
                pin_code=request.POST.get('pin_code'),
                certificate_image=request.FILES.get('certificate_image'),
                experience=request.POST.get('experience'),
                joining_date=request.POST.get('joining_date'),
                password=password,
                is_approved=False,  # Not approved yet
                parents_name=request.POST.get('parents_name'),
                parents_aadhaar_image=request.FILES.get('parents_aadhaar_image'),
                parents_contact_number=request.POST.get('parents_contact_number'),
            )
            messages.success(request, "Thank you for applying! Your application is being reviewed.")
            return redirect('home')
        except Exception as e:
            messages.error(request, "This mobile number is already registered. Please use a different mobile number.")
            return render(request, 'public_add_nurse.html')

    return render(request, 'public_add_nurse.html')



def subadmin_nurse_list(request):
    nurses = Nurse.objects.all().order_by('-id')
    return render(request, 'subadmin/nurse_list.html', {'nurses': nurses})

def nurse_view(request, id):
    nurse = get_object_or_404(Nurse, id=id)
    return render(request, "subadmin/nurse_view.html", {"nurse": nurse})


#ADMIN SEEN NURSE LIST==============================
def admin_nurse_list(request):
    nurses = Nurse.objects.all()
    return render(request, 'admin/nurse_list.html', {'nurses': nurses})


def admin_nurse_view(request, id):
    nurse = get_object_or_404(Nurse, id=id)
    return render(request, 'admin/nurse_view.html', {'nurse': nurse})


#Customer Inquirey ===========================================
from django.shortcuts import render, redirect
from .models import Inquiry

def inquiry_form(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        nurse_type = request.POST.get('nurse_type')
        remark = request.POST.get('remark')   # ← New Field

        Inquiry.objects.create(
            customer_name=customer_name,
            phone=phone,
            address=address,
            nurse_type=nurse_type,
            remark=remark
        )

        return redirect('inquiry_list')

    return render(request, "subadmin/inquiry_form.html")



def inquiry_list(request):
    inquiries = Inquiry.objects.all().order_by('-id')
    return render(request, "subadmin/inquiry_list.html", {"inquiries": inquiries})


def admin_inquiry_list(request):
    inquiries = Inquiry.objects.all().order_by('-id')
    return render(request, 'admin/admin_inquiry_list.html', {'inquiries': inquiries})   #ADMIN SEEN


def nurse_login(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        try:
            nurse = Nurse.objects.get(phone=phone, password=password)
            if not nurse.is_approved:
                return render(request, 'nurse/nurse_login.html', {'error': 'Your application is pending approval. Please wait for admin approval.'})
            request.session['nurse_id'] = nurse.id
            return redirect('nurse_dashboard')
        except Nurse.DoesNotExist:
            return render(request, 'nurse/nurse_login.html', {'error': 'Invalid Phone or Password'})
    return render(request, 'nurse/nurse_login.html')


def nurse_dashboard(request):
    if not request.session.get('nurse_id'):
        return redirect('nurse_login')
    
    nurse = get_object_or_404(Nurse, id=request.session['nurse_id'])
    assignments = NurseAssignment.objects.filter(nurse=nurse, status__in=['Pending', 'Approved']).order_by('-assigned_at')
    attendances = Attendance.objects.filter(nurse=nurse).order_by('-date', '-created_at')
    # Get active temporary assignments
    from django.utils import timezone
    today = timezone.now().date()
    temporary_assignments = TemporaryAssignment.objects.filter(
        replacement_nurse=nurse,
        start_date__lte=today,
        end_date__gte=today
    ).order_by('-start_date')
    # Get active leave and leave history
    active_leave = get_nurse_active_leave(nurse)
    leave_history = NurseLeave.objects.filter(nurse=nurse).order_by('-created_at')[:10]
    
    return render(request, 'nurse/nurse_dashboard.html', {
        'nurse': nurse,
        'assignments': assignments,
        'temporary_assignments': temporary_assignments,
        'attendances': attendances,
        'active_leave': active_leave,
        'leave_history': leave_history
    })


def nurse_logout(request):
    if 'nurse_id' in request.session:
        del request.session['nurse_id']
    return redirect('nurse_login')


def nurse_edit(request, id):
    nurse = get_object_or_404(Nurse, id=id)
    if request.method == 'POST':
        nurse.full_name = request.POST.get('full_name')
        nurse.gender = request.POST.get('gender')
        nurse.dob = request.POST.get('dob')
        nurse.email = request.POST.get('email')
        nurse.phone = request.POST.get('phone')
        nurse.address = request.POST.get('address')
        nurse.pin_code = request.POST.get('pin_code')
        nurse.experience = request.POST.get('experience')
        nurse.joining_date = request.POST.get('joining_date')
        nurse.parents_name = request.POST.get('parents_name')
        nurse.parents_contact_number = request.POST.get('parents_contact_number')
        
        if request.FILES.get('profile_image'):
            nurse.profile_image = request.FILES.get('profile_image')
        if request.FILES.get('aadhaar_image'):
            nurse.aadhaar_image = request.FILES.get('aadhaar_image')
        if request.FILES.get('certificate_image'):
            nurse.certificate_image = request.FILES.get('certificate_image')
        if request.FILES.get('parents_aadhaar_image'):
            nurse.parents_aadhaar_image = request.FILES.get('parents_aadhaar_image')
        
        if request.POST.get('password'):
            nurse.password = request.POST.get('password')
        
        nurse.save()
        messages.success(request, "Nurse updated successfully!")
        
        if 'subadmin' in request.path:
            return redirect('subadmin_nurse_list')
        else:
            return redirect('admin_nurse_list')
    return render(request, 'subadmin/edit_nurse.html', {'nurse': nurse})


def nurse_delete(request, id):
    nurse = get_object_or_404(Nurse, id=id)
    nurse.delete()
    messages.success(request, "Nurse deleted successfully!")
    
    if 'subadmin' in request.path:
        return redirect('subadmin_nurse_list')
    else:
        return redirect('admin_nurse_list')


def approve_nurse(request, id):
    nurse = get_object_or_404(Nurse, id=id)
    nurse.is_approved = True
    nurse.save()
    messages.success(request, "Nurse approved successfully!")
    if 'sub_admin_id' in request.session:
        return redirect('subadmin_nurse_list')
    else:
        return redirect('admin_nurse_list')


def reject_nurse(request, id):
    nurse = get_object_or_404(Nurse, id=id)
    nurse.delete()
    messages.success(request, "Nurse application rejected!")
    if 'sub_admin_id' in request.session:
        return redirect('subadmin_nurse_list')
    else:
        return redirect('admin_nurse_list')


# ---------------- PATIENT MANAGEMENT ----------------
@login_required
def admin_add_patient(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'admin/add_patient.html')
        
        Patient.objects.create(
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            profile_image=request.FILES.get('profile_image'),
            address=request.POST.get('address'),
            pin_code=request.POST.get('pin_code'),
            aadhaar_image=request.FILES.get('aadhaar_image'),
            agreement_image=request.FILES.get('agreement_image'),
            patient_representative_name=request.POST.get('patient_representative_name'),
            patient_representative_phone=request.POST.get('patient_representative_phone'),
            password=password,
            is_approved=True
        )
        messages.success(request, "Patient added successfully!")
        return redirect('admin_patient_list')
    
    return render(request, 'admin/add_patient.html')


@login_required
def admin_patient_list(request):
    patients = Patient.objects.all().order_by('-id')
    return render(request, 'admin/patient_list.html', {'patients': patients})


@login_required
def admin_patient_view(request, id):
    patient = get_object_or_404(Patient, id=id)
    return render(request, 'admin/patient_view.html', {'patient': patient})


@login_required
def admin_patient_edit(request, id):
    patient = get_object_or_404(Patient, id=id)
    if request.method == 'POST':
        patient.full_name = request.POST.get('full_name')
        patient.phone = request.POST.get('phone')
        patient.email = request.POST.get('email')
        patient.address = request.POST.get('address')
        patient.pin_code = request.POST.get('pin_code')
        patient.patient_representative_name = request.POST.get('patient_representative_name')
        patient.patient_representative_phone = request.POST.get('patient_representative_phone')
        
        if request.FILES.get('profile_image'):
            patient.profile_image = request.FILES.get('profile_image')
        if request.FILES.get('aadhaar_image'):
            patient.aadhaar_image = request.FILES.get('aadhaar_image')
        if request.FILES.get('agreement_image'):
            patient.agreement_image = request.FILES.get('agreement_image')
        
        if request.POST.get('password'):
            patient.password = request.POST.get('password')
        
        patient.save()
        messages.success(request, "Patient updated successfully!")
        return redirect('admin_patient_list')
    return render(request, 'admin/patient_edit.html', {'patient': patient})


@login_required
def admin_patient_delete(request, id):
    patient = get_object_or_404(Patient, id=id)
    patient.delete()
    messages.success(request, "Patient deleted successfully!")
    return redirect('admin_patient_list')


# ---------------- SUBADMIN PATIENT MANAGEMENT ----------------
def subadmin_add_patient(request):
    if not request.session.get('sub_admin_id'):
        return redirect('sub_admin_login')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'subadmin/add_patient.html')
        
        phone = request.POST.get('phone')
        if Patient.objects.filter(phone=phone).exists():
            messages.error(request, "This mobile number is already registered. Please use a different mobile number.")
            return render(request, 'subadmin/add_patient.html')
        
        try:
            Patient.objects.create(
                full_name=request.POST.get('full_name'),
                phone=phone,
                email=request.POST.get('email'),
                profile_image=request.FILES.get('profile_image'),
                address=request.POST.get('address'),
                pin_code=request.POST.get('pin_code'),
                aadhaar_image=request.FILES.get('aadhaar_image'),
                agreement_image=request.FILES.get('agreement_image'),
                patient_representative_name=request.POST.get('patient_representative_name'),
                patient_representative_phone=request.POST.get('patient_representative_phone'),
                password=password,
                is_approved=True
            )
            messages.success(request, "Patient added successfully!")
            return redirect('subadmin_patient_list')
        except Exception as e:
            messages.error(request, "This mobile number is already registered. Please use a different mobile number.")
            return render(request, 'subadmin/add_patient.html')
    
    return render(request, 'subadmin/add_patient.html')


def subadmin_patient_list(request):
    if not request.session.get('sub_admin_id'):
        return redirect('sub_admin_login')
    
    patient_type = request.GET.get('type', 'all')
    all_patients = Patient.objects.all().order_by('-id')
    patients = []
    
    if patient_type == 'all':
        patients = all_patients
    elif patient_type == 'not-assigned':
        # Only APPROVED patients with NO active nurse assignment
        for patient in all_patients:
            if patient.is_approved and not patient.has_active_assignment:
                patients.append(patient)
    elif patient_type == 'assigned':
        # Only patients with ACTIVE nurse assignment
        for patient in all_patients:
            if patient.has_active_assignment:
                patients.append(patient)
    
    return render(request, 'subadmin/patient_list.html', {
        'patients': patients,
        'patient_type': patient_type
    })


def subadmin_patient_view(request, id):
    if not request.session.get('sub_admin_id'):
        return redirect('sub_admin_login')
    
    patient = get_object_or_404(Patient, id=id)
    return render(request, 'subadmin/patient_view.html', {'patient': patient})


def subadmin_patient_edit(request, id):
    if not request.session.get('sub_admin_id'):
        return redirect('sub_admin_login')
    
    patient = get_object_or_404(Patient, id=id)
    if request.method == 'POST':
        patient.full_name = request.POST.get('full_name')
        patient.phone = request.POST.get('phone')
        patient.email = request.POST.get('email')
        patient.address = request.POST.get('address')
        patient.pin_code = request.POST.get('pin_code')
        patient.patient_representative_name = request.POST.get('patient_representative_name')
        patient.patient_representative_phone = request.POST.get('patient_representative_phone')
        
        if request.FILES.get('profile_image'):
            patient.profile_image = request.FILES.get('profile_image')
        if request.FILES.get('aadhaar_image'):
            patient.aadhaar_image = request.FILES.get('aadhaar_image')
        if request.FILES.get('agreement_image'):
            patient.agreement_image = request.FILES.get('agreement_image')
        
        if request.POST.get('password'):
            patient.password = request.POST.get('password')
        
        patient.save()
        messages.success(request, "Patient updated successfully!")
        return redirect('subadmin_patient_list')
    return render(request, 'subadmin/patient_edit.html', {'patient': patient})


def subadmin_patient_delete(request, id):
    if not request.session.get('sub_admin_id'):
        return redirect('sub_admin_login')
    
    patient = get_object_or_404(Patient, id=id)
    patient.delete()
    messages.success(request, "Patient deleted successfully!")
    return redirect('subadmin_patient_list')


# ---------------- CUSTOMER LOGIN & DASHBOARD ----------------
def customer_login(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        try:
            patient = Patient.objects.get(phone=phone, password=password)
            if not patient.is_approved:
                return render(request, 'customer/customer_login.html', {'error': 'Your account is pending approval. Please wait for admin approval.'})
            request.session['patient_id'] = patient.id
            return redirect('customer_dashboard')
        except Patient.DoesNotExist:
            return render(request, 'customer/customer_login.html', {'error': 'Invalid Phone or Password'})
    return render(request, 'customer/customer_login.html')


def customer_dashboard(request):
    if not request.session.get('patient_id'):
        return redirect('customer_login')
    patient = Patient.objects.get(id=request.session['patient_id'])
    # Get approved nurse assignment
    approved_assignment = patient.nurse_assignments.filter(status='Approved').first()
    # Get all attendances for patient
    attendances = Attendance.objects.filter(patient=patient).order_by('-date', '-created_at')
    # Check for active leave notification
    active_leave = get_patient_leave_notification(patient)
    # Check for active temporary assignment
    active_temporary_assignment = None
    if approved_assignment:
        from django.utils import timezone
        today = timezone.now().date()
        active_temporary_assignment = TemporaryAssignment.objects.filter(
            original_assignment=approved_assignment,
            start_date__lte=today,
            end_date__gte=today
        ).first()
    return render(request, 'customer/customer_dashboard.html', {
        'patient': patient,
        'assigned_nurse': approved_assignment.nurse if approved_assignment else None,
        'assignment': approved_assignment,
        'attendances': attendances,
        'active_leave': active_leave,
        'active_temporary_assignment': active_temporary_assignment
    })


def customer_logout(request):
    if 'patient_id' in request.session:
        del request.session['patient_id']
    return redirect('customer_login')


def public_add_patient(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'public_add_patient.html')
        
        phone = request.POST.get('phone')
        if Patient.objects.filter(phone=phone).exists():
            messages.error(request, "This mobile number is already registered. Please use a different mobile number.")
            return render(request, 'public_add_patient.html')
        
        try:
            Patient.objects.create(
                full_name=request.POST.get('full_name'),
                phone=phone,
                email=request.POST.get('email'),
                profile_image=request.FILES.get('profile_image'),
                address=request.POST.get('address'),
                pin_code=request.POST.get('pin_code'),
                aadhaar_image=request.FILES.get('aadhaar_image'),
                agreement_image=request.FILES.get('agreement_image'),
                patient_representative_name=request.POST.get('patient_representative_name'),
                patient_representative_phone=request.POST.get('patient_representative_phone'),
                password=password,
                is_approved=False
            )
            messages.success(request, "Thank you for registering! Your account is pending approval.")
            return redirect('home')
        except Exception as e:
            messages.error(request, "This mobile number is already registered. Please use a different mobile number.")
            return render(request, 'public_add_patient.html')
    
    return render(request, 'public_add_patient.html')


def approve_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    patient.is_approved = True
    patient.save()
    messages.success(request, "Patient approved successfully!")
    # Check if it's subadmin or admin
    if 'sub_admin_id' in request.session:
        return redirect('subadmin_patient_list')
    else:
        return redirect('admin_patient_list')


def reject_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    patient.delete()
    messages.success(request, "Patient registration rejected.")
    # Check if it's subadmin or admin
    if 'sub_admin_id' in request.session:
        return redirect('subadmin_patient_list')
    else:
        return redirect('admin_patient_list')


def get_nurses(request):
    if not request.session.get('sub_admin_id'):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    from django.utils import timezone
    today = timezone.now().date()
    
    # Get IDs of nurses on approved leave
    nurses_on_leave = NurseLeave.objects.filter(
        status='Approved',
        from_date__lte=today,
        to_date__gte=today
    ).values_list('nurse_id', flat=True)
    
    nurses = Nurse.objects.filter(is_approved=True).exclude(id__in=nurses_on_leave).values('id', 'full_name', 'phone', 'pin_code', 'address')
    return JsonResponse(list(nurses), safe=False)


def assign_nurse(request):
    if not request.session.get('sub_admin_id'):
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401)
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
    try:
        data = json.loads(request.body)
        patient_id = data.get('patient_id')
        nurse_id = data.get('nurse_id')
        remark = data.get('remark', '')
        
        patient = get_object_or_404(Patient, id=patient_id)
        nurse = get_object_or_404(Nurse, id=nurse_id)
        
        # First, check if there's an existing active assignment for this patient
        existing_active = NurseAssignment.objects.filter(patient=patient, status__in=['Pending', 'Approved']).first()
        if existing_active:
            # If it's a different nurse, reject the old one
            if existing_active.nurse.id != nurse_id:
                existing_active.status = 'Rejected'
                existing_active.save()
        
        # Check if assignment with this nurse already exists
        existing = NurseAssignment.objects.filter(patient=patient, nurse=nurse).first()
        if existing:
            if existing.status != 'Rejected':
                return JsonResponse({'success': False, 'message': 'Nurse already assigned to this patient'})
            else:
                # Reactivate rejected assignment
                existing.status = 'Pending'
                existing.remark = remark
                existing.save()
                return JsonResponse({'success': True, 'message': 'Nurse reassigned successfully!'})
        
        # Create new assignment
        NurseAssignment.objects.create(
            patient=patient,
            nurse=nurse,
            remark=remark,
            status='Pending'
        )
        
        return JsonResponse({'success': True, 'message': 'Nurse assigned successfully!'})
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


def update_nurse_dashboard(request):
    if not request.session.get('nurse_id'):
        return redirect('nurse_login')
    
    nurse = get_object_or_404(Nurse, id=request.session['nurse_id'])
    assignments = NurseAssignment.objects.filter(nurse=nurse).order_by('-assigned_at')
    return render(request, 'nurse/nurse_dashboard.html', {'nurse': nurse, 'assignments': assignments})


def approve_assignment(request, assignment_id):
    if not request.session.get('nurse_id'):
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401)
    
    assignment = get_object_or_404(NurseAssignment, id=assignment_id)
    assignment.status = 'Approved'
    assignment.save()
    
    messages.success(request, "Patient assignment approved!")
    return redirect('nurse_dashboard')


def reject_assignment(request, assignment_id):
    if not request.session.get('nurse_id'):
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=401)
    
    assignment = get_object_or_404(NurseAssignment, id=assignment_id)
    assignment.status = 'Rejected'
    assignment.save()
    
    messages.success(request, "Patient assignment rejected!")
    return redirect('nurse_dashboard')


def approve_temp_assignment(request, temp_assignment_id):
    if not request.session.get('nurse_id'):
        return redirect('nurse_login')
    
    temp_assignment = get_object_or_404(TemporaryAssignment, id=temp_assignment_id, replacement_nurse_id=request.session['nurse_id'])
    temp_assignment.status = 'Approved'
    temp_assignment.save()
    
    messages.success(request, "Temporary assignment approved!")
    return redirect('nurse_dashboard')


def reject_temp_assignment(request, temp_assignment_id):
    if not request.session.get('nurse_id'):
        return redirect('nurse_login')
    
    temp_assignment = get_object_or_404(TemporaryAssignment, id=temp_assignment_id, replacement_nurse_id=request.session['nurse_id'])
    temp_assignment.status = 'Rejected'
    temp_assignment.save()
    
    messages.success(request, "Temporary assignment rejected!")
    return redirect('nurse_dashboard')

def subadmin_assign_nurse_page(request, patient_id):
    if not request.session.get('sub_admin_id'):
        return redirect('sub_admin_login')
    
    patient = get_object_or_404(Patient, id=patient_id)
    reassign = request.GET.get('reassign', 'false') == 'true'
    
    from django.utils import timezone
    today = timezone.now().date()
    
    # Get all nurses that are completely free (NO active assignments anywhere)
    active_assignment_nurse_ids = NurseAssignment.objects.filter(
        status__in=['Pending', 'Approved']
    ).values_list('nurse_id', flat=True)
    
    # Get IDs of nurses on approved leave
    nurses_on_leave = NurseLeave.objects.filter(
        status='Approved',
        from_date__lte=today,
        to_date__gte=today
    ).values_list('nurse_id', flat=True)
    
    # Get IDs of nurses with active temporary assignments
    active_temp_nurse_ids = TemporaryAssignment.objects.filter(
        start_date__lte=today,
        end_date__gte=today
    ).values_list('replacement_nurse_id', flat=True)
    
    # Combine all lists to exclude
    exclude_ids = list(active_assignment_nurse_ids) + list(nurses_on_leave) + list(active_temp_nurse_ids)
    
    # Only show FREE nurses (approved and NOT in any exclude list)
    nurses = Nurse.objects.filter(is_approved=True).exclude(id__in=exclude_ids)
    
    return render(request, 'subadmin/assign_nurse.html', {
        'patient': patient,
        'nurses': nurses,
        'reassign': reassign
    })

def subadmin_submit_nurse_assignment(request, patient_id):
    if not request.session.get('sub_admin_id'):
        return redirect('sub_admin_login')
    
    if request.method == 'POST':
        patient = get_object_or_404(Patient, id=patient_id)
        nurse_id = request.POST.get('nurse_id')
        remark = request.POST.get('remark', '')
        
        nurse = get_object_or_404(Nurse, id=nurse_id)
        
        # First mark ALL existing active assignments for this patient as rejected
        existing_assignments = NurseAssignment.objects.filter(
            patient=patient,
            status__in=['Pending', 'Approved']
        )
        for assn in existing_assignments:
            assn.status = 'Rejected'
            assn.save()
        
        # Check if there's already an assignment for this patient and nurse (any status)
        assignment = NurseAssignment.objects.filter(
            patient=patient,
            nurse=nurse
        ).first()
        
        if assignment:
            # Update existing assignment
            assignment.status = 'Pending'
            assignment.remark = remark
            assignment.save()
        else:
            # Create new assignment
            NurseAssignment.objects.create(
                patient=patient,
                nurse=nurse,
                remark=remark,
                status='Pending'
            )
        
        messages.success(request, 'Nurse assigned successfully!')
        return redirect('subadmin_patient_list')
    
    return redirect('subadmin_patient_list')


def nurse_view_patient(request, patient_id):
    if not request.session.get('nurse_id'):
        return redirect('nurse_login')
    
    nurse = get_object_or_404(Nurse, id=request.session['nurse_id'])
    patient = get_object_or_404(Patient, id=patient_id)
    
    return render(request, 'nurse/nurse_view_patient.html', {
        'nurse': nurse,
        'patient': patient
    })


# ==================================
# ATTENDANCE MANAGEMENT SYSTEM
# ==================================

def nurse_check_in(request, assignment_id):
    if not request.session.get('nurse_id'):
        return redirect('nurse_login')
    
    nurse = Nurse.objects.get(id=request.session['nurse_id'])
    
    # Check if nurse is on active leave
    if is_nurse_on_leave(nurse):
        active_leave = get_nurse_active_leave(nurse)
        messages.error(request, f"You are currently on approved leave from {active_leave.from_date} to {active_leave.to_date}!")
        return redirect('nurse_dashboard')
    
    assignment = get_object_or_404(NurseAssignment, id=assignment_id, nurse_id=request.session['nurse_id'])
    
    # Check if attendance already exists for today
    today = timezone.now().date()
    attendance, created = Attendance.objects.get_or_create(
        assignment=assignment,
        patient=assignment.patient,
        nurse=assignment.nurse,
        date=today,
        defaults={}
    )
    
    if not created and attendance.check_in_time:
        messages.warning(request, "You have already checked in today!")
        return redirect('nurse_dashboard')
    
    attendance.check_in_time = timezone.now()
    attendance.check_in_status = 'Pending'
    attendance.save()
    
    messages.success(request, "Check-in successful! Waiting for patient approval.")
    return redirect('nurse_dashboard')


def nurse_check_out(request, attendance_id):
    if not request.session.get('nurse_id'):
        return redirect('nurse_login')
    
    attendance = get_object_or_404(Attendance, id=attendance_id, nurse_id=request.session['nurse_id'])
    
    if not attendance.check_in_time:
        messages.error(request, "Please check in first!")
        return redirect('nurse_dashboard')
    
    if attendance.check_in_status != 'Approved':
        messages.error(request, "Check-in needs to be approved by patient first!")
        return redirect('nurse_dashboard')
    
    attendance.check_out_time = timezone.now()
    attendance.check_out_status = 'Pending'
    attendance.save()
    
    messages.success(request, "Check-out successful! Waiting for patient approval.")
    return redirect('nurse_dashboard')


def nurse_temp_check_in(request, temp_assignment_id):
    if not request.session.get('nurse_id'):
        return redirect('nurse_login')
    
    nurse = Nurse.objects.get(id=request.session['nurse_id'])
    
    # Check if nurse is on active leave
    if is_nurse_on_leave(nurse):
        active_leave = get_nurse_active_leave(nurse)
        messages.error(request, f"You are currently on approved leave from {active_leave.from_date} to {active_leave.to_date}!")
        return redirect('nurse_dashboard')
    
    temp_assignment = get_object_or_404(TemporaryAssignment, id=temp_assignment_id, replacement_nurse_id=request.session['nurse_id'])
    
    if temp_assignment.status != 'Approved':
        messages.error(request, "You need to approve this temporary assignment first!")
        return redirect('nurse_dashboard')
    
    # Check if attendance already exists for today
    today = timezone.now().date()
    attendance, created = Attendance.objects.get_or_create(
        assignment=temp_assignment.original_assignment,
        patient=temp_assignment.patient,
        nurse=nurse,
        date=today,
        defaults={}
    )
    
    if not created and attendance.check_in_time:
        messages.warning(request, "You have already checked in today!")
        return redirect('nurse_dashboard')
    
    attendance.check_in_time = timezone.now()
    attendance.check_in_status = 'Pending'
    attendance.save()
    
    messages.success(request, "Check-in successful! Waiting for patient approval.")
    return redirect('nurse_dashboard')


def patient_approve_check_in(request, attendance_id):
    if not request.session.get('patient_id'):
        return redirect('customer_login')
    
    attendance = get_object_or_404(Attendance, id=attendance_id, patient_id=request.session['patient_id'])
    attendance.check_in_status = 'Approved'
    attendance.check_in_approved_at = timezone.now()
    attendance.save()
    
    messages.success(request, "Nurse check-in approved!")
    return redirect('customer_dashboard')


def patient_reject_check_in(request, attendance_id):
    if not request.session.get('patient_id'):
        return redirect('customer_login')
    
    attendance = get_object_or_404(Attendance, id=attendance_id, patient_id=request.session['patient_id'])
    attendance.check_in_status = 'Rejected'
    attendance.check_in_time = None
    attendance.save()
    
    messages.success(request, "Nurse check-in rejected!")
    return redirect('customer_dashboard')


def patient_approve_check_out(request, attendance_id):
    if not request.session.get('patient_id'):
        return redirect('customer_login')
    
    attendance = get_object_or_404(Attendance, id=attendance_id, patient_id=request.session['patient_id'])
    attendance.check_out_status = 'Approved'
    attendance.check_out_approved_at = timezone.now()
    
    # Calculate total duty time
    if attendance.check_in_time and attendance.check_out_time:
        delta = attendance.check_out_time - attendance.check_in_time
        total_seconds = delta.total_seconds()
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        
        attendance.total_duty_hours = round(total_seconds / 3600, 2)
        attendance.total_duty_minutes = int(total_seconds // 60)
        attendance.total_duty_display = f"{int(hours)} Hours {int(minutes)} Minutes"
        attendance.save()
    
    messages.success(request, "Nurse check-out approved! Duty time calculated.")
    return redirect('customer_dashboard')


def patient_reject_check_out(request, attendance_id):
    if not request.session.get('patient_id'):
        return redirect('customer_login')
    
    attendance = get_object_or_404(Attendance, id=attendance_id, patient_id=request.session['patient_id'])
    attendance.check_out_status = 'Rejected'
    attendance.check_out_time = None
    attendance.save()
    
    messages.success(request, "Nurse check-out rejected!")
    return redirect('customer_dashboard')


def admin_attendance_list(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    filter_date = request.GET.get('date', '')
    filter_nurse = request.GET.get('nurse', '')
    filter_patient = request.GET.get('patient', '')
    
    attendances = Attendance.objects.all().order_by('-date', '-created_at')
    
    if filter_date:
        attendances = attendances.filter(date=filter_date)
    
    if filter_nurse:
        attendances = attendances.filter(nurse_id=filter_nurse)
    
    if filter_patient:
        attendances = attendances.filter(patient_id=filter_patient)
    
    nurses = Nurse.objects.filter(is_approved=True)
    patients = Patient.objects.filter(is_approved=True)
    
    return render(request, 'admin/attendance_list.html', {
        'attendances': attendances,
        'nurses': nurses,
        'patients': patients,
        'filter_date': filter_date,
        'filter_nurse': filter_nurse,
        'filter_patient': filter_patient
    })

def subadmin_attendance_list(request):
    if not request.session.get('sub_admin_id'):
        return redirect('sub_admin_login')
    
    filter_date = request.GET.get('date', '')
    filter_nurse = request.GET.get('nurse', '')
    filter_patient = request.GET.get('patient', '')
    
    attendances = Attendance.objects.all().order_by('-date', '-created_at')
    
    if filter_date:
        attendances = attendances.filter(date=filter_date)
    
    if filter_nurse:
        attendances = attendances.filter(nurse_id=filter_nurse)
    
    if filter_patient:
        attendances = attendances.filter(patient_id=filter_patient)
    
    nurses = Nurse.objects.filter(is_approved=True)
    patients = Patient.objects.filter(is_approved=True)
    
    return render(request, 'subadmin/attendance_list.html', {
        'attendances': attendances,
        'nurses': nurses,
        'patients': patients,
        'filter_date': filter_date,
        'filter_nurse': filter_nurse,
        'filter_patient': filter_patient
    })


# ==============================================
# LEAVE MANAGEMENT VIEWS
# ==============================================

def nurse_apply_leave(request):
    if not request.session.get('nurse_id'):
        return redirect('nurse_login')
    
    nurse = Nurse.objects.get(id=request.session['nurse_id'])
    
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        reason = request.POST.get('reason')
        
        # Convert string dates to date objects
        from django.utils.dateparse import parse_date
        from_date_obj = parse_date(from_date)
        to_date_obj = parse_date(to_date)
        
        # Validation
        today = timezone.now().date()
        if from_date_obj < today:
            messages.error(request, "From date cannot be in the past!")
            return redirect('nurse_apply_leave')
        
        if to_date_obj < from_date_obj:
            messages.error(request, "To date cannot be before from date!")
            return redirect('nurse_apply_leave')
        
        # Create leave request
        leave = NurseLeave.objects.create(
            nurse=nurse,
            from_date=from_date_obj,
            to_date=to_date_obj,
            reason=reason
        )
        messages.success(request, "Leave request submitted successfully!")
        return redirect('nurse_dashboard')
    
    # Get leave history
    leave_history = NurseLeave.objects.filter(nurse=nurse).order_by('-created_at')
    
    return render(request, 'nurse/apply_leave.html', {
        'nurse': nurse,
        'leave_history': leave_history
    })


def admin_leave_list(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admin_login')
    
    leaves = NurseLeave.objects.all().order_by('-created_at')
    nurses = Nurse.objects.filter(is_approved=True)
    
    return render(request, 'admin/leave_list.html', {
        'leaves': leaves,
        'nurses': nurses
    })


def subadmin_leave_list(request):
    if not request.session.get('sub_admin_id'):
        return redirect('sub_admin_login')
    
    leaves = NurseLeave.objects.all().order_by('-created_at')
    nurses = Nurse.objects.filter(is_approved=True)
    
    return render(request, 'subadmin/leave_list.html', {
        'leaves': leaves,
        'nurses': nurses
    })


def approve_leave(request, leave_id):
    if request.user.is_authenticated and request.user.is_superuser:
        leave = get_object_or_404(NurseLeave, id=leave_id)
        leave.status = 'Approved'
        leave.save()
        messages.success(request, "Leave approved!")
        return redirect('admin_leave_list')
    elif request.session.get('sub_admin_id'):
        leave = get_object_or_404(NurseLeave, id=leave_id)
        leave.status = 'Approved'
        leave.save()
        messages.success(request, "Leave approved!")
        return redirect('subadmin_leave_list')
    return redirect('home')


def reject_leave(request, leave_id):
    if request.method == 'POST':
        admin_remark = request.POST.get('admin_remark', '')
        if request.user.is_authenticated and request.user.is_superuser:
            leave = get_object_or_404(NurseLeave, id=leave_id)
            leave.status = 'Rejected'
            leave.admin_remark = admin_remark
            leave.save()
            messages.success(request, "Leave rejected!")
            return redirect('admin_leave_list')
        elif request.session.get('sub_admin_id'):
            leave = get_object_or_404(NurseLeave, id=leave_id)
            leave.status = 'Rejected'
            leave.admin_remark = admin_remark
            leave.save()
            messages.success(request, "Leave rejected!")
            return redirect('subadmin_leave_list')
    return redirect('home')


def assign_replacement_nurse(request, leave_id):
    from django.utils import timezone
    
    if request.user.is_authenticated and request.user.is_superuser:
        leave = get_object_or_404(NurseLeave, id=leave_id)
        
        # Get active assignment of original nurse
        active_assignment = NurseAssignment.objects.filter(
            nurse=leave.nurse,
            status='Approved'
        ).first()
        
        if request.method == 'POST':
            replacement_nurse_id = request.POST.get('replacement_nurse')
            remark = request.POST.get('remark', '')
            replacement_nurse = get_object_or_404(Nurse, id=replacement_nurse_id, is_approved=True)
            
            if active_assignment:
                # Create temporary assignment
                TemporaryAssignment.objects.create(
                    original_assignment=active_assignment,
                    patient=active_assignment.patient,
                    replacement_nurse=replacement_nurse,
                    leave=leave,
                    start_date=leave.from_date,
                    end_date=leave.to_date,
                    remark=remark
                )
                messages.success(request, "Replacement nurse assigned successfully!")
            return redirect('admin_leave_list')
        
        # Get all available approved nurses except original nurse
        # Exclude:
        # 1. Original nurse
        # 2. Nurses on approved leave overlapping with this leave period
        # 3. Nurses with active normal assignments (Pending/Approved)
        # 4. Nurses who already have temporary assignments overlapping with this leave period
        overlapping_leaves = NurseLeave.objects.filter(
            status='Approved',
            from_date__lte=leave.to_date,  # Other leave starts before or on our leave ends
            to_date__gte=leave.from_date   # Other leave ends after or on our leave starts
        ).values_list('nurse_id', flat=True)
        
        active_assignment_nurse_ids = NurseAssignment.objects.filter(
            status__in=['Pending', 'Approved']
        ).values_list('nurse_id', flat=True)
        
        overlapping_temp_assignments = TemporaryAssignment.objects.filter(
            start_date__lte=leave.to_date,
            end_date__gte=leave.from_date
        ).values_list('replacement_nurse_id', flat=True)
        
        exclude_ids = [leave.nurse.id] + list(overlapping_leaves) + list(active_assignment_nurse_ids) + list(overlapping_temp_assignments)
        
        available_nurses = Nurse.objects.filter(is_approved=True).exclude(id__in=exclude_ids)
        return render(request, 'admin/assign_replacement.html', {
            'leave': leave,
            'available_nurses': available_nurses,
            'active_assignment': active_assignment
        })
    elif request.session.get('sub_admin_id'):
        leave = get_object_or_404(NurseLeave, id=leave_id)
        
        # Get active assignment of original nurse
        active_assignment = NurseAssignment.objects.filter(
            nurse=leave.nurse,
            status='Approved'
        ).first()
        
        if request.method == 'POST':
            replacement_nurse_id = request.POST.get('replacement_nurse')
            remark = request.POST.get('remark', '')
            replacement_nurse = get_object_or_404(Nurse, id=replacement_nurse_id, is_approved=True)
            
            if active_assignment:
                TemporaryAssignment.objects.create(
                    original_assignment=active_assignment,
                    patient=active_assignment.patient,
                    replacement_nurse=replacement_nurse,
                    leave=leave,
                    start_date=leave.from_date,
                    end_date=leave.to_date,
                    remark=remark
                )
                messages.success(request, "Replacement nurse assigned successfully!")
            return redirect('subadmin_leave_list')
        
        # Get all available approved nurses except original nurse
        # Exclude same as above
        overlapping_leaves = NurseLeave.objects.filter(
            status='Approved',
            from_date__lte=leave.to_date,  # Other leave starts before or on our leave ends
            to_date__gte=leave.from_date   # Other leave ends after or on our leave starts
        ).values_list('nurse_id', flat=True)
        
        active_assignment_nurse_ids = NurseAssignment.objects.filter(
            status__in=['Pending', 'Approved']
        ).values_list('nurse_id', flat=True)
        
        overlapping_temp_assignments = TemporaryAssignment.objects.filter(
            start_date__lte=leave.to_date,
            end_date__gte=leave.from_date
        ).values_list('replacement_nurse_id', flat=True)
        
        exclude_ids = [leave.nurse.id] + list(overlapping_leaves) + list(active_assignment_nurse_ids) + list(overlapping_temp_assignments)
        
        available_nurses = Nurse.objects.filter(is_approved=True).exclude(id__in=exclude_ids)
        return render(request, 'subadmin/assign_replacement.html', {
            'leave': leave,
            'available_nurses': available_nurses,
            'active_assignment': active_assignment
        })
    return redirect('home')


# Helper function to check if nurse is on active leave
def is_nurse_on_leave(nurse):
    today = timezone.now().date()
    return NurseLeave.objects.filter(
        nurse=nurse,
        status='Approved',
        from_date__lte=today,
        to_date__gte=today
    ).exists()


# Helper function to get active leave for nurse
def get_nurse_active_leave(nurse):
    today = timezone.now().date()
    return NurseLeave.objects.filter(
        nurse=nurse,
        status='Approved',
        from_date__lte=today,
        to_date__gte=today
    ).first()


# Helper function to get patient's active leave notification
def get_patient_leave_notification(patient):
    active_assignment = NurseAssignment.objects.filter(
        patient=patient,
        status='Approved'
    ).first()
    
    if active_assignment:
        active_leave = get_nurse_active_leave(active_assignment.nurse)
        if active_leave:
            return active_leave
    return None


# Helper function to calculate monthly statistics for a nurse
def calculate_monthly_stats(nurse, year, month):
    from datetime import datetime, timedelta
    import calendar
    
    # Get first and last day of month
    first_day = datetime(year, month, 1).date()
    last_day = datetime(year, month, calendar.monthrange(year, month)[1]).date()
    
    # Get active assignments during this month
    active_assignments = NurseAssignment.objects.filter(
        nurse=nurse,
        status='Approved',
        assigned_at__date__lte=last_day
    )
    
    # Collect all unique duty days in month where nurse had active assignment
    duty_days = set()
    
    # Also collect present days
    present_days = set()
    leave_days = set()
    
    # Get all attendances in month
    attendances = Attendance.objects.filter(
        nurse=nurse,
        date__gte=first_day,
        date__lte=last_day,
        check_in_status='Approved'
    )
    for att in attendances:
        present_days.add(att.date)
        duty_days.add(att.date)
    
    # Get all approved leaves in month
    leaves = NurseLeave.objects.filter(
        nurse=nurse,
        status='Approved',
        from_date__lte=last_day,
        to_date__gte=first_day
    )
    for leave in leaves:
        current_date = max(leave.from_date, first_day)
        end_date = min(leave.to_date, last_day)
        delta = end_date - current_date
        for i in range(delta.days + 1):
            leave_day = current_date + timedelta(days=i)
            leave_days.add(leave_day)
            duty_days.add(leave_day)
    
    # Also, we need to check all days in month and see which days nurse had active assignment
    # Let's loop through each day in month
    all_days_in_month = []
    day = first_day
    while day <= last_day:
        all_days_in_month.append(day)
        day += timedelta(days=1)
    
    for day in all_days_in_month:
        # Check if nurse had active assignment on that day
        had_active = active_assignments.filter(assigned_at__date__lte=day).exists()
        if had_active:
            duty_days.add(day)
    
    # Calculate absent days: duty days - present - leave
    absent_days = duty_days - present_days - leave_days
    
    return {
        'nurse': nurse,
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'assigned_duty_days': len(duty_days),
        'present_days': len(present_days),
        'approved_leave_days': len(leave_days),
        'absent_days': len(absent_days)
    }


# Admin monthly statistics
def admin_monthly_stats(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admin_login')
    
    # Get year and month from request or default to current
    from datetime import datetime
    now = datetime.now()
    year = int(request.GET.get('year', now.year))
    month = int(request.GET.get('month', now.month))
    
    nurses = Nurse.objects.filter(is_approved=True)
    stats_list = []
    for nurse in nurses:
        stats = calculate_monthly_stats(nurse, year, month)
        stats_list.append(stats)
    
    return render(request, 'admin/monthly_stats.html', {
        'stats_list': stats_list,
        'year': year,
        'month': month,
        'nurses': nurses
    })


# Subadmin monthly statistics
def subadmin_monthly_stats(request):
    if not request.session.get('sub_admin_id'):
        return redirect('sub_admin_login')
    
    # Get year and month from request or default to current
    from datetime import datetime
    now = datetime.now()
    year = int(request.GET.get('year', now.year))
    month = int(request.GET.get('month', now.month))
    
    nurses = Nurse.objects.filter(is_approved=True)
    stats_list = []
    for nurse in nurses:
        stats = calculate_monthly_stats(nurse, year, month)
        stats_list.append(stats)
    
    return render(request, 'subadmin/monthly_stats.html', {
        'stats_list': stats_list,
        'year': year,
        'month': month,
        'nurses': nurses
    })
