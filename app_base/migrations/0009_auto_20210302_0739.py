# Generated by Django 3.1.7 on 2021-03-02 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_base', '0008_order_verbose_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='verbose_id',
            field=models.CharField(max_length=255),
        ),
    ]
