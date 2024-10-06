from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .models import Course, QuotaRequest


def index(request):
   return render(request, 'index.html')

def hello(request,id):
    
    return HttpResponse('Hello World' + str(id))

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  
            auth_login(request, user)  # ล็อกอินหลังจากสมัครสมาชิกสำเร็จ
            return redirect('course_list')  # เปลี่ยนไปหน้า home หลังจากล็อกอิน
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('course/')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('login')  # กลับไปที่หน้า login หลัง logout




#def course(request):
#    return render(request, 'course.html')
    


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})


def request_quota(request, course_id):
    course = Course.objects.get(id=course_id)

    # ตรวจสอบว่าผู้ใช้มีคำขอโควต้าอยู่แล้วหรือไม่
    existing_request = QuotaRequest.objects.filter(user=request.user, course=course, is_approved=True).exists()
    
    if existing_request:
        return render(request, 'error.html', {'message': 'You have already requested a quota for this course.'})

    if course.is_quota_open and course.seats > 0:
        QuotaRequest.objects.create(user=request.user, course=course, is_approved=True)
        course.seats -= 1  # ลดจำนวนที่นั่ง
        course.save()  # บันทึกการเปลี่ยนแปลง
        return redirect('quota_success')
    else:
        return render(request, 'error.html', {'message': 'This subject has full seat. Please try again.'})

def quota_success(request):
    # หน้าสำเร็จหลังจากขอโควต้า
    return render(request, 'quota_success.html')


def my_quota_requests(request):
    quota_requests = QuotaRequest.objects.filter(user=request.user, is_approved=True)
    return render(request, 'my_quota_requests.html', {'quota_requests': quota_requests})


def cancel_quota_request(request, request_id):
    quota_request = QuotaRequest.objects.get(id=request_id)
    if quota_request.user == request.user:
        # เพิ่มจำนวนที่นั่งใน Course
        course = quota_request.course
        course.seats += 1  # เพิ่มที่นั่ง
        course.save()  # บันทึกการเปลี่ยนแปลง
        
        quota_request.delete()  # ลบคำขอโควต้า
    return redirect('my_quota_requests')
 