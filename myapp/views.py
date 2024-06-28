import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from urllib import parse
from .forms import EmployeeForm, VisitorForm, VisiteForm, CourrierForm, CourrierReceptionForm, EmployeeAuthenticationForm
from .models import Employee, Visitor, Visite, Courrier
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_deny
from django.views.decorators.clickjacking import xframe_options_sameorigin
def navbar(request):
    return render(request, 'navbar.html')



import time

def addnew(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee added successfully!')
            return redirect('index')
    else:
        form = EmployeeForm()
    
    return render(request, 'addnew.html', {'form': form})



def index(request):  
    employees = Employee.objects.all()  
    return render(request, "show.html", {'employees': employees})  

def edit(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'edit.html', {'form': form, 'employee': employee})

def update(request, id):
    existing_employee = Employee.objects.get(id=id)
    old_pass = existing_employee.password 
    if request.method == 'POST':
        decoded_string = request.body.decode('utf-8')
        parsed_dict = parse.parse_qs(decoded_string)
        data = {k: v[0] for k, v in parsed_dict.items()}
        
        form = EmployeeForm(data, instance=existing_employee)

        if form.is_valid():
            form.update(old_pass)
            messages.success(request, 'Employee modified successfully!')
            return redirect('index')
    else:
        form = EmployeeForm(instance=existing_employee)
    
    return render(request, 'edit.html', {'form': form, 'employee': existing_employee})

def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    messages.success(request, 'Employee deleted successfully!')
    return redirect('index')

def login_view(request):
    if request.method == 'POST':
        form = EmployeeAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f'Trying to authenticate user: {username}')
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                print(f'Authentication successful: {user.email}')
                auth_login(request, user)
                # Set session data
                request.session['user_id'] = user.id
                request.session['user_email'] = user.email
                request.session['user_role'] = user.role

                # Print session data for debugging

                if user.role == 'admin':
                    print('Redirecting to admin dashboard')
                    return redirect('home')
                else:
                    print('Redirecting to user dashboard')
                    return redirect('home')
            else:
                print('Authentication failed')
                messages.error(request, 'Invalid username or password')
        else:
            print('Form is not valid')
            print(form.errors)  # Print form errors for debugging
            messages.error(request, 'Invalid username or password')
    else:
        form = EmployeeAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def out(request):
    return render(request, 'out.html')

def sidebar(request):
    return render(request, 'sidebar.html')

def home(request):
    return render(request, 'home.html')

@xframe_options_sameorigin
def bi_user(request):
    return render(request, 'bi_user.html')

@xframe_options_sameorigin
def bi_admin(request):
    return render(request, 'bi_admin.html')

def add_visitor(request):
    if request.method == 'POST':
        form = VisitorForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Visitor added successfully')
            return redirect('gestion_visites')
    else:
        form = VisitorForm()
    return render(request, 'add_visitor.html', {'form': form})

def edit_visitor(request, visitor_id):
    visitor = get_object_or_404(Visitor, pk=visitor_id)
    if request.method == 'POST':
        form = VisitorForm(request.POST, instance=visitor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Visitor modified successfully')
            return redirect('gestion_visites')
    else:
        form = VisitorForm(instance=visitor)
    return render(request, 'edit_visitor.html', {'visitor': visitor})


@require_POST
def delete_visitor(request, visitor_id):
    visitor = get_object_or_404(Visitor, pk=visitor_id)
    visitor.delete()
    messages.success(request, 'Visitor deleted successfully')
    return redirect('gestion_visites')

def update_visitor(request, visitor_id):
    visitor = Visitor.objects.get(id=visitor_id)
    if request.method == 'POST':
        form = VisitorForm(request.POST, instance=visitor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Visitor modified successfully')
            time.sleep(1)
            return redirect('gestion_visites')
    else:
        form = VisitorForm(instance=visitor)
    return render(request, 'update_visitor.html', {'form': form, 'visitor': visitor})

def logout_view(request):
    # Clear session data
    request.session.flush()
    auth_logout(request)
    return redirect('login')

from django.contrib.auth.decorators import login_required, permission_required


@login_required
@permission_required('myapp.view_gestion_courriers', raise_exception=True)
def gestion_courriers(request):
    return render(request, 'gestion_courriers.html')

@login_required
def admin_dashboard(request):
    print('Admin dashboard accessed')
    if request.user.role != 'admin':
        print('User is not admin, redirecting to user dashboard')
        return redirect('user_dashboard')
    return render(request, "admin_dashboard.html")

@login_required
def user_dashboard(request):
    context = {
        'no_sidebar': True,
        'can_view_visites': request.user.has_perm('myapp.view_gestion_visites'),
        'can_view_courriers': request.user.has_perm('myapp.view_gestion_courriers'),
        'can_view_employes': request.user.has_perm('myapp.view_gestion_employes'),
        'can_view_visiteurs': request.user.has_perm('myapp.view_gestion_visiteurs'),
    }
    print(context) 
    return render(request, "user_dashboard.html", context)

@login_required
def gestion_visites(request):
    type_visite = request.GET.get('type', 'all')
    if request.user.role == 'user':
        visites = Visite.objects.filter(employee=request.user)
    else:
        if type_visite == 'en_cours':
            visites = Visite.objects.filter(date_fin__isnull=True).select_related('employee', 'visiteur')
        elif type_visite == 'historique':
            visites = Visite.objects.filter(date_fin__lte=timezone.now()).select_related('employee', 'visiteur')
        else:
            visites = Visite.objects.all().select_related('employee', 'visiteur')
    print(Visitor.objects.all())
    return render(request, 'gestion_visites.html', {
        'visites': visites,
        'type': type_visite,
        'visitors': Visitor.objects.all()
    })

class VisiteListView(ListView):
    model = Visite
    context_object_name = 'visites'
    template_name = 'gestion_visites.html'

class VisiteCreateView(CreateView):
    model = Visite
    form_class = VisiteForm
    template_name = 'visite_form.html'
    success_url = reverse_lazy('gestion_visites')

class VisiteUpdateView(UpdateView):
    model = Visite
    form_class = VisiteForm
    template_name = 'visite_form.html'
    success_url = reverse_lazy('gestion_visites')

class VisiteDeleteView(DeleteView):
    model = Visite
    context_object_name = 'visite'
    template_name = 'visite_confirm_delete.html'
    success_url = reverse_lazy('gestion_visites')

@login_required
def historique_visites(request):
    visites = Visite.objects.filter(date_fin__lte=timezone.now()).order_by('-date_fin')
    return render(request, 'historique_visites.html', {'visites': visites})

@login_required
def visites_en_cours(request):
    visites = Visite.objects.filter(date_fin__isnull=True).select_related('employee', 'visiteur')
    return render(request, 'visites_en_cours.html', {'visites': visites})

@login_required
def terminer_visite(request, pk):
    visite = Visite.objects.get(pk=pk)
    visite.date_fin = timezone.now()
    visite.save()
    messages.success(request, 'Visite terminée avec succès')
    return redirect('gestion_visites')

@login_required
def bi_admin(request):
    iframe = "https://app.powerbi.com/groups/me/reports/5d059524-1094-46d7-bc4c-5096e5c904d7/22f55a4ea78c26a24afd?experience=power-bi"
    return render(request, 'bi_admin.html', {'iframe': iframe})

@login_required
def create_visite(request, visitor_id=None, employee_id=None):
    initial_data = {}
    if visitor_id:
        initial_data['visiteur'] = Visitor.objects.get(id=visitor_id)
    if employee_id:
        initial_data['employee'] = Employee.objects.get(id=employee_id)

    if request.method == 'POST':
        form = VisiteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('visites_en_cours')
    else:
        form = VisiteForm(initial=initial_data)

    return render(request, 'create_visite.html', {'form': form})

@login_required
def list_courriers(request):
    courriers = Courrier.objects.all()
    return render(request, 'list_courriers.html', {'courriers': courriers})

@login_required
def add_courrier(request):
    if request.method == 'POST':
        form = CourrierForm(request.POST)
        if form.is_valid():
            courrier = form.save(commit=False)
            courrier.statut = 'en cours'
            courrier.save()
            messages.success(request, 'Courrier ajouté avec succès')
            return redirect('list_courriers')
    else:
        form = CourrierForm()
    return render(request, 'add_courrier.html', {'form': form})

@login_required
def edit_courrier(request, pk):
    courrier = get_object_or_404(Courrier, pk=pk) 
    if request.method == 'POST':
        decoded_string = request.body.decode('utf-8')
        parsed_dict = json.loads(decoded_string)
        form = CourrierForm(parsed_dict, instance=courrier)
        if form.is_valid():
            form.save()
            return redirect('list_courriers')
    else:
        form = CourrierForm(instance=courrier)
    return render(request, 'edit_courrier.html', {'form': form, 'courrier': courrier})

@login_required
def delete_courrier(request, pk):
    courrier = get_object_or_404(Courrier, pk=pk)
    courrier.delete()
    messages.success(request, 'Courrier supprimé avec succès')
    return redirect('list_courriers')

@login_required
def gestion_courriers(request):
    if request.method == 'POST':
        form = CourrierReceptionForm(request.POST)
        if form.is_valid():
            courrier_id = request.POST.get('courrier_id')
            courrier = Courrier.objects.get(id=courrier_id)
            courrier.est_recu = form.cleaned_data['est_recu']
            courrier.save()
            return redirect('gestion_courriers')
    else:
        courriers = Courrier.objects.all()
        courriers_and_forms = [(courrier, CourrierReceptionForm(instance=courrier)) for courrier in courriers]
    return render(request, 'gestion_courriers.html', {'courriers_and_forms': courriers_and_forms})

@login_required
def courriers(request):
    courriers = Courrier.objects.filter(est_recu=True)
    return render(request, 'list_courriers.html', {'courriers': courriers})

@login_required
def courriers_en_cours(request):
    courriers = Courrier.objects.filter(statut='en cours')
    return render(request, 'courriers_en_cours.html', {'courriers': courriers})

@login_required
def terminer_courrier(request, pk):
    courrier = get_object_or_404(Courrier, pk=pk)
    courrier.statut = 'terminé'
    courrier.est_recu = True
    courrier.save()
    return redirect('list_courriers')
