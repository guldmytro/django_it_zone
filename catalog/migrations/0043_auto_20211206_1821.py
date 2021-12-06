# Generated by Django 3.2.7 on 2021-12-06 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0042_alter_product_parent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='описание')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.group', verbose_name='группа для вариации товара'),
        ),
    ]
