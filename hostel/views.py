from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from authen.models import CustomUser, Location, HostelInformation, RentalInformation  # Import your CustomUser model
from django.contrib import messages
from django.core.exceptions import ValidationError


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
                                  location=location, date_of_birth=date_of_birth, college=college,
                                  profile_type='student')
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
            if user.profile_type == 'owner':
                return redirect('ownership')
            elif user.profile_type == 'student':
                return redirect('studenthp')
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
                user = CustomUser(email=email, username=user_name, phone_number=phone_number, college=None,
                                  location=None, date_of_birth=None, profile_type='owner')
                user.set_password(password)
                user.save()
                messages.success(request, "Owner registration successful.")
                return redirect('ownersignup')  # Redirect to your desired page after successful owner signup

    return render(request, 'html/owner sign up.html')


@login_required
def studenthp(request):
    locations = Location.objects.all()
    return render(request, 'html/studentshp.html', {'locations': locations})


@login_required
def ownership(request):
    return render(request, 'html/ownershp.html')


def logout_view(request):
    logout(request)
    return redirect('signin')


@login_required
def upload(request):
    return render(request, 'html/ownerupload1.html')


@login_required
def upload_hostel(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        hostel_type = request.POST.get('Hosteltype')
        water_facilities = 'waterFacilities' in request.POST
        image = request.FILES.get('imageUpload')
        wifi = 'electricity' in request.POST
        proximity_to_grocery_stores = 'groceryStores' in request.POST
        nearest_transportation = request.POST.get('nearestTransportBus')
        room_type = request.POST.get('Roomtype')
        max_people = request.POST.get('maxPeople')
        location = request.POST.get('location')
        extra_info = request.POST.get('extraInfo')
        owner_name = request.POST.get('Ownername')
        phone = request.POST.get('phone')
        has_whatsapp = 'hasWhatsApp' in request.POST
        email = request.POST.get('email')
        price = request.POST.get('price')

        # Check for empty fields
        if not name or not hostel_type or not max_people or not location or not owner_name or not phone or not email or not price:
            error_message = "All fields are required."
            return render(request, 'html/ownerupload3.html', {'error_message': error_message})

        try:
            hostel = HostelInformation(
                name=name,
                hostel_type=hostel_type,
                water_facilities=water_facilities,
                image=image,
                wifi=wifi,
                proximity_to_grocery_stores=proximity_to_grocery_stores,
                nearest_transportation=nearest_transportation,
                room_type=room_type,
                max_people=max_people,
                location=location,
                extra_info=extra_info,
                owner_name=owner_name,
                phone=phone,
                has_whatsapp=has_whatsapp,
                email=email,
                price=price
            )
            hostel.full_clean()  # Validate the model fields
            hostel.save()  # Save the model instance to the database
            messages.success(request, "Hostel information uploaded successfully.")
            return redirect('ownerupload')  # Replace with the actual URL name for the upload page
        except ValidationError as e:
            error_message = e.message_dict
            return render(request, 'html/ownerupload3.html', {'error_message': error_message})

    return render(request, 'html/ownerupload3.html')


@login_required
def upload_room(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        rental_type = request.POST.get('rentalType')
        water_facilities = request.POST.get('waterFacilities') == 'yes'
        electricity = request.POST.get('electricity') == 'yes'
        proximity_to_grocery_stores = request.POST.get('groceryStores') == 'yes'
        nearest_transportation = request.POST.get('nearestTransportBus')
        max_people = request.POST.get('maxPeople')
        num_rooms = request.POST.get('numRooms')
        location = request.POST.get('location')
        extra_info = request.POST.get('extraInfo')
        owner_name = request.POST.get('Ownername')
        phone = request.POST.get('phone')
        has_whatsapp = request.POST.get('hasWhatsApp') == 'on'
        email = request.POST.get('email')
        image = request.FILES.get('image')
        price = request.POST.get('price')
        # Check for empty fields
        if not name or not rental_type or not max_people or not num_rooms or not location or not owner_name or not phone or not email or not price:
            error_message = "All fields are required."
            return render(request, 'html/ownerupload2.html', {'error_message': error_message})

        RentalInformation.objects.create(
            name=name,
            rental_type=rental_type,
            water_facilities=water_facilities,
            electricity=electricity,
            proximity_to_grocery_stores=proximity_to_grocery_stores,
            nearest_transportation=nearest_transportation,
            max_people=max_people,
            num_rooms=num_rooms,
            location=location,
            extra_info=extra_info,
            owner_name=owner_name,
            phone=phone,
            has_whatsapp=has_whatsapp,
            email=email,
            image=image,
            price=price
        )

        messages.success(request, "Rental information uploaded successfully.")
        return redirect('ownerupload')  # Replace with the actual URL name

    return render(request, 'html/ownerupload2.html')


@login_required
def display(request):
    if request.method == 'GET':
        city = request.GET.get('city')

        # Filter RentalInformation and HostelInformation objects based on state and city
        rental_results = RentalInformation.objects.filter(location__icontains=city)
        hostel_results = HostelInformation.objects.filter(location__icontains=city)

        context = {
            'rental_results': rental_results,
            'hostel_results': hostel_results,
        }
        return render(request, 'html/display.html', context)
    return render(request, 'html/display.html')


@login_required
def display_detail(request, model_type, model_id):
    try:
        if model_type == 'hostel':
            model = HostelInformation.objects.get(id=model_id)
        elif model_type == 'rental':
            model = RentalInformation.objects.get(id=model_id)
        else:
            # Handle an invalid model type
            pass

        return render(request, 'html/display2.html', {
            'model': model,
        })
    except (HostelInformation.DoesNotExist, RentalInformation.DoesNotExist):
        # Handle the case where the hostel or rental doesn't exist
        pass
