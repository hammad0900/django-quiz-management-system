# Generated by Django 2.2.3 on 2019-10-02 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quizapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mcqs',
            name='mcq_picture',
            field=models.ImageField(default=1, upload_to='images/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='theory',
            name='theory_pic',
            field=models.ImageField(default=1, upload_to='images/'),
            preserve_default=False,
        ),
    ]
