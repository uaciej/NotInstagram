# Generated by Django 4.2.5 on 2023-10-03 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_account_tier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tier',
            name='thumbnail_sizes',
            field=models.CharField(blank=True, max_length=100, verbose_name='Thumbnail Sizes'),
        ),
    ]