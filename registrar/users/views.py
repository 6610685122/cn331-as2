from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout


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
            return redirect('course')  # เปลี่ยนไปหน้า home หลังจากล็อกอิน
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

def course(request):
    return render(request, 'course.html')








