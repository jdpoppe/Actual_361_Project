# Generated by Django 3.2 on 2021-04-19 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0004_alter_employee_emp_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='EMP_ROLE',
            field=models.CharField(choices=[('TA', 'Ta'), ('Instructor', 'Ins')], default='TA', max_length=12),
        ),
    ]
