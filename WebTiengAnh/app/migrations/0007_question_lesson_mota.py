# Generated by Django 4.2.4 on 2023-10-29 09:46

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_question_lesson_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='question_lesson',
            name='mota',
            field=ckeditor.fields.RichTextField(null=True),
        ),
    ]
