# Generated by Django 5.2.2 on 2025-06-19 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="chat",
            name="chat_type",
            field=models.CharField(
                choices=[("private", "Личный"), ("group", "Групповой")],
                default="private",
                max_length=10,
            ),
        ),
    ]
