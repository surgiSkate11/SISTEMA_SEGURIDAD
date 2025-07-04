from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django .contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from applications.security.forms.user import CustomUserCreationForm

# ----------------- Cerrar Sesion -----------------
@login_required
def signout(request):
    logout(request)
    return redirect("security:signin")

# # ----------------- Iniciar Sesion -----------------
def signin(request):
    
    data = {"title": "Login",
            "title1": "home de Sesión"}
    if request.method == "GET":
        # Obtener mensajes de éxito de la cola de mensajes
        success_messages = messages.get_messages(request)
        return render(request, "security/auth/signin.html", {
            "form": AuthenticationForm(),
            "success_messages": success_messages,  # Pasar mensajes de éxito a la plantilla
            **data
        })
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                return render(request, "security/auth/signin.html", {
                    "form": form,
                    "error": "El usuario o la contraseña son incorrectos",
                    **data
                })
        else:
            return render(request, "security/auth/signin.html", {
                "form": form,
                 "error": "Datos invalidos",
                **data
            })

# # ----------------- Registrar Nuevo Usuario -----------------
def signup(request):
    data = {"title1": "Registro", "title2": "Crea tu cuenta"}
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "¡Registro exitoso! Ahora puedes acceder al sistema.")
            return redirect("home")
        else:
            return render(request, "security/auth/signup.html", {"form": form, **data})
    else:
        form = CustomUserCreationForm()
        return render(request, "security/auth/signup.html", {"form": form, **data})