# Generated by Django 5.0.6 on 2024-06-27 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0003_alter_outfit_person'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outfit',
            name='person',
        ),
        migrations.AddField(
            model_name='outfit',
            name='persons',
            field=models.ManyToManyField(related_name='outfit_set', to='snippets.person'),
        ),
    ]
