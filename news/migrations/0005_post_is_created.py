# Generated by Django 4.0.6 on 2022-08-18 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_categorysubscriber_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_created',
            field=models.BooleanField(default=True),
        ),
    ]
