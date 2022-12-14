# Generated by Django 4.1 on 2022-09-06 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_no', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=15)),
                ('state', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='FinanceCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Hsn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=8)),
                ('description', models.CharField(max_length=20)),
                ('rate', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time_created', models.DateTimeField(auto_now_add=True)),
                ('invoice_no', models.IntegerField(default=0)),
                ('total_amount', models.IntegerField(default=0)),
                ('total_qty', models.IntegerField(default=0)),
                ('taxable_amount', models.IntegerField(default=0)),
                ('due', models.IntegerField(default=0)),
                ('cgst', models.IntegerField(default=0)),
                ('sgst', models.IntegerField(default=0)),
                ('igst', models.IntegerField(default=0)),
                ('remark', models.CharField(max_length=100)),
                ('emi', models.IntegerField(default=0)),
                ('downpayment', models.IntegerField(default=0)),
                ('financeDisbursement', models.IntegerField(default=0)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.account')),
                ('finance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.financecompany')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paymentMethod', models.CharField(max_length=10)),
                ('balance', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_code', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=15)),
                ('state', models.CharField(max_length=15)),
                ('website', models.CharField(default='website', max_length=30)),
                ('email', models.CharField(default='email', max_length=30)),
                ('phone_no1', models.CharField(max_length=10)),
                ('phone_no2', models.CharField(max_length=10)),
                ('GST_no', models.CharField(max_length=15)),
                ('shop_current_invoice_no', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(default='', max_length=100)),
                ('qty', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
                ('taxable_value', models.IntegerField(default=0)),
                ('cgst', models.IntegerField(default=0)),
                ('sgst', models.IntegerField(default=0)),
                ('igst', models.IntegerField(default=0)),
                ('hsn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.hsn')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.invoice')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('date_time_created', models.DateTimeField(auto_now_add=True)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.invoice')),
                ('paymentMethod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.paymentmethod')),
            ],
        ),
        migrations.AddField(
            model_name='invoice',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shop'),
        ),
    ]
