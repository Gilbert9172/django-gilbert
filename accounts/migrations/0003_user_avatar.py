# Generated by Django 3.0.14 on 2021-09-29 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210929_2325'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='accounts/profile/%Y/%m/%d'),
        ),
    ]
