from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaccion, Cartera, Categoria
from .forms import TransaccionForm, CategoriaForm, CarteraForm
from django.utils import timezone
from django.db.models import Sum, DecimalField, ProtectedError
from django.db.models.functions import Coalesce
from decimal import Decimal
from django.core.paginator import Paginator
from django.contrib import messages

# ... (Vistas index, Transacciones, Categorías) ...
def index(request):
    now = timezone.now()
    current_year = now.year
    current_month = now.month
    ingresos_mes = Transaccion.objects.filter(tipo='I', fecha__year=current_year, fecha__month=current_month).aggregate(total=Coalesce(Sum('monto'), Decimal(0), output_field=DecimalField()))['total']
    gastos_mes = Transaccion.objects.filter(tipo='G', fecha__year=current_year, fecha__month=current_month).aggregate(total=Coalesce(Sum('monto'), Decimal(0), output_field=DecimalField()))['total']
    total_saldo_inicial = Cartera.objects.aggregate(total=Coalesce(Sum('saldo_inicial'), Decimal(0)))['total']
    total_ingresos = Transaccion.objects.filter(tipo='I').aggregate(total=Coalesce(Sum('monto'), Decimal(0)))['total']
    total_gastos = Transaccion.objects.filter(tipo='G').aggregate(total=Coalesce(Sum('monto'), Decimal(0)))['total']
    balance_total = total_saldo_inicial + total_ingresos - total_gastos
    transacciones_recientes = Transaccion.objects.select_related('categoria', 'cartera').order_by('-fecha', '-fecha_creacion')[:10]
    context = {'transacciones': transacciones_recientes,'ingresos_mes': ingresos_mes,'gastos_mes': gastos_mes,'balance_total': balance_total,'current_month_name': now.strftime("%B").capitalize(),}
    return render(request, 'gestion/index.html', context)

def crear_transaccion(request):
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Transacción creada exitosamente!')
            return redirect('gestion:listar_transacciones')
    else:
        form = TransaccionForm()
    context = {'form': form }
    return render(request, 'gestion/crear_transaccion.html', context)

def listar_transacciones(request):
    transacciones_list = Transaccion.objects.select_related('categoria', 'cartera').order_by('-fecha', '-fecha_creacion')
    paginator = Paginator(transacciones_list, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj }
    return render(request, 'gestion/listar_transacciones.html', context)

def listar_categorias(request):
    categorias = Categoria.objects.all().order_by('nombre')
    context = {'categorias': categorias,}
    return render(request, 'gestion/listar_categorias.html', context)

def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Categoría creada exitosamente!')
            return redirect('gestion:listar_categorias')
    else:
        form = CategoriaForm()
    context = {'form_cat': form }
    return render(request, 'gestion/crear_categoria.html', context)

def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, f'¡Categoría "{categoria.nombre}" actualizada!')
            return redirect('gestion:listar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    context = {'form_cat': form, 'categoria': categoria }
    return render(request, 'gestion/editar_categoria.html', context)

def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        try:
            categoria.delete()
            messages.success(request, f'¡Categoría "{categoria.nombre}" eliminada!')
        except ProtectedError:
            messages.error(request, f'No se puede eliminar la categoría "{categoria.nombre}" porque tiene transacciones asociadas.')
        return redirect('gestion:listar_categorias')
    context = {'categoria': categoria }
    return render(request, 'gestion/eliminar_categoria.html', context)

def listar_carteras(request):
    carteras = Cartera.objects.all().order_by('nombre')
    context = {'carteras': carteras,}
    return render(request, 'gestion/listar_carteras.html', context)

def crear_cartera(request):
    if request.method == 'POST':
        form = CarteraForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cartera creada exitosamente!')
            return redirect('gestion:listar_carteras')
    else:
        form = CarteraForm()
    context = {'form_cart': form }
    return render(request, 'gestion/crear_cartera.html', context)

# --- Nuevas Vistas ---

def editar_cartera(request, pk):
    """
    Vista para editar una cartera existente.
    """
    cartera = get_object_or_404(Cartera, pk=pk)

    if request.method == 'POST':
        form = CarteraForm(request.POST, instance=cartera)
        if form.is_valid():
            form.save()
            messages.success(request, f'¡Cartera "{cartera.nombre}" actualizada!')
            return redirect('gestion:listar_carteras')
    else:
        form = CarteraForm(instance=cartera)

    context = {
        'form_cart': form,
        'cartera': cartera
    }
    return render(request, 'gestion/editar_cartera.html', context)

def eliminar_cartera(request, pk):
    """
    Vista para eliminar una cartera existente (con confirmación).
    """
    cartera = get_object_or_404(Cartera, pk=pk)

    if request.method == 'POST':
        nombre_cartera = cartera.nombre # Guardamos el nombre antes de borrar
        cartera.delete()
        messages.success(request, f'¡Cartera "{nombre_cartera}" eliminada! (Y todas sus transacciones asociadas).')
        return redirect('gestion:listar_carteras')

    context = {
        'cartera': cartera
    }
    return render(request, 'gestion/eliminar_cartera.html', context)
