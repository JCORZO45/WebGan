from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from .forms import RegistroForm
from .models import LotsCattle, Animals, Vaccines, AnimalVaccines

def inicio(request):
    return render(request, 'inicio.html')

def noticias(request):
    return render(request, 'noticias.html')

def foro(request):
    return render(request, 'foro.html')

def compra_venta(request):
    return render(request, 'compra_venta.html')

def mi_ganado(request):
    return render(request, 'mi_ganado.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("inicio")  # Redirige al inicio después del login
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, "login.html")

def registro_view(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Tu cuenta ha sido creada exitosamente!")
            return redirect("login")  # Redirige al login después del registro
    else:
        form = RegistroForm()
    return render(request, "registro.html", {"form": form})

def acerca_de_nosotros(request):
    return render(request, 'acerca_de_nosotros.html')

@login_required
def perfil_view(request):
    return render(request, "perfil.html", {"user": request.user})

@login_required
def lotes_view(request):
    lotes = LotsCattle.objects.filter(user=request.user).annotate(
        avg_weight=Avg('animals__weight', filter=Q(animals__weight__isnull=False)),  # Ignorar valores nulos
        animal_count=Count('animals')  # Contar la cantidad de animales en el lote
    ).distinct()  # Asegurarse de que no haya duplicados
    return render(request, 'lotes.html', {'lotes': lotes})

@login_required
def crear_lote_view(request):
    if request.method == "POST":
        lot_name = request.POST["lot_name"]
        description = request.POST["description"]
        type = request.POST["type"]
        ability = request.POST["ability"]
        LotsCattle.objects.create(
            lot_name=lot_name,
            description=description,
            type=type,
            ability=ability,
            user=request.user
        )
        return redirect('lotes')  # Redirige a la lista de lotes después de crear uno
    return render(request, 'crear_lote.html')

@login_required
def eliminar_lote_view(request, lot_id):
    lote = get_object_or_404(LotsCattle, id=lot_id, user=request.user)
    if request.method == "POST":
        lote.delete()
        return redirect('lotes')  # Redirige a la lista de lotes después de eliminar
    return render(request, 'eliminar_lote.html', {'lote': lote})

@login_required
def animales_view(request):
    animales = Animals.objects.filter(lot__user=request.user)
    return render(request, 'animales.html', {'animales': animales})

@login_required
def crear_animal_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        weight = request.POST.get("weight")
        birth_date = request.POST.get("birth_date")
        lot_id = request.POST.get("lot")
        vaccine_ids = request.POST.getlist("vaccines")
        
        if not birth_date:
            messages.error(request, "La fecha de nacimiento es obligatoria.")
            return redirect('crear_animal')

        lot = get_object_or_404(LotsCattle, id=lot_id, user=request.user)
        animal = Animals.objects.create(
            name=name,
            weight=weight,
            birth_date=birth_date,
            lot=lot
        )
        
        # Crear registros en AnimalVaccines para cada vacuna seleccionada
        for vaccine_id in vaccine_ids:
            vaccine = get_object_or_404(Vaccines, id=vaccine_id, user=request.user)
            AnimalVaccines.objects.create(
                animal=animal,
                vaccine=vaccine,
                date_application=birth_date,  # Puedes ajustar esta fecha según sea necesario
                dose=1.0  # Ajusta la dosis según sea necesario
            )
        
        return redirect('animales')  # Redirige a la lista de animales después de crear uno
    lots = LotsCattle.objects.filter(user=request.user)
    vaccines = Vaccines.objects.filter(user=request.user)
    return render(request, 'crear_animal.html', {'lots': lots, 'vaccines': vaccines})

@login_required
def editar_animal_view(request, animal_id):
    animal = get_object_or_404(Animals, code_number=animal_id, lot__user=request.user)  # Cambiar id por code_number
    if request.method == "POST":
        animal.name = request.POST["name"]
        animal.weight = request.POST["weight"]
        lot_id = request.POST["lot"]
        vaccine_ids = request.POST.getlist("vaccines")
        animal.lot = get_object_or_404(LotsCattle, id=lot_id, user=request.user)
        animal.save()
        # Actualizar las vacunas asociadas
        AnimalVaccines.objects.filter(animal=animal).delete()
        for vaccine_id in vaccine_ids:
            vaccine = get_object_or_404(Vaccines, id=vaccine_id, user=request.user)
            AnimalVaccines.objects.create(
                animal=animal,
                vaccine=vaccine,
                date_application=animal.birth_date,
                dose=1.0
            )
        return redirect('animales')
    lots = LotsCattle.objects.filter(user=request.user)
    vaccines = Vaccines.objects.filter(user=request.user)
    associated_vaccine_ids = list(animal.animalvaccines_set.values_list('vaccine_id', flat=True))  # Obtener IDs de vacunas asociadas
    return render(request, 'editar_animal.html', {
        'animal': animal,
        'lots': lots,
        'vaccines': vaccines,
        'associated_vaccine_ids': associated_vaccine_ids
    })

@login_required
def eliminar_animal_view(request, animal_id):
    animal = get_object_or_404(Animals, code_number=animal_id, lot__user=request.user)  # Cambiar id por code_number
    if request.method == "POST":
        animal.delete()
        return redirect('animales')
    return render(request, 'eliminar_animal.html', {'animal': animal})

@login_required
def crear_vacuna_view(request):
    if request.method == "POST":
        name = request.POST["name"]
        application_date = request.POST["date"]  # Correct field name
        state = request.POST["description"]  # Map 'description' to 'state'
        Vaccines.objects.create(
            name=name,
            application_date=application_date,
            state=state,
            user=request.user
        )
        return redirect('vacunas')  # Redirect to the vaccine list after creation
    return render(request, 'crear_vacuna.html')

@login_required
def vacunas_view(request):
    vacunas = Vaccines.objects.filter(user=request.user)
    return render(request, 'vacunas.html', {'vacunas': vacunas})