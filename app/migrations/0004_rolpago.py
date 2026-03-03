from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_empleado'),
    ]

    operations = [
        migrations.CreateModel(
            name='RolPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('datos', models.JSONField(default=list)),
            ],
            options={
                'ordering': ['-fecha_creacion'],
            },
        ),
    ]
