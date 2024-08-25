# Generated by Django 5.1 on 2024-08-25 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_image_download', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarNumberPlate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/temp')),
                ('number_plate_text', models.CharField(max_length=100)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]