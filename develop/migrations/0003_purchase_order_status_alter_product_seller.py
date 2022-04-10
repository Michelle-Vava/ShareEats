# Generated by Django 4.0.3 on 2022-03-23 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('develop', '0002_remove_order_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='order_status',
            field=models.CharField(default='seller notified', max_length=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SellerInfo', to='develop.sellerinfo'),
        ),
    ]