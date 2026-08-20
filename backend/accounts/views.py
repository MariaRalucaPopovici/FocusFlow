from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def register(request):
    if request.method == "POST":
        username = request.POST["uname"]
        email = request.POST["mail"]
        password = request.POST["pass"]
        confirm_password = request.POST["pass2"]

        if password != confirm_password:
            print("Passwords do not match!")

        elif User.objects.filter(username=username).exists():
            print("Username already exists!")

        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            print("User registered!")

    return render(request, "accounts/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["uname"]
        password = request.POST["psw"]
        user = authenticate(request, username=username, password=password)
        
        if user is None:
            print("Invalid username or password")
        else:
            login(request, user)
            print("Success")
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)
            return redirect("task_list")
        
    return render(request,"accounts/login.html")

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return redirect("login")
    
    

