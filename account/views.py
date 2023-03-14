from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# Create your views here.
def login_request(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username = username, password = password)
        print(user)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, "account/login.html", {
                "error": "Kullanıcı adı veya parola yanlış."
            })

    return render(request, "account/login.html")
def register(request):
    if request.method == "POST":
        realname = request.POST["realname"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password != password2:
            return render(request, "account/register.html", {
            "error": "Parolalar eşleşmiyor."
        })

        if User.objects.filter(username=username).exists():
            return render(request, "account/register.html", {
            "error": "Username kullanımda."
        })

        if User.objects.filter(email=email).exists():
            return render(request, "account/register.html", {
            "error": "Email kullanımda."
        })

        user = User.objects.create_user(username = username, email=email, first_name=realname, password=password)
        user.save()
        return redirect("home")
    return render(request, "account/register.html")

def logout_request(request):
    logout(request)
    return redirect("home")

def user_page(request, username):
   pass
