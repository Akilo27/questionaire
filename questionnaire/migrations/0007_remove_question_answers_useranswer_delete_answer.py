# Generated by Django 5.0.1 on 2024-02-06 15:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0006_alter_user_chosen_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='answers',
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.BooleanField(default=None)),
                ('competence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.competence')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.user')),
            ],
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
    ]