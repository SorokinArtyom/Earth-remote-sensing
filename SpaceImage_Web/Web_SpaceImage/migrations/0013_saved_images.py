# Generated by Django 4.1.7 on 2023-03-28 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web_SpaceImage', '0012_city_images_meadows_images_water_images'),
    ]

    operations = [
        migrations.CreateModel(
            name='Saved_Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.IntegerField(db_column='ID_Image')),
                ('Users', models.IntegerField(db_column='ID_User')),
            ],
            options={
                'db_table': 'Saved_Image',
                'managed': True,
            },
        ),
    ]
