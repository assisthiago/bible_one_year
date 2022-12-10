# Generated by Django 4.1.3 on 2022-12-10 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='nome')),
                ('abbreviation', models.CharField(max_length=3, verbose_name='abreviação')),
            ],
            options={
                'verbose_name': 'livro',
                'verbose_name_plural': 'livros',
            },
        ),
        migrations.CreateModel(
            name='Versicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter', models.IntegerField(verbose_name='capítulo')),
                ('number', models.IntegerField(verbose_name='versículo')),
                ('text', models.CharField(max_length=255, verbose_name='texto')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.book', verbose_name='livro')),
            ],
            options={
                'verbose_name': 'versículo',
                'verbose_name_plural': 'versículos',
            },
        ),
    ]
