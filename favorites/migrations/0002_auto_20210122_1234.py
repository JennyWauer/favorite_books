# Generated by Django 2.2 on 2021-01-22 18:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('favorites', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='uploaded_by_id',
            new_name='uploaded_by',
        ),
    ]