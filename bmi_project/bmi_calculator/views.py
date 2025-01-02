from django.shortcuts import render,redirect
from .forms import BMIForm,Login
from django.contrib.auth import authenticate, login

def login_view(request):
    error_message = None

    if request.method == "POST":
        form = Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data['uname']
            password = form.cleaned_data['pwd']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Log the user in
                return redirect('calculate_bmi')  # Redirect to the BMI calculation page
            else:
                error_message = "Invalid username or password."
    else:
        form = Login()

    return render(request, "bmi_calculator/login.html", {
        'form': form,
        'error_message': error_message,
    })

def calculate_bmi(request):
    bmi = None
    category = None

    if request.method == "POST":
        form = BMIForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data['weight']
            height_cm = form.cleaned_data['height']  # Height in cm
            height_m = height_cm / 100  # Convert to meters
            
            # Calculate BMI
            bmi = weight / (height_m ** 2)
            
            # Determine category
            if bmi < 18.5:
                category = "Underweight"
            elif 18.5 <= bmi < 24.9:
                category = "Normal weight"
            elif 25 <= bmi < 29.9:
                category = "Overweight"
            else:
                category = "Obesity"
    else:
        form = BMIForm()

    return render(request, "bmi_calculator/bmi_form.html", {
        'form': form,
        'bmi': bmi,
        'category': category
    })
