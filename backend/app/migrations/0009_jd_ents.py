# Generated by Django 4.1.6 on 2024-02-29 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_parse_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jd_ents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('education', models.CharField(max_length=255)),
                ('worked_as', models.CharField(max_length=255)),
                ('skills', models.CharField(max_length=500)),
                ('experience', models.CharField(max_length=255)),
                ('extracted_data', models.TextField(blank=True)),
            ],
        ),
    ]