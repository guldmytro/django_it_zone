# Generated by Django 3.2.7 on 2021-10-10 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0026_alter_product_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryimage',
            name='image_url',
            field=models.URLField(default=0),
            preserve_default=False,
        ),
    ]
