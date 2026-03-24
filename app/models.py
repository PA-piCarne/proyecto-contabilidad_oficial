from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):

    telefono = models.CharField(max_length=10)

    PREGUNTAS = [
        ('mascota', '¿Cómo se llama tu primera mascota?'),
        ('madre', '¿Cuál es el segundo nombre de tu madre?'),
        ('ciudad', '¿En qué ciudad naciste?'),
    ]

    pregunta_seguridad = models.CharField(max_length=50, choices=PREGUNTAS)
    respuesta_seguridad = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Empleado(models.Model):
    MODALIDAD_DECIMO_CHOICES = [
        ('anual', 'Anual'),
        ('mensual', 'Mensual'),
    ]

    apellidos_nombres = models.CharField(max_length=200)
    cedula_pasaporte = models.CharField(max_length=20, unique=True)
    cargo = models.CharField(max_length=120)
    fecha_ingreso = models.DateField()
    sueldo = models.DecimalField(max_digits=10, decimal_places=2)
    decimo_tercer_sueldo_modalidad = models.CharField(
        max_length=10,
        choices=MODALIDAD_DECIMO_CHOICES,
        default='anual',
    )
    decimo_cuarto_sueldo_modalidad = models.CharField(
        max_length=10,
        choices=MODALIDAD_DECIMO_CHOICES,
        default='anual',
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.apellidos_nombres} - {self.cedula_pasaporte}"


class RolPago(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    datos = models.JSONField(default=list)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Rol #{self.id} - {self.fecha_creacion:%Y-%m-%d %H:%M}"


class Factura(models.Model):
    TIPO_IDENTIFICACION_CHOICES = [
        ('04', 'RUC'),
        ('05', 'Cédula'),
        ('06', 'Pasaporte'),
        ('07', 'Consumidor final'),
    ]

    numero_factura = models.CharField(max_length=17, unique=True)
    razon_social = models.CharField(max_length=255)
    ruc = models.CharField(max_length=13)
    direccion = models.CharField(max_length=255)
    establecimiento = models.CharField(max_length=3, default='001')
    punto_emision = models.CharField(max_length=3, default='001')
    secuencial = models.CharField(max_length=9)

    cliente_nombre = models.CharField(max_length=255)
    cliente_identificacion = models.CharField(max_length=13)
    tipo_identificacion = models.CharField(max_length=2, choices=TIPO_IDENTIFICACION_CHOICES, default='05')
    cliente_direccion = models.CharField(max_length=255)

    subtotal_0 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    subtotal_12 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_descuento = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    forma_pago = models.CharField(max_length=100)
    tiempo_pago = models.CharField(max_length=100, blank=True)
    correo = models.EmailField(blank=True)
    telefono = models.CharField(max_length=15, blank=True)

    clave_acceso = models.CharField(max_length=49)
    numero_autorizacion = models.CharField(max_length=49, blank=True)
    fecha_emision = models.DateField()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.numero_factura} - {self.cliente_nombre}"


class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='detalles')
    codigo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_sin_impuestos = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"
