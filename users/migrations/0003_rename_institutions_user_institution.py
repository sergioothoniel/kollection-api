# Generated by Django 4.1.1 on 2022-09-08 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_institutions"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="institutions",
            new_name="institution",
        ),
    ]
