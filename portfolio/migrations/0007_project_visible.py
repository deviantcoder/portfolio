# Generated by Django 5.0.7 on 2024-07-31 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0006_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='visible',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
