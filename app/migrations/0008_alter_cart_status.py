# Generated by Django 3.2 on 2021-04-18 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='status',
            field=models.CharField(choices=[('CLOSED', 'closed'), ('OPEN', 'open')], default='open', max_length=100),
        ),
    ]