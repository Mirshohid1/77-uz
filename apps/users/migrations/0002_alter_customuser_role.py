# Generated by Django 5.1.1 on 2025-01-25 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('seller', 'Seller'), ('user', 'User')], default='user', max_length=20, verbose_name='Role'),
        ),
    ]
