# Generated by Django 5.0.7 on 2024-07-23 16:18

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_rename_website_portfolio_github'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=100, null=True)),
                ('message', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
    ]
