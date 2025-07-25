# Generated by Django 5.2.2 on 2025-06-08 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("social_media", "0002_profile_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="avatar",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="avatars/",
                verbose_name="avatar",
            ),
        ),
    ]
