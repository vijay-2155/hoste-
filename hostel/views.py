from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from authen.models import CustomUser  # Import your CustomUser model
from django.contrib import messages


def index(request):
    return render(request, 'html/mainhp.html')


def aboutus(request):
    return render(request, 'html/about us.html')


def contact(request):
    return render(request, 'html/contact.html')


def feedback(request):
    return render(request, 'html/follow us.html')


def profile(request):
    return render(request, 'html/FIRST PAGE .HTML')


def signup(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        email = request.POST['email']
        password = request.POST['pswd']
        location = request.POST['location']
        date_of_birth = request.POST['dob']
        phone_number = request.POST['phno']
        college = request.POST['clgname']

        if not user_name or not email or not password or not location or not date_of_birth or not phone_number or not college:
            messages.error(request, "All fields are required.")
        else:
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
            else:
                user = CustomUser(email=email, username=user_name, phone_number=phone_number,
                                  location=location, date_of_birth=date_of_birth, college=college)
                user.set_password(password)
                user.save()
                messages.success(request, "Registration successful.")
                return redirect('signup')  # Redirect to your desired page after successful signup

    return render(request, 'html/sign up.html')


def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pswd']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            # Redirect to the desired page after successful login
            return redirect('index')  # Replace 'dashboard' with the actual URL name of your dashboard page
        else:
            messages.error(request, "Incorrect email or password. Please try again.")

    return render(request, 'html/sign up.html')


def ownersignup(request):
    if request.method == 'POST':
        user_name = request.POST['txt']
        email = request.POST['email']
        password = request.POST['pswd']
        name = request.POST['NAME']
        phone_number = request.POST['phno']

        if not user_name or not email or not password or not name or not phone_number:
            messages.error(request, "All fields are required.")
        else:
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
            else:
                user = CustomUser(email=email, username=user_name, phone_number=phone_number, college=None, location=None, date_of_birth=None)
                user.set_password(password)
                user.save()
                messages.success(request, "Owner registration successful.")
                return redirect('ownersignup')  # Redirect to your desired page after successful owner signup

    return render(request, 'html/owner sign up.html')
