# Generated by Django 4.2.6 on 2023-10-22 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_alter_customuser_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, primary_key=True, serialize=False, unique=True),
        ),
    ]
