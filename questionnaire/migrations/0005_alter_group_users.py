# Generated by Django 5.0.1 on 2024-02-05 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0004_rename_chosen_answer_user_chosen_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='users',
            field=models.ManyToManyField(blank=True, to='questionnaire.user'),
        ),
    ]
