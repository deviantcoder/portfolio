# Generated by Django 5.0.7 on 2024-08-01 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0011_remove_socials_portfolio'),
    ]

    operations = [
        migrations.AddField(
            model_name='socials',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='socials',
            name='url',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
