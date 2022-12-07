# Generated by Django 3.2.15 on 2022-11-15 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mega_menu', '0002_remove_featured_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='language',
            field=models.CharField(choices=[('ar', 'Arabic'), ('zh-Hans', 'Chinese (Simplified)'), ('zh-Hant', 'Chinese (Traditional)'), ('en', 'English'), ('ht', 'Haitian Creole'), ('ko', 'Korean'), ('ru', 'Russian'), ('es', 'Spanish'), ('tl', 'Tagalog'), ('vi', 'Vietnamese')], max_length=100, primary_key=True, serialize=False),
        ),
    ]
