# Generated by Django 3.1.7 on 2021-03-02 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_base', '0010_remove_order_verbose_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='verbose_id',
            field=models.CharField(default=' ', max_length=255),
            preserve_default=False,
        ),
    ]
