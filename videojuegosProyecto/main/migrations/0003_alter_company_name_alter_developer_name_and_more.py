# Generated by Django 5.1.4 on 2025-01-02 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_videogame_date_scraped'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='developer',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='platform',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='videogame',
            name='companies',
            field=models.ManyToManyField(to='main.company'),
        ),
        migrations.AlterField(
            model_name='videogame',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='videogame',
            name='developers',
            field=models.ManyToManyField(to='main.developer'),
        ),
        migrations.AlterField(
            model_name='videogame',
            name='platforms',
            field=models.ManyToManyField(to='main.platform'),
        ),
        migrations.AlterField(
            model_name='videogame',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='videogame',
            name='year',
            field=models.IntegerField(),
        ),
    ]
