# Generated by Django 3.1.7 on 2021-07-04 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionpackage',
            name='description',
            field=models.CharField(max_length=400, null=True, verbose_name='Description'),
        ),
    ]