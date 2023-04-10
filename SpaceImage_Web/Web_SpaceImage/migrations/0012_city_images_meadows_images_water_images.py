# Generated by Django 4.1.7 on 2023-03-27 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web_SpaceImage', '0011_alter_forest_images_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='City_Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(upload_to='Images')),
            ],
            options={
                'db_table': 'City_Images',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Meadows_Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(upload_to='Images')),
            ],
            options={
                'db_table': 'Meadows_Images',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Water_Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(upload_to='Images')),
            ],
            options={
                'db_table': 'Water_Images',
                'managed': True,
            },
        ),
    ]
