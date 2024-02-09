# Generated by Django 5.0.1 on 2024-02-07 11:55

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0007_remove_question_answers_useranswer_delete_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useranswer',
            name='answer',
        ),
        migrations.AddField(
            model_name='useranswer',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='useranswer',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='questionnaire.group'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='useranswer',
            name='competence',
            field=models.IntegerField(default=0),
        ),
    ]
