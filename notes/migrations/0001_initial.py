# Generated by Django 5.0 on 2024-01-01 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(verbose_name='Description')),
                ('create_date', models.DateField(auto_now_add=True)),
                ('last_modified_date', models.DateField(auto_now=True)),
            ],
        ),
    ]
