# Generated by Django 5.2.2 on 2025-06-15 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("remember_line", "0004_remove_dictionary_owner"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="cardassociation",
            unique_together=set(),
        ),
    ]
