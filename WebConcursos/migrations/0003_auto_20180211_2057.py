# Generated by Django 2.0.2 on 2018-02-12 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebConcursos', '0002_customuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='empresa',
            field=models.CharField(max_length=200),
        ),
    ]
