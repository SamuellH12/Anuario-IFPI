# Generated by Django 3.2.13 on 2023-01-05 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anuario', '0011_auto_20230105_0144'),
    ]

    operations = [
        migrations.AddField(
            model_name='aluno',
            name='reporter',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='noticia',
            field=models.BooleanField(default=False),
        ),
    ]