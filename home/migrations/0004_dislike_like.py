# Generated by Django 3.2.9 on 2022-01-18 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_reply_quesno'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dislike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dislikedAnsSno', models.IntegerField()),
                ('dislikedAnsOfQueSno', models.IntegerField()),
                ('dislikedBy', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likedAnsSno', models.IntegerField()),
                ('likedAnsOfQueSno', models.IntegerField()),
                ('likedBy', models.TextField()),
            ],
        ),
    ]