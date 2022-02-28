# Generated by Django 4.0.2 on 2022-02-28 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_student_level_alter_superadmin_level_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_valid',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='superadmin',
            name='is_valid',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='is_valid',
            field=models.BooleanField(default=True),
        ),
    ]
