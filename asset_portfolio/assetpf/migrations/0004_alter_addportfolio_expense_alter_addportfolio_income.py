# Generated by Django 4.0.3 on 2022-04-17 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assetpf', '0003_addportfolio_personalinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addportfolio',
            name='expense',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='addportfolio',
            name='income',
            field=models.FloatField(null=True),
        ),
    ]
