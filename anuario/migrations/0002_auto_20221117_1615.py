# Generated by Django 3.2.13 on 2022-11-17 16:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anuario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='turma',
            name='turno',
            field=models.CharField(choices=[('M', 'Manhã'), ('T', 'Tarde'), ('N', 'Noite')], default='M', max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='turma',
            name='anoDaFormatura',
            field=models.IntegerField(unique_for_year=True, validators=[django.core.validators.MinValueValidator(2000), django.core.validators.MaxValueValidator(2100)]),
        ),
    ]
