from decimal import Decimal
from random import randint

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import DetalleFacturaFormSet, EmpleadoForm, FacturaForm, RegistroForm
from .models import DetalleFactura, Empleado, Factura, RolPago, Usuario


# =========================
# 🏠 HOME
# =========================
def home(request):
    return render(request, 'home.html')


# =========================
# 📝 REGISTER
# =========================
def register(request):

    if request.method == 'POST':
        form = RegistroForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Usuario registrado correctamente.")
            return redirect('login')

        messages.error(request, "Corrija los errores del formulario.")

    else:
        form = RegistroForm()

    return render(request, 'register.html', {'form': form})


# =========================
# 🔐 LOGIN
# =========================
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect("login")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("menu_principal")

        messages.error(request, "Usuario o contraseña incorrectos.")
        return redirect("login")

    return render(request, "login.html")


# =========================
# 📋 MENÚ PRINCIPAL (ROL DE PAGOS)
# =========================
@login_required(login_url='login')
def menu_principal(request):
    return render(request, 'menu_principal.html')


# =========================
# 👤 MÓDULO EMPLEADOS (CRUD)
# =========================
@login_required(login_url='login')
def modulo_empleados(request):
    empleado_edicion = None
    form = EmpleadoForm()

    if request.method == 'POST':
        accion = request.POST.get('accion')

        if accion == 'guardar':
            empleado_id = request.POST.get('empleado_id')
            empleado_edicion = get_object_or_404(Empleado, id=empleado_id) if empleado_id else None
            form = EmpleadoForm(request.POST, instance=empleado_edicion)

            if form.is_valid():
                form.save()
                if empleado_edicion:
                    messages.success(request, 'Empleado actualizado correctamente.')
                else:
                    messages.success(request, 'Empleado agregado correctamente.')
                return redirect('modulo_empleados')

            messages.error(request, 'Revise los datos del formulario.')

        elif accion == 'eliminar':
            empleado_id = request.POST.get('empleado_id')
            empleado = get_object_or_404(Empleado, id=empleado_id)
            empleado.delete()
            messages.success(request, 'Empleado eliminado correctamente.')
            return redirect('modulo_empleados')

    empleado_id_editar = request.GET.get('editar')
    if empleado_id_editar and request.method == 'GET':
        empleado_edicion = get_object_or_404(Empleado, id=empleado_id_editar)
        form = EmpleadoForm(instance=empleado_edicion)

    empleados = Empleado.objects.all()

    return render(
        request,
        'modulo_empleados.html',
        {
            'form': form,
            'empleados': empleados,
            'empleado_edicion': empleado_edicion,
        }
    )


# =========================
# 💵 MÓDULO ROL DE PAGOS
# =========================
@login_required(login_url='login')
def modulo_rol_pagos(request):
    empleados = Empleado.objects.all()
    return render(request, 'modulo_rol_pagos.html', {'empleados': empleados})


@login_required(login_url='login')
def guardar_rol_pagos(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido.'}, status=405)

    try:
        import json
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido.'}, status=400)

    detalle = data.get('detalle', [])
    if not detalle:
        return JsonResponse({'error': 'No hay datos para guardar.'}, status=400)

    rol = RolPago.objects.create(datos=data)
    return JsonResponse({'message': f'Rol guardado correctamente (ID: {rol.id}).'})


def _generar_numero_factura(establecimiento: str, punto_emision: str):
    ultima = (
        Factura.objects.filter(establecimiento=establecimiento, punto_emision=punto_emision)
        .order_by('-id')
        .first()
    )
    siguiente = int(ultima.secuencial) + 1 if ultima else 1
    secuencial = f"{siguiente:09d}"
    numero = f"{establecimiento}-{punto_emision}-{secuencial}"
    return numero, secuencial


def _generar_clave_acceso(fecha_emision, ruc):
    fecha = fecha_emision.strftime('%d%m%Y')
    aleatorio = ''.join(str(randint(0, 9)) for _ in range(29))
    base = f"{fecha}01{ruc}{aleatorio}"
    return base[:49].ljust(49, '0')


@login_required(login_url='login')
def generar_factura(request):
    if request.method == 'POST':
        form = FacturaForm(request.POST)
        formset = DetalleFacturaFormSet(request.POST, prefix='detalles')

        if form.is_valid() and formset.is_valid():
            detalles_limpios = [
                f for f in formset.cleaned_data
                if f and not f.get('DELETE', False)
            ]

            if not detalles_limpios:
                messages.error(request, 'Debe agregar al menos un producto en la factura.')
                return render(request, 'generar_factura.html', {'form': form, 'formset': formset})

            subtotal_0 = Decimal('0.00')
            subtotal_12 = Decimal('0.00')
            total_descuento = Decimal('0.00')

            try:
                with transaction.atomic():
                    factura = form.save(commit=False)
                    factura.establecimiento = factura.establecimiento.zfill(3)
                    factura.punto_emision = factura.punto_emision.zfill(3)

                    numero_factura, secuencial = _generar_numero_factura(
                        factura.establecimiento,
                        factura.punto_emision,
                    )
                    factura.numero_factura = numero_factura
                    factura.secuencial = secuencial

                    factura.clave_acceso = _generar_clave_acceso(factura.fecha_emision, factura.ruc)
                    factura.numero_autorizacion = factura.clave_acceso

                    factura.save()

                    for detalle_form in detalles_limpios:
                        cantidad = Decimal(detalle_form['cantidad'])
                        precio_unitario = Decimal(detalle_form['precio_unitario'])
                        descuento = Decimal(detalle_form.get('descuento') or 0)
                        total_sin_impuestos = (cantidad * precio_unitario) - descuento

                        if total_sin_impuestos < 0:
                            raise ValueError('El descuento no puede ser mayor al total de la línea.')

                        subtotal_12 += total_sin_impuestos
                        total_descuento += descuento

                        DetalleFactura.objects.create(
                            factura=factura,
                            codigo=detalle_form['codigo'],
                            descripcion=detalle_form['descripcion'],
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            descuento=descuento,
                            total_sin_impuestos=total_sin_impuestos,
                        )

                    factura.subtotal_0 = subtotal_0.quantize(Decimal('0.01'))
                    factura.subtotal_12 = subtotal_12.quantize(Decimal('0.01'))
                    factura.iva = (subtotal_12 * Decimal('0.12')).quantize(Decimal('0.01'))
                    factura.total_descuento = total_descuento.quantize(Decimal('0.01'))
                    factura.total = (factura.subtotal_0 + factura.subtotal_12 + factura.iva).quantize(Decimal('0.01'))
                    factura.save()
            except ValueError as exc:
                messages.error(request, str(exc))
                return render(request, 'generar_factura.html', {'form': form, 'formset': formset})

            messages.success(request, f'Factura {factura.numero_factura} guardada correctamente.')
            return redirect('detalle_factura', id=factura.id)

        messages.error(request, 'Revise los campos obligatorios del formulario.')

    else:
        datos_iniciales = {
            'fecha_emision': timezone.localdate(),
            'establecimiento': '001',
            'punto_emision': '001',
        }
        form = FacturaForm(initial=datos_iniciales)
        formset = DetalleFacturaFormSet(prefix='detalles')

    return render(request, 'generar_factura.html', {'form': form, 'formset': formset})


@login_required(login_url='login')
def buscar_factura(request):
    termino = request.GET.get('numero_factura', '').strip()
    resultados = []

    if termino:
        resultados = Factura.objects.filter(numero_factura__icontains=termino)
        if not resultados:
            messages.error(request, 'No se encontraron facturas con ese número.')

    return render(
        request,
        'buscar_factura.html',
        {
            'resultados': resultados,
            'termino': termino,
        },
    )


@login_required(login_url='login')
def detalle_factura(request, id):
    factura = get_object_or_404(Factura, id=id)
    detalles = factura.detalles.all()
    return render(request, 'detalle_factura.html', {'factura': factura, 'detalles': detalles})


# =========================
# 🚪 LOGOUT
# =========================
@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')


# =========================
# 🔑 RECUPERAR CONTRASEÑA
# =========================
def password_reset(request):

    if request.method == "POST":

        if "email" in request.POST and "respuesta_seguridad" not in request.POST:

            email = request.POST.get("email")

            if not email:
                messages.error(request, "Debe ingresar un correo.")
                return redirect("password_reset")

            usuario = Usuario.objects.filter(email=email).first()

            if not usuario:
                messages.error(request, "No existe un usuario con ese correo.")
                return redirect("password_reset")

            return render(request, "password_reset.html", {"usuario": usuario})

        if "respuesta_seguridad" in request.POST:

            email = request.POST.get("email")
            respuesta = request.POST.get("respuesta_seguridad")
            nueva_password = request.POST.get("nueva_password")

            usuario = Usuario.objects.filter(email=email).first()

            if not usuario:
                messages.error(request, "Error inesperado.")
                return redirect("password_reset")

            if not respuesta or not nueva_password:
                messages.error(request, "Todos los campos son obligatorios.")
                return render(request, "password_reset.html", {"usuario": usuario})

            if usuario.respuesta_seguridad.lower() == respuesta.lower():

                usuario.set_password(nueva_password)
                usuario.save()

                messages.success(request, "Contraseña cambiada correctamente.")
                return redirect("login")

            messages.error(request, "La respuesta no coincide.")
            return render(request, "password_reset.html", {"usuario": usuario})

    return render(request, "password_reset.html")


def meme(request):
    return render(request, 'meme.html')
