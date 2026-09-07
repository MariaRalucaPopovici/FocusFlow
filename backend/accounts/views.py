from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def register(request):
    if request.method == "POST":
        username = request.POST["uname"]
        email = request.POST["mail"]
        password = request.POST["pass"]
        confirm_password = request.POST["pass2"]

        if password != confirm_password:
            messages.error(request,"Passwords do not match!")

        elif User.objects.filter(username=username).exists():
            messages.error(request,"That username is already taken!")

        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, "Account created! You can now log in.")
            return redirect("login")

    return render(request, "accounts/register.html", {
        "old_username": request.POST.get("uname", ""),
        "old_email": request.POST.get("mail", ""),
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST["uname"]
        password = request.POST["psw"]
        user = authenticate(request, username=username, password=password)
        
        if user is None:
            messages.error(request, "Invalid username or password")
        else:
            login(request, user)
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)
            return redirect("dashboard")
        
    return render(request,"accounts/login.html")

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return redirect("login")
    
    

