# Generated by Django 5.0.3 on 2024-04-18 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_courseprerequisite_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseprerequisite',
            name='Type',
            field=models.CharField(choices=[('Mandatory', 'Mandatory'), ('Choice', 'Choice')], default='Mandatory', max_length=255),
        ),
    ]
