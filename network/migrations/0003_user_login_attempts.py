# Generated by Django 5.0.1 on 2024-06-02 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0002_post_picture_alter_post_user_likes"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="login_attempts",
            field=models.IntegerField(default=0),
        ),
    ]