# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-01 11:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Days',
            fields=[
                ('day_id', models.AutoField(primary_key=True, serialize=False)),
                ('day_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('faculty_id', models.AutoField(primary_key=True, serialize=False)),
                ('faculty_name', models.CharField(max_length=200)),
                ('position', models.IntegerField()),
                ('work_load', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Faculty_subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faculty_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='time_table_test.Faculty')),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('sub_code', models.IntegerField(primary_key=True, serialize=False)),
                ('sub_name', models.CharField(max_length=200)),
                ('semester_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='time_table_test.Semester')),
            ],
        ),
        migrations.CreateModel(
            name='Subject_Scheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_load', models.IntegerField()),
                ('sub_theory_class', models.IntegerField()),
                ('sub_tutorial_class', models.IntegerField()),
                ('sub_practical_class', models.IntegerField()),
                ('sub_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='time_table_test.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='Timeslot',
            fields=[
                ('timeslot_id', models.AutoField(primary_key=True, serialize=False)),
                ('timeslot', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Timeslot_day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.IntegerField()),
                ('day_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='time_table_test.Days')),
                ('faculty_subject_table_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='time_table_test.Faculty_subject')),
                ('timeslot_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='time_table_test.Timeslot')),
            ],
        ),
        migrations.CreateModel(
            name='Timetable_master',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.IntegerField()),
                ('timeslot_day_table_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='time_table_test.Timeslot_day')),
            ],
        ),
        migrations.AddField(
            model_name='faculty_subject',
            name='sub_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='time_table_test.Subject'),
        ),
    ]