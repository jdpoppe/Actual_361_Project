# Generated by Django 3.2 on 2021-04-26 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('credits', models.IntegerField(max_length=1)),
                ('location', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EMP_ROLE', models.CharField(choices=[('Supervisor', 'Supe'), ('Instructor', 'Ins'), ('TA', 'Ta')], default='TA', max_length=12)),
                ('EMP_LNAME', models.CharField(max_length=25)),
                ('EMP_FNAME', models.CharField(max_length=25)),
                ('EMP_INITIAL', models.CharField(max_length=1)),
                ('EMP_EMAIL', models.EmailField(max_length=254)),
                ('EMP_PASSWORD', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('location', models.CharField(max_length=10)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_app.course')),
                ('ta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school_app.employee')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school_app.employee'),
        ),
    ]
