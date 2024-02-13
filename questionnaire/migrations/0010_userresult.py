# Generated by Django 5.0.1 on 2024-02-13 13:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0009_group_show_results'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competence_name', models.CharField(max_length=100)),
                ('competence_count', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.user')),
            ],
        ),
    ]