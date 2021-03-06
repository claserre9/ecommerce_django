# Generated by Django 3.1.7 on 2021-02-25 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_base', '0005_cart_cartitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, max_length=255)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='USD Order total')),
                ('email_address', models.EmailField(blank=True, max_length=255, verbose_name='Email address')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('billing_name', models.CharField(blank=True, max_length=255)),
                ('billing_address', models.CharField(blank=True, max_length=255)),
                ('billing_city', models.CharField(blank=True, max_length=255)),
                ('billing_country', models.CharField(blank=True, max_length=255)),
                ('billing_postal_code', models.CharField(blank=True, max_length=255)),
                ('shipping_name', models.CharField(blank=True, max_length=255)),
                ('shipping_address', models.CharField(blank=True, max_length=255)),
                ('shipping_city', models.CharField(blank=True, max_length=255)),
                ('shipping_country', models.CharField(blank=True, max_length=255)),
                ('shipping_postal_code', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'db_table': 'Order',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=255)),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='USD Price')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_base.order')),
            ],
            options={
                'db_table': 'OrderItem',
            },
        ),
    ]
