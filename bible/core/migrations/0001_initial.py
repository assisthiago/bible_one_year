# Generated by Django 4.1.3 on 2022-12-23 15:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(verbose_name='ordem')),
            ],
            options={
                'verbose_name': 'leitura',
                'verbose_name_plural': 'leituras',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Versicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.CharField(max_length=150, verbose_name='livro')),
                ('book_abbreviation', models.CharField(max_length=3, verbose_name='abreviação')),
                ('chapter', models.CharField(max_length=3, verbose_name='capítulo')),
                ('number', models.CharField(max_length=3, verbose_name='versículo')),
                ('text', models.TextField(max_length=255, verbose_name='texto')),
                ('lection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.lection', verbose_name='leitura')),
            ],
            options={
                'verbose_name': 'versículo',
                'verbose_name_plural': 'versículos',
                'ordering': ('book', 'chapter'),
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False, verbose_name='concluído')),
                ('completed_at', models.DateTimeField(blank=True, null=True, verbose_name='concluído em')),
                ('lection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.lection', verbose_name='leitura')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='usuário')),
            ],
            options={
                'verbose_name': 'tarefa',
                'verbose_name_plural': 'tarefas',
            },
        ),
    ]
