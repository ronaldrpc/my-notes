# Generated by Django 5.0 on 2024-01-05 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_alter_note_create_date_alter_note_last_modified_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
