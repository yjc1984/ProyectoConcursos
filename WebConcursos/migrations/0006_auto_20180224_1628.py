# Generated by Django 2.0.2 on 2018-02-24 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebConcursos', '0005_auto_20180224_1617'),
    ]

    operations = [
        migrations.CreateModel(
            name='foto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='cars')),
            ],
        ),
        migrations.AlterField(
            model_name='concurso',
            name='imagen_file',
            field=models.FileField(blank=True, null=True, upload_to='media/media'),
        ),
    ]