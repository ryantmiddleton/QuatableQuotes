# Generated by Django 2.2 on 2020-11-07 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes_app', '0002_auto_20201107_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='quoted_by',
            field=models.CharField(default='William Shakespeare', max_length=255),
            preserve_default=False,
        ),
    ]
