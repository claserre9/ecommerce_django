# Generated by Django 3.1.7 on 2021-02-20 04:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_base', '0002_auto_20210219_2028'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('name',), 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
    ]
