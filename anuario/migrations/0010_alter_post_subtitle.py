# Generated by Django 3.2.13 on 2023-01-04 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anuario', '0009_post_aluno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='subtitle',
            field=models.CharField(blank=True, default=' ', max_length=400),
        ),
    ]
