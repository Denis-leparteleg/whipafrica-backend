# Generated by Django 3.2.9 on 2022-02-02 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_artist'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Artist',
        ),
    ]
