# Generated by Django 2.1.1 on 2018-09-10 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_exercise_muscle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musclegroup',
            name='muscle_group',
            field=models.CharField(choices=[('Back', 'b'), ('Chest', 'c'), ('Arms', 'a'), ('Legs', 'l')], help_text='name of body area', max_length=20),
        ),
    ]
