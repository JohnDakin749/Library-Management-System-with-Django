# Generated by Django 4.2 on 2023-05-25 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_language'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='language',
            name='language',
        ),
        migrations.AddField(
            model_name='language',
            name='name',
            field=models.CharField(default='English', help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)", max_length=200),
        ),
    ]
