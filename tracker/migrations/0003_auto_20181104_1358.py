# Generated by Django 2.1.2 on 2018-11-04 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_auto_20181104_1356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='classification',
        ),
        migrations.AddField(
            model_name='exercise',
            name='classification',
            field=models.ManyToManyField(to='tracker.Classification'),
        ),
    ]