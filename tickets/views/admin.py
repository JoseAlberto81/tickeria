from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from tickets.models import Ticket

def admin_login(request):
    mensaje = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            mensaje = "Credenciales incorrectas o no autorizado."
    return render(request, 'tickets/admin_login.html', {'mensaje': mensaje})

@login_required
def admin_dashboard(request):
    tickets = Ticket.objects.all().order_by('-creado')
    return render(request, 'tickets/admin_dashboard.html', {'tickets': tickets})