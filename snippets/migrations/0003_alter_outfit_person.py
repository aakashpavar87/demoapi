# Generated by Django 5.0.6 on 2024-06-26 12:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0002_outfit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outfit',
            name='person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='snippets.person'),
        ),
    ]