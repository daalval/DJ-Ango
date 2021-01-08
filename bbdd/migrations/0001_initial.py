# Generated by Django 3.1.3 on 2021-01-08 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id_persona', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=45, null=True)),
                ('apellidos', models.CharField(max_length=45, null=True)),
            ],
            options={
                'unique_together': {('nombre', 'apellidos')},
            },
        ),
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('id_publicacion', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('titulo', models.CharField(max_length=45, null=True, unique=True)),
                ('anyo', models.IntegerField(null=True)),
                ('URL', models.CharField(max_length=45, null=True)),
            ],
            options={
                'unique_together': {('titulo', 'anyo', 'URL')},
            },
        ),
        migrations.CreateModel(
            name='Revista',
            fields=[
                ('id_revista', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=45, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Libro',
            fields=[
                ('editorial', models.CharField(max_length=45, null=True)),
                ('publicacion', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='bbdd.publicacion')),
            ],
        ),
        migrations.CreateModel(
            name='PersonaPublicacion',
            fields=[
                ('id_personapublicacion', models.IntegerField(primary_key=True, serialize=False)),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbdd.persona')),
                ('publicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbdd.publicacion')),
            ],
            options={
                'unique_together': {('persona', 'publicacion')},
            },
        ),
        migrations.CreateModel(
            name='Ejemplar',
            fields=[
                ('id_ejemplar', models.IntegerField(primary_key=True, serialize=False)),
                ('volumen', models.IntegerField(null=True)),
                ('numero', models.IntegerField(null=True)),
                ('mes', models.IntegerField(null=True)),
                ('revista', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bbdd.revista')),
            ],
            options={
                'unique_together': {('volumen', 'numero', 'mes')},
            },
        ),
        migrations.CreateModel(
            name='Com_con',
            fields=[
                ('congreso', models.CharField(max_length=45, null=True)),
                ('edicion', models.CharField(max_length=45, null=True)),
                ('lugar', models.CharField(max_length=45, null=True)),
                ('pagina_inicio', models.IntegerField(null=True)),
                ('pagina_fin', models.IntegerField(null=True)),
                ('publicacion', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='bbdd.publicacion')),
            ],
            options={
                'unique_together': {('congreso', 'edicion', 'lugar', 'pagina_inicio', 'pagina_fin')},
            },
        ),
        migrations.CreateModel(
            name='Articulo',
            fields=[
                ('pagina_inicio', models.IntegerField(null=True)),
                ('pagina_fin', models.IntegerField(null=True)),
                ('publicacion', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='bbdd.publicacion')),
                ('ejemplar', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bbdd.ejemplar')),
            ],
            options={
                'unique_together': {('pagina_inicio', 'pagina_fin', 'ejemplar')},
            },
        ),
    ]
