from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib import messages

from store.forms import CustomUserForm

def register(request):
    if request.user.is_authenticated:
        messages.success(request, "Ya posees la sesión iniciada")
        return redirect('/')
    else:
        form = CustomUserForm()
        if request.method == 'POST':
            form = CustomUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Registro completado!. Inicia sesion par continuar.")
                return redirect('/login')
        context = {'form':form}
        return render(request, "store/auth/register.html", context)

def loginpage(request):
    if request.user.is_authenticated:
        messages.success(request, "Ya posees la sesión iniciada")
        return redirect('/')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=name, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Logueado correctamente")
                return redirect("/")
            else:
                messages.error(request, "Correo/contraseña incorrecta")
                return redirect('/login')

        return render(request, "store/auth/login.html")

def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Session cerrada correctamente")
        return redirect("/")
    