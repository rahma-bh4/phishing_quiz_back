# Generated by Django 5.1.5 on 2025-01-29 02:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenario',
            name='button',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='footer',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='mail_body',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='objet',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='sender',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='sender_mail',
            field=models.EmailField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='url',
            field=models.URLField(blank=True, max_length=255),
        ),
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nbre_questions', models.IntegerField()),
                ('nbCorrect', models.IntegerField()),
                ('nbFausse', models.IntegerField()),
                ('date_test', models.DateTimeField(auto_now_add=True)),
                ('score', models.IntegerField()),
                ('pourcentage', models.FloatField()),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.user')),
            ],
        ),
    ]
